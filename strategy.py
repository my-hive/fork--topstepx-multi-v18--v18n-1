"""MCL large-EIA-shock continuation.
Unusually large inventory-release shock reveals sustained commercial dealer hedge demand.
Falsify: stressed PnL/eras/year gates fail or primary is zero.
"""
import numpy as np
import pandas as pd
FAMILY='energy-eia-magnitude-conditioned-continuation-micro'
PARAMS={'lookback_releases':20,'decision':34440,'exit':50400,'stop_pts':.5}
def entry_risk(panel):return {s:np.full(len(d),55.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='MCL':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();hist=[]
  for sess,ix in d.groupby('session',sort=False).indices.items():
   if pd.Timestamp(sess).day_of_week!=2:continue
   a=np.where(t[ix]==34140)[0];b=np.where(t[ix]==PARAMS['decision'])[0]
   if not len(a) or not len(b):continue
   move=c[ix[b[0]]]-c[ix[a[0]]]
   if len(hist)>=PARAMS['lookback_releases'] and abs(move)>np.median(hist[-PARAMS['lookback_releases']:]):
    side=int(np.sign(move));ref=c[ix[b[0]]]
    if side:
     for r in ix[b[0]+1:]:
      if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
      out[s][r]=side
   hist.append(abs(move))
 return out
