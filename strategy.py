"""Experiment 15: ES opening impulse continuation.
Mechanism: large first-hour price discovery reflects institutional imbalance; later
participants continue direction. Use only exceptional first-hour moves, avoid overnight.
Falsifier: stressed PnL <=0 or any era block <=0.
"""
import numpy as np

FAMILY = "index-opening-impulse-continuation"
PARAMS = {"open_ct_sec": 30600, "decision_ct_sec": 34200, "exit_ct_sec": 43200, "lookback_sessions": 20, "z_threshold": 1.5, "risk_dollars": 250}

def entry_risk(panel): return {s:np.full(len(d),PARAMS['risk_dollars'],dtype=float) for s,d in panel.items()}
def signals(panel):
 ans={}
 for s,df in panel.items():
  out=np.zeros(len(df),dtype=np.int64)
  if s=='ES':
   c,sec=df.close.to_numpy(),df.ct_sec.to_numpy(); gs=list(df.groupby('session',sort=False).indices.values()); moves=[]
   for k,g in enumerate(gs):
    a=g[sec[g]==PARAMS['open_ct_sec']]; b=g[sec[g]==PARAMS['decision_ct_sec']]
    move=(c[b[0]]-c[a[0]]) if len(a) and len(b) else 0.; moves.append(move)
    if k>=PARAMS['lookback_sessions'] and len(a) and len(b):
     w=np.array(moves[k-PARAMS['lookback_sessions']:k]); z=(move-w.mean())/(w.std() or np.inf)
     if abs(z)>PARAMS['z_threshold']:
      out[g[(sec[g]>=PARAMS['decision_ct_sec'])&(sec[g]<PARAMS['exit_ct_sec'])]]=int(np.sign(move))
  ans[s]=out
 return ans
