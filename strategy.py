"""Experiment 16: ZN-to-ES cross-asset lead-lag.
Mechanism: macro releases reprice bonds first; equities then adjust through discount-rate
and growth channel. Observe ZN 07:30-08:30 CT, trade ES 08:30-10:00 CT. Costs unchanged.
Falsifier: stressed PnL <=0 or any era block <=0.
"""
import numpy as np

FAMILY = "cross-asset-bond-equity-leadlag"
PARAMS = {"obs_start_ct_sec": 27000, "obs_end_ct_sec": 30600, "exit_ct_sec": 36000, "risk_dollars": 250}

def entry_risk(panel): return {s:np.full(len(d),PARAMS['risk_dollars'],dtype=float) for s,d in panel.items()}
def signals(panel):
 ans={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if 'ZN' not in panel or 'ES' not in panel: return ans
 z,e=panel['ZN'],panel['ES']; zc,zs=z.close.to_numpy(),z.ct_sec.to_numpy(); ec,es=e.ct_sec.to_numpy(),e.ct_sec.to_numpy()
 sides={}
 for sess,g in z.groupby('session',sort=False).indices.items():
  a=g[zs[g]==PARAMS['obs_start_ct_sec']]; b=g[zs[g]==PARAMS['obs_end_ct_sec']]
  if len(a) and len(b): sides[sess]=-int(np.sign(zc[b[0]]-zc[a[0]]))  # bond yield up (price down) -> equity risk-on? sign tested
 out=ans['ES']
 for sess,g in e.groupby('session',sort=False).indices.items():
  if sess in sides: out[g[(es[g]>=PARAMS['obs_end_ct_sec'])&(es[g]<PARAMS['exit_ct_sec'])]]=sides[sess]
 return ans
