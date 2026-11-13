"""Experiment 23: natural-gas winter storage-withdrawal trend.
Mechanism: Nov-Mar heating withdrawals create demand pressure; storage reports and cold
weather cause trend persistence. Known calendar + prior completed 3-session momentum.
Falsifier: stressed PnL <=0 or any era block <=0.
"""
import numpy as np,pandas as pd
FAMILY='energy-gas-storage-withdrawal-trend'
PARAMS={'start_month':11,'end_month':3,'lookback_sessions':3,'risk_dollars':250}
def entry_risk(panel): return {s:np.full(len(d),PARAMS['risk_dollars'],dtype=float) for s,d in panel.items()}
def signals(panel):
 ans={}
 for s,d in panel.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='NG':
   c=d.close.to_numpy(); gs=list(d.groupby('session',sort=False).indices.values()); r=np.array([c[g[-1]]-c[g[0]] for g in gs]); m=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10]).dt.month.to_numpy()
   for k in range(PARAMS['lookback_sessions'],len(gs)):
    if m[k]>=PARAMS['start_month'] or m[k]<=PARAMS['end_month']: o[gs[k]]=int(np.sign(r[k-1:k].sum()))
  ans[s]=o
 return ans
