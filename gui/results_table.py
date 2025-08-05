from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QTableWidgetItem, QLabel, QGroupBox, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ResultsTable(QWidget):
    """
    Widget for displaying calculation results.
    """

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Initialize the user interface."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        # Summary section
        self.summary_group = QGroupBox("Match Analysis Summary")
        summary_layout = QVBoxLayout(self.summary_group)

        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(2)
        self.summary_table.setHorizontalHeaderLabels(["Metric", "Value"])
        self.summary_table.horizontalHeader().setStretchLastSection(True)
        self.summary_table.verticalHeader().setVisible(False)
        self.summary_table.setAlternatingRowColors(True)
        self.summary_table.setMaximumHeight(250)

        summary_layout.addWidget(self.summary_table)
        main_layout.addWidget(self.summary_group)

        # Market analysis section
        self.market_group = QGroupBox("Over/Under Markets Analysis")
        market_layout = QVBoxLayout(self.market_group)

        self.market_table = QTableWidget()
        self.market_table.setColumnCount(6)
        self.market_table.setHorizontalHeaderLabels([
            "Market", "Probability", "Fair Odds", "Odds + 3% Margin",
            "Over Probability", "Over Odds + Margin"
        ])

        # Set table properties
        self.market_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.market_table.verticalHeader().setVisible(False)
        self.market_table.setAlternatingRowColors(True)
        self.market_table.setSelectionBehavior(QTableWidget.SelectRows)

        market_layout.addWidget(self.market_table)

        # Add explanation label
        explanation = QLabel(
            "• Probability: Chance of Under outcome occurring (calculated directly)\n"
            "• Fair Odds: True Under odds without bookmaker margin\n"
            "• Odds + Margin: Under odds with 3% bookmaker margin\n"
            "• Over Probability: Chance of Over outcome (1 - Under)\n"
            "• Over Odds + Margin: Over odds with margin applied\n\n"
            "Value Betting: Look for bookmaker odds higher than calculated odds + margin"
        )
        explanation.setWordWrap(True)
        explanation.setStyleSheet("""
            QLabel {
                background-color: #e8f4fd;
                border: 1px solid #b3d9ff;
                border-radius: 4px;
                padding: 10px;
                color: #003d6b;
                font-size: 9pt;
            }
        """)
        market_layout.addWidget(explanation)

        main_layout.addWidget(self.market_group)

        # Initially hide both sections
        self.summary_group.hide()
        self.market_group.hide()

        # Add placeholder text
        self.placeholder_label = QLabel("Enter match data and click 'Calculate Probabilities' to see results.")
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setStyleSheet("""
            QLabel {
                color: #666666;
                font-size: 14pt;
                font-style: italic;
                padding: 50px;
            }
        """)
        main_layout.addWidget(self.placeholder_label)

    def update_results(self, summary_info, market_results):
        """
        Update the results display with new calculation data.

        Args:
            summary_info (dict): Summary statistics
            market_results (pd.DataFrame): Market analysis results
        """
        # Hide placeholder and show results
        self.placeholder_label.hide()
        self.summary_group.show()
        self.market_group.show()

        # Update summary table
        self.update_summary_table(summary_info)

        # Update market table
        self.update_market_table(market_results)

    def update_summary_table(self, summary_info):
        """Update the summary statistics table."""
        self.summary_table.setRowCount(len(summary_info))

        for row, (metric, value) in enumerate(summary_info.items()):
            # Metric name
            metric_item = QTableWidgetItem(metric)
            metric_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self.summary_table.setItem(row, 0, metric_item)

            # Value
            value_item = QTableWidgetItem(str(value))
            value_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            value_item.setTextAlignment(Qt.AlignCenter)

            # Highlight important values
            if "Expected Goals" in metric:
                font = QFont()
                font.setBold(True)
                value_item.setFont(font)

            self.summary_table.setItem(row, 1, value_item)

        # Resize columns to content
        self.summary_table.resizeColumnsToContents()

    def update_market_table(self, market_results):
        """Update the market analysis table."""
        self.market_table.setRowCount(len(market_results))

        for row in range(len(market_results)):
            data_row = market_results.iloc[row]

            for col, column_name in enumerate(market_results.columns):
                item = QTableWidgetItem(str(data_row[column_name]))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                item.setTextAlignment(Qt.AlignCenter)

                # Style the market column differently
                if column_name == "Market":
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                self.market_table.setItem(row, col, item)

        # Resize columns to content
        self.market_table.resizeColumnsToContents()