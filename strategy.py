"""Experiment 49: Treasury quarter-end duration-index demand.
Mechanism: duration index rebalance and balance-sheet allocation at quarter-end create
Treasury buying. Long ZN final five known calendar business days of quarter.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='rates-quarter-end-duration-index-demand'
PARAMS={'business_days_to_quarter_end':5,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZN':
   dt=pd.to_datetime(d.session.astype(str).str[:10]);qe=dt+pd.offsets.QuarterEnd(0);left=np.array([np.busday_count(x.date(),y.date()) for x,y in zip(dt,qe)]);o[(left<5)&dt.dt.month.isin([3,6,9,12])]=1
  a[s]=o
 return a
