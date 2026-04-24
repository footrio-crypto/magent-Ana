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
TIMEZONE = os.environ.get("TIMEZONE", "Asia/Singapore")

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

def fetch_data(ticker):
    return yf.download(ticker, period="1y", progress=False)

def calc(df):
    latest = df["Close"].iloc[-1]
    ytd_start = df[df.index >= f"{datetime.datetime.now().year}-01-01"]["Close"].iloc[0]
    one_year_start = df["Close"].iloc[0]

    ytd = (latest - ytd_start) / ytd_start * 100
    one_year = (latest - one_year_start) / one_year_start * 100

    return round(float(latest), 2), round(float(ytd), 2), round(float(one_year), 2)

def chart(df, name):
    plt.figure()
    df["Close"].plot(title=f"{name} - 1 Year Chart")
    file = f"{name.replace(' ', '_')}.png"
    plt.savefig(file, bbox_inches="tight")
    plt.close()
    return file

def send_email(text):
    msg = EmailMessage()
    msg["Subject"] = "Daily Market Report"
    msg["From"] = EMAIL
    msg["To"] = EMAIL
    msg.set_content(text)

    with open("market_report.pdf", "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename="market_report.pdf"
        )

    with smtplib.SMTP("smtp.office365.com", 587) as s:
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(msg)

def job():
    results = {}
    charts = []

    for name, ticker in TICKERS.items():
        df = fetch_data(ticker)

        if df.empty:
            continue

        price, ytd, one_year = calc(df)

        results[name] = {
            "price": price,
            "ytd": ytd,
            "1y": one_year
        }

        charts.append(chart(df, name))

    signals = analyze(results)

    report = "Daily Market Report\n\n"

    for name, data in results.items():
        report += f"{name}: {data['price']} | YTD: {data['ytd']}% | 1Y: {data['1y']}%\n"

    report += "\nSignals:\n"
    for name, signal in signals.items():
        report += f"{name}: {signal}\n"

    report += "\nSingapore Time: 9:30 PM scheduled report"

    create_pdf(report, charts)
    send_email(report)

schedule.every().day.at(SEND_TIME, TIMEZONE).do(job)

print(f"Market agent running. Daily report scheduled at {SEND_TIME} {TIMEZONE}.")

while True:
    schedule.run_pending()
    time.sleep(60)