"""MNQ opening trend after cross-index high-volume basket-flow confirmation.
Both MES and MNQ agree at open and have unusually high second-half-hour volume.
Falsify: stressed PnL, era/year gate, or primary failure.
"""
import numpy as np
FAMILY='equity-open-cross-index-volume-confirmed-flow'
PARAMS={'lookback':20,'entry':34200,'exit':50400,'stop_pts':100.}
def entry_risk(panel):return {s:np.full(len(d),205.) for s,d in panel.items()}
def _states(d):
 c=d.close.to_numpy();t=d.ct_sec.to_numpy();v=d.volume.to_numpy();hist=[];ans={}
 for sess,ix in d.groupby('session',sort=False).indices.items():
  a=np.where(t[ix]==30540)[0];b=np.where(t[ix]==32340)[0];vol=v[ix][(t[ix]>=32400)&(t[ix]<34200)].sum()
  if len(a) and len(b):ans[sess]=(int(np.sign(c[ix[b[0]]]-c[ix[a[0]]])),len(hist)>=20 and vol>np.median(hist[-20:]));hist.append(vol)
 return ans
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'MES','MNQ'}<=set(panel):return out
 ms=_states(panel['MES']);ns=_states(panel['MNQ']);d=panel['MNQ'];c=d.close.to_numpy();t=d.ct_sec.to_numpy()
 for sess,ix in d.groupby('session',sort=False).indices.items():
  if sess not in ms or sess not in ns:continue
  side,active=ns[sess]; other,confirm=ms[sess]
  if not side or side!=other or not active or not confirm:continue
  j=np.where(t[ix]==PARAMS['entry']-60)[0]
  if not len(j):continue
  ref=c[ix[j[0]]]
  for r in ix[j[0]+1:]:
   if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
   out['MNQ'][r]=side
 return out
