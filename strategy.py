"""Monday MNQ high-volume opening inventory reversal.
High first-hour Monday volume can mark weekend-gap inventory unwinding after cash auction.
Falsify: stressed PnL, era/year, or primary failure.
"""
import numpy as np
import pandas as pd
FAMILY='equity-mnq-monday-weekend-volume-confirmed-reversal'
PARAMS={'lookback':20,'entry':32400,'exit':50400,'stop_pts':100.}
def entry_risk(panel):return {s:np.full(len(d),205.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='MNQ':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();v=d.volume.to_numpy();hist=[]
  for sess,ix in d.groupby('session',sort=False).indices.items():
   a=np.where(t[ix]==30540)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0];vol=v[ix][(t[ix]>=30600)&(t[ix]<34200)].sum()
   if pd.Timestamp(sess).day_of_week==0 and len(a) and len(b) and len(hist)>=PARAMS['lookback'] and vol>np.median(hist[-PARAMS['lookback']:]):
    side=-int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]));ref=c[ix[b[0]]]
    if side:
     for r in ix[b[0]+1:]:
      if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
      out[s][r]=side
   hist.append(vol)
 return out
