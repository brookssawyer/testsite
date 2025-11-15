"""
Configuration for NCAA Basketball Betting Monitor
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent

# ========== DATA SOURCE CONFIGURATION ==========
# Toggle between KenPom (paid) and ESPN (free)
USE_KENPOM = os.getenv("USE_KENPOM", "false").lower() == "true"

# KenPom credentials (only needed if USE_KENPOM=true)
KENPOM_EMAIL = os.getenv("KENPOM_EMAIL", "")
KENPOM_PASSWORD = os.getenv("KENPOM_PASSWORD", "")

# The Odds API key for live game data and odds
ODDS_API_KEY = os.getenv("ODDS_API_KEY", "")

# ========== SPORTSBOOK CONFIGURATION ==========
# Default sportsbook for odds (can be changed via frontend selector)
# Common options: "fanduel", "draftkings", "betmgm", "caesars", "pointsbet", "bovada"
# Set to "consensus" to use average of all available books
DEFAULT_SPORTSBOOK = os.getenv("DEFAULT_SPORTSBOOK", "fanduel")

# List of supported sportsbooks (in priority order if default not available)
SUPPORTED_SPORTSBOOKS = [
    "fanduel",
    "draftkings",
    "betmgm",
    "caesars",
    "pointsbet",
    "bovada",
    "wynnbet",
    "unibet"
]

# ========== MONITORING CONFIGURATION ==========
# Sport mode: "ncaa" or "nba" (for testing with live NBA games)
SPORT_MODE = os.getenv("SPORT_MODE", "ncaa").lower()

# Polling interval in seconds
POLL_INTERVAL = 15  # 15 seconds - faster refresh for ESPN and Odds API

# Game filtering settings
FILTER_LAST_MINUTE_GAMES = True  # Hide games with ≤1 minute remaining from the site
MIN_TIME_REMAINING = 1.0  # Minimum minutes remaining to display a game

# PPM thresholds for triggering alerts (BALANCED - neutral between over/under)
PPM_THRESHOLD_UNDER = 3.0   # Trigger UNDER when required PPM is HIGH (need to score fast)
PPM_THRESHOLD_OVER = 3.0    # Trigger OVER when required PPM is LOW (scoring fast already)

# PPM difference threshold (absolute difference between current_ppm and required_ppm)
PPM_DIFFERENCE_THRESHOLD = 0.5  # Trigger when pace difference is significant (more responsive)

# Legacy alias for backward compatibility
PPM_THRESHOLD = PPM_THRESHOLD_UNDER

# Team stats refresh frequency (in hours)
STATS_REFRESH_HOURS = 24

# ========== CONFIDENCE SCORING WEIGHTS ==========
# These can be adjusted via admin panel
# BALANCED - Reduced under-favoring bonuses by ~40% for neutrality
CONFIDENCE_WEIGHTS = {
    # Pace factors (possessions per game)
    "slow_pace_threshold": 67,      # Below this = slow
    "fast_pace_threshold": 72,      # Above this = fast
    "slow_pace_bonus": 7,           # Reduced from 12 (favors under)
    "medium_pace_bonus": 3,         # Reduced from 5
    "fast_pace_penalty": -6,        # Reduced from -10 (more neutral)

    # 3-Point factors
    "low_3p_rate_threshold": 0.30,  # 30% of FGA
    "high_3p_pct_threshold": 0.38,  # 38% accuracy
    "low_3p_rate_bonus": 5,         # Reduced from 8 (favors under)
    "high_3p_pct_penalty": -5,      # Unchanged (already balanced)

    # Free throw factors
    "low_ft_rate_threshold": 18,    # FTA per game
    "high_ft_rate_threshold": 24,
    "low_ft_rate_bonus": 4,         # Reduced from 6 (favors under)
    "high_ft_rate_penalty": -6,     # Unchanged (already balanced)

    # Turnover factors
    "high_to_rate_threshold": 14,   # TO per game
    "high_to_rate_bonus": 3,        # Reduced from 5 (favors under)

    # Defensive factors
    "strong_defense_threshold": 95, # Points per 100 poss
    "strong_defense_bonus": 6,      # Reduced from 10 (favors under)

    # Matchup bonuses
    "both_slow_bonus": 9,           # Reduced from 15 (favors under)
    "both_strong_defense_bonus": 6, # Reduced from 10 (favors under)
    "pace_mismatch_penalty": -5,    # Unchanged (already balanced)
}

# Unit sizing based on confidence
UNIT_SIZES = {
    "no_bet": (0, 40),      # 0-40: Don't bet
    "low": (41, 60),        # 41-60: 0.5 units
    "medium": (61, 75),     # 61-75: 1 unit
    "high": (76, 85),       # 76-85: 2 units
    "max": (86, 100),       # 86-100: 3 units
}

# ========== DATABASE/STORAGE CONFIGURATION ==========
# CSV file paths
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

TEAM_STATS_FILE = DATA_DIR / "team_stats.csv"
LIVE_LOG_FILE = DATA_DIR / "ncaa_live_log.csv"
RESULTS_FILE = DATA_DIR / "ncaa_results.csv"

# Cache directory
CACHE_DIR = BASE_DIR / "cache"
CACHE_DIR.mkdir(exist_ok=True)

# ========== API CONFIGURATION ==========
# FastAPI settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
# Render provides PORT env var, fallback to API_PORT or 8000
API_PORT = int(os.getenv("PORT", os.getenv("API_PORT", "8000")))
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production-please")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

# CORS settings
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",") if os.getenv("ALLOWED_ORIGINS") != "*" else ["*"]

# ========== LOGGING CONFIGURATION ==========
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "monitor.log"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ========== DEPLOYMENT CONFIGURATION ==========
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")  # development, production
IS_PRODUCTION = ENVIRONMENT == "production"

# Railway backend URL (set in production)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Frontend URL (Vercel)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# ========== EMAIL CONFIGURATION ==========
EMAIL_ENABLED = os.getenv("EMAIL_ENABLED", "false").lower() == "true"
EMAIL_FROM = os.getenv("EMAIL_FROM", "")
EMAIL_TO = os.getenv("EMAIL_TO", "")
EMAIL_SMTP_SERVER = os.getenv("EMAIL_SMTP_SERVER", "smtp.gmail.com")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
DAILY_REPORT_TIME = os.getenv("DAILY_REPORT_TIME", "09:00")  # HH:MM format
