"""MNQ continuation after cross-index-confirmed large opening imbalance.
Shared unusually large MES/MNQ opening move identifies broad institutional information.
Falsify: stressed PnL/eras/year gates fail or primary is zero.
"""
import numpy as np
import pandas as pd
FAMILY='equity-large-opening-magnitude-cross-index-continuation-micro'
PARAMS={'lookback':20,'entry':32400,'exit':50400,'stop_pts':100.}
def entry_risk(panel):return {s:np.full(len(d),205.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'MES','MNQ'}<=set(panel):return out
 md=panel['MES'];mc=md.close.to_numpy();mt=md.ct_sec.to_numpy(); mh=[];msig={}
 for sess,ix in md.groupby('session',sort=False).indices.items():
  a=np.where(mt[ix]==30540)[0];b=np.where(mt[ix]==PARAMS['entry']-60)[0]
  if len(a) and len(b):
   z=mc[ix[b[0]]]/mc[ix[a[0]]]-1; msig[sess]=(np.sign(z),len(mh)>=PARAMS['lookback'] and abs(z)>np.median(mh[-PARAMS['lookback']:])) ;mh.append(abs(z))
 d=panel['MNQ'];c=d.close.to_numpy();t=d.ct_sec.to_numpy();nh=[]
 for sess,ix in d.groupby('session',sort=False).indices.items():
  a=np.where(t[ix]==30540)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0]
  if not len(a) or not len(b):continue
  z=c[ix[b[0]]]/c[ix[a[0]]]-1; side=int(np.sign(z));active=len(nh)>=PARAMS['lookback'] and abs(z)>np.median(nh[-PARAMS['lookback']:]) and sess in msig and msig[sess][1] and side==int(msig[sess][0]);nh.append(abs(z))
  if not active or not side:continue
  ref=c[ix[b[0]]]
  for r in ix[b[0]+1:]:
   if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
   out['MNQ'][r]=side
 return out
