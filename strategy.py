"""Rates exp 6: Treasury futures reopen liquidity reversion.
Mechanism: thin overnight reopening overshoots; price mean-reverts when US depth returns.
Falsifier: stressed PnL <=0 or any chronological era block <=0.
"""
import numpy as np

FAMILY = "rates-reopen-liquidity-reversion"
PARAMS = {"lookback_minutes": 30, "entry_ct_sec": 28800, "exit_ct_sec": 30600, "risk_dollars": 250}

def entry_risk(panel):
    return {s: np.full(len(df), PARAMS["risk_dollars"], dtype=float) for s, df in panel.items()}

def signals(panel):
    result = {}
    for s, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if s == 'ZN':
            c, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
            for idx in df.groupby('session', sort=False).indices.values():
                for j in range(PARAMS['lookback_minutes'], len(idx)):
                    i = idx[j]
                    if PARAMS['entry_ct_sec'] <= sec[i] < PARAMS['exit_ct_sec']:
                        out[i] = -int(np.sign(c[i] - c[idx[j-PARAMS['lookback_minutes']]]))
        result[s] = out
    return result
