"""Experiment 20: FX overnight carry/liquidity capture.
Mechanism: overnight G10 liquidity premium and rate-differential carry produce drift
when overnight regime established by prior completed session. Continuous 6E reduces
re-entry churn. Stop modeled as causal trailing adverse move from entry.
Falsifier: stressed PnL <=0 or any era block <=0.
"""
import numpy as np
FAMILY='fx-overnight-carry-liquidity-capture'
PARAMS={'lookback_sessions':5,'stop_points':0.0015,'risk_dollars':250}
def entry_risk(panel): return {s:np.full(len(d),PARAMS['risk_dollars'],dtype=float) for s,d in panel.items()}
def signals(panel):
 ans={}
 for s,d in panel.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='6E':
   c=d.close.to_numpy(); gs=list(d.groupby('session',sort=False).indices.values())
   rets=np.array([c[g[-1]]-c[g[0]] for g in gs]); pos=0; basis=0.
   for k in range(PARAMS['lookback_sessions'],len(gs)):
    side=int(np.sign(rets[k-1:k].sum()))
    for i in gs[k]:
     if pos and abs(c[i]-basis)>=PARAMS['stop_points']: pos=0
     if not pos and side: pos=side; basis=c[i]
     o[i]=pos
  ans[s]=o
 return ans
