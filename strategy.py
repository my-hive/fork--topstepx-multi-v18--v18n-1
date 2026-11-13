"""Wednesday NQ extreme lunch institutional-execution continuation.
Systematic midweek allocation can make exceptional lunch repricing persist into closing liquidity.
Falsify: stressed PnL, era/year, or primary failure.
"""
import numpy as np
import pandas as pd
FAMILY='equity-nasdaq-wednesday-lunch-extreme-continuation'
PARAMS={'lookback':120,'quantile':.9,'entry':43200,'exit':54000,'stop_pts':12.}
def entry_risk(panel):return {s:np.full(len(d),245.) for s,d in panel.items()}
def signals(panel):
 out={s:np.zeros(len(d),dtype=np.int64) for s,d in panel.items()}
 for s,d in panel.items():
  if s!='NQ':continue
  c=d.close.to_numpy();t=d.ct_sec.to_numpy();hist=[]
  for sess,ix in d.groupby('session',sort=False).indices.items():
   a=np.where(t[ix]==39600)[0];b=np.where(t[ix]==PARAMS['entry']-60)[0]
   if len(a) and len(b):
    r=c[ix[b[0]]]/c[ix[a[0]]]-1
    if pd.Timestamp(sess).day_of_week==2 and len(hist)>=PARAMS['lookback'] and abs(r)>np.quantile(hist[-PARAMS['lookback']:],PARAMS['quantile']):
     side=int(np.sign(r));ref=c[ix[b[0]]]
     if side:
      for j in ix[b[0]+1:]:
       if t[j]>=PARAMS['exit'] or (c[j]-ref)*side<=-PARAMS['stop_pts']:break
       out[s][j]=side
    hist.append(abs(r))
 return out
