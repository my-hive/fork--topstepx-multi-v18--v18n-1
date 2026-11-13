"""CL high-volume prior close-extreme continuation.
A high-volume close at a session extreme can represent durable physical hedging carried into cash hours.
Falsify: stressed PnL, era/year, or primary failure.
"""
import numpy as np
FAMILY='energy-crude-prior-settlement-extreme-volume-continuation'
PARAMS={'lookback':20,'entry':30600,'exit':50400,'stop_pts':.15}
def entry_risk(panel):return {s:np.full(len(d),155.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='CL':continue
  c=d.close.to_numpy();h=d.high.to_numpy();l=d.low.to_numpy();v=d.volume.to_numpy();t=d.ct_sec.to_numpy();lasts=[];ranges=[];vols=[]
  for _,ix in d.groupby('session',sort=False).indices.items():
   j=np.where(t[ix]==PARAMS['entry']-60)[0]
   if len(j) and len(vols)>=PARAMS['lookback']:
    lo,hi,last=ranges[-1][0],ranges[-1][1],lasts[-1];loc=(last-lo)/(hi-lo) if hi>lo else .5
    if (loc<=.25 or loc>=.75) and vols[-1]>np.median(vols[-PARAMS['lookback']:]):
     side=1 if loc>=.75 else -1;ref=c[ix[j[0]]]
     for r in ix[j[0]+1:]:
      if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
      out[s][r]=side
   lasts.append(c[ix[-1]]);ranges.append((l[ix].min(),h[ix].max()));vols.append(v[ix].sum())
 return out
