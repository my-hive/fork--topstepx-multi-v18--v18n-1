"""Crude volatility-compression morning breakout.
Prior-session compressed range signals deferred inventory-risk transfer; first 30-min range break expands.
Falsify: nonpositive stressed PnL or fewer than 70 percent positive years.
"""
import numpy as np
FAMILY='energy-qm-volatility-compression-breakout'
PARAMS={'range_start':30600,'range_end':32400,'exit_sec':50400,'lookback_sessions':20,'risk_pts':.5}
def entry_risk(panel): return {s:np.full(len(d),255.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='QM':continue
  hi=d.high.to_numpy();lo=d.low.to_numpy();cl=d.close.to_numpy();t=d.ct_sec.to_numpy(); groups=list(d.groupby('session',sort=False).indices.values()); ranges=[]
  for i,ix in enumerate(groups):
   active=i>=PARAMS['lookback_sessions'] and ranges[-1]<np.median(ranges[-PARAMS['lookback_sessions']:])
   if active:
    pre=(t[ix]>=PARAMS['range_start'])&(t[ix]<PARAMS['range_end'])
    if pre.any():
     upper=hi[ix][pre].max(); lower=lo[ix][pre].min(); side=0
     for k,row in enumerate(ix):
      if t[row]<PARAMS['range_end'] or t[row]>=PARAMS['exit_sec']:continue
      if not side:
       side=1 if cl[row]>upper else (-1 if cl[row]<lower else 0)
      if side:out[s][row]=side
   ranges.append(hi[ix].max()-lo[ix].min())
 return out
