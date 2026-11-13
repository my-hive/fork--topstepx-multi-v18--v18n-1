"""Extreme EUR/GBP overnight divergence reversal into US cash liquidity.
Large opposing European FX flows can be temporary relative-value positioning that normalizes in US liquidity.
Falsify: stressed PnL, era/year, or primary failure.
"""
import numpy as np
FAMILY='fx-euro-pound-overnight-relativevalue-extreme-reversal'
PARAMS={'lookback':120,'entry':30600,'exit':50400,'stop_pts':.002}
def entry_risk(panel):return {s:np.full(len(d),255.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 a=panel.get('6E');b=panel.get('6B')
 if a is None or b is None:return out
 ae=[];be=[]
 ag={k:v for k,v in a.groupby('session',sort=False).indices.items()};bg={k:v for k,v in b.groupby('session',sort=False).indices.items()}
 ca=a.close.to_numpy();cb=b.close.to_numpy();ta=a.ct_sec.to_numpy()
 for sess,ix in ag.items():
  jx=bg.get(sess)
  ia=np.where(ta[ix]==61200)[0];ib=np.where(ta[ix]==PARAMS['entry']-60)[0]
  tb=b.ct_sec.to_numpy()
  ja=np.where(tb[jx]==61200)[0] if jx is not None else [];jb=np.where(tb[jx]==PARAMS['entry']-60)[0] if jx is not None else []
  if len(ia) and len(ib) and len(ja) and len(jb):
   re=ca[ix[ib[0]]]/ca[ix[ia[0]]]-1;rb=cb[jx[jb[0]]]/cb[jx[ja[0]]]-1
   if len(ae)>=PARAMS['lookback'] and np.sign(re)!=np.sign(rb) and abs(re)>np.median(ae[-PARAMS['lookback']:]) and abs(rb)>np.median(be[-PARAMS['lookback']:]):
    side=-int(np.sign(re));ref=ca[ix[ib[0]]]
    for z in ix[ib[0]+1:]:
     if ta[z]>=PARAMS['exit'] or (ca[z]-ref)*side<=-PARAMS['stop_pts']:break
     out['6E'][z]=side
   ae.append(abs(re));be.append(abs(rb))
 return out
