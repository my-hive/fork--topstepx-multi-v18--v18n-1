"""Prior-session crude settlement reversion after overnight displacement.
Commercial inventory hedges tend to restore prior settlement after thin overnight moves.
Falsify: nonpositive stressed PnL or less than 70 percent positive years.
"""
import numpy as np
FAMILY = 'energy-prior-session-settlement-mean-reversion'
PARAMS = {'entry_sec': 30600, 'exit_sec': 50400, 'risk_pts': .5}
def entry_risk(panel): return {s: np.full(len(d), 255.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='QM': continue
  c=d.close.to_numpy(); sec=d.ct_sec.to_numpy()
  prev=None
  for _,ix in d.groupby('session',sort=False).indices.items():
   # first liquid 08:30 decision based on completed 08:29 bar vs prior session close
   if prev is not None:
    hits=np.where(sec[ix]==PARAMS['entry_sec']-60)[0]
    if len(hits):
     j=hits[0]; side=-int(np.sign(c[ix[j]]-prev))
     if side: out[s][ix[(sec[ix]>=PARAMS['entry_sec'])&(sec[ix]<PARAMS['exit_sec'])]]=side
   prev=c[ix[-1]]
 return out
