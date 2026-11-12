"""Monday weekend ES gap reversal at cash open.
Weekend news gap can unwind when institutional cash liquidity arrives Monday.
Falsify: nonpositive stressed PnL or fewer than 70 percent positive years.
"""
import numpy as np
import pandas as pd
FAMILY='equity-weekend-gap-reversal'
PARAMS={'entry_sec':30600,'exit_sec':50400,'stop_pts':4.0}
def entry_risk(panel): return {s:np.full(len(d),205.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='ES':continue
  c=d.close.to_numpy(); t=d.ct_sec.to_numpy(); prev=None
  for sess,ix in d.groupby('session',sort=False).indices.items():
   monday=pd.Timestamp(sess).day_of_week==0
   if monday and prev is not None:
    j=np.where(t[ix]==PARAMS['entry_sec']-60)[0]
    # Friday settlement/reopen proxy: prior session final printed close.
    if len(j):
     side=-int(np.sign(c[ix[j[0]]]-prev)); ref=c[ix[j[0]]]
     if side:
      for r in ix[j[0]+1:]:
       if t[r]>=PARAMS['exit_sec'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
       out[s][r]=side
   prev=c[ix[-1]]
 return out
