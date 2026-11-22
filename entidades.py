"""Clase abstracta Entidad y clase Cliente (con encapsulación y validaciones)."""
import re
from abc import ABC, abstractmethod

from excepciones import ClienteInvalidoError
from logger_fj import log


class Entidad(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    def __init__(self, identificador: int):
        self._identificador = identificador  # atributo protegido (encapsulado)

    @property
    def identificador(self) -> int:
        return self._identificador

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad debe describirse a sí misma (polimorfismo)."""


class Cliente(Entidad):
    """Cliente con datos personales privados y validados."""

    def __init__(self, identificador: int, nombre: str, correo: str, telefono: str):
        super().__init__(identificador)
        # Los setters validan; si algo es inválido lanzan ClienteInvalidoError
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        log.info(f"Cliente creado: {self._nombre} (id={identificador})")

    # ---- nombre ----
    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()

    # ---- correo ----
    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not isinstance(valor, str) or not re.fullmatch(r"[\w.+-]+@[\w-]+\.[\w.-]+", valor):
            raise ClienteInvalidoError(f"Correo inválido: {valor!r}")
        self._correo = valor

    # ---- teléfono ----
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not isinstance(valor, str) or not valor.isdigit() or len(valor) != 10:
            raise ClienteInvalidoError(f"Teléfono inválido (deben ser 10 dígitos): {valor!r}")
        self._telefono = valor

    def describir(self) -> str:
        return f"Cliente #{self.identificador}: {self._nombre} <{self._correo}>"
