"""Experiment 14: stable harvest-pressure hold.
Mechanism: September-October wheat supply pressure; hold continuously through month
and out of month so roll/gap exits do not churn. Same idea as exp 12, correct contract.
Falsifier: stressed PnL <=0 or any era block <=0.
"""
import numpy as np
import pandas as pd

FAMILY = "grains-harvest-pressure-seasonality-stable-hold"
PARAMS = {"start_month": 9, "end_month": 10, "risk_dollars": 250}

def entry_risk(panel):
    return {s: np.full(len(df), PARAMS['risk_dollars'], dtype=float) for s,df in panel.items()}

def signals(panel):
    ans={}
    for s,df in panel.items():
        out=np.zeros(len(df),dtype=np.int64)
        if s=='ZW':
            months=pd.to_datetime(df.session.astype(str).str[:10]).dt.month.to_numpy()
            on=(months>=PARAMS['start_month'])&(months<=PARAMS['end_month'])
            out[on]=-1
            # Causality note: calendar months are known at entry; no price lookahead.
        ans[s]=out
    return ans
