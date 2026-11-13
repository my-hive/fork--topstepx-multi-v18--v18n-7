"""Experiment 39: equity turn-of-month institutional rebalancing drift.
Mechanism: pension contributions, 401k flows and index rebalancing cluster around month
boundary, supporting equity futures. Long ES during last/first three business days.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='index-turn-of-month-institutional-drift'
PARAMS={'window_business_days':3,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ES':
   dates=pd.to_datetime(d.session.astype(str).str[:10]); uniq=pd.Series(dates.drop_duplicates()); # last 3 or first 3 business dates
   first=uniq.groupby([uniq.dt.year,uniq.dt.month]).rank(method='dense').to_numpy()
   last=uniq.groupby([uniq.dt.year,uniq.dt.month]).transform('max').to_numpy()-first+1
   lookup=dict(zip(uniq.astype(str), (first<=3)|(last<=3))); o=np.array([int(lookup[str(x)]) for x in dates],dtype=np.int64)
  a[s]=o
 return a
