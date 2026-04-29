def analyze(results):
    signals = {}

    gold = results.get("Gold", {})
    silver = results.get("Silver", {})
    dbs = results.get("DBS", {})
    boc = results.get("Bank of China", {})
    nvda = results.get("NVIDIA", {})

    # Gold strategy
    if gold.get("price", 0) < 170:
        signals["Gold"] = {
            "signal": "BUY",
            "outlook": "Gold buy zone",
            "strength": 5,
            "key_level": "Below 170"
        }
    elif gold.get("price", 0) > 200:
        signals["Gold"] = {
            "signal": "WAIT",
            "outlook": "Gold may be overheated",
            "strength": 3,
            "key_level": "Above 200"
        }
    else:
        signals["Gold"] = {
            "signal": "HOLD",
            "outlook": "Neutral zone",
            "strength": 3,
            "key_level": "170 - 200"
        }

    # Silver
    if silver.get("ytd", 0) > 15:
        signals["Silver"] = {
            "signal": "HOLD",
            "outlook": "Strong momentum",
            "strength": 4,
            "key_level": "Monitor pullback"
        }
    else:
        signals["Silver"] = {
            "signal": "WATCH",
            "outlook": "Mixed momentum",
            "strength": 3,
            "key_level": "Watch trend"
        }

    # DBS
    if dbs.get("ytd", 0) < 5:
        signals["DBS"] = {
            "signal": "BUY",
            "outlook": "Accumulation zone",
            "strength": 4,
            "key_level": "Low YTD growth"
        }
    else:
        signals["DBS"] = {
            "signal": "HOLD",
            "outlook": "Stable income stock",
            "strength": 3,
            "key_level": "Dividend support"
        }

    # Bank of China
    if boc.get("ytd", 0) < 5:
        signals["Bank of China"] = {
            "signal": "WATCH",
            "outlook": "Policy-driven bank",
            "strength": 3,
            "key_level": "China policy risk"
        }
    else:
        signals["Bank of China"] = {
            "signal": "HOLD",
            "outlook": "Stable but policy sensitive",
            "strength": 3,
            "key_level": "Monitor China macro"
        }

    # AI stocks
    if nvda.get("ytd", 0) > 40:
        signals["AI Stocks"] = {
            "signal": "RISK",
            "outlook": "Possible AI overheat",
            "strength": 2,
            "key_level": "High YTD momentum"
        }
    else:
        signals["AI Stocks"] = {
            "signal": "HOLD",
            "outlook": "AI trend still active",
            "strength": 4,
            "key_level": "Monitor valuation"
        }

    return signals
