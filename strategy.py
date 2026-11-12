"""Rates exp 8: confirmed impulse regime across the Treasury curve.
Mechanism: large prior-session move reflects genuine repricing; next session tends to
continue before profit-taking. Trade only top-decile absolute moves (z-score filter),
longer hold to reduce cost drag.
Falsifier: stressed PnL <=0 or any era block <=0.
"""
import numpy as np

FAMILY = "rates-impulse-regime-continuation"
PARAMS = {"z_lookback_sessions": 20, "z_threshold": 1.5, "hold_sessions": 2, "risk_dollars": 250}


def entry_risk(panel):
    return {s: np.full(len(df), PARAMS["risk_dollars"], dtype=float) for s, df in panel.items()}


def signals(panel):
    result = {}
    for symbol, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if symbol not in ("ZT", "ZN"):
            result[symbol] = out
            continue
        closes = df.close.to_numpy()
        groups = list(df.groupby("session", sort=False).indices.values())
        sess_ret = np.array([closes[g[-1]] - closes[g[0]] if len(g) > 1 else 0. for g in groups])
        hold_left = 0
        side = 0
        for g in range(PARAMS["z_lookback_sessions"], len(groups)):
            window = sess_ret[g - PARAMS["z_lookback_sessions"]:g]
            std = window.std()
            if std > 0 and abs(sess_ret[g - 1] - window.mean()) > PARAMS["z_threshold"] * std:
                side = int(np.sign(sess_ret[g - 1] - window.mean()))
                hold_left = PARAMS["hold_sessions"]
            if hold_left > 0:
                out[groups[g]] = side
                hold_left -= 1
        result[symbol] = out
    return result
