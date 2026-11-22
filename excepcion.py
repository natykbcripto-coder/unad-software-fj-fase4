"""Excepciones personalizadas de Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base: todas las demás heredan de ella."""


class ClienteInvalidoError(SoftwareFJError):
    """Datos del cliente inválidos (nombre, correo, teléfono)."""


class ParametroInvalidoError(SoftwareFJError):
    """Parámetro faltante o fuera de rango en un servicio."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio no está disponible para reservar."""


class ReservaInvalidaError(SoftwareFJError):
    """Operación no permitida sobre una reserva (estado incorrecto)."""


class CalculoInconsistenteError(SoftwareFJError):
    """El cálculo de costos produjo un resultado inconsistente."""
