from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QWidget,
                             QScrollArea, QSplitter, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

from .input_section import InputSection
from .results_table import ResultsTable
from models import PoissonCalculator


class MainWindow(QMainWindow):
    """
    Main application window for the Football Predictor.
    """

    def __init__(self):
        super().__init__()
        self.calculator = PoissonCalculator()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Football Match Probability Calculator")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)

        # Set application font
        font = QFont("Segoe UI", 10)
        self.setFont(font)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)

        # Create input section
        self.input_section = InputSection()
        self.input_section.calculation_requested.connect(self.calculate_probabilities)
        splitter.addWidget(self.input_section)

        # Create results section with scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(300)

        self.results_table = ResultsTable()
        scroll_area.setWidget(self.results_table)
        splitter.addWidget(scroll_area)

        # Set initial splitter sizes (input section smaller than results)
        splitter.setSizes([300, 400])

        # Set window properties
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 8px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 4px;
                padding: 4px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #0078d4;
            }
            QCheckBox {
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: white;
                alternate-background-color: #f8f8f8;
            }
            QHeaderView::section {
                background-color: #0078d4;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)

    def calculate_probabilities(self):
        """Calculate probabilities based on current input values."""
        try:
            # Get input data from input section
            input_data = self.input_section.get_input_data()

            if not input_data:
                return  # Input validation failed

            # Set data in calculator
            if input_data['use_detailed_league']:
                # Use detailed league averages methods
                if input_data['use_averages']:
                    self.calculator.set_team_averages_detailed(
                        input_data['home_goals_for'],
                        input_data['home_goals_against'],
                        input_data['away_goals_for'],
                        input_data['away_goals_against'],
                        input_data['league_home_for'],
                        input_data['league_away_for']
                    )
                else:
                    self.calculator.set_team_from_totals_detailed(
                        input_data['home_games'],
                        input_data['home_goals_scored'],
                        input_data['home_goals_conceded'],
                        input_data['away_games'],
                        input_data['away_goals_scored'],
                        input_data['away_goals_conceded'],
                        input_data['league_home_for'],
                        input_data['league_away_for']
                    )
            else:
                # Use simple league average methods
                if input_data['use_averages']:
                    self.calculator.set_team_averages(
                        input_data['home_goals_for'],
                        input_data['home_goals_against'],
                        input_data['away_goals_for'],
                        input_data['away_goals_against'],
                        input_data['league_avg']
                    )
                else:
                    self.calculator.set_team_from_totals(
                        input_data['home_games'],
                        input_data['home_goals_scored'],
                        input_data['home_goals_conceded'],
                        input_data['away_games'],
                        input_data['away_goals_scored'],
                        input_data['away_goals_conceded'],
                        input_data['league_avg']
                    )

            # Calculate strengths
            self.calculator.calculate_strengths()

            # Get results
            summary_info = self.calculator.get_summary_info()
            market_results = self.calculator.generate_market_analysis()

            # Update results display
            self.results_table.update_results(summary_info, market_results)

        except Exception as e:
            # Show error message
            QMessageBox.critical(
                self,
                "Calculation Error",
                f"An error occurred during calculation:\n\n{str(e)}"
            )