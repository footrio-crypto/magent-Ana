import yfinance as yf
import datetime
import schedule
import time
import os
import matplotlib.pyplot as plt
from analysis import analyze
from report_generator import create_pdf
import smtplib
from email.message import EmailMessage

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
SEND_TIME = os.environ.get("TIME", "21:30")

TICKERS = {
    "Gold": "GC=F",
    "Silver": "SI=F",
    "DBS": "D05.SI",
    "Bank of China": "3988.HK",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Alphabet": "GOOGL",
    "Broadcom": "AVGO"
}

# ==============================
# FETCH DATA
# ==============================

def fetch_data(ticker):
    df = yf.download(ticker, period="1y", progress=False)
    return df

# ==============================
# SAFE CALCULATION (FIXED)
# ==============================

def calc(df):
    close = df["Close"]

    # If DataFrame (multi-column), take first column
    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    # Drop NaN just in case
    close = close.dropna()

    if len(close) < 10:
        return None, None, None

    latest = close.iloc[-1]

    year = datetime.datetime.now().year
    ytd_data = close[close.index >= f"{year}-01-01"]

    if len(ytd_data) == 0:
        return None, None, None

    ytd_start = ytd_data.iloc[0]
    one_year_start = close.iloc[0]

    ytd = (latest - ytd_start) / ytd_start * 100
    one_year = (latest - one_year_start) / one_year_start * 100

    return round(float(latest), 2), round(float(ytd), 2), round(float(one_year), 2)

# ==============================
# CHART
# ==============================

def chart(df, name):
    try:
        plt.figure()
        df["Close"].plot(title=f"{name} - 1 Year")
        file = f"{name.replace(' ', '_')}.png"
        plt.savefig(file, bbox_inches="tight")
        plt.close()
        return file
    except:
        return None

# ==============================
# EMAIL
# ==============================

def send_email(text):
    msg = EmailMessage()
    msg["Subject"] = "Daily Market Report"
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg.set_content(text)

    try:
        with open("market_report.pdf", "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="pdf",
                filename="market_report.pdf"
            )
    except:
        pass

    with smtplib.SMTP("smtp.office365.com", 587) as s:
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(msg)

# ==============================
# MAIN JOB
# ==============================

def job():
    print("Running market job...")

    results = {}
    charts = []

    for name, ticker in TICKERS.items():
        df = fetch_data(ticker)

        if df.empty:
            continue

        price, ytd, one_year = calc(df)

        if price is None:
            continue

        results[name] = {
            "price": price,
            "ytd": ytd,
            "1y": one_year
        }

        c = chart(df, name)
        if c:
            charts.append(c)

    if len(results) == 0:
        print("No data retrieved.")
        return

    signals = analyze(results)

    report = "Daily Market Report\n\n"

    for name, data in results.items():
        report += f"{name}: {data['price']} | YTD: {data['ytd']}% | 1Y: {data['1y']}%\n"

    report += "\nSignals:\n"
    for name, signal in signals.items():
        report += f"{name}: {signal}\n"

    report += "\nScheduled time: 9:30 PM Singapore"

    create_pdf(report, charts)
    send_email(report)

    print("Email sent successfully.")

# ==============================
# SCHEDULE
# ==============================

print("Running scheduled market report now...")
job()
print("Job completed. Exiting.")