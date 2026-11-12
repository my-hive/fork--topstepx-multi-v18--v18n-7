"""Experiment 18: EURUSD European-opening range breakout.
Mechanism: European cash participation resolves Asian range and carries through London.
Observe 01:00-02:00 CT; trade continuation 02:00-04:00 CT. Falsifier: nonpositive PnL/era.
"""
import numpy as np
FAMILY='fx-european-opening-range-breakout'
PARAMS={'observe_ct_sec':3600,'entry_ct_sec':7200,'exit_ct_sec':14400,'risk_dollars':250}
def entry_risk(panel): return {s:np.full(len(d),PARAMS['risk_dollars'],dtype=float) for s,d in panel.items()}
def signals(panel):
 ans={}
 for s,d in panel.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='6E':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    a=g[t[g]==PARAMS['observe_ct_sec']]; b=g[t[g]==PARAMS['entry_ct_sec']]
    if len(a) and len(b): o[g[(t[g]>=PARAMS['entry_ct_sec'])&(t[g]<PARAMS['exit_ct_sec'])]]=int(np.sign(c[b[0]]-c[a[0]]))
  ans[s]=o
 return ans
