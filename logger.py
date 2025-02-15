import logging

logging.basicConfig(
    filename="premiere.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


def info(event):
    logging.info(f"Evento: {event}")


def error(event):
    logging.error(f"Evento: {event}")


def warning(event):
    logging.warning(f"Evento: {event}")


def debug(event):
    logging.debug(f"Evento: {event}")


def critical(event):
    logging.critical(f"Evento: {event}")


def exception(event):
    logging.exception(f"Evento: {event}")
