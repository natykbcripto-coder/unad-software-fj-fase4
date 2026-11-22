"""Clase abstracta Servicio y tres servicios especializados (herencia + polimorfismo)."""
from abc import abstractmethod

from entidades import Entidad
from excepciones import CalculoInconsistenteError, ParametroInvalidoError
from logger_fj import log

IVA = 0.19  # impuesto por defecto


class Servicio(Entidad):
    """Servicio genérico: define el contrato que deben cumplir los hijos."""

    def __init__(self, identificador: int, nombre: str, tarifa_hora: float, disponible: bool = True):
        super().__init__(identificador)
        if not nombre or not isinstance(nombre, str):
            raise ParametroInvalidoError("El servicio requiere un nombre.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ParametroInvalidoError(f"Tarifa por hora inválida: {tarifa_hora!r}")
        self._nombre = nombre
        self._tarifa_hora = float(tarifa_hora)
        self.disponible = disponible

    @property
    def nombre(self) -> str:
        return self._nombre

    def validar_parametros(self, horas: float) -> None:
        """Validación común; los hijos la extienden con super()."""
        if not isinstance(horas, (int, float)) or horas <= 0:
            raise ParametroInvalidoError(f"Duración inválida: {horas!r}")

    @abstractmethod
    def calcular_costo_base(self, horas: float) -> float:
        """Costo sin impuestos ni descuentos (cada hijo lo sobrescribe)."""

    def calcular_costo(self, horas: float, descuento: float = 0.0, impuesto: float = IVA) -> float:
        """
        'Sobrecarga' por parámetros opcionales (Python no tiene sobrecarga real):
          calcular_costo(2)                   -> con IVA
          calcular_costo(2, descuento=0.1)    -> con 10% de descuento
          calcular_costo(2, 0.1, 0.0)         -> con descuento y sin impuesto
        """
        self.validar_parametros(horas)
        if not 0 <= descuento < 1:
            raise ParametroInvalidoError(f"Descuento fuera de rango: {descuento}")
        if impuesto < 0:
            raise ParametroInvalidoError(f"Impuesto inválido: {impuesto}")
        total = self.calcular_costo_base(horas) * (1 - descuento) * (1 + impuesto)
        if total <= 0:
            raise CalculoInconsistenteError(f"Costo no válido: {total}")
        return round(total, 2)


class ReservaSala(Servicio):
    """Reserva de salas: el costo depende de la capacidad."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad: int, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ParametroInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self._capacidad = capacidad

    def validar_parametros(self, horas):
        super().validar_parametros(horas)
        if horas > 12:
            raise ParametroInvalidoError("Una sala no se puede reservar más de 12 horas.")

    def calcular_costo_base(self, horas):
        recargo = 1.2 if self._capacidad > 20 else 1.0  # salas grandes cuestan 20% más
        return self._tarifa_hora * horas * recargo

    def describir(self):
        return f"Sala '{self._nombre}' (capacidad {self._capacidad}) - ${self._tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos: se paga una tarifa fija de entrega además de las horas."""

    def __init__(self, identificador, nombre, tarifa_hora, tipo_equipo: str, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not tipo_equipo:
            raise ParametroInvalidoError("Debe indicar el tipo de equipo.")
        self._tipo_equipo = tipo_equipo

    def calcular_costo_base(self, horas):
        return self._tarifa_hora * horas + 15000  # 15.000 por entrega/recogida

    def describir(self):
        return f"Equipo '{self._nombre}' ({self._tipo_equipo}) - ${self._tarifa_hora:,.0f}/h + entrega"


class AsesoriaEspecializada(Servicio):
    """Asesorías: el nivel del asesor multiplica la tarifa."""

    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, identificador, nombre, tarifa_hora, nivel: str, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if nivel not in self.NIVELES:
            raise ParametroInvalidoError(f"Nivel de asesor inválido: {nivel!r}")
        self._nivel = nivel

    def validar_parametros(self, horas):
        super().validar_parametros(horas)
        if horas < 1:
            raise ParametroInvalidoError("La asesoría dura mínimo 1 hora.")

    def calcular_costo_base(self, horas):
        return self._tarifa_hora * horas * self.NIVELES[self._nivel]

    def describir(self):
        return f"Asesoría '{self._nombre}' nivel {self._nivel} - ${self._tarifa_hora:,.0f}/h"
