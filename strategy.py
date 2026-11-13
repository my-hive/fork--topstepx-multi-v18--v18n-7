"""Experiment 25: soybean planting-weather risk premium.
Mechanism: Apr-May planting weather uncertainty raises soybean risk premium. Known
seasonal calendar, low turnover. Falsifier: nonpositive stressed PnL or any era <=0.
"""
import numpy as np,pandas as pd
FAMILY='grains-planting-weather-risk-premium'
PARAMS={'start_month':4,'end_month':5,'risk_dollars':250}
def entry_risk(panel):return{s:np.full(len(d),PARAMS['risk_dollars'],dtype=float)for s,d in panel.items()}
def signals(panel):
 ans={}
 for s,d in panel.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZS':
   m=pd.to_datetime(d.session.astype(str).str[:10]).dt.month.to_numpy();o[(m>=4)&(m<=5)]=1
  ans[s]=o
 return ans
