def analyze(results):
    signals = {}

    gold = results.get("Gold", {})
    dbs = results.get("DBS", {})
    ai = results.get("NVIDIA", {})

    # GOLD STRATEGY
    if gold.get("ytd", 0) > 15:
        signals["Gold"] = "SELL / TAKE PROFIT"
    elif gold.get("ytd", 0) < 5:
        signals["Gold"] = "BUY / ACCUMULATE"
    else:
        signals["Gold"] = "HOLD"

    # DBS STRATEGY
    if dbs.get("ytd", 0) < 3:
        signals["DBS"] = "BUY"
    else:
        signals["DBS"] = "HOLD"

    # AI STOCKS
    if ai.get("ytd", 0) > 40:
        signals["AI"] = "RISK / TRIM"
    else:
        signals["AI"] = "HOLD"

    return signals
