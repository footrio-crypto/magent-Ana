def analyze(results):
    signals = {}

    signals["AI"] = "RISK" if results["NVIDIA"]["ytd"] > 30 else "BUY"
    signals["Macro"] = "RISK" if results["Gold"]["ytd"] > 15 else "STABLE"
    signals["DBS"] = "BUY" if results["DBS"]["ytd"] < 5 else "HOLD"

    return signals
