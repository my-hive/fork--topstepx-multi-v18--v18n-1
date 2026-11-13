"""Wednesday MYM cash-session systematic allocation drift.
Midweek institutional basket allocation can create a Dow cash-session premium.
Falsify: stressed PnL, era/year, or primary failure.
"""
import numpy as np
import pandas as pd
FAMILY='equity-mym-wednesday-systematic-allocation-cash-drift'
PARAMS={'entry':30600,'exit':50400,'stop_pts':200.}
def entry_risk(panel):return {s:np.full(len(d),205.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='MYM':continue
  t=d.ct_sec.to_numpy();c=d.close.to_numpy()
  for sess,ix in d.groupby('session',sort=False).indices.items():
   if pd.Timestamp(sess).day_of_week!=2:continue
   j=np.where(t[ix]==PARAMS['entry']-60)[0]
   if not len(j):continue
   ref=c[ix[j[0]]]
   for r in ix[j[0]+1:]:
    if t[r]>=PARAMS['exit'] or c[r]-ref<=-PARAMS['stop_pts']:break
    out[s][r]=1
 return out
