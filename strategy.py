"""Heating-oil lead into gasoline spread trend day.
Distillate demand can lead refined-product inventory allocation and next RB direction.
Falsify: nonpositive stressed PnL or fewer than 70 percent positive years.
"""
import numpy as np
FAMILY='cross-energy-ho-rb-spread-trend-day'
PARAMS={'entry_sec':30600,'exit_sec':50400,'stop_pts':.02}
def entry_risk(panel):return {s:np.full(len(d),210.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'HO','RB'}<=set(panel):return out
 h=panel['HO'].groupby('session',sort=False).close.last().diff();r=panel['RB']; c=r.close.to_numpy();t=r.ct_sec.to_numpy(); prev=None
 for sess,ix in r.groupby('session',sort=False).indices.items():
  if prev is not None and prev in h.index and np.isfinite(h[prev]):
   side=int(np.sign(h[prev]));j=np.where(t[ix]==PARAMS['entry_sec']-60)[0]
   if side and len(j):
    ref=c[ix[j[0]]]
    for q in ix[j[0]+1:]:
     if t[q]>=PARAMS['exit_sec'] or (c[q]-ref)*side<=-PARAMS['stop_pts']:break
     out['RB'][q]=side
  prev=sess
 return out
