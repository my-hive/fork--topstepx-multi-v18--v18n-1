"""Spring gasoline seasonal trend continuation.
Seasonal demand ramp changes commercial hedge balance and can sustain prior trend.
Falsify: nonpositive stressed PnL or fewer than 70 percent positive years.
"""
import numpy as np
import pandas as pd
FAMILY='energy-rb-gasoline-seasonal-window-trend'
PARAMS={'entry_sec':30600,'exit_sec':50400,'lookback_sessions':20,'stop_pts':.02}
def entry_risk(panel):return {s:np.full(len(d),210.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='RB':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy(); groups=list(d.groupby('session',sort=False).indices.values()); closes=[]
  for i,ix in enumerate(groups):
   m=pd.Timestamp(d.session.iloc[ix[0]]).month
   if i>=PARAMS['lookback_sessions'] and m in (3,4,5,6):
    side=int(np.sign(closes[-1]-closes[-PARAMS['lookback_sessions']]))
    if side:
     ref=c[ix[np.where(t[ix]==PARAMS['entry_sec']-60)[0][0]]] if np.any(t[ix]==PARAMS['entry_sec']-60) else c[ix[0]]
     for r in ix[(t[ix]>=PARAMS['entry_sec'])&(t[ix]<PARAMS['exit_sec'])]:
      if (c[r]-ref)*side<=-PARAMS['stop_pts']:break
      out[s][r]=side
   closes.append(c[ix[-1]])
 return out
