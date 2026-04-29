import json
import datetime


def create_html_dashboard(results, signals, market_views, alerts):
    updated_at = datetime.datetime.utcnow().strftime("%d %B %Y, %H:%M UTC")

    data_json = json.dumps(results)
    signals_json = json.dumps(signals)
    views_json = json.dumps(market_views)
    alerts_json = json.dumps(alerts)

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="theme-color" content="#07111f" />
  <title>Market Intelligence Dashboard</title>

  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      background: radial-gradient(circle at top, #102033 0%, #07111f 45%, #030712 100%);
      color: #e5e7eb;
    }}

    header {{
      padding: 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      border-bottom: 1px solid rgba(255,255,255,0.08);
    }}

    .title-wrap h1 {{
      margin: 0;
      font-size: 30px;
      letter-spacing: -0.5px;
    }}

    .title-wrap p {{
      margin: 8px 0 0;
      color: #9ca3af;
    }}

    .updated {{
      text-align: right;
      color: #cbd5e1;
      font-size: 14px;
    }}

    .container {{
      max-width: 1280px;
      margin: auto;
      padding: 24px;
    }}

    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 16px;
    }}

    .wide-grid {{
      display: grid;
      grid-template-columns: 1.2fr 0.8fr;
      gap: 16px;
    }}

    .card {{
      background: rgba(15, 23, 42, 0.86);
      border: 1px solid rgba(148, 163, 184, 0.20);
      border-radius: 18px;
      padding: 18px;
      box-shadow: 0 16px 40px rgba(0,0,0,0.25);
    }}

    .card h2 {{
      margin: 0 0 12px;
      font-size: 18px;
    }}

    .price {{
      font-size: 28px;
      font-weight: 800;
      margin: 8px 0;
    }}

    .positive {{
      color: #22c55e;
      font-weight: 700;
    }}

    .negative {{
      color: #ef4444;
      font-weight: 700;
    }}

    .neutral {{
      color: #facc15;
      font-weight: 700;
    }}

    .section-title {{
      margin: 30px 0 14px;
      font-size: 22px;
    }}

    .asset-row {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
    }}

    .symbol {{
      font-size: 28px;
    }}

    canvas {{
      max-height: 320px;
    }}

    .signal-table {{
      width: 100%;
      border-collapse: collapse;
    }}

    .signal-table th,
    .signal-table td {{
      padding: 12px;
      border-bottom: 1px solid rgba(255,255,255,0.08);
      text-align: left;
    }}

    .signal-badge {{
      display: inline-block;
      padding: 6px 10px;
      border-radius: 999px;
      font-weight: 800;
      font-size: 12px;
    }}

    .buy {{
      background: rgba(34,197,94,0.16);
      color: #22c55e;
    }}

    .hold {{
      background: rgba(250,204,21,0.16);
      color: #facc15;
    }}

    .risk, .wait {{
      background: rgba(239,68,68,0.16);
      color: #ef4444;
    }}

    .watch {{
      background: rgba(96,165,250,0.16);
      color: #60a5fa;
    }}

    .strength {{
      display: flex;
      gap: 4px;
    }}

    .bar {{
      width: 8px;
      height: 18px;
      border-radius: 3px;
      background: #334155;
    }}

    .bar.on {{
      background: #22c55e;
    }}

    .alert-card {{
      border-left: 4px solid #facc15;
    }}

    .headline {{
      margin-bottom: 10px;
      color: #cbd5e1;
      font-size: 14px;
      line-height: 1.4;
    }}

    footer {{
      text-align: center;
      padding: 28px;
      color: #9ca3af;
      font-size: 13px;
    }}

    @media (max-width: 800px) {{
      header {{
        display: block;
      }}

      .updated {{
        text-align: left;
        margin-top: 14px;
      }}

      .wide-grid {{
        grid-template-columns: 1fr;
      }}

      .title-wrap h1 {{
        font-size: 24px;
      }}

      .container {{
        padding: 14px;
      }}

      .card {{
        padding: 14px;
        border-radius: 14px;
      }}

      .price {{
        font-size: 24px;
      }}

      .signal-table th,
      .signal-table td {{
        padding: 9px 6px;
        font-size: 13px;
      }}
    }}
  </style>
</head>

<body>
  <header>
    <div class="title-wrap">
      <h1>📈 Market Intelligence Dashboard</h1>
      <p>Daily Market Overview with AI Insights & External Intelligence</p>
    </div>
    <div class="updated">
      <div>Last Updated</div>
      <strong>{updated_at}</strong>
    </div>
  </header>

  <div class="container">

    <h2 class="section-title">Market Snapshot</h2>
    <div class="grid" id="marketCards"></div>

    <h2 class="section-title">Gold Strategy Alerts</h2>
    <div class="grid" id="alerts"></div>

    <div class="wide-grid">
      <div>
        <h2 class="section-title">Price Trends</h2>
        <div class="card">
          <canvas id="combinedChart"></canvas>
        </div>
      </div>

      <div>
        <h2 class="section-title">AI Market Insights</h2>
        <div class="card" id="insights"></div>
      </div>
    </div>

    <h2 class="section-title">Trading Signals</h2>
    <div class="card">
      <table class="signal-table">
        <thead>
          <tr>
            <th>Market</th>
            <th>Signal</th>
            <th>Strength</th>
            <th>Key Level</th>
            <th>Outlook</th>
          </tr>
        </thead>
        <tbody id="signalRows"></tbody>
      </table>
    </div>

    <h2 class="section-title">External Market Views</h2>
    <div class="grid" id="views"></div>

  </div>

  <footer>
    Disclaimer: This dashboard is for monitoring and education only. It is not financial advice.
  </footer>

