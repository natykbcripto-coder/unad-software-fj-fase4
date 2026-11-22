"""Clase Reserva: integra cliente, servicio, duración y estado."""
from entidades import Cliente, Entidad
from excepciones import (CalculoInconsistenteError, ParametroInvalidoError, ReservaInvalidaError,
                         ServicioNoDisponibleError, SoftwareFJError)
from logger_fj import log
from servicios import Servicio


class Reserva(Entidad):
    ESTADOS = ("pendiente", "confirmada", "cancelada")

    def __init__(self, identificador: int, cliente: Cliente, servicio: Servicio, horas: float):
        super().__init__(identificador)
        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Cliente y un Servicio válidos.")
        servicio.validar_parametros(horas)  # falla pronto si la duración no sirve
        self._cliente, self._servicio, self._horas = cliente, servicio, horas
        self._estado = "pendiente"
        log.info(f"Reserva #{identificador} creada (pendiente) para {cliente.nombre}")

    @property
    def estado(self) -> str:
        return self._estado

    def confirmar(self) -> float:
        """Confirma la reserva y devuelve el costo. Usa try/except/else/finally."""
        try:
            if self._estado != "pendiente":
                raise ReservaInvalidaError(f"No se puede confirmar una reserva {self._estado}.")
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(f"'{self._servicio.nombre}' no está disponible.")
            costo = self._servicio.calcular_costo(self._horas)
        except (ParametroInvalidoError, CalculoInconsistenteError) as e:
            # Encadenamiento de excepciones: conserva la causa original con 'from e'
            raise ReservaInvalidaError("No fue posible calcular la reserva.") from e
        except SoftwareFJError as e:
            log.error(f"Reserva #{self.identificador}: {e}")
            raise
        else:  # solo se ejecuta si NO hubo excepción
            self._estado = "confirmada"
            log.info(f"Reserva #{self.identificador} confirmada. Costo ${costo:,.2f}")
            return costo
        finally:  # se ejecuta siempre
            log.info(f"Intento de confirmación de reserva #{self.identificador} finalizado")

    def cancelar(self) -> None:
        if self._estado == "cancelada":
            raise ReservaInvalidaError("La reserva ya estaba cancelada.")
        self._estado = "cancelada"
        log.info(f"Reserva #{self.identificador} cancelada")

    def procesar(self) -> str:
        """Confirma y devuelve un resumen; nunca deja caer la aplicación."""
        try:
            costo = self.confirmar()
            return f"Reserva #{self.identificador} OK: {self._servicio.describir()} | {self._horas}h | ${costo:,.2f}"
        except SoftwareFJError as e:
            causa = f" (causa: {e.__cause__})" if e.__cause__ else ""
            log.error(f"procesar() reserva #{self.identificador}: {e}{causa}")
            return f"Reserva #{self.identificador} FALLÓ: {e}{causa}"

    def describir(self) -> str:
        return f"Reserva #{self.identificador} [{self._estado}] {self._cliente.nombre} -> {self._servicio.nombre}"
