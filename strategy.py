"""Winter heating-oil storage trend continuation.
Oct-Mar commercial heating-oil storage hedging can sustain daily trend into next US morning.
Falsify: nonpositive stressed PnL or fewer than 70 percent positive years.
"""
import numpy as np
import pandas as pd
FAMILY='energy-heating-oil-winter-storage-trend'
PARAMS={'entry_sec':30600,'exit_sec':50400,'lookback_sessions':20,'risk_pts':.005}
def entry_risk(panel): return {s:np.full(len(d),215.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='HO':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy(); groups=list(d.groupby('session',sort=False).indices.values()); closes=[]
  for i,ix in enumerate(groups):
   month=pd.Timestamp(d.session.iloc[ix[0]]).month
   if i>=PARAMS['lookback_sessions'] and month in (10,11,12,1,2,3):
    side=int(np.sign(closes[-1]-np.mean(closes[-PARAMS['lookback_sessions']:]))); 
    if side:out[s][ix[(t[ix]>=PARAMS['entry_sec'])&(t[ix]<PARAMS['exit_sec'])]]=side
   closes.append(c[ix[-1]])
 return out
