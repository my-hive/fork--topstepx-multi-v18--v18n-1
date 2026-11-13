"""HO high-volume midday inventory reversion.
High-volume midday refined-product move can be dealer inventory transfer unwinding into afternoon.
Falsify: stressed PnL/eras/year gates fail or primary is zero.
"""
import numpy as np
FAMILY='energy-heating-oil-high-volume-midday-liquidity-reversion'
PARAMS={'lookback':20,'entry':43200,'exit':50400,'stop_pts':.05}
def entry_risk(panel):return {s:np.full(len(d),255.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='HO':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();v=d.volume.to_numpy();hist=[]
  for _,ix in d.groupby('session',sort=False).indices.items():
   a=np.where(t[ix]==39540)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0];vol=v[ix][(t[ix]>=39600)&(t[ix]<43200)].sum()
   if len(a) and len(b):
    if len(hist)>=PARAMS['lookback'] and vol>np.median(hist[-PARAMS['lookback']:])):
     side=-int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]));ref=c[ix[b[0]]]
     if side:
      for r in ix[b[0]+1:]:
       if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
       out[s][r]=side
    hist.append(vol)
 return out
