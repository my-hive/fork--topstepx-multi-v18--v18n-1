"""Thursday EIA natural-gas-storage release reversal.
Initial gas-storage surprise may overshoot before commercial liquidity normalizes price.
Falsify: nonpositive stressed PnL or fewer than 70 percent positive years.
"""
import numpy as np
import pandas as pd
FAMILY='energy-natural-gas-storage-event-reversal'
PARAMS={'decision_sec':34440,'exit_sec':50400,'stop_pts':.08}
def entry_risk(panel):return {s:np.full(len(d),205.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='NG':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy()
  for sess,ix in d.groupby('session',sort=False).indices.items():
   if pd.Timestamp(sess).day_of_week!=3:continue
   a=np.where(t[ix]==34140)[0];b=np.where(t[ix]==PARAMS['decision_sec'])[0]
   if not len(a) or not len(b):continue
   side=-int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]));ref=c[ix[b[0]]]
   if not side:continue
   for r in ix[b[0]+1:]:
    if t[r]>=PARAMS['exit_sec'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
    out[s][r]=side
 return out
