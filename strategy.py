"""Experiment 10: gold daily-trend regime continuation.
Mechanism: macro inflation/real-rate repricing persists over multiple sessions; one
session trend signal avoids intraday noise and churn. Prior completed sessions only.
Falsifier: stressed PnL <=0 or any chronological era block <=0.
"""
import numpy as np

FAMILY = "metals-daily-trend-regime"
PARAMS = {"lookback_sessions": 5, "risk_dollars": 250}

def entry_risk(panel):
    return {s: np.full(len(df), PARAMS['risk_dollars'], dtype=float) for s,df in panel.items()}

def signals(panel):
    ans={}
    for s,df in panel.items():
        out=np.zeros(len(df),dtype=np.int64)
        if s=='MGC':
            c=df.close.to_numpy(); gs=list(df.groupby('session',sort=False).indices.values())
            ends=np.array([c[g[-1]] for g in gs])
            for k in range(PARAMS['lookback_sessions'],len(gs)):
                out[gs[k]]=int(np.sign(ends[k-1]-ends[k-PARAMS['lookback_sessions']]))
        ans[s]=out
    return ans
