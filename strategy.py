"""Approximate FOMC-statement late NQ drift.
Statement shock reprices discount-rate expectations after 13:00 CT.
Falsify: nonpositive stressed PnL or fewer than 70 percent positive years.
"""
import numpy as np
import pandas as pd
FAMILY='equity-fomc-statement-late-drift'
PARAMS={'decision':48600,'exit':54000,'stop_pts':15.}
def entry_risk(panel):return {s:np.full(len(d),305.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='NQ':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy()
  for sess,ix in d.groupby('session',sort=False).indices.items():
   day=pd.Timestamp(sess)
   # third Wednesday: approximate calendar, a declared non-optimized proxy
   if day.day_of_week!=2 or not 15<=day.day<=21:continue
   a=np.where(t[ix]==46800-60)[0];b=np.where(t[ix]==PARAMS['decision']-60)[0]
   if not len(a) or not len(b):continue
   side=int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]));ref=c[ix[b[0]]]
   if not side:continue
   for r in ix[b[0]+1:]:
    if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
    out[s][r]=side
 return out
