"""Experiment 11: index prior-day reversal (archived v16 lead retest).
Mechanism: overreaction/position unwinding after a large daily move. Uses ES history,
target only fully available completed prior sessions. No MNQ negative control.
Falsifier: <9/14 years positive or any chronological era block <=0.
"""
import numpy as np

FAMILY = "index-prior-day-reversal"
PARAMS = {"risk_dollars": 250}

def entry_risk(panel):
    return {s: np.full(len(df), PARAMS['risk_dollars'], dtype=float) for s,df in panel.items()}

def signals(panel):
    ans={}
    for s,df in panel.items():
        out=np.zeros(len(df),dtype=np.int64)
        if s=='ES':
            c=df.close.to_numpy(); gs=list(df.groupby('session',sort=False).indices.values())
            for k in range(1,len(gs)):
                prev=gs[k-1]
                out[gs[k]]=-int(np.sign(c[prev[-1]]-c[prev[0]]))
        ans[s]=out
    return ans
