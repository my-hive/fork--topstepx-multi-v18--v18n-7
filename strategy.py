"""v18n-7 independent causal audit of CL month-boundary hedging continuation.
Prior five completed session return, first/last three weekday business dates,
08:00-12:00 CT. One CL, completed-bar $250 stop (not guaranteed fill loss cap).
"""
import numpy as np
import pandas as pd
FAMILY = "energy-crude-turn-of-month-causal-independent-audit"
PARAMS = {"trend_sessions": 5, "boundary_business_days": 3,
          "entry_sec": 28800, "exit_sec": 43200, "stop_dollars": 250}

def signals(panel):
    ans = {s: np.zeros(len(d), dtype=np.int64) for s, d in panel.items()}
    if "CL" not in panel:
        return ans
    d = panel["CL"]
    labels = d.session.astype(str)
    last = d.close.groupby(labels, sort=False).last()
    # Shift before mapping: no current-session closing value in any signal.
    sides = np.sign(last.shift(1) - last.shift(1 + PARAMS["trend_sessions"]))
    c, sec = d.close.to_numpy(), d.ct_sec.to_numpy()
    for label, ix in d.groupby(labels, sort=False).indices.items():
        date = pd.Timestamp(label).normalize()
        first = date.replace(day=1)
        end = first + pd.offsets.MonthEnd(0)
        grid = pd.bdate_range(first, end)
        chosen = date in grid[:PARAMS["boundary_business_days"]] or date in grid[-PARAMS["boundary_business_days"]:]
        side = sides.get(label, np.nan)
        if not chosen or not np.isfinite(side) or side == 0:
            continue
        hit = ix[(sec[ix] >= PARAMS["entry_sec"]) & (sec[ix] < PARAMS["exit_sec"])]
        if not len(hit):
            continue
        ref = c[hit[0]]
        for i in hit:
            if side * (c[i] - ref) * 1000 <= -PARAMS["stop_dollars"]:
                break
            ans["CL"][i] = int(side)
    return ans

def entry_risk(panel):
    return {s: np.full(len(d), PARAMS["stop_dollars"] if s == "CL" else 0., dtype=float)
            for s, d in panel.items()}
