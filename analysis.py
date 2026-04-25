def analyze(results):
    signals = {}

    if "NVIDIA" in results and results["NVIDIA"]["ytd"] > 30:
        signals["AI"] = "RISK - AI stocks may be overheated"
    else:
        signals["AI"] = "WATCH - AI trend stable"

    if "Gold" in results and results["Gold"]["ytd"] > 15:
        signals["Macro"] = "RISK - Gold strength suggests defensive demand"
    else:
        signals["Macro"] = "STABLE - No strong crisis signal"

    if "DBS" in results and results["DBS"]["ytd"] < 5:
        signals["DBS"] = "WATCH / BUY ZONE"
    else:
        signals["DBS"] = "HOLD / MONITOR"

    return signals
