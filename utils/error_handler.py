import os

ENV = os.getenv("ENV", "PRODUCTION")  # Default a "PRODUCTION"

def get_error_message(base_message, error):
    """Genera un mensaje de error detallado solo en entorno de desarrollo."""
    error_details = getattr(error, "orig", "No details available")  # Evita errores si `orig` no existe
    return f"{base_message} Details: {error_details}" if ENV == "DEVELOPMENT" else base_message