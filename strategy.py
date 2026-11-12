"""Crypto cash-open high-range breakout.
US liquidity can resolve an unusually wide pre-open range into continuation.
Falsify: nonpositive stressed PnL or fewer than 70 percent positive years.
"""
import numpy as np
FAMILY='crypto-cash-open-volatility-breakout'
PARAMS={'start':28800,'decision':30600,'exit':36000,'lookback':20,'stop':600.}
def entry_risk(panel):return {s:np.full(len(d),280.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='MBT':continue
  h=d.high.to_numpy();l=d.low.to_numpy();c=d.close.to_numpy();t=d.ct_sec.to_numpy();rng=[]
  for ix in d.groupby('session',sort=False).indices.values():
   active=len(rng)>=PARAMS['lookback'] and rng[-1]>np.median(rng[-PARAMS['lookback']:])
   if active:
    pre=(t[ix]>=PARAMS['start'])&(t[ix]<PARAMS['decision']);ref=np.where(t[ix]==PARAMS['decision'])[0]
    if pre.any() and len(ref):
     up=h[ix][pre].max();dn=l[ix][pre].min();side=0;base=c[ix[ref[0]]]
     for r in ix[ref[0]:]:
      if t[r]>=PARAMS['exit']:break
      if not side:
       side=1 if c[r]>up else (-1 if c[r]<dn else 0)
      if side:
       if (c[r]-base)*side<=-PARAMS['stop']:break
       out[s][r]=side
   rng.append(h[ix].max()-l[ix].min())
 return out
