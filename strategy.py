"""SIL prior-session liquidity-shock reversion at COMEX.
Prior silver session displacement may reverse as metal-dealer inventory arbitrage normalizes.
Falsify: stressed PnL/eras/year gates fail or primary is zero.
"""
import numpy as np
FAMILY='metals-silver-prior-session-reversion-micro'
PARAMS={'entry':30600,'exit':50400,'stop_pts':.35}
def entry_risk(panel):return {s:np.full(len(d),355.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='SIL':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();prev=None
  for _,ix in d.groupby('session',sort=False).indices.items():
   if prev is not None:
    j=np.where(t[ix]==PARAMS['entry']-60)[0];side=-int(np.sign(prev))
    if len(j) and side:
     ref=c[ix[j[0]]]
     for r in ix[j[0]+1:]:
      if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
      out[s][r]=side
   prev=c[ix[-1]]/c[ix[0]]-1
 return out
