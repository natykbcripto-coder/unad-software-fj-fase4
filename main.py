"""Simulación de 12 operaciones (válidas e inválidas). El programa nunca se detiene."""
from entidades import Cliente
from excepciones import SoftwareFJError
from logger_fj import log
from reserva import Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala

clientes, servicios, reservas = [], [], []  # listas internas (sin base de datos)


def operacion(numero: int, titulo: str, funcion):
    """Ejecuta una operación capturando cualquier error para que el sistema siga vivo."""
    print(f"\n[{numero}] {titulo}")
    try:
        resultado = funcion()
        print("   ✔", resultado)
        log.info(f"Operación {numero} OK: {titulo}")
    except SoftwareFJError as e:
        print("   ✘ Error controlado:", e)
        log.error(f"Operación {numero} falló: {titulo} -> {e}")
    except Exception as e:  # cualquier error inesperado también se registra
        print("   ✘ Error inesperado:", e)
        log.exception(f"Operación {numero} error inesperado: {e}")


def registrar(lista, objeto):
    lista.append(objeto)
    return objeto.describir()


def main():
    log.info("===== Inicio de la simulación =====")
    operacion(1, "Cliente válido", lambda: registrar(clientes, Cliente(1, "Ana Pérez", "ana@mail.com", "3001234567")))
    operacion(2, "Cliente con correo inválido", lambda: registrar(clientes, Cliente(2, "Luis Gómez", "luis#mail", "3001234567")))
    operacion(3, "Cliente con teléfono inválido", lambda: registrar(clientes, Cliente(3, "Marta", "marta@mail.com", "123")))
    operacion(4, "Cliente válido", lambda: registrar(clientes, Cliente(4, "Carlos Ruiz", "carlos@mail.com", "3109876543")))
    operacion(5, "Sala válida", lambda: registrar(servicios, ReservaSala(1, "Sala Norte", 50000, 25)))
    operacion(6, "Equipo válido", lambda: registrar(servicios, AlquilerEquipo(2, "Portátil Pro", 12000, "Computador")))
    operacion(7, "Asesoría con nivel inválido", lambda: registrar(servicios, AsesoriaEspecializada(3, "Asesoría Cloud", 80000, "maestro")))
    operacion(8, "Asesoría válida", lambda: registrar(servicios, AsesoriaEspecializada(3, "Asesoría Cloud", 80000, "senior")))
    operacion(9, "Reserva exitosa (sala 3h)", lambda: _reservar(1, 0, 0, 3))
    operacion(10, "Reserva fallida (sala 20h, excede límite)", lambda: _reservar(2, 0, 0, 20))
    operacion(11, "Reserva de servicio no disponible", lambda: _reservar_no_disponible())
    operacion(12, "Confirmar dos veces la misma reserva", lambda: _doble_confirmacion())
    operacion(13, "Costos con variantes (sobrecarga)", lambda: _variantes())
    operacion(14, "Reserva con cliente inexistente", lambda: Reserva(9, None, servicios[0], 2))
    print("\nSimulación terminada. Revise logs/eventos.log")
    log.info("===== Fin de la simulación =====")


def _reservar(id_reserva, i_cliente, i_servicio, horas):
    r = Reserva(id_reserva, clientes[i_cliente], servicios[i_servicio], horas)
    reservas.append(r)
    return r.procesar()


def _reservar_no_disponible():
    servicios[1].disponible = False
    r = Reserva(3, clientes[1], servicios[1], 2)
    resultado = r.procesar()
    servicios[1].disponible = True
    return resultado


def _doble_confirmacion():
    r = Reserva(4, clientes[0], servicios[2], 2)
    r.confirmar()
    r.confirmar()  # lanza ReservaInvalidaError (ya está confirmada)


def _variantes():
    s = servicios[2]
    return (f"base+IVA=${s.calcular_costo(2):,.2f} | con 10% dto=${s.calcular_costo(2, descuento=0.1):,.2f} "
            f"| sin IVA=${s.calcular_costo(2, 0.0, 0.0):,.2f}")


if __name__ == "__main__":
    main()
