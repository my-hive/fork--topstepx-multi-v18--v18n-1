"""Month-end crude roll-pressure continuation.
Roll-related commercial hedging can extend overnight direction in final two business sessions.
Falsify: nonpositive stressed PnL or <70 percent positive years.
"""
import numpy as np
import pandas as pd
FAMILY='energy-month-end-roll-pressure'
PARAMS={'entry_sec':30600,'exit_sec':50400,'risk_pts':.5}
def entry_risk(panel): return {s:np.full(len(d),255.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='QM':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy()
  for sess,ix in d.groupby('session',sort=False).indices.items():
   day=pd.Timestamp(sess); # calendar last two weekdays intentionally, holiday sessions still harmless
   if (day+pd.offsets.BDay(2)).month==day.month: continue
   j=np.where(t[ix]==PARAMS['entry_sec']-60)[0]
   k=np.where(t[ix]==64800-60)[0]
   if len(j) and len(k):
    side=int(np.sign(c[ix[j[0]]]-c[ix[k[0]]]))
    if side:out[s][ix[(t[ix]>=PARAMS['entry_sec'])&(t[ix]<PARAMS['exit_sec'])]]=side
 return out
