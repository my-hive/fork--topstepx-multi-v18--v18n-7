"""Independent CL calendar hedging plus Friday MES basket-flow combination.
CL: prior completed five-session crude trend during known month-boundary sessions.
MES: Friday opening basket imbalance continuation. Falsify on causality, risk, economics, or primary.
"""
import numpy as np
import pandas as pd
FAMILY='energy-equity-calendar-flow-combination'
PARAMS={'cl_stop_pts':.15,'mes_stop_pts':10.,'entry':32400,'exit':43200,'cl_lookback':5}
def entry_risk(panel):
 return {s:np.full(len(d),155. if s=='CL' else 55. if s=='MES' else 301.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'CL' in panel:
  d=panel['CL'];c=d.close.to_numpy();t=d.ct_sec.to_numpy();hist=[]
  for sess,ix in d.groupby('session',sort=False).indices.items():
   day=pd.Timestamp(sess); boundary=day.day<=3 or day.day>=29
   if len(hist)>=PARAMS['cl_lookback'] and boundary:
    side=int(np.sign(np.prod([1]) * np.sign(np.sum(hist[-PARAMS['cl_lookback']:])))); j=np.where(t[ix]==28800-60)[0]
    if len(j) and side:
     ref=c[ix[j[0]]]
     for r in ix[j[0]+1:]:
      if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['cl_stop_pts']:break
      out['CL'][r]=side
   hist.append(c[ix[-1]]/c[ix[0]]-1)
 if 'MES' in panel:
  d=panel['MES'];c=d.close.to_numpy();t=d.ct_sec.to_numpy()
  for sess,ix in d.groupby('session',sort=False).indices.items():
   if pd.Timestamp(sess).day_of_week!=4:continue
   a=np.where(t[ix]==30540)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0]
   if not len(a) or not len(b):continue
   side=int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]));ref=c[ix[b[0]]]
   if side:
    for r in ix[b[0]+1:]:
     if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['mes_stop_pts']:break
     out['MES'][r]=side
 return out
