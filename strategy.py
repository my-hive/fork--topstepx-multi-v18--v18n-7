"""Experiment 31: NQ cash-open liquidity continuation.
Mechanism: premarket institutional positioning into US cash open reveals imbalance;
cash-market participation continues direction. Observe 08:00-08:30 CT, trade 08:30-10:30.
Falsifier: stressed total PnL or any chronological era PnL nonpositive.
"""
import numpy as np
FAMILY = 'index-cash-open-premarket-impulse'
PARAMS = {'observe_ct_sec': 28800, 'entry_ct_sec': 30600, 'exit_ct_sec': 37800, 'risk_dollars': 250}
def entry_risk(panel): return {s: np.full(len(d), PARAMS['risk_dollars'], dtype=float) for s,d in panel.items()}
def signals(panel):
    ans={}
    for s,d in panel.items():
        out=np.zeros(len(d),dtype=np.int64)
        if s=='NQ':
            c,t=d.close.to_numpy(),d.ct_sec.to_numpy()
            for g in d.groupby('session',sort=False).indices.values():
                a=g[t[g]==PARAMS['observe_ct_sec']]; b=g[t[g]==PARAMS['entry_ct_sec']]
                if len(a) and len(b): out[g[(t[g]>=PARAMS['entry_ct_sec'])&(t[g]<PARAMS['exit_ct_sec'])]]=int(np.sign(c[b[0]]-c[a[0]]))
        ans[s]=out
    return ans
