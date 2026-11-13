"""Experiment 109: equity year-end institutional risk-on drift.
Mechanism: tax planning, performance chasing and retirement allocation create equity
buying pressure in final December sessions. Long ES Dec 15-31. Known calendar only.
Falsifier: stressed PnL <=0 or any era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='index-yearend-institutional-riskon-drift'
PARAMS={'start_day':15,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ES':
   dt=pd.to_datetime(d.session.astype(str).str[:10]);o[(dt.dt.month==12)&(dt.dt.day>=15)]=1
  a[s]=o
 return a
