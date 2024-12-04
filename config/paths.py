import os

CONFIG_DIR = str(os.path.dirname(os.path.abspath(__file__)))
ROOT_PATH = str(os.path.dirname(CONFIG_DIR))


def create_filepath(*args: str) -> str:
    """Создает абсолютный путь к файлу"""
    return os.path.join(ROOT_PATH, *args)
