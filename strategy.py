"""NQ opening trend with second-half-hour institutional volume confirmation.
Volume confirmation identifies ETF/basket participation after cash-open imbalance.
Falsify: stressed PnL, era/year gate, or primary failure.
"""
import numpy as np
FAMILY='equity-nq-morning-volume-confirmed-trend'
PARAMS={'lookback':20,'entry':34200,'exit':50400,'stop_pts':12.}
def entry_risk(panel):return {s:np.full(len(d),245.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='NQ':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();v=d.volume.to_numpy();hist=[]
  for _,ix in d.groupby('session',sort=False).indices.items():
   a=np.where(t[ix]==30540)[0];b=np.where(t[ix]==32340)[0];j=np.where(t[ix]==PARAMS['entry']-60)[0]
   vol=v[ix][(t[ix]>=32400)&(t[ix]<34200)].sum()
   if len(a) and len(b) and len(j):
    if len(hist)>=PARAMS['lookback'] and vol>np.median(hist[-PARAMS['lookback']]):
     side=int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]));ref=c[ix[j[0]]]
     if side:
      for r in ix[j[0]+1:]:
       if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
       out[s][r]=side
    hist.append(vol)
 return out
