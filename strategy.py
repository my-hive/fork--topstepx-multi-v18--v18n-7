"""Experiment 17: EURUSD London-fix liquidity reversion.
Mechanism: dealer hedging flows into London benchmark can temporarily dislocate EURUSD;
post-fix liquidity mean-reverts. Observe causal 15:00-16:00 CT move, trade 16:00-17:00.
Falsifier: stressed PnL <=0 or any era block <=0.
"""
import numpy as np
FAMILY='fx-london-fix-liquidity-reversion'
PARAMS={'observe_ct_sec':54000,'entry_ct_sec':57600,'exit_ct_sec':61200,'risk_dollars':250}
def entry_risk(panel): return {s:np.full(len(d),PARAMS['risk_dollars'],dtype=float) for s,d in panel.items()}
def signals(panel):
 ans={}
 for s,d in panel.items():
  out=np.zeros(len(d),dtype=np.int64)
  if s=='6E':
   c,sec=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    a=g[sec[g]==PARAMS['observe_ct_sec']]; b=g[sec[g]==PARAMS['entry_ct_sec']]
    if len(a) and len(b): out[g[(sec[g]>=PARAMS['entry_ct_sec'])&(sec[g]<PARAMS['exit_ct_sec'])]]=-int(np.sign(c[b[0]]-c[a[0]]))
  ans[s]=out
 return ans
