import numpy as np
import pandas as pd
import math


class PoissonCalculator:
    """
    A class to calculate football match probabilities using Poisson distribution
    and convert them to betting odds for various Over/Under markets.
    """

    def __init__(self):
        # Only store the essential averages as class properties
        self.home_avg_goals_for = None
        self.home_avg_goals_against = None
        self.away_avg_goals_for = None
        self.away_avg_goals_against = None
        self.league_avg_goals = None

        # Detailed league averages (optional)
        self.using_detailed_averages = False
        self.league_home_goals_for = None
        self.league_home_goals_against = None
        self.league_away_goals_for = None
        self.league_away_goals_against = None

        # Calculated strength values
        self.home_attack_strength = None
        self.home_defense_strength = None
        self.away_attack_strength = None
        self.away_defense_strength = None

    def set_team_averages(self, home_goals_for, home_goals_against,
                          away_goals_for, away_goals_against, league_avg):
        """
        Set team averages directly using simple league average.

        Args:
            home_goals_for (float): Home team average goals scored per game
            home_goals_against (float): Home team average goals conceded per game
            away_goals_for (float): Away team average goals scored per game
            away_goals_against (float): Away team average goals conceded per game
            league_avg (float): League average goals per game
        """
        self.home_avg_goals_for = home_goals_for
        self.home_avg_goals_against = home_goals_against
        self.away_avg_goals_for = away_goals_for
        self.away_avg_goals_against = away_goals_against
        self.league_avg_goals = league_avg
        self.using_detailed_averages = False

    def set_team_averages_detailed(self, home_goals_for, home_goals_against,
                                   away_goals_for, away_goals_against,
                                   league_home_for, league_away_for):
        """
        Set team averages with detailed league averages for more accurate calculations.

        Args:
            home_goals_for (float): Home team average goals scored per game
            home_goals_against (float): Home team average goals conceded per game
            away_goals_for (float): Away team average goals scored per game
            away_goals_against (float): Away team average goals conceded per game
            league_home_for (float): League average goals scored by home teams
            league_away_for (float): League average goals scored by away teams
        """
        self.home_avg_goals_for = home_goals_for
        self.home_avg_goals_against = home_goals_against
        self.away_avg_goals_for = away_goals_for
        self.away_avg_goals_against = away_goals_against

        # Set league averages and derive the logical relationships
        self.league_home_goals_for = league_home_for
        self.league_away_goals_for = league_away_for
        self.league_home_goals_against = league_away_for  # Home goals against = Away goals for
        self.league_away_goals_against = league_home_for  # Away goals against = Home goals for

        self.using_detailed_averages = True

    def set_team_from_totals_detailed(self, home_games, home_goals_scored, home_goals_conceded,
                                      away_games, away_goals_scored, away_goals_conceded,
                                      league_home_for, league_away_for):
        """
        Calculate team averages from totals with detailed league averages.

        Args:
            home_games (int): Number of home games played
            home_goals_scored (int): Total goals scored at home
            home_goals_conceded (int): Total goals conceded at home
            away_games (int): Number of away games played
            away_goals_scored (int): Total goals scored away
            away_goals_conceded (int): Total goals conceded away
            league_home_for (float): League average goals scored by home teams
            league_away_for (float): League average goals scored by away teams
        """
        # Calculate team averages
        self.home_avg_goals_for = home_goals_scored / home_games
        self.home_avg_goals_against = home_goals_conceded / home_games
        self.away_avg_goals_for = away_goals_scored / away_games
        self.away_avg_goals_against = away_goals_conceded / away_games

        # Set league averages and derive the logical relationships
        self.league_home_goals_for = league_home_for
        self.league_away_goals_for = league_away_for
        self.league_home_goals_against = league_away_for  # Home goals against = Away goals for
        self.league_away_goals_against = league_home_for  # Away goals against = Home goals for

        self.using_detailed_averages = True

    def set_team_from_totals(self, home_games, home_goals_scored, home_goals_conceded,
                             away_games, away_goals_scored, away_goals_conceded, league_avg):
        """
        Calculate and set team averages from total games and goals using simple league average.
        Does NOT store the totals, only the calculated averages.

        Args:
            home_games (int): Number of home games played
            home_goals_scored (int): Total goals scored at home
            home_goals_conceded (int): Total goals conceded at home
            away_games (int): Number of away games played
            away_goals_scored (int): Total goals scored away
            away_goals_conceded (int): Total goals conceded away
            league_avg (float): League average goals per game
        """
        # Calculate averages and set the class properties
        self.home_avg_goals_for = home_goals_scored / home_games
        self.home_avg_goals_against = home_goals_conceded / home_games
        self.away_avg_goals_for = away_goals_scored / away_games
        self.away_avg_goals_against = away_goals_conceded / away_games
        self.league_avg_goals = league_avg
        self.using_detailed_averages = False

    def calculate_strengths(self):
        """
        Calculate attacking and defensive strengths relative to league average.
        Uses detailed league averages if available, otherwise falls back to simple average.
        Sets the strength properties on the class.
        """
        if self.using_detailed_averages:
            # Validate detailed averages are set
            if not all([self.home_avg_goals_for, self.home_avg_goals_against,
                        self.away_avg_goals_for, self.away_avg_goals_against,
                        self.league_home_goals_for, self.league_home_goals_against,
                        self.league_away_goals_for, self.league_away_goals_against]):
                raise ValueError("Team and detailed league averages must be set before calculating strengths")

            # Calculate strengths using detailed league averages (more accurate)
            self.home_attack_strength = self.home_avg_goals_for / self.league_home_goals_for
            self.home_defense_strength = self.home_avg_goals_against / self.league_away_goals_for
            self.away_attack_strength = self.away_avg_goals_for / self.league_away_goals_for
            self.away_defense_strength = self.away_avg_goals_against / self.league_home_goals_for

        else:
            # Validate simple averages are set
            if not all([self.home_avg_goals_for, self.home_avg_goals_against,
                        self.away_avg_goals_for, self.away_avg_goals_against,
                        self.league_avg_goals]):
                raise ValueError("Team averages must be set before calculating strengths")

            # Calculate strengths using simple league average (original method)
            self.home_attack_strength = self.home_avg_goals_for / self.league_avg_goals
            self.home_defense_strength = self.home_avg_goals_against / self.league_avg_goals
            self.away_attack_strength = self.away_avg_goals_for / self.league_avg_goals
            self.away_defense_strength = self.away_avg_goals_against / self.league_avg_goals

    def _calculate_goal_expectancy(self):
        """
        Calculate expected goals for each team in the matchup.
        Uses appropriate league averages based on calculation mode.
        Returns the values rather than storing them.

        Returns:
            tuple: (home_goal_expectancy, away_goal_expectancy)
        """
        if not all([self.home_attack_strength, self.home_defense_strength,
                    self.away_attack_strength, self.away_defense_strength]):
            raise ValueError("Strengths must be calculated before goal expectancy")

        if self.using_detailed_averages:
            # Use detailed league averages for more accurate expectancy
            home_goal_expectancy = (self.home_attack_strength *
                                    self.away_defense_strength *
                                    self.league_home_goals_for)

            away_goal_expectancy = (self.away_attack_strength *
                                    self.home_defense_strength *
                                    self.league_away_goals_for)
        else:
            # Use simple league average (original method)
            home_goal_expectancy = (self.home_attack_strength *
                                    self.away_defense_strength *
                                    self.league_avg_goals)

            away_goal_expectancy = (self.away_attack_strength *
                                    self.home_defense_strength *
                                    self.league_avg_goals)

        return home_goal_expectancy, away_goal_expectancy

    def _poisson_pmf(self, k, lam):
        """
        Calculate Poisson probability mass function.

        Args:
            k (int): Number of events
            lam (float): Expected number of events (lambda)

        Returns:
            float: Probability
        """
        return (lam ** k) * np.exp(-lam) / math.factorial(k)

    def _generate_scoreline_probabilities(self, home_expectancy, away_expectancy, max_goals=8):
        """
        Generate probability matrix for all possible scorelines using Poisson distribution.

        Args:
            home_expectancy (float): Expected goals for home team
            away_expectancy (float): Expected goals for away team
            max_goals (int): Maximum number of goals to calculate for (default 8)

        Returns:
            numpy.ndarray: Matrix of scoreline probabilities
        """
        goals_range = range(max_goals + 1)
        prob_matrix = np.zeros((max_goals + 1, max_goals + 1))

        for home_goals in goals_range:
            for away_goals in goals_range:
                home_prob = self._poisson_pmf(home_goals, home_expectancy)
                away_prob = self._poisson_pmf(away_goals, away_expectancy)
                prob_matrix[home_goals][away_goals] = home_prob * away_prob

        return prob_matrix

    def _calculate_over_under_probabilities(self, prob_matrix):
        """
        Calculate probabilities for Over/Under markets from scoreline matrix.
        Calculate UNDER probabilities directly (finite), then derive OVER as 1 - UNDER.

        Args:
            prob_matrix (numpy.ndarray): Scoreline probability matrix

        Returns:
            dict: Probabilities for different Over/Under thresholds
        """
        results = {}
        thresholds = [0.5, 1.5, 2.5, 3.5]

        for threshold in thresholds:
            under_prob = 0

            # Calculate UNDER probability (finite number of scorelines)
            for home_goals in range(len(prob_matrix)):
                for away_goals in range(len(prob_matrix[0])):
                    total_goals = home_goals + away_goals

                    if total_goals <= threshold:
                        prob = prob_matrix[home_goals][away_goals]
                        under_prob += prob

            # OVER probability is the complement
            over_prob = 1 - under_prob

            results[f"Under {threshold}"] = {
                'under_probability': under_prob,
                'over_probability': over_prob,
                'under_odds': 1 / under_prob if under_prob > 0 else float('inf'),
                'over_odds': 1 / over_prob if over_prob > 0 else float('inf')
            }

        return results

    def _apply_margin(self, odds, margin_percent=3):
        """
        Apply bookmaker margin to odds.

        Args:
            odds (float): Original fair odds
            margin_percent (float): Margin percentage (default 3%)

        Returns:
            float: Odds with margin applied
        """
        margin_multiplier = 1 + (margin_percent / 100)
        return odds * margin_multiplier

    def get_summary_info(self):
        """
        Get summary information about the calculation inputs and expectations.
        Must be called after calculate_strengths().

        Returns:
            dict: Summary information
        """
        if not all([self.home_attack_strength, self.away_attack_strength]):
            raise ValueError("Strengths must be calculated before getting summary info")

        home_expectancy, away_expectancy = self._calculate_goal_expectancy()

        return {
            'Home Team Expected Goals': f"{home_expectancy:.2f}",
            'Away Team Expected Goals': f"{away_expectancy:.2f}",
            'Total Expected Goals': f"{home_expectancy + away_expectancy:.2f}",
            'Home Attack Strength': f"{self.home_attack_strength:.2f}",
            'Home Defense Strength': f"{self.home_defense_strength:.2f}",
            'Away Attack Strength': f"{self.away_attack_strength:.2f}",
            'Away Defense Strength': f"{self.away_defense_strength:.2f}"
        }

    def generate_market_analysis(self, margin_percent=3):
        """
        Generate complete market analysis table.
        This is the main method that orchestrates all calculations and returns results.

        Args:
            margin_percent (float): Margin percentage to apply (default 3%)

        Returns:
            pd.DataFrame: Formatted results table
        """
        # Ensure strengths are calculated
        if not all([self.home_attack_strength, self.away_attack_strength]):
            raise ValueError("Strengths must be calculated before generating market analysis")

        # Calculate goal expectancies
        home_expectancy, away_expectancy = self._calculate_goal_expectancy()

        # Generate scoreline probabilities
        prob_matrix = self._generate_scoreline_probabilities(home_expectancy, away_expectancy)

        # Calculate over/under probabilities
        over_under_results = self._calculate_over_under_probabilities(prob_matrix)

        # Format results into a clean table
        results_data = []

        for market, data in over_under_results.items():
            under_odds_with_margin = self._apply_margin(data['under_odds'], margin_percent)
            over_odds_with_margin = self._apply_margin(data['over_odds'], margin_percent)

            results_data.append({
                'Market': market,
                'Probability': f"{data['under_probability']:.2%}",
                'Fair Odds': f"{data['under_odds']:.2f}",
                'Odds + Margin': f"{under_odds_with_margin:.2f}",
                'Opposite Probability': f"{data['over_probability']:.2%}",
                'Opposite Odds + Margin': f"{over_odds_with_margin:.2f}"
            })

        return pd.DataFrame(results_data)