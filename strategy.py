"""Risk-scaled Friday MES continuation after cross-index-confirmed opening flow.
Shared MNQ/MES sign identifies basket/ETF institutional imbalance; 5 MES uses allowed capacity.
Falsify: primary zero, risk breach, or any era/year gate failure.
"""
import numpy as np
import pandas as pd
FAMILY='equity-friday-opening-cross-index-mes-risk-scaled'
PARAMS={'size':5,'entry':32400,'exit':50400,'stop_pts':10.}
def entry_risk(panel):return {s:np.full(len(d),PARAMS['size']*PARAMS['stop_pts']*5+5.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'MES','MNQ'}<=set(panel):return out
 p=panel['MNQ'].pivot_table(index='session',columns='ct_sec',values='close',aggfunc='last'); ns=np.sign(p[32340]-p[30540])
 d=panel['MES'];c=d.close.to_numpy();t=d.ct_sec.to_numpy()
 for sess,ix in d.groupby('session',sort=False).indices.items():
  if pd.Timestamp(sess).day_of_week!=4 or sess not in ns.index:continue
  a=np.where(t[ix]==30540)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0]
  if not len(a) or not len(b):continue
  side=int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]))
  if not side or side!=int(ns[sess]):continue
  ref=c[ix[b[0]]]
  for r in ix[b[0]+1:]:
   if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
   out['MES'][r]=side*PARAMS['size']
 return out
