"""MNQ high-volume late-day benchmark-flow continuation.
High-volume 13:00-14:00 activity can be benchmark flow continuing into close.
Falsify: stressed PnL/eras/year gates fail or primary is zero.
"""
import numpy as np
FAMILY='equity-nq-late-day-high-volume-continuation-micro'
PARAMS={'lookback':20,'entry':50400,'exit':54000,'stop_pts':100.}
def entry_risk(panel):return {s:np.full(len(d),205.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='MNQ':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();v=d.volume.to_numpy();hist=[]
  for _,ix in d.groupby('session',sort=False).indices.items():
   a=np.where(t[ix]==46740)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0];vol=v[ix][(t[ix]>=46800)&(t[ix]<50400)].sum()
   if len(a) and len(b):
    if len(hist)>=PARAMS['lookback'] and vol>np.median(hist[-PARAMS['lookback']:]):
     side=int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]));ref=c[ix[b[0]]]
     if side:
      for r in ix[b[0]+1:]:
       if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
       out[s][r]=side
    hist.append(vol)
 return out
