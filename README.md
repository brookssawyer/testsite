# NCAA Basketball Live Betting Monitor 🏀

An intelligent, real-time NCAA basketball betting monitoring system with smart confidence scoring.

## Features

### 📊 Smart Confidence Scoring
- Analyzes team statistics (pace, efficiency, shooting, defense)
- Calculates confidence scores (0-100) for betting opportunities
- Recommends unit sizing (0.5, 1, 2, or 3 units) based on confidence
- Detailed breakdown showing how each factor contributes to the score

### 🎯 Live Game Monitoring
- Polls The Odds API every 30 seconds for live game data and odds
- Calculates Required PPM (Points Per Minute) to hit Over/Under
- Triggers alerts when PPM > 4.5
- Real-time updates in dashboard
- Includes live betting odds from major sportsbooks

### 📈 Dual Data Sources
- **KenPom** (Recommended): Premium advanced metrics (requires subscription ~$20/year)
- **ESPN** (Free): Calculated metrics from box score data
- Easy config toggle between sources

### 📝 Comprehensive Logging
- CSV logging of every 30-second poll
- End-of-game result tracking
- Performance analytics by confidence tier
- Win rate, ROI, and unit profit tracking

### 🎨 Modern Dashboard
- Real-time game cards with confidence display
- Color-coded by confidence level (red/yellow/green)
- Sort and filter options
- Mobile-responsive dark theme
- Historical accuracy tracking

### 🔐 Admin Panel
- User management (add/remove users)
- Manual team stats refresh
- Adjustable confidence formula weights
- System status monitoring
- CSV data exports

## Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: Next.js 14, TailwindCSS, TypeScript
- **Data Sources**: The Odds API (live games & odds), KenPom or ESPN (team stats)
- **Storage**: CSV files (portable and simple)
- **Deployment**: Railway (backend 24/7) + Vercel (frontend)

## Quick Start

### Prerequisites

1. **The Odds API Key** (required)
   - Sign up at https://the-odds-api.com
   - Free tier: 500 requests/month
   - Get your API key from dashboard

2. **KenPom Subscription** (optional but recommended)
   - Subscribe at https://kenpom.com (~$20/year)
   - Or use free ESPN data source

### Installation

1. **Clone and setup backend**:
```bash
cd basketball-betting

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

2. **Configure data source**:
```bash
# In .env file:
USE_KENPOM=true  # or false for ESPN
KENPOM_EMAIL=your-email@example.com  # if using KenPom
KENPOM_PASSWORD=your-password
ODDS_API_KEY=your-odds-api-key
```

3. **Install frontend**:
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local if needed
```

### Running Locally

1. **Start backend** (in one terminal):
```bash
# From project root
python api/main.py
# API runs on http://localhost:8000
```

2. **Start monitor** (in another terminal):
```bash
# From project root
python monitor.py
```

3. **Start frontend** (in third terminal):
```bash
cd frontend
npm run dev
# Dashboard runs on http://localhost:3000
```

4. **Login**:
- Default credentials: `admin` / `changeme`
- Change password immediately in admin panel

## Deployment

**For complete deployment instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)**

### Quick Deployment Overview

**Backend (Railway):**
- Deploy from GitHub repo
- Runs both API server and monitor worker
- Set environment variables (see DEPLOYMENT.md)

**Frontend (Vercel):**
- Deploy from GitHub repo (set root to `frontend/`)
- Set `NEXT_PUBLIC_API_URL` to Railway backend URL

**Custom Domain:**
- Add domain to Vercel
- Configure DNS records at registrar
- SSL auto-provisioned by Vercel

See [DEPLOYMENT.md](./DEPLOYMENT.md) for step-by-step instructions, environment variables, DNS configuration, troubleshooting, and more.

## Usage

### Dashboard

- **Triggered Games**: Shows only games with confidence > 40
- **All Games**: Shows all live games
- **Sort by Confidence**: Best bets first
- **Game Cards**: Click for detailed breakdown

### Admin Panel

Access at `/admin` (admin users only):
- **Users**: Add/remove dashboard users
- **Team Stats**: Refresh statistics manually
- **Weights**: Adjust confidence scoring formula
- **Export**: Download CSV logs

## Confidence Scoring Logic

Base score starts at 50 (trigger met), then:

**Pace Analysis** (+12, +5, or -10 per team):
- Slow pace (< 67 poss/game): Bonus
- Fast pace (> 72): Penalty

**3-Point Analysis** (+8, -5):
- Low attempt rate (< 30%): Bonus
- High accuracy (> 38%): Penalty

**Defense** (+10 per team):
- Strong defense (< 95 pts/100 poss): Bonus

**Matchup Bonuses** (+15, +10, -5):
- Both teams slow: Big bonus
- Both strong defense: Bonus
- Pace mismatch: Penalty

**PPM Severity** (+0 to +15):
- Higher required PPM = more confident in under

Final score capped at 0-100.

## Data Files

All data stored in `/data/` directory:
- `team_stats.csv`: Cached team statistics
- `ncaa_live_log.csv`: Every 30-second poll logged
- `ncaa_results.csv`: Final game results
- `users.json`: User accounts

## Customization

### Adjust Confidence Weights

Edit `config.py` or use admin panel:
```python
CONFIDENCE_WEIGHTS = {
    "slow_pace_threshold": 67,
    "slow_pace_bonus": 12,
    # ... adjust as needed
}
```

### Change Polling Interval

In `config.py`:
```python
POLL_INTERVAL = 30  # seconds
```

### Modify Unit Sizes

In `config.py`:
```python
UNIT_SIZES = {
    "no_bet": (0, 40),
    "low": (41, 60),      # 0.5 units
    "medium": (61, 75),   # 1 unit
    "high": (76, 85),     # 2 units
    "max": (86, 100),     # 3 units
}
```

## File Structure

```
basketball-betting/
├── api/                    # FastAPI backend
│   ├── main.py            # API endpoints
│   └── auth.py            # Authentication
├── utils/                 # Core utilities
│   ├── team_stats.py      # Unified stats manager
│   ├── team_stats_kenpom.py
│   ├── team_stats_espn.py
│   ├── confidence_scorer.py
│   └── csv_logger.py
├── frontend/              # Next.js dashboard
│   ├── src/
│   │   ├── app/          # Pages
│   │   ├── components/   # React components
│   │   └── lib/          # API client
│   └── package.json
├── monitor.py             # Main monitoring script
├── config.py              # Configuration
├── requirements.txt       # Python dependencies
└── data/                  # CSV logs and cache
```

## Troubleshooting

### Team stats not loading
```bash
# Manually refresh
python -c "from utils.team_stats import get_stats_manager; get_stats_manager().fetch_all_stats(force_refresh=True)"
```

### KenPom login failing
- Check credentials in `.env`
- Verify subscription is active
- Switch to ESPN: `USE_KENPOM=false`

### No live games showing
- Check The Odds API key
- Verify API quota not exceeded (500/month on free tier)
- Check if games are actually live
- NCAA basketball season runs November-April

## Support

- Issues: Create GitHub issue
- Questions: Check CLAUDE.md for development guide

## License

Private use only.
