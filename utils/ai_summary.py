"""
AI-Powered Betting Summary Generator

Uses OpenAI API to generate intelligent, context-aware betting summaries
for live NCAA basketball games based on:
- Current game state (score, time remaining, pace)
- Team statistics and metrics (pace, defense, shooting)
- Confidence scores and betting triggers
- Historical matchup data
"""

import os
from typing import Dict, Any, Optional
from openai import OpenAI
from loguru import logger
import config


class AISummaryGenerator:
    """Generate AI-powered betting summaries using OpenAI"""

    def __init__(self):
        """Initialize OpenAI client"""
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.warning("OPENAI_API_KEY not set in environment")
            self.client = None
        else:
            self.client = OpenAI(api_key=api_key)
            logger.info("AI Summary Generator initialized")

    def generate_summary(
        self,
        game_data: Dict[str, Any],
        home_metrics: Optional[Dict[str, Any]] = None,
        away_metrics: Optional[Dict[str, Any]] = None
    ) -> Dict[str, str]:
        """
        Generate AI betting summary for a game

        Args:
            game_data: Current game state (score, time, odds, etc.)
            home_metrics: Home team statistics
            away_metrics: Away team statistics

        Returns:
            Dictionary with summary, recommendation, and reasoning
        """
        if not self.client:
            return {
                "summary": "AI summary unavailable - OpenAI API key not configured",
                "recommendation": "PASS",
                "reasoning": "Configure OPENAI_API_KEY environment variable to enable AI summaries"
            }

        try:
            # Build the prompt
            prompt = self._build_prompt(game_data, home_metrics, away_metrics)

            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",  # Fast and cost-effective
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=500
            )

            # Parse response
            content = response.choices[0].message.content
            parsed = self._parse_response(content)

            logger.info(f"Generated AI summary for {game_data.get('away_team')} @ {game_data.get('home_team')}")
            return parsed

        except Exception as e:
            logger.error(f"Error generating AI summary: {e}")
            return {
                "summary": f"Error generating AI summary: {str(e)}",
                "recommendation": "PASS",
                "reasoning": "Unable to generate summary due to API error"
            }

    def _get_system_prompt(self) -> str:
        """Get the system prompt that defines the AI's role"""
        return """You are an expert NCAA basketball betting analyst with deep knowledge of:
- Live in-game betting strategies (especially under/over totals)
- Team pace, efficiency, and defensive metrics
- How game situations affect scoring (halftime adjustments, foul trouble, time management)
- Points Per Minute (PPM) analysis for live totals

Your job: Analyze live game data and provide sharp, actionable betting recommendations.

Format your response EXACTLY as:
RECOMMENDATION: [BET UNDER / BET OVER / PASS]
CONFIDENCE: [1-5 stars]
SUMMARY: [2-3 sentences explaining the current situation]
REASONING: [3-4 key factors supporting your recommendation]

Be concise, direct, and focus on the most important factors. No fluff."""

    def _build_prompt(
        self,
        game_data: Dict[str, Any],
        home_metrics: Optional[Dict[str, Any]],
        away_metrics: Optional[Dict[str, Any]]
    ) -> str:
        """Build the user prompt with game context"""

        # Extract game state
        away_team = game_data.get('away_team', 'Away')
        home_team = game_data.get('home_team', 'Home')
        away_score = game_data.get('away_score', 0)
        home_score = game_data.get('home_score', 0)
        total_points = game_data.get('total_points', 0)
        period = game_data.get('period', 1)
        minutes_remaining = game_data.get('minutes_remaining', 20)
        ou_line = game_data.get('ou_line', 0)
        required_ppm = game_data.get('required_ppm', 0)
        current_ppm = game_data.get('current_ppm', 0)
        confidence_score = game_data.get('confidence_score', 0)
        bet_type = game_data.get('bet_type', 'under')

        # Build prompt
        prompt = f"""Analyze this live NCAA basketball game for betting:

GAME STATE:
{away_team} {away_score} @ {home_team} {home_score}
Total Points: {total_points} | Period: {period} | Minutes Left: {minutes_remaining}

BETTING DATA:
Over/Under Line: {ou_line}
Required PPM to hit Over: {required_ppm:.2f}
Current PPM: {current_ppm:.2f}
System Confidence: {confidence_score}% for {bet_type.upper()}
"""

        # Add team metrics if available
        if home_metrics or away_metrics:
            prompt += "\nTEAM METRICS:\n"

            if home_metrics:
                prompt += f"{home_team}:\n"
                prompt += f"  Pace (poss/game): {home_metrics.get('pace_per_game', 'N/A')}\n"
                prompt += f"  Defensive Eff: {home_metrics.get('adj_defensive_efficiency', 'N/A')}\n"
                prompt += f"  3PT Rate: {home_metrics.get('three_point_rate', 'N/A')}\n"
                prompt += f"  FT Rate: {home_metrics.get('free_throw_rate', 'N/A')}\n"

            if away_metrics:
                prompt += f"{away_team}:\n"
                prompt += f"  Pace (poss/game): {away_metrics.get('pace_per_game', 'N/A')}\n"
                prompt += f"  Defensive Eff: {away_metrics.get('adj_defensive_efficiency', 'N/A')}\n"
                prompt += f"  3PT Rate: {away_metrics.get('three_point_rate', 'N/A')}\n"
                prompt += f"  FT Rate: {away_metrics.get('free_throw_rate', 'N/A')}\n"

        prompt += f"\nShould I bet {bet_type.upper()} on this game? Why or why not?"

        return prompt

    def _parse_response(self, content: str) -> Dict[str, str]:
        """Parse the AI response into structured format"""
        lines = content.strip().split('\n')

        result = {
            "recommendation": "PASS",
            "confidence": "",
            "summary": "",
            "reasoning": ""
        }

        current_section = None

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith("RECOMMENDATION:"):
                result["recommendation"] = line.split(":", 1)[1].strip()
            elif line.startswith("CONFIDENCE:"):
                result["confidence"] = line.split(":", 1)[1].strip()
            elif line.startswith("SUMMARY:"):
                current_section = "summary"
                result["summary"] = line.split(":", 1)[1].strip()
            elif line.startswith("REASONING:"):
                current_section = "reasoning"
                result["reasoning"] = line.split(":", 1)[1].strip()
            elif current_section == "summary":
                result["summary"] += " " + line
            elif current_section == "reasoning":
                result["reasoning"] += " " + line

        # Combine into a single formatted summary
        full_summary = f"""**{result['recommendation']}** {result['confidence']}

{result['summary']}

**Key Factors:**
{result['reasoning']}"""

        return {
            "summary": full_summary,
            "recommendation": result['recommendation'],
            "reasoning": result['reasoning']
        }


# Singleton instance
_ai_generator = None


def get_ai_summary_generator() -> AISummaryGenerator:
    """Get singleton AI summary generator instance"""
    global _ai_generator
    if _ai_generator is None:
        _ai_generator = AISummaryGenerator()
    return _ai_generator
