"""Experiment 48: Treasury month-start duration reinvestment.
Mechanism: coupon/principal reinvestment and index flows around month start create demand
for duration. Long ZN first three calendar business days, all-session low turnover.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='rates-month-start-reinvestment-demand'
PARAMS={'business_days':3,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZN':
   dt=pd.to_datetime(d.session.astype(str).str[:10]); left=np.array([np.busday_count(x.replace(day=1).date(),x.date()) for x in dt]);o[left<3]=1
  a[s]=o
 return a
