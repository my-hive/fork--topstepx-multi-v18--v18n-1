"""MNQ large cash-open imbalance continuation.
Opening move above trailing median identifies institutional information rather than noise.
Falsify: stressed PnL/eras/year gates fail or primary is zero.
"""
import numpy as np
FAMILY='equity-nq-large-opening-imbalance-continuation-micro'
PARAMS={'lookback':20,'entry':32400,'exit':50400,'stop_pts':100.}
def entry_risk(panel):return {s:np.full(len(d),205.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='MNQ':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();hist=[]
  for _,ix in d.groupby('session',sort=False).indices.items():
   a=np.where(t[ix]==30540)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0]
   if len(a) and len(b):
    move=c[ix[b[0]]]-c[ix[a[0]]]
    if len(hist)>=PARAMS['lookback'] and abs(move)>np.median(hist[-PARAMS['lookback']:]):
     side=int(np.sign(move));ref=c[ix[b[0]]]
     if side:
      for r in ix[b[0]+1:]:
       if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
       out[s][r]=side
    hist.append(abs(move))
 return out
