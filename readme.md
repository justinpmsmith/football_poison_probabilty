# Football Match Probability Calculator

A desktop application built with PyQt5 that calculates football match probabilities using Poisson distribution. The application analyzes team strengths and generates betting odds for Over/Under markets.

## Features

- **Team Analysis**: Calculate attacking and defensive strengths relative to league averages
- **Multiple Input Modes**: Enter team data as averages or calculate from totals (games played, goals scored/conceded)
- **Advanced League Modeling**: Choose between simple league averages or detailed home/away league statistics for more accurate calculations
- **Market Analysis**: Generate probabilities and odds for Over/Under 0.5, 1.5, 2.5, and 3.5 goals markets
- **Professional Interface**: Clean, intuitive GUI with input validation and real-time results

## Mathematical Approach

The application uses Poisson distribution to model goal-scoring patterns:

1. **Team Strength Calculation**: Compares team performance against league averages
2. **Goal Expectancy**: Calculates expected goals for each team based on their strengths
3. **Probability Matrix**: Generates probabilities for all possible scorelines
4. **Market Odds**: Converts probabilities to betting odds with configurable margins

### Simple vs Detailed League Modeling

- **Simple Mode**: Uses overall league average goals per game
- **Detailed Mode**: Uses separate home/away team averages for more accurate strength calculations

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Setup

1. **Clone the repository:**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python main.py
   ```

## Usage

### Basic Usage

1. **Enter Team Data**: Input goals scored/conceded averages or total statistics
2. **Choose League Mode**: Select simple or detailed league averaging
3. **Calculate**: Click "Calculate Probabilities" to generate results
4. **Analyze Results**: View team strengths, expected goals, and market odds

### Input Options

**Team Data (for each team):**
- ☑️ **Use averages directly**: Enter goals per game averages
- ☐ **Calculate from totals**: Enter games played, total goals scored/conceded

**League Information:**
- ☐ **Simple**: Single league average goals per game
- ☑️ **Detailed**: Separate home/away team averages (more accurate)

### Example Calculation

**Team Data:**
- Home Team: 1.89 goals for, 0.58 goals against per game
- Away Team: 1.12 goals for, 1.68 goals against per game

**League Averages (Detailed):**
- Home teams average: 1.65 goals for
- Away teams average: 1.10 goals for

**Results:**
- Expected goals, team strengths, and Over/Under market probabilities with betting odds

## Project Structure

```
football_predictor/
├── main.py                    # Application entry point
├── models/
│   ├── __init__.py
│   └── poisson_calculator.py  # Core calculation logic
├── gui/
│   ├── __init__.py
│   ├── main_window.py         # Main application window
│   ├── input_section.py       # Input fields and validation
│   └── results_table.py       # Results display
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## Requirements

- **PyQt5**: GUI framework
- **pandas**: Data manipulation and analysis
- **numpy**: Mathematical computations

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/improvement`)
6. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Based on Poisson distribution modeling techniques commonly used in football analytics
- Inspired by statistical approaches to sports betting and value identification

## Disclaimer

This application is for educational and analytical purposes only. Always gamble responsibly and within your means.