import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from gui import MainWindow


def main():
    """
    Main entry point for the Football Predictor application.
    """
    # Create the application
    app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("Football Predictor")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Football Analytics")

    # Enable high DPI scaling
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Start the event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()