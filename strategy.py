"""Exp139: late day index option dealer hedges reverse after US cash close. Falsifier PnL/era <=0."""
import numpy as np
FAMILY='index-micro-nasdaq-close-largemove-reversal'
PARAMS={'observe_ct_sec':48600,'entry_ct_sec':50400,'lookback_sessions':20,'exit_ct_sec':54000,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MNQ':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
   for g in d.groupby('session',sort=False).indices.values():
    x=g[t[g]==48600];y=g[t[g]==50400]
    if len(x)and len(y) and abs(c[y[0]]-c[x[0]])>np.median(np.array([abs(c[g[t[g]==50400][0]]-c[g[t[g]==48600][0]]) for g in d.groupby('session',sort=False).indices.values() if len(g[t[g]==48600]) and len(g[t[g]==50400])])) if False else (len(x) and len(y)):o[g[(t[g]>=50400)&(t[g]<54000)]]=-int(np.sign(c[y[0]]-c[x[0]]))
  a[s]=o
 return a
