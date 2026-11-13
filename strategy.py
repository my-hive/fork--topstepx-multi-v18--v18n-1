"""MNQ midday reversion after broad high-volume cross-index inventory flow.
Synchronized MES/MNQ 11:00-12:00 volume and direction indicates dealer inventory transfer.
Falsify: stressed PnL, era/year gate, or primary failure.
"""
import numpy as np
FAMILY='equity-midday-cross-index-volume-reversion'
PARAMS={'lookback':20,'entry':43200,'exit':50400,'stop_pts':100.}
def entry_risk(panel):return {s:np.full(len(d),205.) for s,d in panel.items()}
def _states(d):
 c=d.close.to_numpy();t=d.ct_sec.to_numpy();v=d.volume.to_numpy();hist=[];ans={}
 for sess,ix in d.groupby('session',sort=False).indices.items():
  a=np.where(t[ix]==39540)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0];vol=v[ix][(t[ix]>=39600)&(t[ix]<43200)].sum()
  if len(a) and len(b):ans[sess]=(int(np.sign(c[ix[b[0]]]-c[ix[a[0]]])),len(hist)>=PARAMS['lookback'] and vol>np.median(hist[-PARAMS['lookback']:]))
  hist.append(vol)
 return ans
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'MES','MNQ'}<=set(panel):return out
 ms=_states(panel['MES']);ns=_states(panel['MNQ']);d=panel['MNQ'];c=d.close.to_numpy();t=d.ct_sec.to_numpy()
 for sess,ix in d.groupby('session',sort=False).indices.items():
  if sess not in ms or sess not in ns:continue
  side,active=ns[sess];other,confirm=ms[sess]
  if not side or side!=other or not active or not confirm:continue
  j=np.where(t[ix]==PARAMS['entry']-60)[0]
  if not len(j):continue
  ref=c[ix[j[0]]];side=-side
  for r in ix[j[0]+1:]:
   if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
   out['MNQ'][r]=side
 return out
