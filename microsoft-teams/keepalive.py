import pyautogui
import time
import random
import logging

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

def random_move():
    # Get screen resolution
    screen_width, screen_height = pyautogui.size()

    while True:
        # Generate a random position within the screen boundaries
        x = random.randint(0, screen_width - 1)
        y = random.randint(0, screen_height - 1)

        # Move the mouse to the random position
        pyautogui.moveTo(x, y, duration=0.1)

        # Log the new position of the mouse
        logging.info(f"Mouse moved to position: ({x}, {y})")

        # Wait for x seconds
        time.sleep(60)


if __name__ == "__main__":
    try:
        random_move()
    except KeyboardInterrupt:
        # Handle interruption gracefully
        logging.info("Program terminated. Have a great day! ;-)")
