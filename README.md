# Global Macro Tracker
### Team: Pandas

An intelligent real-time dashboard for asset managers that transforms fragmented macroeconomic data into actionable portfolio insights. The platform tracks six core macro themes — Inflation, GDP, Employment, Housing, Tech, and Energy — classifying each as **HOT** (elevated risk) or **COOL** (stable), then generates cross-market impact chains, portfolio signals, and AI-driven risk narratives.

Built for speed: the dashboard auto-refreshes every 10 seconds, flashes updated cards, and alerts on trend flips so portfolio managers never miss a regime change.

## Key Features

### Core Intelligence
- **Sentiment Classification** — Every macro event scored 0-100% and classified HOT or COOL with color-coded heat bars
- **Cross-Market Impact Chains** — Causal mapping showing how one sector ripples into others (e.g., Inflation -> Housing -> Employment)
- **Institutional Memory** — Persistent event log tracking all macro developments over time
- **Trend-Change Alerts** — Real-time detection when a sector flips from HOT to COOL or vice versa
- **Risk Mapping** — Automatic mapping of macro themes to financial risk outcomes (yield curve, credit spreads, etc.)

### Analytics & Signals
- **Market Pulse Gauge** — Aggregate risk score (0-100) combining HOT ratio and sentiment intensity across all sectors
- **Portfolio Signals** — Per-theme actionable recommendations: Hedge, Reduce Exposure, Accumulate, Watch Closely, or Hold
- **Volatility Ranking** — Horizontal bar chart ranking which sectors fluctuate the most
- **Theme Momentum** — Heating/Cooling/Flat indicators per sector with HOT-to-COOL ratio bars and directional strength
- **Sentiment Distribution** — Donut chart + sector breakdown table with bias badges (Risk-On / Stable / Neutral)
- **AI Analysis Panel** — Market-wide narrative summary with risk level assessment and dominant theme identification

### Data & UI
- **Real FRED Data Integration** — Pulls live macroeconomic data from the Federal Reserve (CPI, GDP, Unemployment Rate, Housing Starts, NASDAQ, Oil)
- **Live News Ticker** — Scrolling banner with breaking macro developments
- **Sentiment History Charts** — Click any theme to see its tracked sentiment trajectory
- **Tabbed Dashboard** — Clean 4-tab layout: Overview, Impacts, Analytics, Memory
- **Theme Filter Chips** — Filter the event log by sector with clickable badges
- **Auto-Refresh Polling** — 10-second live updates with connection indicator and card flash animations

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React.js, Recharts |
| Backend | Python, Flask, Flask-CORS |
| Data | FRED API (Federal Reserve Economic Data) |
| Deployment | Railway (Docker) |
| Design | Figma |

## Getting Started (Local Development)

### Prerequisites
- Python 3.10+
- Node.js 18+
- (Optional) FRED API key for real data — [Get one free here](https://fred.stlouisfed.org/docs/api/api_key.html)

### Backend
```bash
cd backend
pip install -r ../requirements.txt

# Optional: enable real FRED data (works without it in simulation mode)
set FRED_API_KEY=your_key_here

python app.py
```
The API server starts at `http://127.0.0.1:5000`.

### Frontend
```bash
cd frontend
npm install
npm start
```
The dashboard opens at `http://localhost:3000`.

## Deployment (Railway)

### Quick Deploy
1. Push this repo to GitHub
2. Go to [railway.app](https://railway.app) and create a new project
3. Select "Deploy from GitHub repo"
4. Railway auto-detects the Dockerfile and builds everything
5. Add environment variable `FRED_API_KEY` in the Railway dashboard (Settings > Variables)
6. Railway assigns a public URL like `https://your-app.up.railway.app`

### What happens on deploy
- React frontend is built with `REACT_APP_API_URL=''` (same-origin)
- Flask serves both the API endpoints and the React build
- Single service, single URL — no separate frontend/backend hosting needed

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/trends` | GET | Latest state for all 6 macro themes |
| `/api/memory` | GET | Recent institutional memory (last 50 events) |
| `/api/summary` | GET | AI-generated market summary and narrative |
| `/api/alerts` | GET | Trend-change alerts (HOT/COOL flips) |
| `/api/impacts/<theme>` | GET | Cross-market causal impact chain |
| `/api/distribution` | GET | Sentiment distribution across themes |
| `/api/analytics-extended` | GET | Volatility, momentum, market pulse, and portfolio signals |
| `/api/theme-history/<theme>` | GET | Historical sentiment data for charting |

## Data Sources

When `FRED_API_KEY` is set, the dashboard pulls real data from:

| Series | Theme | Description |
|--------|-------|-------------|
| CPIAUCSL | Inflation | Consumer Price Index |
| GDP | GDP | Gross Domestic Product |
| UNRATE | Employment | Unemployment Rate |
| HOUST | Housing | Housing Starts |
| NASDAQCOM | Tech | NASDAQ Composite |
| DCOILWTICO | Energy | Crude Oil Price (WTI) |

Without a key, the app runs in simulation mode with realistic mock data and dynamic headline generation.

## Project Structure
```
├── backend/
│   ├── app.py            # Flask REST API (8 endpoints) + serves React build
│   ├── analyzer.py       # MacroTracker engine (sentiment, risk, memory, impacts, analytics)
│   └── data_fetcher.py   # FRED API integration
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── Dashboard.js  # Main dashboard (tabbed layout, 15+ sub-components)
│   │   ├── Dashboard.css # Styles (dark navy theme)
│   │   └── index.js
│   └── public/
├── Dockerfile            # Multi-stage build for Railway deployment
├── railway.json          # Railway config
├── nixpacks.toml         # Nixpacks config (Railway alternative)
├── Procfile              # Process file
├── requirements.txt
└── README.md
```
