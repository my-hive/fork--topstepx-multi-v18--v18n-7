"""Experiment 43: 2-year Treasury auction short-covering.
Mechanism: front-end Treasury supply concession before monthly 2-year auction is covered
after auction; long ZT on known fourth-Monday-ish auction calendar proxy.
Falsifier: stressed PnL <=0 or any chronological era PnL <=0.
"""
import numpy as np,pandas as pd
FAMILY='rates-front-end-auction-shortcovering'
PARAMS={'weekday':0,'week_number':4,'entry_ct_sec':36000,'exit_ct_sec':43200,'risk_dollars':250}
def entry_risk(p):return{s:np.full(len(d),250.,dtype=float)for s,d in p.items()}
def signals(p):
 a={}
 for s,d in p.items():
  o=np.zeros(len(d),dtype=np.int64)
  if s=='ZT':
   date=pd.to_datetime(d.session.astype(str).str[:10]); on=(date.dt.weekday==0)&(date.dt.day.between(22,28));t=d.ct_sec.to_numpy();o[on&(t>=36000)&(t<43200)]=1
  a[s]=o
 return a
