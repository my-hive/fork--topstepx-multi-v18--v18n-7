"""Experiment 21: Treasury auction supply-concession reversal.
Mechanism: pre-auction cheapening and post-auction short covering cause mean reversion
around scheduled coupon auctions. Calendar proxied by regular Treasury auction days;
use second Wednesday/month as simple known calendar event. Falsifier: nonpositive PnL/era.
"""
import numpy as np, pandas as pd
FAMILY='rates-auction-concession-reversal'
PARAMS={'weekday':2,'nth_week':2,'entry_ct_sec':36000,'exit_ct_sec':50400,'risk_dollars':250}
def entry_risk(panel): return {s:np.full(len(d),PARAMS['risk_dollars'],dtype=float) for s,d in panel.items()}
def signals(panel):
 ans={}
 for s,d in panel.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZN':
   dates=pd.to_datetime(d.session.astype(str).str[:10]); on=np.array([x.weekday()==PARAMS['weekday'] and 7<(x.day)<=14 for x in dates]); sec=d.ct_sec.to_numpy(); o[on&(sec>=PARAMS['entry_ct_sec'])&(sec<PARAMS['exit_ct_sec'])]=1
  ans[s]=o
 return ans
