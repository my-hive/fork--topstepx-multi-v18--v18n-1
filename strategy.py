"""NQ late-session institutional benchmark-flow continuation.
13:30-14:00 direction can persist into close as benchmark and ETF hedges execute.
Falsify: stressed PnL nonpositive, era/year gates fail, or primary is zero.
"""
import numpy as np
FAMILY='equity-nq-late-session-institutional-continuation'
PARAMS={'entry':50400,'exit':54000,'stop_pts':12.}
def entry_risk(panel):return {s:np.full(len(d),245.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='NQ':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy()
  for _,ix in d.groupby('session',sort=False).indices.items():
   a=np.where(t[ix]==48600-60)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0]
   if not len(a) or not len(b):continue
   side=int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]));ref=c[ix[b[0]]]
   if not side:continue
   for r in ix[b[0]+1:]:
    if t[r]>=PARAMS['exit'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
    out[s][r]=side
 return out
