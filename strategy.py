"""Experiment 56: crude weekend risk-premium continuation.
Mechanism: geopolitical and inventory uncertainty accumulates over weekend; Friday late
move signals risk premium that continues into Monday institutional liquidity.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='energy-crude-weekend-risk-premium'
PARAMS={'entry_ct_sec':30600,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='CL':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());dt=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10])
   for k in range(1,len(gs)):
    if dt.iloc[k].weekday()==0:
     q=gs[k-1];side=int(np.sign(c[q[-1]]-c[q[0]]));g=gs[k];o[g[(t[g]>=30600)&(t[g]<43200)]]=side
  a[s]=o
 return a
