"""Experiment 12: wheat harvest-pressure seasonal short.
Mechanism: Northern Hemisphere harvest delivery and storage hedging add supply pressure
in September-October. Calendar is known in advance; hold one low-turnover position.
Falsifier: stressed PnL <=0 or any chronological era block <=0.
"""
import numpy as np
import pandas as pd

FAMILY = "grains-harvest-pressure-seasonality"
PARAMS = {"start_month": 9, "end_month": 10, "risk_dollars": 250}

def entry_risk(panel):
    return {s: np.full(len(df), PARAMS['risk_dollars'], dtype=float) for s,df in panel.items()}

def signals(panel):
    ans={}
    for s,df in panel.items():
        out=np.zeros(len(df),dtype=np.int64)
        if s=='ZW':
            months=pd.to_datetime(df.session.astype(str).str[:10]).dt.month.to_numpy()
            out[(months>=PARAMS['start_month'])&(months<=PARAMS['end_month'])]=-1
        ans[s]=out
    return ans