<script>
const marketData = {data_json};
const signals = {signals_json};
const views = {views_json};
const alerts = {alerts_json};

function pctClass(value) {{
  if (value > 0) return "positive";
  if (value < 0) return "negative";
  return "neutral";
}}

function symbolFor(name) {{
  const symbols = {{
    "Gold": "🟡",
    "Silver": "⚪",
    "DBS": "🏦",
    "Bank of China": "🏛️",
    "NVIDIA": "🤖",
    "Amazon": "🛒",
    "Alphabet": "🔎",
    "Broadcom": "🔌"
  }};
  return symbols[name] || "📊";
}}

function badgeClass(signal) {{
  const s = signal.toLowerCase();
  if (s.includes("buy")) return "buy";
  if (s.includes("risk")) return "risk";
  if (s.includes("wait")) return "wait";
  if (s.includes("watch")) return "watch";
  return "hold";
}}

function strengthBars(level) {{
  let html = '<div class="strength">';
  for (let i = 1; i <= 5; i++) {{
    html += `<span class="bar ${{i <= level ? "on" : ""}}"></span>`;
  }}
  html += '</div>';
  return html;
}}

const marketCards = document.getElementById("marketCards");

Object.entries(marketData).forEach(([name, data]) => {{
  const card = document.createElement("div");
  card.className = "card";

  card.innerHTML = `
    <div class="asset-row">
      <div>
        <h2>${{name}}</h2>
        <div class="price">${{data.price}}</div>
      </div>
      <div class="symbol">${{symbolFor(name)}}</div>
    </div>
    <p>1D: <span class="${{pctClass(data["1d"])}}">${{data["1d"]}}%</span></p>
    <p>YTD: <span class="${{pctClass(data.ytd)}}">${{data.ytd}}%</span></p>
    <p>1Y: <span class="${{pctClass(data["1y"])}}">${{data["1y"]}}%</span></p>
  `;

  marketCards.appendChild(card);
}});

const alertsDiv = document.getElementById("alerts");

alerts.forEach(alert => {{
  const card = document.createElement("div");
  card.className = "card alert-card";
  card.innerHTML = `<strong>${{alert}}</strong>`;
  alertsDiv.appendChild(card);
}});

const datasets = Object.entries(marketData).map(([name, data]) => {{
  return {{
    label: name,
    data: data.chart.map(item => item.price),
    borderWidth: 2,
    tension: 0.25,
    pointRadius: 0
  }};
}});

const firstAsset = Object.values(marketData)[0];
const labels = firstAsset.chart.map(item => item.date);

new Chart(document.getElementById("combinedChart"), {{
  type: "line",
  data: {{
    labels: labels,
    datasets: datasets
  }},
  options: {{
    responsive: true,
    plugins: {{
      legend: {{
        labels: {{
          color: "#e5e7eb"
        }}
      }}
    }},
    scales: {{
      x: {{
        ticks: {{
          color: "#9ca3af",
          maxTicksLimit: 6
        }},
        grid: {{
          color: "rgba(255,255,255,0.08)"
        }}
      }},
      y: {{
        ticks: {{
          color: "#9ca3af"
        }},
        grid: {{
          color: "rgba(255,255,255,0.08)"
        }}
      }}
    }}
  }}
}});

const insights = document.getElementById("insights");

insights.innerHTML = `
  <p><strong class="positive">Precious Metals</strong><br>
  Gold and silver are tracked for defensive demand, inflation expectations, and safe-haven flow.</p>

  <p><strong class="neutral">Financial Markets</strong><br>
  DBS and Bank of China are monitored for income, macro stability, and policy sensitivity.</p>

  <p><strong style="color:#a78bfa;">AI Market Sentiment</strong><br>
  AI stocks are watched for momentum, valuation risk, and DeepSeek-related efficiency disruption.</p>
`;

const signalRows = document.getElementById("signalRows");

Object.entries(signals).forEach(([market, data]) => {{
  const row = document.createElement("tr");

  row.innerHTML = `
    <td>${{symbolFor(market)}} ${{market}}</td>
    <td><span class="signal-badge ${{badgeClass(data.signal)}}">${{data.signal}}</span></td>
    <td>${{strengthBars(data.strength)}}</td>
    <td>${{data.key_level}}</td>
    <td>${{data.outlook}}</td>
  `;

  signalRows.appendChild(row);
}});

const viewsDiv = document.getElementById("views");

Object.entries(views).forEach(([asset, data]) => {{
  const card = document.createElement("div");
  card.className = "card";

  let headlines = "";

  if (data.headlines && data.headlines.length > 0) {{
    headlines = data.headlines
      .map(item => `<div class="headline">• ${{item.title}}</div>`)
      .join("");
  }} else {{
    headlines = "<p>No headlines found.</p>";
  }}

  card.innerHTML = `
    <h2>${{asset}}</h2>
    <p><strong>${{data.sentiment}}</strong></p>
    <p>Positive score: ${{data.positive_score}} | Negative score: ${{data.negative_score}}</p>
    ${{headlines}}
  `;

  viewsDiv.appendChild(card);
}});
</script>

</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
