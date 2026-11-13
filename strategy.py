"""Experiment 120: Treasury quarter-start pension duration rebalance reversal.
Mechanism: quarter-start portfolio rebalancing can reverse late-quarter duration demand.
Fade ZN prior session direction in first five calendar business days of quarter.
Falsifier: stressed PnL <=0 or any era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='rates-quarterstart-duration-rebalance-reversal'
PARAMS={'business_days':5,'entry_ct_sec':30600,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZN':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy();gs=list(d.groupby('session',sort=False).indices.values());r=np.array([c[g[-1]]-c[g[0]] for g in gs]);dt=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10]);first=np.array([np.busday_count(x.replace(day=1).date(),x.date()) for x in dt])
   for k in range(1,len(gs)):
    if dt.iloc[k].month in [1,4,7,10] and first[k]<5:
     g=gs[k];o[g[(t[g]>=30600)&(t[g]<43200)]]=-int(np.sign(r[k-1]))
  a[s]=o
 return a
