"""Experiment 74: heating-oil winter commercial-demand drift.
Mechanism: heating season distillate drawdown and distributor hedging cause persistent
winter demand pressure. Follow prior completed-session HO direction Nov-Feb.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='energy-heating-oil-winter-commercial-drift'
PARAMS={'lookback_sessions':3,'entry_ct_sec':30600,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='HO':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());r=np.array([c[g[-1]]-c[g[0]] for g in gs]);m=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10]).dt.month.to_numpy()
   for k in range(3,len(gs)):
    if m[k] in [11,12,1,2]:
     g=gs[k];o[g[(t[g]>=30600)&(t[g]<43200)]]=int(np.sign(r[k-3:k].sum()))
  a[s]=o
 return a
