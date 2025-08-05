from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from models.poisson_calculator import PoissonCalculator


def get_float_input(prompt, allow_empty=False):
    """
    Get float input from user with validation.

    Args:
        prompt (str): Input prompt message
        allow_empty (bool): Whether to allow empty input

    Returns:
        float or None: The input value or None if empty and allowed
    """
    while True:
        try:
            user_input = input(prompt).strip()

            if allow_empty and user_input == "":
                return None

            if user_input == "":
                print("Input cannot be empty. Please enter a valid number.")
                continue

            value = float(user_input)
            if value < 0:
                print("Please enter a positive number.")
                continue

            return value

        except ValueError:
            if allow_empty:
                print("Invalid input. Press Enter for empty or enter a valid number.")
            else:
                print("Invalid input. Please enter a valid number.")


def get_int_input(prompt):
    """
    Get integer input from user with validation.

    Args:
        prompt (str): Input prompt message

    Returns:
        int: The input value
    """
    while True:
        try:
            user_input = input(prompt).strip()

            if user_input == "":
                print("Input cannot be empty. Please enter a valid number.")
                continue

            value = int(user_input)
            if value < 0:
                print("Please enter a positive number.")
                continue

            return value

        except ValueError:
            print("Invalid input. Please enter a valid whole number.")


def get_team_data(team_name, location):
    """
    Get team data from user - either averages or totals to calculate averages.

    Args:
        team_name (str): Name of the team
        location (str): 'home' or 'away'

    Returns:
        tuple: (goals_for_avg, goals_against_avg)
    """
    console = Console()

    # Try to get averages first
    console.print(f"\n[bold blue]📊 {team_name} ({location.title()}) Statistics[/bold blue]")

    goals_for_avg = get_float_input(
        f"Average goals scored {location} per game (press Enter to input totals instead): ",
        allow_empty=True
    )

    if goals_for_avg is None:
        # Get totals instead
        console.print(f"[yellow]📝 Enter total statistics for {team_name} {location} games:[/yellow]")

        games_played = get_int_input(f"Number of {location} games played: ")
        total_goals_scored = get_int_input(f"Total goals scored in {location} games: ")
        total_goals_conceded = get_int_input(f"Total goals conceded in {location} games: ")

        goals_for_avg = total_goals_scored / games_played
        goals_against_avg = total_goals_conceded / games_played

        console.print(
            f"[green]✓ Calculated averages: {goals_for_avg:.2f} scored, {goals_against_avg:.2f} conceded per game[/green]")

    else:
        # Get goals against average
        goals_against_avg = get_float_input(f"Average goals conceded {location} per game: ")

    return goals_for_avg, goals_against_avg


def display_results(calculator, console):
    """
    Display the calculation results using Rich formatting.

    Args:
        calculator (PoissonCalculator): The calculator instance with results
        console (Console): Rich console instance
    """
    # Display summary information
    summary = calculator.get_summary_info()

    console.print("\n[bold green]🎯 Match Analysis Summary[/bold green]")
    summary_table = Table(show_header=True, header_style="bold magenta")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="yellow")

    for metric, value in summary.items():
        summary_table.add_row(metric, value)

    console.print(summary_table)

    # Generate and display market results
    results_df = calculator.generate_market_analysis()

    console.print("\n[bold green]📈 Over/Under Markets Analysis[/bold green]")

    # Create Rich table
    results_table = Table(show_header=True, header_style="bold magenta")
    results_table.add_column("Market", style="cyan", width=12)
    results_table.add_column("Probability", style="green", justify="center")
    results_table.add_column("Fair Odds", style="blue", justify="center")
    results_table.add_column("Odds + 3% Margin", style="yellow", justify="center")
    results_table.add_column("Over Probability", style="green", justify="center")
    results_table.add_column("Over Odds + Margin", style="yellow", justify="center")

    # Add rows to table
    for _, row in results_df.iterrows():
        results_table.add_row(
            row['Market'],
            row['Probability'],
            row['Fair Odds'],
            row['Odds + Margin'],
            row['Opposite Probability'],
            row['Opposite Odds + Margin']
        )

    console.print(results_table)

    # Add explanation panel
    explanation = """
    [bold]How to read this table:[/bold]
    • [cyan]Probability[/cyan]: Chance of the Under outcome occurring (calculated directly)
    • [blue]Fair Odds[/blue]: True Under odds without bookmaker margin
    • [yellow]Odds + 3% Margin[/yellow]: Under odds with typical bookmaker margin added
    • [green]Over Probability[/green]: Chance of the Over outcome occurring (1 - Under)
    • [yellow]Over Odds + Margin[/yellow]: Over odds with margin applied

    [bold]Value Betting:[/bold] Look for bookmaker odds higher than your calculated odds + margin
    """

    console.print(Panel(explanation, title="[bold blue]📚 Guide[/bold blue]", border_style="blue"))


def main():
    """
    Main function to run the Poisson football prediction calculator.
    """
    console = Console()

    # Display welcome message
    console.print(Panel(
        "[bold green]⚽ Football Match Probability Calculator[/bold green]\n"
        "Using Poisson Distribution for Over/Under Markets",
        title="[bold blue]Welcome[/bold blue]",
        border_style="green"
    ))

    try:
        # Get team data
        console.print("\n[bold yellow]🏠 HOME TEAM DATA[/bold yellow]")
        home_goals_for, home_goals_against = get_team_data("Home Team", "home")

        console.print("\n[bold yellow]✈️  AWAY TEAM DATA[/bold yellow]")
        away_goals_for, away_goals_against = get_team_data("Away Team", "away")

        # Get league average
        console.print("\n[bold yellow]🏆 LEAGUE DATA[/bold yellow]")
        league_avg = get_float_input("League average goals per game: ")

        # Create calculator and set data
        calculator = PoissonCalculator()
        calculator.set_team_averages(
            home_goals_for, home_goals_against,
            away_goals_for, away_goals_against,
            league_avg
        )

        # Calculate strengths (required before any analysis)
        calculator.calculate_strengths()

        # Display results
        display_results(calculator, console)

        # Ask if user wants to run another calculation
        console.print("\n[bold cyan]Would you like to analyze another match? (y/n):[/bold cyan]", end=" ")
        if input().lower().strip() == 'y':
            console.print("\n" + "=" * 60 + "\n")
            main()  # Recursive call for another calculation

    except KeyboardInterrupt:
        console.print("\n\n[yellow]👋 Thanks for using the calculator![/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]❌ An error occurred: {str(e)}[/bold red]")


if __name__ == "__main__":
    main()