"""Experiment 77: crude turn-of-month refinery scheduling drift.
Mechanism: refinery nominations, producer hedge rolls, and inventory scheduling cluster
around month boundary. Prior five-session CL direction continues in final/first 3 sessions.
Five CL contracts use evaluator's maximum exposure; daily DLL truncation is part of test.
Falsifier: stressed PnL <=0 or any era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='energy-crude-turn-month-scheduling-max-exposure'
PARAMS={'trend_sessions':5,'window_business_days':3,'contracts':5,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='CL':
   c=d.close.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());r=np.array([c[g[-1]]-c[g[0]] for g in gs]);dates=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10]);me=dates+pd.offsets.MonthEnd(0);left=np.array([np.busday_count(x.date(),y.date()) for x,y in zip(dates,me)]);first=np.array([np.busday_count(x.replace(day=1).date(),x.date()) for x in dates])
   for k in range(5,len(gs)):
    if left[k]<3 or first[k]<3:o[gs[k]]=int(np.sign(r[k-5:k].sum()))*5
  a[s]=o
 return a
