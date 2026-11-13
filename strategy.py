"""Experiment 36: rare high-conviction NQ macro drift.
Mechanism: only unusually large 08:30-09:00 moves represent information shocks;
those continue into cash-session liquidity. Rolling daily move distribution is causal.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
FAMILY='index-rare-macro-shock-drift'
PARAMS={'observe_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':43200,'lookback_sessions':20,'z_threshold':1.5,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='NQ':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());moves=[]
   for k,g in enumerate(gs):
    x=g[t[g]==30600];y=g[t[g]==32400]; move=c[y[0]]-c[x[0]] if len(x)and len(y)else 0.;moves.append(move)
    if k>=20 and len(x)and len(y):
     w=np.array(moves[k-20:k]); z=(move-w.mean())/(w.std() or np.inf)
     if abs(z)>1.5:o[g[(t[g]>=32400)&(t[g]<43200)]]=int(np.sign(move))
  a[s]=o
 return a
