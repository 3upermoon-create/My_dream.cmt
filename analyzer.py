import math

def poisson(lam, k):
    return math.exp(-lam) * (lam ** k) / math.factorial(k)

def probabilities(home_xg, away_xg, max_goals=10):
    hw=draw=aw=0.0
    for h in range(max_goals+1):
        for a in range(max_goals+1):
            p=poisson(home_xg,h)*poisson(away_xg,a)
            if h>a: hw+=p
            elif h==a: draw+=p
            else: aw+=p
    total=hw+draw+aw
    total_goals=home_xg+away_xg
    under25=sum(poisson(total_goals,k) for k in range(3))
    over25=1-under25
    btts=(1-poisson(home_xg,0))*(1-poisson(away_xg,0))
    return {"home":hw/total,"draw":draw/total,"away":aw/total,
            "over25":over25,"under25":under25,"btts":btts}

def implied(odds): return 1/odds if odds and odds>0 else None
def ev(prob,odds): return prob*odds-1 if odds and odds>0 else None

def label(ev_value):
    if ev_value is None: return "NO DATA"
    if ev_value >= 0.05: return "BET CANDIDATE"
    if ev_value >= 0: return "WAIT"
    return "NO BET"
