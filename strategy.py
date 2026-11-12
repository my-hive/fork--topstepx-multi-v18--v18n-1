"""Refined-product lead/lag into mini crude.
Mechanism: product price discovery transmits to crude hedging through crack spreads.
Use last completed 30-min RB/HO returns, enter QM next 30-min bar, flat after bar.
Falsify: stressed PnL <= 0 or positive year fraction < .70.
"""
import numpy as np

FAMILY = "energy-refined-product-leadlag"
PARAMS = {'bar_sec': 1800, 'start_sec': 32400, 'end_sec': 50400, 'risk_pts': 0.5}

def entry_risk(panel):
    return {s: np.full(len(d), PARAMS['risk_pts'] * 500 + 5) for s, d in panel.items()}

def signals(panel):
    out = {s: np.zeros(len(d), dtype=np.int64) for s, d in panel.items()}
    if not {'QM', 'RB', 'HO'} <= set(panel):
        return out
    q, rb, ho = (panel[s] for s in ('QM', 'RB', 'HO'))
    # Exact common bars only: feature available at completed x:29/x:59 minute.
    lead = {}
    for sess, ix in rb.groupby('session', sort=False).indices.items():
        b = rb.iloc[ix]; h = ho[(ho.session == sess)]
        if h.empty: continue
        bp = b.set_index('ct_sec').close; hp = h.set_index('ct_sec').close
        for sec in range(PARAMS['start_sec'] + 2 * PARAMS['bar_sec'] - 60, PARAMS['end_sec'], PARAMS['bar_sec']):
            prev = sec - PARAMS['bar_sec']
            if sec in bp.index and prev in bp.index and sec in hp.index and prev in hp.index:
                # Percentage makes contracts commensurate; equal product legs.
                lead[(str(sess), sec)] = np.sign((bp[sec]/bp[prev]-1) + (hp[sec]/hp[prev]-1))
    for sess, ix in q.groupby('session', sort=False).indices.items():
        secs = q.ct_sec.to_numpy()[ix]
        for j, row in enumerate(ix):
            sec = secs[j]; key = (str(sess), sec - 60)
            if sec % PARAMS['bar_sec'] == 0 and key in lead:
                side = int(lead[key])
                if side:
                    # Order submitted after previous constituent bar; next open fill.
                    until = sec + PARAMS['bar_sec']
                    out['QM'][ix[(secs >= sec) & (secs < until)]] = side
    return out
