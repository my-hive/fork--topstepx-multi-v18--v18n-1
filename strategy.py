"""RB extreme opening-shock dealer-inventory reversal.
An extreme first cash hour can exhaust RBOB dealer liquidity and reverse into settlement.
Falsify: stressed PnL, era/year, or primary failure.
"""
import numpy as np
FAMILY='energy-rbob-us-opening-shock-reversal'
PARAMS={'lookback':120,'quantile':.9,'entry':34200,'exit':54000,'stop_pts':.03}
def entry_risk(panel):return {s:np.full(len(d),255.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='RB':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();hist=[]
  for _,ix in d.groupby('session',sort=False).indices.items():
   a=np.where(t[ix]==30540)[0];b=np.where(t[ix]==34140)[0]
   if len(a) and len(b):
    z=c[ix[b[0]]]/c[ix[a[0]]]-1
    if len(hist)>=PARAMS['lookback'] and abs(z)>np.quantile(hist[-PARAMS['lookback']:],PARAMS['quantile']):
     side=-int(np.sign(z));ref=c[ix[b[0]]]
     if side:
      for r in ix[b[0]+1:]:
       if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
       out[s][r]=side
    hist.append(abs(z))
 return out
