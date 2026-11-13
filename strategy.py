"""ES month-end allocator-flow trend continuation.
Known month-end calendar and prior completed five-session ES trend proxy index allocation flow.
Falsify: stressed PnL, era/year, or primary failure.
"""
import numpy as np
import pandas as pd
FAMILY='equity-es-month-end-rebalance-trend'
PARAMS={'lookback':5,'entry':28800,'exit':43200,'stop_pts':6.}
def entry_risk(panel):return {s:np.full(len(d),305.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='ES':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();hist=[]
  for sess,ix in d.groupby('session',sort=False).indices.items():
   day=pd.Timestamp(sess);j=np.where(t[ix]==PARAMS['entry']-60)[0]
   if day.day>=29 and len(hist)>=PARAMS['lookback'] and len(j):
    side=int(np.sign(sum(hist[-PARAMS['lookback']:])))
    if side:
     ref=c[ix[j[0]]]
     for r in ix[j[0]+1:]:
      if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
      out[s][r]=side
   hist.append(c[ix[-1]]/c[ix[0]]-1)
 return out
