"""Experiment 22: live-cattle grilling-demand seasonal long.
Mechanism: summer grilling demand and feedlot drawdowns support cattle May-July.
Known calendar, low turnover. Falsifier: stressed PnL <=0 or any era block <=0.
"""
import numpy as np,pandas as pd
FAMILY='livestock-grilling-demand-seasonality'
PARAMS={'start_month':5,'end_month':7,'risk_dollars':250}
def entry_risk(panel): return {s:np.full(len(d),PARAMS['risk_dollars'],dtype=float) for s,d in panel.items()}
def signals(panel):
 ans={}
 for s,d in panel.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='LE':
   m=pd.to_datetime(d.session.astype(str).str[:10]).dt.month.to_numpy();o[(m>=PARAMS['start_month'])&(m<=PARAMS['end_month'])]=1
  ans[s]=o
 return ans
