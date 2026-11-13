"""Causal audit of CL month-boundary refinery and producer hedging flow.
Known final three/initial three calendar business sessions; prior five fully completed session returns.
Falsify on causality, stressed era/year failure, or zero primary statistic.
"""
import numpy as np
import pandas as pd
FAMILY='energy-crude-turn-of-month-causal-audit'
PARAMS={'trend_sessions':5,'boundary_sessions':3,'entry':28800,'exit':43200,'stop_pts':.15}
def entry_risk(panel):return {s:np.full(len(d),155.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='CL':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();groups=list(d.groupby('session',sort=False).indices.items()); rets=[]
  # calendar groups use dates alone: future month sessions are never consulted
  for k,(sess,ix) in enumerate(groups):
   day=pd.Timestamp(sess); nxt=day+pd.Timedelta(days=1)
   boundary=day.day<=PARAMS['boundary_sessions'] or nxt.day<=PARAMS['boundary_sessions']
   if k>=PARAMS['trend_sessions'] and boundary:
    side=int(np.sign(sum(rets[-PARAMS['trend_sessions']:])));j=np.where(t[ix]==PARAMS['entry']-60)[0]
    if side and len(j):
     ref=c[ix[j[0]]]
     for r in ix[j[0]+1:]:
      if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
      out[s][r]=side
   rets.append(c[ix[-1]]/c[ix[0]]-1)
 return out
