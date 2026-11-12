"""M6E London-fix inventory reversal.
09:30-10:00 CT dealer flow into London fix can revert after inventory transfer.
Falsify: nonpositive stressed PnL or fewer than 70 percent positive years.
"""
import numpy as np
FAMILY='fx-london-fix-reversal-micro'
PARAMS={'signal_start':34200,'entry':36000,'exit':39600,'risk_dollars':250.}
def entry_risk(panel):return {s:np.full(len(d),PARAMS['risk_dollars']) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='M6E':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy()
  for ix in d.groupby('session',sort=False).indices.values():
   a=np.where(t[ix]==PARAMS['signal_start']-60)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0]
   if not len(a) or not len(b):continue
   side=-int(np.sign(c[ix[b[0]]]-c[ix[a[0]]]))
   if side:out[s][ix[(t[ix]>=PARAMS['entry'])&(t[ix]<PARAMS['exit'])]]=side
 return out
