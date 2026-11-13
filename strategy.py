"""Quarter-end MNQ opening allocation-flow continuation.
Quarter-end benchmark and ETF rebalancing can sustain first cash-open imbalance.
Falsify: stressed PnL/eras/year gates fail or primary is zero.
"""
import numpy as np
import pandas as pd
FAMILY='equity-micro-opening-imbalance-quarter-end-allocation'
PARAMS={'entry':32400,'exit':50400,'stop_pts':100.}
def entry_risk(panel):return {s:np.full(len(d),205.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='MNQ':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy()
  dates=list(d.groupby('session',sort=False).indices.items()); bymonth={}
  for sess,ix in dates:bymonth.setdefault(pd.Timestamp(sess).to_period('M'),[]).append((sess,ix))
  for month,days in bymonth.items():
   if month.month not in (3,6,9,12):continue
   pick=days[:2]+days[-2:]
   for sess,ix in pick:
    a=np.where(t[ix]==30540)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0]
    if not len(a) or not len(b):continue
    side=int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]));ref=c[ix[b[0]]]
    if not side:continue
    for r in ix[b[0]+1:]:
     if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
     out[s][r]=side
 return out
