"""Friday NQ late-session benchmark-rebalance flow.
Friday benchmark and allocator rebalance demand can create a final-hour Nasdaq premium.
Falsify: stressed PnL, era/year, or primary failure.
"""
import numpy as np
import pandas as pd
FAMILY='equity-nasdaq-friday-close-rebalance-flow'
PARAMS={'entry':50400,'exit':54000,'stop_pts':12.}
def entry_risk(panel):return {s:np.full(len(d),245.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='NQ':continue
  t=d.ct_sec.to_numpy();c=d.close.to_numpy()
  for sess,ix in d.groupby('session',sort=False).indices.items():
   if pd.Timestamp(sess).day_of_week!=4:continue
   a=np.where(t[ix]==PARAMS['entry']-60)[0]
   if not len(a):continue
   ref=c[ix[a[0]]]
   for j in ix[a[0]+1:]:
    if t[j]>=PARAMS['exit'] or c[j]-ref<=-PARAMS['stop_pts']:break
    out[s][j]=1
 return out
