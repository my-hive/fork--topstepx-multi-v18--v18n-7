"""Experiment 40: ES quarter-end pension allocation drift.
Mechanism: institutional allocation and benchmark rebalancing concentrates at quarter-end.
Long final five observed business sessions of Mar/Jun/Sep/Dec. Falsifier: PnL<=0/era<=0.
"""
import numpy as np,pandas as pd
FAMILY='index-quarter-end-allocation-drift'
PARAMS={'final_sessions':5,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ES':
   sess=pd.Series(d.session.astype(str).drop_duplicates()); date=pd.to_datetime(sess.str[:10]); q=date.dt.to_period('Q'); rank=date.groupby(q).cumcount(); n=date.groupby(q).transform('size'); active=((n-rank)<=5)&date.dt.month.isin([3,6,9,12]); lookup=dict(zip(sess,active));o=np.array([int(lookup[x]) for x in d.session.astype(str)],dtype=np.int64)
  a[s]=o
 return a
