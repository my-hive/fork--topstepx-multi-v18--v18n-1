"""Natural-gas overnight weather-risk gap reversion in US liquidity.
Thin overnight weather repricing often unwinds as US commercial liquidity arrives.
Falsify: nonpositive stressed PnL or fewer than 70 percent positive years.
"""
import numpy as np
FAMILY='energy-natural-gas-weather-gap-reversal'
PARAMS={'entry_sec':30600,'exit_sec':50400,'risk_pts':.1}
def entry_risk(panel): return {s:np.full(len(d),255.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='NG':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy(); prev=None
  for ix in d.groupby('session',sort=False).indices.values():
   if prev is not None:
    j=np.where(t[ix]==PARAMS['entry_sec']-60)[0]
    if len(j):
     side=-int(np.sign(c[ix[j[0]]]-prev))
     if side:out[s][ix[(t[ix]>=PARAMS['entry_sec'])&(t[ix]<PARAMS['exit_sec'])]]=side
   prev=c[ix[-1]]
 return out
