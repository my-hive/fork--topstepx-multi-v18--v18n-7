"""Experiment 119: front-end month-end collateral demand drift.
Mechanism: month-end balance-sheet and collateral demand alters short-rate futures
positioning, creating ZT drift during final/first three business days. Known calendar.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='rates-front-end-monthend-collateral-drift'
PARAMS={'window_business_days':3,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZT':
   dt=pd.to_datetime(d.session.astype(str).str[:10]); me=dt+pd.offsets.MonthEnd(0); left=np.array([np.busday_count(x.date(),y.date()) for x,y in zip(dt,me)]); first=np.array([np.busday_count(x.replace(day=1).date(),x.date()) for x in dt]);o[(left<3)|(first<3)]=1
  a[s]=o
 return a
