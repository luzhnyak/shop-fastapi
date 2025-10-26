import logging
import sys

# Отримуємо або створюємо logger
logger = logging.getLogger("app")

# Налаштовуємо logger тільки якщо він ще не налаштований
if not logger.hasHandlers():
    # Налаштовуємо рівень логування
    logger.setLevel(logging.INFO)

    # Налаштовуємо формат логів
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Створюємо і додаємо handler для консолі
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Запобігаємо передачі логів до root logger (щоб уникнути дублювання)
    logger.propagate = False
