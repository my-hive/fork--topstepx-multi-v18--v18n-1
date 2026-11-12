"""EIA Wednesday crude inventory-release drift on QM (mini crude, 500 bbl).
Mechanism: 09:30 CT Wed EIA report; surprise digested over hours (dealer inventory/hedging).
Signal: sign of 09:30-09:34 CT return, enter 09:35 fill, hold to 14:00 CT, fixed stop.
Falsify: negative stressed PnL or <70% positive years.
"""
import numpy as np

FAMILY = "energy-eia-wed-inventory-drift"
PARAMS = {'stop_pts': 0.5, 'decision_sec': 34440, 'exit_sec': 50400}
SYMS = ('QM',)

def entry_risk(panel):
    return {s: np.full(len(df), PARAMS['stop_pts'] * 500 + 5.) for s, df in panel.items()}

def signals(panel):
    res = {}
    for s, df in panel.items():
        out = np.zeros(len(df), dtype=np.int64)
        if s in SYMS:
            close = df.close.to_numpy(); sec = df.ct_sec.to_numpy()
            for sess, idx in df.groupby('session', sort=False).indices.items():
                if pd_dow(sess) != 2:
                    continue
                c, t = close[idx], sec[idx]
                a = np.where(t == 34200 - 60)[0]; b = np.where(t == PARAMS['decision_sec'])[0]
                if not len(a) or not len(b):
                    continue
                d = int(np.sign(c[b[0]] - c[a[0]]))
                if d == 0:
                    continue
                ref = c[b[0]]
                for j in range(b[0], len(idx)):
                    if t[j] >= PARAMS['exit_sec'] or (c[j] - ref) * d <= -PARAMS['stop_pts']:
                        break
                    out[idx[j]] = d
        res[s] = out
    return res

def pd_dow(sess):
    import pandas as pd
    return pd.Timestamp(sess).dayofweek
