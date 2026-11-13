"""6E extreme overnight macro-repricing continuation into US session.
Top-tail overnight EURUSD repricing can carry information into US macro hedge flows.
Falsify: stressed PnL, era/year, or primary failure.
"""
import numpy as np
FAMILY='fx-euro-extreme-overnight-us-continuation'
PARAMS={'lookback':120,'quantile':.95,'entry':30600,'exit':50400,'stop_pts':.002}
def entry_risk(panel):return {s:np.full(len(d),255.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='6E':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();hist=[]
  for _,ix in d.groupby('session',sort=False).indices.items():
   a=np.where(t[ix]==61200)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0]
   if len(a) and len(b):
    ret=c[ix[b[0]]]/c[ix[a[0]]-1
    if len(hist)>=PARAMS['lookback'] and abs(ret)>np.quantile(hist[-PARAMS['lookback']:],PARAMS['quantile']):
     side=int(np.sign(ret));ref=c[ix[b[0]]]
     if side:
      for r in ix[b[0]+1:]:
       if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
       out[s][r]=side
    hist.append(abs(ret))
 return out
