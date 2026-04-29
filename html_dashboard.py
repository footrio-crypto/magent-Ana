import json
import datetime


def create_html_dashboard(results, signals, market_views, alerts):
    updated_at = datetime.datetime.utcnow().strftime("%B %d, %Y %I:%M %p UTC")

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
      font-family: Inter, Arial, Helvetica, sans-serif;
      background:
        radial-gradient(circle at top left, rgba(20, 55, 90, 0.65), transparent 32%),
        radial-gradient(circle at top right, rgba(35, 20, 70, 0.45), transparent 28%),
        linear-gradient(135deg, #06101d 0%, #071522 42%, #020617 100%);
      color: #e5e7eb;
      min-height: 100vh;
    }}

    .app {{
      max-width: 1500px;
      margin: 0 auto;
      padding: 26px;
    }}

    header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      gap: 20px;
      margin-bottom: 26px;
    }}

    .brand {{
      display: flex;
      gap: 18px;
      align-items: center;
    }}

    .logo {{
      width: 52px;
      height: 52px;
      border: 2px solid rgba(255,255,255,0.88);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 30px;
      box-shadow: 0 0 30px rgba(96,165,250,0.16);
    }}

    h1 {{
      margin: 0;
      font-size: 34px;
      letter-spacing: -0.8px;
      color: #f8fafc;
    }}

    .subtitle {{
      margin-top: 8px;
      color: #cbd5e1;
      font-size: 16px;
    }}

    .updated {{
      text-align: right;
      color: #cbd5e1;
      font-size: 14px;
      line-height: 1.5;
    }}

    .refresh {{
      margin-top: 8px;
      display: inline-flex;
      width: 46px;
      height: 46px;
      align-items: center;
      justify-content: center;
      border-radius: 14px;
      background: rgba(15,23,42,0.82);
      border: 1px solid rgba(148,163,184,0.24);
      color: #e5e7eb;
      font-size: 24px;
    }}

    .top-grid {{
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 16px;
      margin-bottom: 18px;
    }}

    .dashboard-grid {{
      display: grid;
      grid-template-columns: 1.45fr 0.95fr;
      gap: 18px;
      margin-bottom: 18px;
    }}

    .bottom-grid {{
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 18px;
    }}

    .card {{
      background: linear-gradient(180deg, rgba(15,23,42,0.88), rgba(8,18,31,0.92));
      border: 1px solid rgba(148,163,184,0.22);
      border-radius: 16px;
      box-shadow:
        0 20px 48px rgba(0,0,0,0.32),
        inset 0 1px 0 rgba(255,255,255,0.04);
      overflow: hidden;
    }}

    .metric-card {{
      padding: 20px;
      min-height: 126px;
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .metric-icon {{
      width: 46px;
      height: 46px;
      border-radius: 15px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 28px;
      flex-shrink: 0;
    }}

    .gold-bg {{ background: rgba(245,158,11,0.16); }}
    .silver-bg {{ background: rgba(203,213,225,0.14); }}
    .dbs-bg {{ background: rgba(239,68,68,0.17); }}
    .boc-bg {{ background: rgba(220,38,38,0.17); }}
    .ai-bg {{ background: rgba(168,85,247,0.18); }}

    .metric-title {{
      font-weight: 800;
      font-size: 16px;
      margin-bottom: 8px;
      color: #f8fafc;
    }}

    .metric-price {{
      font-size: 25px;
      font-weight: 900;
      letter-spacing: -0.5px;
      margin-bottom: 8px;
      color: #f8fafc;
    }}

    .metric-change {{
      font-size: 14px;
      font-weight: 800;
    }}

    .positive {{ color: #22c55e; }}
    .negative {{ color: #ff3b30; }}
    .neutral {{ color: #facc15; }}
    .purple {{ color: #a78bfa; }}

    .panel-title {{
      padding: 18px 22px 10px;
      font-size: 20px;
      font-weight: 900;
      color: #f8fafc;
    }}

    .chart-card {{
      padding: 0 22px 20px;
      min-height: 370px;
    }}

    .chart-tabs {{
      display: flex;
      gap: 10px;
      margin: 8px 0 18px;
    }}

    .tab {{
      padding: 9px 16px;
      border-radius: 9px;
      background: rgba(15,23,42,0.95);
      border: 1px solid rgba(148,163,184,0.22);
      color: #e5e7eb;
      font-weight: 800;
      font-size: 14px;
    }}

    .tab.active {{
      background: rgba(59,130,246,0.18);
      border-color: rgba(96,165,250,0.45);
      box-shadow: 0 0 20px rgba(96,165,250,0.12);
    }}

    #combinedChart {{
      height: 270px !important;
    }}

    .insights {{
      padding: 8px 24px 22px;
    }}

    .insight-row {{
      display: grid;
      grid-template-columns: 54px 1fr;
      gap: 16px;
      padding: 16px 0;
      border-bottom: 1px solid rgba(148,163,184,0.16);
    }}

    .insight-row:last-child {{
      border-bottom: none;
    }}

    .insight-icon {{
      width: 48px;
      height: 48px;
      border-radius: 999px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
    }}

    .insight-title {{
      font-weight: 900;
      margin-bottom: 6px;
      font-size: 16px;
    }}

    .insight-text {{
      color: #d1d5db;
      line-height: 1.45;
      font-size: 15px;
    }}

    .table-card {{
      padding-bottom: 12px;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
    }}

    th, td {{
      padding: 15px 22px;
      text-align: left;
      border-bottom: 1px solid rgba(148,163,184,0.14);
      font-size: 15px;
    }}

    th {{
      color: #e5e7eb;
      font-weight: 900;
      background: rgba(15,23,42,0.34);
    }}

    td {{
      color: #e5e7eb;
    }}

    .signal-badge {{
      font-weight: 900;
      letter-spacing: 0.3px;
    }}

    .buy {{ color: #22c55e; }}
    .hold {{ color: #facc15; }}
    .watch {{ color: #60a5fa; }}
    .risk, .wait, .sell {{ color: #ff3b30; }}

    .strength {{
      display: flex;
      gap: 5px;
    }}

    .bar {{
      width: 9px;
      height: 17px;
      border-radius: 3px;
      background: rgba(71,85,105,0.85);
    }}

    .bar.on {{
      background: #22c55e;
      box-shadow: 0 0 8px rgba(34,197,94,0.25);
    }}

    .views-card {{
      padding-bottom: 12px;
    }}

    .view-row {{
      display: grid;
      grid-template-columns: 38px 135px 1fr;
      gap: 14px;
      align-items: center;
      padding: 14px 22px;
      border-bottom: 1px solid rgba(148,163,184,0.14);
    }}

    .view-row:last-child {{
      border-bottom: none;
    }}

    .source-icon {{
      width: 30px;
      height: 30px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      color: white;
      background: #334155;
    }}

    .source-name {{
      font-weight: 900;
      color: #f8fafc;
    }}

    .headline {{
      color: #d1d5db;
      font-size: 14px;
      line-height: 1.35;
    }}

    .alerts-strip {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 14px;
      margin-bottom: 18px;
    }}

    .alert {{
      padding: 14px 18px;
      border-left: 4px solid #facc15;
      background: rgba(15,23,42,0.86);
      border-radius: 14px;
      border-top: 1px solid rgba(148,163,184,0.16);
      border-right: 1px solid rgba(148,163,184,0.16);
      border-bottom: 1px solid rgba(148,163,184,0.16);
      font-weight: 800;
      color: #f8fafc;
    }}

    .disclaimer {{
      margin: 28px 24px 6px;
      color: #9ca3af;
      font-size: 14px;
    }}

    @media (max-width: 1100px) {{
      .top-grid {{
        grid-template-columns: repeat(2, 1fr);
      }}

      .dashboard-grid,
      .bottom-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    @media (max-width: 640px) {{
      .app {{
        padding: 14px;
      }}

      header {{
        flex-direction: column;
      }}

      .brand {{
        align-items: flex-start;
      }}

      .logo {{
        width: 42px;
        height: 42px;
        font-size: 24px;
      }}

      h1 {{
        font-size: 25px;
      }}

      .subtitle {{
        font-size: 14px;
      }}

      .updated {{
        text-align: left;
      }}

      .top-grid {{
        grid-template-columns: 1fr;
      }}

      .metric-card {{
        min-height: 108px;
        padding: 16px;
      }}

      .metric-price {{
        font-size: 23px;
      }}

      .panel-title {{
        padding: 16px 16px 8px;
      }}

      .chart-card {{
        padding: 0 14px 16px;
      }}

      .chart-tabs {{
        overflow-x: auto;
      }}

      th, td {{
        padding: 11px 10px;
        font-size: 12px;
      }}

      .view-row {{
        grid-template-columns: 32px 1fr;
      }}

      .headline {{
        grid-column: 2 / 3;
      }}
    }}
  </style>
</head>

<body>
  <div class="app">
    <header>
      <div class="brand">
        <div class="logo">↗</div>
        <div>
          <h1>Market Intelligence Dashboard</h1>
          <div class="subtitle">Daily Market Overview with AI Insights & External Intelligence</div>
        </div>
      </div>
      <div class="updated">
        <div>Last Updated:</div>
        <strong>{updated_at}</strong>
        <div class="refresh">↻</div>
      </div>
    </header>

    <div class="top-grid" id="topCards"></div>

    <div class="alerts-strip" id="alerts"></div>

    <div class="dashboard-grid">
      <section class="card">
        <div class="panel-title">Price Trends <span style="font-size:14px; color:#cbd5e1;">(1 Year)</span></div>
        <div class="chart-card">
          <div class="chart-tabs">
            <div class="tab active">1Y</div>
            <div class="tab">YTD</div>
            <div class="tab">1M</div>
            <div class="tab">5D</div>
          </div>
          <canvas id="combinedChart"></canvas>
        </div>
      </section>

      <section class="card">
        <div class="panel-title">AI Market Insights</div>
        <div class="insights" id="insights"></div>
      </section>
    </div>

    <div class="bottom-grid">
      <section class="card table-card">
        <div class="panel-title">Trading Signals</div>
        <table>
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
      </section>

      <section class="card views-card">
        <div class="panel-title">External Market Views</div>
        <div id="views"></div>
      </section>
    </div>

    <div class="disclaimer">
      <strong>Disclaimer:</strong> This dashboard is for informational and educational purposes only and not financial advice.
    </div>
  </div>

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
    "DBS": "✖️",
    "Bank of China": "⭕",
    "NVIDIA": "🧠",
    "Amazon": "🛒",
    "Alphabet": "🔎",
    "Broadcom": "🔌",
    "AI Stocks": "🧠"
  }};
  return symbols[name] || "📊";
}}

function iconClass(name) {{
  if (name === "Gold") return "gold-bg";
  if (name === "Silver") return "silver-bg";
  if (name === "DBS") return "dbs-bg";
  if (name === "Bank of China") return "boc-bg";
  return "ai-bg";
}}

function formatPrice(name, price) {{
  if (name === "DBS") return "S$" + price;
  if (name === "Bank of China") return "HK$" + price;
  if (name === "Gold" || name === "Silver") return "$" + price;
  return "$" + price;
}}

function badgeClass(signal) {{
  const s = String(signal).toLowerCase();
  if (s.includes("buy")) return "buy";
  if (s.includes("risk")) return "risk";
  if (s.includes("sell")) return "sell";
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

const topCards = document.getElementById("topCards");
const preferredTop = ["Gold", "Silver", "DBS", "Bank of China", "NVIDIA"];

preferredTop.forEach(name => {{
  if (!marketData[name]) return;
  const data = marketData[name];
  const card = document.createElement("div");
  card.className = "card metric-card";

  let title = name;
  if (name === "Gold") title = "Gold (XAU/USD)";
  if (name === "Silver") title = "Silver (XAG/USD)";
  if (name === "DBS") title = "DBS Group (D05.SI)";
  if (name === "Bank of China") title = "Bank of China (3988.HK)";
  if (name === "NVIDIA") title = "AI Market Sentiment";

  let priceText = formatPrice(name, data.price);
  let changeText = `${{data["1d"]}}%`;
  let changeClass = pctClass(data["1d"]);

  if (name === "NVIDIA") {{
    const aiSignal = signals["AI Stocks"] ? signals["AI Stocks"].signal : "Neutral";
    priceText = aiSignal;
    changeText = "Confidence: " + ((signals["AI Stocks"]?.strength || 3) * 20) + "%";
    changeClass = "purple";
  }}

  card.innerHTML = `
    <div class="metric-icon ${{iconClass(name)}}">${{symbolFor(name)}}</div>
    <div>
      <div class="metric-title">${{title}}</div>
      <div class="metric-price ${{name === "NVIDIA" ? "purple" : ""}}">${{priceText}}</div>
      <div class="metric-change ${{changeClass}}">${{changeText}}</div>
    </div>
  `;
  topCards.appendChild(card);
}});

const alertsDiv = document.getElementById("alerts");
alerts.forEach(alert => {{
  const div = document.createElement("div");
  div.className = "alert";
  div.textContent = alert;
  alertsDiv.appendChild(div);
}});

const chartNames = ["Gold", "Silver", "DBS", "Bank of China"];
const chartColors = {{
  "Gold": "#facc15",
  "Silver": "#e5e7eb",
  "DBS": "#ff3b30",
  "Bank of China": "#22c55e"
}};

const firstAsset = marketData[chartNames.find(n => marketData[n])];
const labels = firstAsset.chart.map(item => item.date);

const datasets = chartNames
  .filter(name => marketData[name])
  .map(name => {{
    const series = marketData[name].chart;
    const first = series[0].price;
    const normalized = series.map(item => Number((((item.price - first) / first) * 100).toFixed(2)));

    return {{
      label: name,
      data: normalized,
      borderColor: chartColors[name],
      backgroundColor: chartColors[name],
      borderWidth: 2,
      tension: 0.25,
      pointRadius: 0
    }};
  }});

new Chart(document.getElementById("combinedChart"), {{
  type: "line",
  data: {{
    labels: labels,
    datasets: datasets
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: false,
    plugins: {{
      legend: {{
        position: "right",
        labels: {{
          color: "#e5e7eb",
          boxWidth: 10,
          boxHeight: 10,
          usePointStyle: true
        }}
      }},
      tooltip: {{
        callbacks: {{
          label: function(context) {{
            return context.dataset.label + ": " + context.parsed.y + "%";
          }}
        }}
      }}
    }},
    scales: {{
      x: {{
        ticks: {{ color: "#cbd5e1", maxTicksLimit: 7 }},
        grid: {{ color: "rgba(148,163,184,0.10)" }}
      }},
      y: {{
        ticks: {{
          color: "#cbd5e1",
          callback: value => value + "%"
        }},
        grid: {{ color: "rgba(148,163,184,0.12)" }}
      }}
    }}
  }}
}});

const insights = document.getElementById("insights");
const goldSignal = signals["Gold"]?.signal || "HOLD";
const dbsSignal = signals["DBS"]?.signal || "HOLD";
const aiSignal = signals["AI Stocks"]?.signal || "HOLD";

insights.innerHTML = `
  <div class="insight-row">
    <div class="insight-icon" style="background:rgba(34,197,94,0.15); color:#22c55e;">↗</div>
    <div>
      <div class="insight-title positive">Precious Metals</div>
      <div class="insight-text">Gold signal is <strong>${{goldSignal}}</strong>. Monitor safe-haven demand, USD direction, and inflation expectations.</div>
    </div>
  </div>

  <div class="insight-row">
    <div class="insight-icon" style="background:rgba(239,68,68,0.15); color:#ef4444;">🏦</div>
    <div>
      <div class="insight-title negative">Financial Markets</div>
      <div class="insight-text">DBS signal is <strong>${{dbsSignal}}</strong>. Bank of China remains policy-sensitive and linked to China macro sentiment.</div>
    </div>
  </div>

  <div class="insight-row">
    <div class="insight-icon" style="background:rgba(168,85,247,0.15); color:#a78bfa;">🌐</div>
    <div>
      <div class="insight-title purple">Overall Sentiment</div>
      <div class="insight-text">AI market signal is <strong>${{aiSignal}}</strong>. Monitor DeepSeek disruption, valuation pressure, and momentum shifts.</div>
    </div>
  </div>
`;

const signalRows = document.getElementById("signalRows");
Object.entries(signals).forEach(([market, data]) => {{
  const row = document.createElement("tr");
  row.innerHTML = `
    <td>${{symbolFor(market)}} ${{market}}</td>
    <td><span class="signal-badge ${{badgeClass(data.signal)}}">${{data.signal}}</span></td>
    <td>${{strengthBars(data.strength || 3)}}</td>
    <td>${{data.key_level || "-"}}</td>
    <td><span class="${{badgeClass(data.signal)}}">${{data.outlook || "-"}}</span></td>
  `;
  signalRows.appendChild(row);
}});

const viewsDiv = document.getElementById("views");
const sources = Object.entries(views).slice(0, 5);

sources.forEach(([asset, data], idx) => {{
  let headline = "No headline found.";
  if (data.headlines && data.headlines.length > 0) {{
    headline = data.headlines[0].title;
  }}

  const row = document.createElement("div");
  row.className = "view-row";
  row.innerHTML = `
    <div class="source-icon">${{asset[0]}}</div>
    <div class="source-name">${{asset}}</div>
    <div class="headline">${{headline}}</div>
  `;
  viewsDiv.appendChild(row);
}});
</script>

</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
