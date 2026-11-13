"""Experiment 9: gold London-to-COMEX handoff continuation.
Mechanism: London price discovery gives directional inventory/FX signal; COMEX open
adds US liquidity and follows strong overnight move. Hold one position, not flips.
Falsifier: stressed PnL <=0 or any era block <=0.
"""
import numpy as np

FAMILY = "metals-london-comex-handoff"
PARAMS = {"observe_start_ct_sec": 7200, "entry_ct_sec": 30600, "exit_ct_sec": 36000, "risk_dollars": 250}

def entry_risk(panel):
    return {s: np.full(len(df), PARAMS['risk_dollars'], dtype=float) for s, df in panel.items()}

def signals(panel):
    ans = {}
    for s, df in panel.items():
        out=np.zeros(len(df), dtype=np.int64)
        if s=='MGC':
            c,sec=df.close.to_numpy(),df.ct_sec.to_numpy()
            for g in df.groupby('session',sort=False).indices.values():
                a=g[sec[g]==PARAMS['observe_start_ct_sec']]; b=g[sec[g]==PARAMS['entry_ct_sec']]
                if len(a) and len(b):
                    side=int(np.sign(c[b[0]]-c[a[0]]))
                    out[g[(sec[g]>=PARAMS['entry_ct_sec'])&(sec[g]<PARAMS['exit_ct_sec'])]]=side
        ans[s]=out
    return ans
