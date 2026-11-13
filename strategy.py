"""Experiment 79: soybean harvest-pressure extreme reversal.
Mechanism: harvest delivery hedging causes transitory daily supply pressure; exceptional
prior-day move reverses in next US grain session as commercials absorb flow. Sep-Nov only.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='grains-soy-harvest-large-shock-reversal'
PARAMS={'lookback_sessions':20,'shock_std':2.0,'entry_ct_sec':30600,'exit_ct_sec':46800,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZS':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());r=np.array([c[g[-1]]-c[g[0]] for g in gs]);m=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10]).dt.month.to_numpy()
   for k in range(20,len(gs)):
    w=r[k-20:k]
    if m[k] in [9,10,11] and abs(r[k-1]-w.mean())>2.0*w.std():
     g=gs[k];o[g[(t[g]>=30600)&(t[g]<46800)]]=-int(np.sign(r[k-1]-w.mean()))
  a[s]=o
 return a
