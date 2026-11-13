"""Experiment 151: causal CL turn-of-month refinery scheduling audit.
Mechanism: refinery nominations and producer hedge rolls cluster around month boundary;
prior five completed sessions' direction persists in US physical-energy hours.
Use causal calendar and only 08:30-13:00 to avoid overnight discontinuity churn.
Falsifier: nonpositive stressed PnL, any era PnL <=0, or zero primary statistic.
"""
import numpy as np
import pandas as pd
FAMILY='energy-crude-turn-month-scheduling-causal-audit'
PARAMS={'trend_sessions':5,'window_business_days':3,'entry_ct_sec':30600,'exit_ct_sec':46800,'risk_dollars':250}
def entry_risk(panel): return {s:np.full(len(d),250.,dtype=float) for s,d in panel.items()}
def signals(panel):
 ans={}
 for s,d in panel.items():
  out=np.zeros(len(d),dtype=np.int64)
  if s=='CL':
   c,t=d.close.to_numpy(),d.ct_sec.to_numpy(); gs=list(d.groupby('session',sort=False).indices.values())
   r=np.array([c[g[-1]]-c[g[0]] for g in gs]); dates=pd.to_datetime(d.session.iloc[[g[0] for g in gs]].astype(str).str[:10])
   month_end=dates+pd.offsets.MonthEnd(0)
   left=np.array([np.busday_count(x.date(),y.date()) for x,y in zip(dates,month_end)])
   first=np.array([np.busday_count(x.replace(day=1).date(),x.date()) for x in dates])
   for k in range(PARAMS['trend_sessions'],len(gs)):
    if left[k]<PARAMS['window_business_days'] or first[k]<PARAMS['window_business_days']:
     side=int(np.sign(r[k-PARAMS['trend_sessions']:k].sum()));g=gs[k]
     out[g[(t[g]>=PARAMS['entry_ct_sec'])&(t[g]<PARAMS['exit_ct_sec'])]]=side
  ans[s]=out
 return ans
