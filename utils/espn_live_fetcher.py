"""
ESPN Live Game Fetcher
Fetches live scores and game time directly from ESPN's unofficial scoreboard API
"""
import requests
from typing import Dict, List, Optional
from datetime import datetime
from loguru import logger


class ESPNLiveFetcher:
    """Fetches live game data from ESPN scoreboard API"""

    BASE_URL = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def fetch_live_games(self) -> List[Dict]:
        """
        Fetch all live and upcoming NCAA Division 1 basketball games from ESPN

        Returns:
            List of game dicts with:
            - game_id: ESPN game ID
            - home_team: Home team name
            - away_team: Away team name
            - home_score: Current home score
            - away_score: Current away score
            - status: Game status (pre-game, in-progress, final)
            - period: Current period (1, 2, OT, etc.)
            - clock: Time remaining in period (MM:SS format)
            - minutes_remaining: Minutes remaining as int
            - seconds_remaining: Seconds remaining as int
            - is_live: Boolean if game is currently in progress
            - completed: Boolean if game is final
        """
        try:
            # Fetch all D1 games (group 50 = Division 1)
            params = {
                'limit': 500,      # Get all games, not just top 25
                'groups': 50       # Division 1
            }

            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            games = []

            # Parse events
            for event in data.get('events', []):
                try:
                    game = self._parse_game(event)
                    if game:
                        games.append(game)
                except Exception as e:
                    logger.warning(f"Error parsing ESPN game: {e}")
                    continue

            logger.info(f"Fetched {len(games)} games from ESPN scoreboard")
            return games

        except Exception as e:
            logger.error(f"Error fetching ESPN scoreboard: {e}")
            return []

    def _parse_game(self, event: Dict) -> Optional[Dict]:
        """Parse a single game event from ESPN API"""
        try:
            # Basic game info
            game_id = event.get('id')
            competitions = event.get('competitions', [])

            if not competitions:
                return None

            competition = competitions[0]
            competitors = competition.get('competitors', [])

            if len(competitors) != 2:
                return None

            # Find home and away teams
            home_team = None
            away_team = None

            for competitor in competitors:
                team_info = competitor.get('team', {})
                score = competitor.get('score', '0')

                if competitor.get('homeAway') == 'home':
                    home_team = {
                        'name': team_info.get('displayName', ''),
                        'abbreviation': team_info.get('abbreviation', ''),
                        'score': int(score) if score else 0
                    }
                else:
                    away_team = {
                        'name': team_info.get('displayName', ''),
                        'abbreviation': team_info.get('abbreviation', ''),
                        'score': int(score) if score else 0
                    }

            if not home_team or not away_team:
                return None

            # Game status
            status = competition.get('status', {})
            status_type = status.get('type', {})
            status_state = status_type.get('state', 'pre')  # pre, in, post
            status_description = status_type.get('description', '')

            # Period and clock
            period_number = status.get('period', 0)
            display_clock = status.get('displayClock', '0:00')

            # Parse clock to get minutes and seconds remaining
            minutes_remaining = 0
            seconds_remaining = 0

            if ':' in display_clock:
                parts = display_clock.split(':')
                try:
                    minutes_remaining = int(parts[0])
                    seconds_remaining = int(parts[1])
                except:
                    pass

            # Determine if game is live
            is_live = status_state == 'in'
            completed = status_state == 'post'

            # Period name (1st Half, 2nd Half, OT, etc.)
            period_name = self._format_period(period_number, status_description)

            return {
                'game_id': game_id,
                'home_team': home_team['name'],
                'home_abbreviation': home_team['abbreviation'],
                'away_team': away_team['name'],
                'away_abbreviation': away_team['abbreviation'],
                'home_score': home_team['score'],
                'away_score': away_team['score'],
                'status': status_state,
                'status_description': status_description,
                'period': period_number,
                'period_name': period_name,
                'clock': display_clock,
                'minutes_remaining': minutes_remaining,
                'seconds_remaining': seconds_remaining,
                'is_live': is_live,
                'completed': completed,
                'timestamp': datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Error parsing ESPN game event: {e}")
            return None

    def _format_period(self, period: int, description: str) -> str:
        """Format period number into readable string"""
        if 'Final' in description or 'final' in description:
            return 'Final'
        elif 'Half' in description or 'Halftime' in description:
            return 'Halftime'
        elif period == 0:
            return 'Scheduled'
        elif period == 1:
            return '1st Half'
        elif period == 2:
            return '2nd Half'
        elif period > 2:
            return f'OT{period - 2}' if period > 3 else 'OT'
        else:
            return str(period)

    def get_game_by_teams(self, home_team: str, away_team: str, all_games: List[Dict]) -> Optional[Dict]:
        """
        Find a specific game by team names from a list of games
        Uses flexible matching to handle name variations
        """
        home_lower = home_team.lower()
        away_lower = away_team.lower()

        for game in all_games:
            game_home = game['home_team'].lower()
            game_away = game['away_team'].lower()

            # Check direct match or partial match
            home_match = (home_lower in game_home or game_home in home_lower or
                         home_lower == game['home_abbreviation'].lower())
            away_match = (away_lower in game_away or game_away in away_lower or
                         away_lower == game['away_abbreviation'].lower())

            if home_match and away_match:
                return game

        return None


# Singleton instance
_espn_live_fetcher = None

def get_espn_live_fetcher() -> ESPNLiveFetcher:
    """Get singleton ESPN live fetcher instance"""
    global _espn_live_fetcher
    if _espn_live_fetcher is None:
        _espn_live_fetcher = ESPNLiveFetcher()
    return _espn_live_fetcher
