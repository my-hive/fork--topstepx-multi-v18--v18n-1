"""NQ contract-roll overnight-gap continuation audit.
A verified new active contract can transmit durable institutional repricing into cash session.
Falsify on execution, cost/risk, era/year, or primary failure.
"""
import numpy as np
FAMILY='equity-nq-contract-roll-gap-continuation'
PARAMS={'entry':30600,'exit':43200,'stop_pts':12.}
def entry_risk(panel):return {s:np.full(len(d),245.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='NQ':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();co=d.contract.to_numpy();prior=None
  for _,ix in d.groupby('session',sort=False).indices.items():
   current=co[ix[0]];a=np.where(t[ix]==61200)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0]
   if prior is not None and current!=prior and len(a) and len(b):
    side=int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]));ref=c[ix[b[0]]]
    if side:
     for r in ix[b[0]+1:]:
      if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
      out[s][r]=side
   prior=current
 return out
