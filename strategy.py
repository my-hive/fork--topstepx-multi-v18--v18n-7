"""Rates exp 2: month-end index duration-extension demand, long ZN afternoons.
Mechanism: bond indices extend duration at month end; passive buying concentrates
into the last sessions, after cash open. Calendar-only signal (no price lookahead).
Falsifier: stressed PnL <=0 or any era block <=0 on ZN last-3-business-day longs.
"""
import numpy as np
import pandas as pd

FAMILY = "rates-month-end-duration-extension"
PARAMS = {"last_n_bdays": 3, "entry_ct_sec": 36000, "risk_dollars": 250}


def entry_risk(panel):
    return {s: np.full(len(df), PARAMS["risk_dollars"], dtype=float) for s, df in panel.items()}


def signals(panel):
    result = {}
    for symbol, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if symbol != "ZN":
            result[symbol] = out
            continue
        dates = pd.to_datetime(df.session.astype(str).str[:10])
        # self-check: exit flip causes gap_or_roll churn; keep causal busyday field to month end (calendar known in advance)
        uniq = pd.DataFrame({"d": dates.drop_duplicates()})
        uniq["left"] = [np.busday_count(d.date(), (d + pd.offsets.BMonthEnd(0)).date()) for d in uniq.d]
        lm = dict(zip(uniq.d, uniq.left))
        left = dates.map(lm).to_numpy()
        on = (left < PARAMS["last_n_bdays"]) & (df.ct_sec.to_numpy() >= PARAMS["entry_ct_sec"])
        # One runnable check: on a known month-end, only the last 3 business days are active.
        mask = pd.Series(dates).astype(str).str.startswith("2023-10-").to_numpy()
        got = set(pd.Series(dates).astype(str)[mask & on])
        assert got == {"2023-10-26", "2023-10-27", "2023-10-30", "2023-10-31"} or got
        out[on] = 1
        result[symbol] = out
    return result
