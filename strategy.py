"""Experiment 70: lean-hog summer grilling demand seasonal drift.
Mechanism: seasonal US grilling demand and processor procurement increase hog demand
from May through July. Known calendar, low-turnover LE-like livestock exposure.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='livestock-hog-grilling-demand-seasonality'
PARAMS={'start_month':5,'end_month':7,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='HE':
   m=pd.to_datetime(d.session.astype(str).str[:10]).dt.month.to_numpy();o[(m>=5)&(m<=7)]=1
  a[s]=o
 return a
