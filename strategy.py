"""Prior-session 3:2:1 crack-spread change continuation, traded via QM with hard stop.
Refining margin change forces crude hedge/inventory adjustment that continues next session.
Falsify: nonpositive stressed PnL or fewer than 70 percent positive years.
"""
import numpy as np
FAMILY='energy-prior-session-crack-spread-continuation'
PARAMS={'entry_sec':30600,'exit_sec':50400,'stop_pts':.45}
def entry_risk(panel): return {s:np.full(len(d),PARAMS['stop_pts']*500+5.) for s,d in panel.items()}
def _last(d):
 return d.groupby('session',sort=False).close.last()
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 if not {'QM','CL','RB','HO'}<=set(panel): return out
 cl,rb,ho=_last(panel['CL']),_last(panel['RB']),_last(panel['HO'])
 crack=((2*rb*42+ho*42-3*cl)/3).dropna(); chg=crack.diff()
 prev_sess=dict(zip(chg.index[1:],chg.index[:-1]))
 d=panel['QM'];c=d.close.to_numpy();t=d.ct_sec.to_numpy()
 for sess,ix in d.groupby('session',sort=False).indices.items():
  p=prev_sess.get(sess)
  if p is None or p not in chg.index: continue
  side=int(np.sign(chg[p]))   # change completed in prior session (known at its close)
  j=np.where(t[ix]==PARAMS['entry_sec']-60)[0]
  if not side or not len(j): continue
  ref=c[ix[j[0]]]
  for r in ix[j[0]+1:]:
   if t[r]>=PARAMS['exit_sec'] or (c[r]-ref)*side<=-PARAMS['stop_pts']:break
   out['QM'][r]=side
 return out
