"""Rates exp 7: scheduled 07:30 CT macro release response in 10y futures.
Mechanism: recurring labor/inflation releases convey rate information; initial move
should continue while dealers digest surprise. Causal: observe first 30 completed bars.
Falsifier: stressed PnL <=0 or any era block <=0.
"""
import numpy as np

FAMILY = "rates-macro-release-repricing-continuation"
PARAMS = {"observe_start_ct_sec": 27000, "entry_ct_sec": 28800, "exit_ct_sec": 32400, "risk_dollars": 250}

def entry_risk(panel):
    return {s: np.full(len(df), PARAMS['risk_dollars'], dtype=float) for s, df in panel.items()}

def signals(panel):
    result = {}
    for s, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if s == 'ZN':
            c, sec = df.close.to_numpy(), df.ct_sec.to_numpy()
            for idx in df.groupby('session', sort=False).indices.values():
                starts = idx[sec[idx] == PARAMS['observe_start_ct_sec']]
                entries = idx[sec[idx] == PARAMS['entry_ct_sec']]
                if len(starts) and len(entries):
                    side = int(np.sign(c[entries[0]] - c[starts[0]]))
                    active = idx[(sec[idx] >= PARAMS['entry_ct_sec']) & (sec[idx] < PARAMS['exit_ct_sec'])]
                    out[active] = side
        result[s] = out
    return result
