"""Rates exp 4: FOMC-date event response, US 10y futures direction after scheduled window.
Mechanism: rate decisions and projections prompt same-day Treasury repricing and
information-driven continuation.
Calendar approximation: all regular FOMC decisions historically occurred Wednesday,
so test Wednesdays with prior-3-session return as event-direction proxy.
Falsifier: stressed PnL <=0 or any era block <=0.
"""
import numpy as np
import pandas as pd

FAMILY = "rates-fomc-event-response"
PARAMS = {"lookback_sessions": 3, "entry_ct_sec": 43200, "exit_ct_sec": 50400, "risk_dollars": 250}


def entry_risk(panel):
    return {s: np.full(len(df), PARAMS["risk_dollars"], dtype=float) for s, df in panel.items()}


def signals(panel):
    result = {}
    for symbol, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if symbol != "ZN":
            result[symbol] = out
            continue
        closes = df.close.to_numpy()
        sec = df.ct_sec.to_numpy()
        groups = list(df.groupby("session", sort=False).indices.values())
        dates = pd.Series([str(x)[:10] for x in df.session.iloc[[g[0] for g in groups]].to_numpy()], dtype='datetime64[ns]')
        wed = (dates.dt.weekday == 2).to_numpy()
        for g in range(PARAMS["lookback_sessions"], len(groups)):
            if not wed[g]:
                continue
            prev = groups[g - 1]
            back = groups[g - PARAMS["lookback_sessions"]]
            side = int(np.sign(closes[prev[-1]] - closes[back[-1]]))
            idx = groups[g]
            active = idx[(sec[idx] >= PARAMS["entry_ct_sec"]) & (sec[idx] < PARAMS["exit_ct_sec"])]
            out[active] = side
        result[symbol] = out
    return result
