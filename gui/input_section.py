from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QGroupBox, QCheckBox, QLineEdit, QLabel, QPushButton,
                             QMessageBox)
from PyQt5.QtCore import pyqtSignal, Qt, QLocale
from PyQt5.QtGui import QDoubleValidator, QIntValidator
import locale


class InputSection(QWidget):
    """
    Widget for handling user input for match prediction.
    """

    calculation_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # Create team input sections
        teams_layout = QHBoxLayout()
        teams_layout.setSpacing(20)

        # Home team section
        self.home_group = self.create_team_group("Home Team", "home")
        teams_layout.addWidget(self.home_group)

        # Away team section
        self.away_group = self.create_team_group("Away Team", "away")
        teams_layout.addWidget(self.away_group)

        main_layout.addLayout(teams_layout)

        # League average section
        league_group = QGroupBox("League Information")
        league_layout = QVBoxLayout(league_group)

        # League calculation mode checkbox
        self.detailed_league_checkbox = QCheckBox("Use detailed home/away league averages (more accurate)")
        self.detailed_league_checkbox.stateChanged.connect(self.toggle_league_mode)
        league_layout.addWidget(self.detailed_league_checkbox)

        # Simple league average (default)
        self.simple_league_widget = QWidget()
        simple_layout = QGridLayout(self.simple_league_widget)
        simple_layout.setContentsMargins(0, 10, 0, 15)  # Add more bottom margin

        simple_layout.addWidget(QLabel("Average Goals per Game:"), 0, 0)
        self.league_avg_edit = QLineEdit()
        self.league_avg_edit.setMinimumHeight(25)  # Ensure minimum height
        league_validator = QDoubleValidator(0.0, 10.0, 2)
        league_validator.setLocale(QLocale(QLocale.C))
        self.league_avg_edit.setValidator(league_validator)
        self.league_avg_edit.setPlaceholderText("e.g., 2.75")
        simple_layout.addWidget(self.league_avg_edit, 0, 1)

        league_layout.addWidget(self.simple_league_widget)

        # Detailed league averages
        self.detailed_league_widget = QWidget()
        detailed_layout = QGridLayout(self.detailed_league_widget)
        detailed_layout.setContentsMargins(0, 10, 0, 15)  # Add more bottom margin
        detailed_layout.setVerticalSpacing(8)  # Add vertical spacing between rows

        detailed_layout.addWidget(QLabel("Home teams avg goals for:"), 0, 0)
        self.league_home_for_edit = QLineEdit()
        self.league_home_for_edit.setMinimumHeight(25)  # Ensure minimum height
        validator1 = QDoubleValidator(0.0, 10.0, 2)
        validator1.setLocale(QLocale(QLocale.C))
        self.league_home_for_edit.setValidator(validator1)
        self.league_home_for_edit.setPlaceholderText("e.g., 1.65")
        detailed_layout.addWidget(self.league_home_for_edit, 0, 1)

        detailed_layout.addWidget(QLabel("Away teams avg goals for:"), 1, 0)
        self.league_away_for_edit = QLineEdit()
        self.league_away_for_edit.setMinimumHeight(25)  # Ensure minimum height
        validator2 = QDoubleValidator(0.0, 10.0, 2)
        validator2.setLocale(QLocale(QLocale.C))
        self.league_away_for_edit.setValidator(validator2)
        self.league_away_for_edit.setPlaceholderText("e.g., 1.10")
        detailed_layout.addWidget(self.league_away_for_edit, 1, 1)

        # Add explanation label with proper spacing
        explanation = QLabel("Note: Home goals against = Away goals for, Away goals against = Home goals for")
        explanation.setStyleSheet("color: #666666; font-style: italic; font-size: 9pt; margin-top: 5px;")
        explanation.setWordWrap(True)
        detailed_layout.addWidget(explanation, 2, 0, 1, 2)

        league_layout.addWidget(self.detailed_league_widget)

        # Initially hide detailed widget
        self.detailed_league_widget.hide()

        main_layout.addWidget(league_group)

        # Calculate button
        self.calculate_btn = QPushButton("Calculate Probabilities")
        self.calculate_btn.clicked.connect(self.on_calculate_clicked)
        self.calculate_btn.setMinimumHeight(40)
        main_layout.addWidget(self.calculate_btn)

    def create_team_group(self, title, team_type):
        """Create input group for a team."""
        group = QGroupBox(title)
        layout = QVBoxLayout(group)

        # Input mode checkbox
        checkbox = QCheckBox("Use averages directly")
        checkbox.setChecked(True)  # Default to averages mode
        checkbox.stateChanged.connect(lambda state, t=team_type: self.toggle_input_mode(t, state))
        layout.addWidget(checkbox)

        # Store reference to checkbox
        setattr(self, f"{team_type}_checkbox", checkbox)

        # Averages input section
        avg_widget = QWidget()
        avg_layout = QGridLayout(avg_widget)
        avg_layout.setContentsMargins(0, 5, 0, 5)

        avg_layout.addWidget(QLabel("Goals scored per game:"), 0, 0)
        goals_for_edit = QLineEdit()
        # Use C locale for consistent decimal point handling
        validator = QDoubleValidator(0.0, 10.0, 2)
        validator.setLocale(QLocale(QLocale.C))
        goals_for_edit.setValidator(validator)
        goals_for_edit.setPlaceholderText("e.g., 1.89")
        avg_layout.addWidget(goals_for_edit, 0, 1)
        setattr(self, f"{team_type}_goals_for_edit", goals_for_edit)

        avg_layout.addWidget(QLabel("Goals conceded per game:"), 1, 0)
        goals_against_edit = QLineEdit()
        validator2 = QDoubleValidator(0.0, 10.0, 2)
        validator2.setLocale(QLocale(QLocale.C))
        goals_against_edit.setValidator(validator2)
        goals_against_edit.setPlaceholderText("e.g., 0.58")
        avg_layout.addWidget(goals_against_edit, 1, 1)
        setattr(self, f"{team_type}_goals_against_edit", goals_against_edit)

        layout.addWidget(avg_widget)
        setattr(self, f"{team_type}_avg_widget", avg_widget)

        # Totals input section
        totals_widget = QWidget()
        totals_layout = QGridLayout(totals_widget)
        totals_layout.setContentsMargins(0, 5, 0, 5)

        totals_layout.addWidget(QLabel("Games played:"), 0, 0)
        games_edit = QLineEdit()
        games_edit.setValidator(QIntValidator(1, 100))
        games_edit.setPlaceholderText("e.g., 19")
        totals_layout.addWidget(games_edit, 0, 1)
        setattr(self, f"{team_type}_games_edit", games_edit)

        totals_layout.addWidget(QLabel("Goals scored:"), 1, 0)
        scored_edit = QLineEdit()
        scored_edit.setValidator(QIntValidator(0, 200))
        scored_edit.setPlaceholderText("e.g., 36")
        totals_layout.addWidget(scored_edit, 1, 1)
        setattr(self, f"{team_type}_scored_edit", scored_edit)

        totals_layout.addWidget(QLabel("Goals conceded:"), 2, 0)
        conceded_edit = QLineEdit()
        conceded_edit.setValidator(QIntValidator(0, 200))
        conceded_edit.setPlaceholderText("e.g., 11")
        totals_layout.addWidget(conceded_edit, 2, 1)
        setattr(self, f"{team_type}_conceded_edit", conceded_edit)

        layout.addWidget(totals_widget)
        setattr(self, f"{team_type}_totals_widget", totals_widget)

        # Initially hide totals widget
        totals_widget.hide()

        return group

    def toggle_input_mode(self, team_type, state):
        """Toggle between averages and totals input mode."""
        use_averages = state == Qt.Checked

        avg_widget = getattr(self, f"{team_type}_avg_widget")
        totals_widget = getattr(self, f"{team_type}_totals_widget")

        if use_averages:
            avg_widget.show()
            totals_widget.hide()
        else:
            avg_widget.hide()
            totals_widget.show()

    def toggle_league_mode(self, state):
        """Toggle between simple and detailed league averages."""
        use_detailed = state == Qt.Checked

        if use_detailed:
            self.simple_league_widget.hide()
            self.detailed_league_widget.show()
        else:
            self.simple_league_widget.show()
            self.detailed_league_widget.hide()

    def get_input_data(self):
        """
        Collect and validate all input data.

        Returns:
            dict: Input data if valid, None if validation fails
        """
        try:
            # Check if using averages or totals
            use_home_averages = self.home_checkbox.isChecked()
            use_away_averages = self.away_checkbox.isChecked()
            use_detailed_league = self.detailed_league_checkbox.isChecked()

            data = {
                'use_averages': use_home_averages and use_away_averages,
                'use_detailed_league': use_detailed_league
            }

            # Get league data
            if use_detailed_league:
                league_home_for = self.get_float_value(self.league_home_for_edit, "Home teams goals for")
                league_away_for = self.get_float_value(self.league_away_for_edit, "Away teams goals for")

                if None in [league_home_for, league_away_for]:
                    return None

                data.update({
                    'league_home_for': league_home_for,
                    'league_away_for': league_away_for
                })
            else:
                league_avg = self.get_float_value(self.league_avg_edit, "League average")
                if league_avg is None:
                    return None
                data['league_avg'] = league_avg

            # Get home team data
            if use_home_averages:
                home_for = self.get_float_value(self.home_goals_for_edit, "Home goals for")
                home_against = self.get_float_value(self.home_goals_against_edit, "Home goals against")
                if home_for is None or home_against is None:
                    return None
                data.update({
                    'home_goals_for': home_for,
                    'home_goals_against': home_against
                })
            else:
                home_games = self.get_int_value(self.home_games_edit, "Home games")
                home_scored = self.get_int_value(self.home_scored_edit, "Home goals scored")
                home_conceded = self.get_int_value(self.home_conceded_edit, "Home goals conceded")
                if home_games is None or home_scored is None or home_conceded is None:
                    return None
                data.update({
                    'home_games': home_games,
                    'home_goals_scored': home_scored,
                    'home_goals_conceded': home_conceded
                })

            # Get away team data
            if use_away_averages:
                away_for = self.get_float_value(self.away_goals_for_edit, "Away goals for")
                away_against = self.get_float_value(self.away_goals_against_edit, "Away goals against")
                if away_for is None or away_against is None:
                    return None
                data.update({
                    'away_goals_for': away_for,
                    'away_goals_against': away_against
                })
            else:
                away_games = self.get_int_value(self.away_games_edit, "Away games")
                away_scored = self.get_int_value(self.away_scored_edit, "Away goals scored")
                away_conceded = self.get_int_value(self.away_conceded_edit, "Away goals conceded")
                if away_games is None or away_scored is None or away_conceded is None:
                    return None
                data.update({
                    'away_games': away_games,
                    'away_goals_scored': away_scored,
                    'away_goals_conceded': away_conceded
                })

            return data

        except Exception as e:
            QMessageBox.warning(self, "Input Error", f"Error processing input: {str(e)}")
            return None

    def get_float_value(self, line_edit, field_name):
        """Get and validate float value from line edit."""
        text = line_edit.text().strip()
        if not text:
            QMessageBox.warning(self, "Input Required", f"{field_name} is required.")
            line_edit.setFocus()
            return None

        # Replace comma with period for consistent parsing
        text = text.replace(',', '.')

        try:
            value = float(text)
            if value < 0:
                QMessageBox.warning(self, "Invalid Input", f"{field_name} must be positive.")
                line_edit.setFocus()
                return None
            return value
        except ValueError:
            QMessageBox.warning(self, "Invalid Input",
                                f"{field_name} must be a valid number (use . for decimal point).")
            line_edit.setFocus()
            return None

    def get_int_value(self, line_edit, field_name):
        """Get and validate integer value from line edit."""
        text = line_edit.text().strip()
        if not text:
            QMessageBox.warning(self, "Input Required", f"{field_name} is required.")
            line_edit.setFocus()
            return None

        try:
            value = int(text)
            if value < 0:
                QMessageBox.warning(self, "Invalid Input", f"{field_name} must be positive.")
                line_edit.setFocus()
                return None
            return value
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", f"{field_name} must be a valid whole number.")
            line_edit.setFocus()
            return None

    def on_calculate_clicked(self):
        """Handle calculate button click."""
        self.calculation_requested.emit()