"""Experiment 24: Bitcoin weekend information-gap continuation.
Mechanism: 24/7 spot discovery over weekend is incorporated into CME reopening; strong
Friday-to-Monday move continues as institutional futures liquidity joins.
Falsifier: nonpositive stressed PnL or any era block <=0.
"""
import numpy as np,pandas as pd
FAMILY='crypto-weekend-information-continuation'
PARAMS={'entry_ct_sec':30600,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(panel): return {s:np.full(len(d),PARAMS['risk_dollars'],dtype=float) for s,d in panel.items()}
def signals(panel):
 ans={}
 for s,d in panel.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='MBT':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy(); gs=list(d.groupby('session',sort=False).indices.values()); dates=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10])
   for k in range(1,len(gs)):
    if dates.iloc[k].weekday()==0:
     side=int(np.sign(c[gs[k][0]]-c[gs[k-1][-1]]));g=gs[k];o[g[(t[g]>=PARAMS['entry_ct_sec'])&(t[g]<PARAMS['exit_ct_sec'])]]=side
  ans[s]=o
 return ans
