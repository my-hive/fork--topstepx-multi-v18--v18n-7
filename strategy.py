"""Experiment 29: safe-haven equity-risk spillover into gold.
Mechanism: large equity risk-off move causes next-day gold demand; use prior completed
ES session only. Falsifier: nonpositive stressed PnL or any era block <=0.
"""
import numpy as np
FAMILY='cross-asset-safehaven-equity-spillover'
PARAMS={'lookback_sessions':1,'entry_ct_sec':30600,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 if 'ES'not in p or 'MGC'not in p:return{s:np.zeros(len(d),dtype=np.int64)for s,d in p.items()}
 e,g=p['ES'],p['MGC'];ec=e.close.to_numpy();gs=list(e.groupby('session',sort=False).indices.values());er=np.array([ec[x[-1]]-ec[x[0]] for x in gs]);dates=[str(x)[:10] for x in e.session.iloc[[x[0] for x in gs]].to_numpy()];smap=dict(zip(dates,-np.sign(er)))
 gc,gt=g.close.to_numpy(),g.ct_sec.to_numpy();ggs=list(g.groupby('session',sort=False).indices.values());gd=[str(x)[:10] for x in g.session.iloc[[x[0] for x in ggs]].to_numpy()]
 o=np.zeros(len(g),dtype=np.int64)
 for k,x in enumerate(ggs):
  prev=[d for d in dates if d<gd[k]]
  if prev and smap[prev[-1]]:o[x[(gt[x]>=30600)&(gt[x]<43200)]]=smap[prev[-1]]
 a['ES']=np.zeros(len(e),dtype=np.int64);a['MGC']=o;return a
