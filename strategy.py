"""Experiment 71: soybean-oil biodiesel demand seasonality.
Mechanism: summer driving/biodiesel blending demand supports soybean oil during May-Aug.
Known seasonal calendar, low turnover. Falsifier: stressed PnL <=0 or any era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='grains-soy-oil-biodiesel-seasonality'
PARAMS={'start_month':5,'end_month':8,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZL':
   m=pd.to_datetime(d.session.astype(str).str[:10]).dt.month.to_numpy();o[(m>=5)&(m<=8)]=1
  a[s]=o
 return a
