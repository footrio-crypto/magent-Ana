def analyze(results):
    signals = {}

    if results["NVIDIA"]["ytd"] > 30:
        signals["AI"] = "RISK"
    else:
        signals["AI"] = "BUY"

    if results["Gold"]["ytd"] > 15:
        signals["Macro"] = "RISK"
    else:
        signals["Macro"] = "STABLE"

    if results["DBS"]["ytd"] < 5:
        signals["DBS"] = "BUY"
    else:
        signals["DBS"] = "HOLD"

    return signals
