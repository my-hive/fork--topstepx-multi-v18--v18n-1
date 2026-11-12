"""Tuesday reversal of prior Monday MES session return.
Monday institutional displacement can partly reverse as active managers rebalance Tuesday.
Falsify: nonpositive stressed PnL or fewer than 70 percent positive years.
"""
import numpy as np
import pandas as pd
FAMILY='equity-tuesday-reversal-micro'
PARAMS={'size':5,'entry':30600,'exit':50400,'stop_pts':10.}
def entry_risk(panel):return {s:np.full(len(d),PARAMS['stop_pts']*5*PARAMS['size']+10.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='MES':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();prev=None
  for sess,ix in d.groupby('session',sort=False).indices.items():
   day=pd.Timestamp(sess)
   if day.day_of_week==1 and prev is not None:
    j=np.where(t[ix]==PARAMS['entry']-60)[0]
    side=-int(np.sign(prev))
    if len(j) and side:
     ref=c[ix[j[0]]]
     for r in ix[j[0]+1:]:
      if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
      out[s][r]=side*PARAMS['size']
   prev=c[ix[-1]]/c[ix[0]]-1
 return out
