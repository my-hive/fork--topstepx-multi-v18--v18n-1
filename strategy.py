"""Platinum overnight global-session continuation into COMEX.
Asian/European industrial price discovery can carry into COMEX hedging.
Falsify: stressed PnL nonpositive, era/year gates fail, or primary is zero.
"""
import numpy as np
FAMILY='metals-platinum-overnight-continuation'
PARAMS={'entry':30600,'exit':50400,'stop_pts':8.}
def entry_risk(panel):return {s:np.full(len(d),205.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='PL':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy()
  for ix in d.groupby('session',sort=False).indices.values():
   a=np.where(t[ix]==61200)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0]
   if not len(a) or not len(b):continue
   side=int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]));ref=c[ix[b[0]]]
   if not side:continue
   for r in ix[b[0]+1:]:
    if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
    out[s][r]=side
 return out
