"""Configuración del archivo de logs (eventos y errores)."""
import logging
import os

RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs", "eventos.log")


def obtener_logger() -> logging.Logger:
    """Crea (una sola vez) el logger que escribe en logs/eventos.log."""
    logger = logging.getLogger("software_fj")
    if not logger.handlers:  # evita duplicar handlers si se llama varias veces
        os.makedirs(os.path.dirname(RUTA_LOG), exist_ok=True)
        logger.setLevel(logging.INFO)
        manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")
        manejador.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
        logger.addHandler(manejador)
    return logger


log = obtener_logger()
