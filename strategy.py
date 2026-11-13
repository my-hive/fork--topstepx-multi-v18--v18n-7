"""Rates experiment 1: prior-session ZN trend continuation at US cash open.
Mechanism: overnight bond repricing persists into scheduled US cash liquidity.
Falsifier: stressed PnL and cross-era blocks fail to stay positive.
"""
import numpy as np

FAMILY = "rates-prior-session-trend-cash-open"
PARAMS = {"entry_ct_sec": 30600, "exit_ct_sec": 34200, "risk_dollars": 250}


def entry_risk(panel):
    return {s: np.full(len(df), PARAMS["risk_dollars"], dtype=float) for s, df in panel.items()}


def signals(panel):
    result = {}
    for symbol, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if symbol != "ZN":
            result[symbol] = out
            continue
        groups = list(df.groupby("session", sort=False).indices.values())
        closes = df.close.to_numpy()
        sec = df.ct_sec.to_numpy()
        for g in range(2, len(groups)):
            prev, prior, idx = groups[g - 1], groups[g - 2], groups[g]
            side = int(np.sign(closes[prev[-1]] - closes[prior[-1]]))
            if side:
                active = idx[(sec[idx] >= PARAMS["entry_ct_sec"]) & (sec[idx] < PARAMS["exit_ct_sec"])]
                out[active] = side
        result[symbol] = out
    return result
