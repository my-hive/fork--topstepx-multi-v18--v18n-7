"""Experiment 73: mini natural-gas storage-shock continuation.
Mechanism: weekly EIA storage report delivers inventory information; initial price
repricing continues while utilities and producers rebalance hedges. QG adds independent
contract/cost evidence versus micro NG test. Thursday calendar is known before entry.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np
import pandas as pd
FAMILY='energy-mini-gas-storage-shock-continuation'
PARAMS={'open_ct_sec':30600,'entry_ct_sec':32400,'exit_ct_sec':39600,'risk_dollars':250}
def entry_risk(panel): return {s:np.full(len(d),250.,dtype=float) for s,d in panel.items()}
def signals(panel):
    ans={}
    for s,d in panel.items():
        out=np.zeros(len(d),dtype=np.int64)
        if s=='QG':
            c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
            weekday=pd.to_datetime(d.session.astype(str).str[:10]).dt.weekday.to_numpy()
            for g in d.groupby('session',sort=False).indices.values():
                x=g[t[g]==30600]; y=g[t[g]==32400]
                if len(x) and len(y) and weekday[g[0]]==3:
                    out[g[(t[g]>=32400)&(t[g]<39600)]]=int(np.sign(c[y[0]]-c[x[0]]))
        ans[s]=out
    return ans
