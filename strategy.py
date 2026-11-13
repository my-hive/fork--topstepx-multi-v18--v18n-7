"""Experiment 41: ES quarter-end allocation drift, causal calendar form.
Mechanism: institutional allocation/rebalancing clusters at quarter-end. Long last five
calendar business days of March, June, September, December. Calendar date known at entry.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='index-quarter-end-allocation-drift-calendar'
PARAMS={'business_days_to_quarter_end':5,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ES':
   dates=pd.to_datetime(d.session.astype(str).str[:10]); qend=dates+pd.offsets.QuarterEnd(0); left=np.array([np.busday_count(x.date(),y.date()) for x,y in zip(dates,qend)]);o[(left<5)&dates.dt.month.isin([3,6,9,12])]=1
  a[s]=o
 return a
