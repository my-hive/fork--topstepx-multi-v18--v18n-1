"""RB opening reversal after a compressed prior session.
Quiet prior product session makes next opening imbalance more likely liquidity inventory than information.
Falsify: stressed PnL, era/year, or primary failure.
"""
import numpy as np
FAMILY='energy-rbob-prior-range-compression-opening-reversal'
PARAMS={'lookback':20,'entry':32400,'exit':50400,'stop_pts':.03}
def entry_risk(panel):return {s:np.full(len(d),255.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='RB':continue
  c=d.close.to_numpy();h=d.high.to_numpy();l=d.low.to_numpy();t=d.ct_sec.to_numpy();hist=[]
  for _,ix in d.groupby('session',sort=False).indices.items():
   a=np.where(t[ix]==30540)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0]
   if len(a) and len(b):
    if len(hist)>=PARAMS['lookback'] and hist[-1]<np.median(hist[-PARAMS['lookback']:]):
     side=-int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]));ref=c[ix[b[0]]]
     if side:
      for r in ix[b[0]+1:]:
       if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
       out[s][r]=side
    hist.append(h[ix].max()-l[ix].min())
 return out
