"""Rates exp 3: 2s30s curve steepener relative value, 2x ZT vs 1x ZB same direction.
Mechanism: ZT and ZB share rate factor; trading their spread targets curve moves
instead of outright duration. Signal = lagged 5-minute spread change extended 1h.
Falsifier: nonpositive stressed PnL or era blocks on the paired ZT/ZB position.
"""
import numpy as np
import pandas as pd

FAMILY = "rates-curve-steepener-relative-value"
PARAMS = {"entry_ct_sec": 36000, "exit_ct_sec": 50400, "risk_dollars": 250}


def entry_risk(panel):
    return {s: np.full(len(df), PARAMS["risk_dollars"], dtype=float) for s, df in panel.items()}


def signals(panel):
    result = {}
    if "ZT" not in panel or "ZB" not in panel:
        return {s: np.zeros(len(df), dtype=np.int64) for s, df in panel.items()}
    df = panel["ZT"]
    merged = pd.concat({"ZT": panel["ZT"].close, "ZB": panel["ZB"].close}, axis=1).dropna()
    spread = merged["ZT"] - merged["ZB"]
    mom = spread - spread.shift(5)
    sign = pd.Series(np.sign(mom), index=merged.index)
    sec = panel["ZT"].ct_sec.to_numpy()
    active = (sec >= PARAMS["entry_ct_sec"]) & (sec < PARAMS["exit_ct_sec"])
    zt_sig = np.where(active, np.sign(sign.reindex(panel["ZT"].index, method="ffill").fillna(0).to_numpy()), 0).astype(int)
    zb_sig = zt_sig.copy()
    result["ZT"] = zt_sig * 2
    result["ZB"] = zb_sig
    return result
