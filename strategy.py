"""MCL prior-session range breakout, micro size.
Stops cluster beyond prior-session extremes; a US-session break forces continuation.
One entry per session; 5 micros; fixed stop; flat 14:00 CT.
Falsify: nonpositive stressed PnL or fewer than 70 percent positive years.
"""
import numpy as np
FAMILY='energy-mcl-prior-range-breakout-micro-size'
PARAMS={'size':5,'stop_pts':.45,'start_sec':30600,'exit_sec':50400}
def entry_risk(panel): return {s:np.full(len(d),PARAMS['stop_pts']*100+4.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='MCL':continue
  h=d.high.to_numpy();l=d.low.to_numpy();c=d.close.to_numpy();t=d.ct_sec.to_numpy(); ph=pl=None
  for ix in d.groupby('session',sort=False).indices.values():
   if ph is not None:
    side=0;ref=0.
    for r in ix:
     if t[r]<PARAMS['start_sec'] or t[r]>=PARAMS['exit_sec']:continue
     if not side:
      side=1 if c[r]>ph else (-1 if c[r]<pl else 0);ref=c[r]
      if side:continue
     if side:
      if (c[r]-ref)*side<=-PARAMS['stop_pts']:break
      out[s][r]=side*PARAMS['size']
   ph,pl=h[ix].max(),l[ix].min()
 return out
