"""Experiment 13: USD momentum spillover into Treasury prices.
Mechanism: dollar strength often co-moves with rate repricing via real-rate channel.
6E (EURUSD) inverted is USD; prior-session USD direction predicts ZN next session.
Falsifier: stressed PnL <=0 or any era block <=0.
"""
import numpy as np

FAMILY = "fx-usd-rates-momentum-spillover"
PARAMS = {"lookback_sessions": 3, "risk_dollars": 250}

def entry_risk(panel):
    out = {s: np.full(len(df), PARAMS['risk_dollars'], dtype=float) for s,df in panel.items()}
    return out

def signals(panel):
    ans={}
    if '6E' not in panel or 'ZN' not in panel:
        return {s: np.zeros(len(df),dtype=np.int64) for s,df in panel.items()}
    e=panel['6E']; z=panel['ZN']
    # invert EURUSD to USD strength
    e_sessions=list(e.groupby('session',sort=False).indices.values())
    e_ret=np.array([e.close.iloc[g[-1]]-e.close.iloc[g[0]] for g in e_sessions])
    e_sess=[str(x)[:10] for x in e.session.iloc[[g[0] for g in e_sessions]].to_numpy()]
    usd_dir=dict(zip(e_sess,-np.sign(e_ret)))
    z_groups=list(z.groupby('session',sort=False).indices.values())
    z_dates=[str(x)[:10] for x in z.session.iloc[[g[0] for g in z_groups]].to_numpy()]
    out=np.zeros(len(z),dtype=np.int64)
    # prior 3 sessions in z own history, using usd direction from same calendar day
    for k in range(PARAMS['lookback_sessions'],len(z_groups)):
        date=z_dates[k]
        # use usd signal from prior available 6E sessions before current date
        prior=[d for d in e_sess if d<date][-PARAMS['lookback_sessions']:]
        if len(prior)==PARAMS['lookback_sessions']:
            sides=[usd_dir[d] for d in prior]
            consensus=int(np.sign(sum(sides)))
            if consensus: out[z_groups[k]]=consensus
    ans['6E']=np.zeros(len(e),dtype=np.int64); ans['ZN']=out
    return ans
