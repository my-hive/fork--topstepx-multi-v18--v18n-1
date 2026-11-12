"""MGC Asian physical-demand range breakout at COMEX.
Overnight Asian physical/central-bank demand establishes range; COMEX break validates it.
Falsify: nonpositive stressed PnL or fewer than 70 percent positive years.
"""
import numpy as np
FAMILY='metals-gold-asian-physical-comex-breakout-micro'
PARAMS={'start':30600,'exit':50400,'stop_pts':8.}
def entry_risk(panel):return {s:np.full(len(d),85.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='MGC':continue
  h=d.high.to_numpy();l=d.low.to_numpy();c=d.close.to_numpy();t=d.ct_sec.to_numpy()
  for ix in d.groupby('session',sort=False).indices.values():
   # session date stores prior evening and daytime; 17:00-08:29 is causal Asian range
   asian=(t[ix]>=61200)|(t[ix]<PARAMS['start'])
   if not asian.any():continue
   up=h[ix][asian].max();dn=l[ix][asian].min();side=0;ref=0.
   for r in ix:
    if t[r]<PARAMS['start'] or t[r]>=PARAMS['exit']:continue
    if not side:
     side=1 if c[r]>up else (-1 if c[r]<dn else 0);ref=c[r]
    if side:
     if (c[r]-ref)*side<=-PARAMS['stop_pts']:break
     out[s][r]=side
 return out
