import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from controllers import game_controller
from UI import main_gui

if __name__ == "__main__":
    print(f"sys.argv: {sys.argv}")

    # Check for --cli argument to launch console version
    if "--cli" in sys.argv:
        game_controller.start_game()
    else:
        # Launch Pygame graphical interface
        main_gui()
