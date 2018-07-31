import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class settings:
    chromedriver_path: str = os.path.join(BASE_DIR, 'assets', 'chromedriver')
    current_session_path: str = os.path.join(
        BASE_DIR, 'assets', 'current_session.txt')
    credentials_path: str = os.path.join(BASE_DIR, "assets", "credentials.txt")
    farmlist_path: str = os.path.join(BASE_DIR, "assets", "farmlist.txt")
    browser_speed: float = 1.0
