"""Experiment 19: crude inventory-session impulse continuation.
Mechanism: EIA weekly petroleum data causes persistent inventory repricing; CL prior-
session impulse continues through US session. Same mechanism family different asset/cost.
Falsifier: stressed PnL <=0 or any era block <=0.
"""
import numpy as np
FAMILY='energy-inventory-session-impulse-continuation'
PARAMS={'lookback_sessions':3,'entry_ct_sec':30600,'exit_ct_sec':46800,'risk_dollars':250}
def entry_risk(panel): return {s:np.full(len(d),PARAMS['risk_dollars'],dtype=float) for s,d in panel.items()}
def signals(panel):
 ans={}
 for s,d in panel.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='CL':
   c=d.close.to_numpy(); gs=list(d.groupby('session',sort=False).indices.values())
   rets=np.array([c[g[-1]]-c[g[0]] for g in gs]); t=d.ct_sec.to_numpy()
   for k in range(PARAMS['lookback_sessions'],len(gs)):
    side=int(np.sign(rets[k-1]+rets[k-2]+rets[k-3]))
    if side:
     g=gs[k]; o[g[(t[g]>=PARAMS['entry_ct_sec'])&(t[g]<PARAMS['exit_ct_sec'])]]=side
  ans[s]=o
 return ans
