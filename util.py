import re
import os
import sys
import platform


PLANTILLA = re.compile(r"\[(\d+)\]")


def parsear_plantilla(s: str) -> str:
    def reemplazar(instancia):
        num_spaces = int(instancia.group(1))
        return " " * num_spaces

    return PLANTILLA.sub(reemplazar, s)


def tic_imprimir(plantilla, **kwargs):
    print(parsear_plantilla(plantilla), **kwargs)


def tic_entrada(s=None, inmediato=True, imprimir=False):
    if s is not None:
        tic_imprimir(s, end="", flush=True)
    if not inmediato:
        return input()

    if os.name == "nt":  # para Windows
        import msvcrt

        car = msvcrt.getch().decode()
    else:  # para sistemas Unix-like
        import termios
        import tty
        from select import select

        fd = sys.stdin.fileno()
        atributos_viejos = termios.tcgetattr(fd)
        car = None
        try:
            tty.setraw(sys.stdin.fileno())
            i, _, _ = select([sys.stdin.fileno()], [], [], None)
            if i:
                car = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, atributos_viejos)

    if imprimir:
        print(car)
        return car
    print()
    return car


def entrada_ciclo(
    funcion_entrada=input,
    validador=lambda _: True,
    transformador=lambda x: x,
    en_invalido=lambda _: None,
    excepcion_manejo=Exception,
    en_error=lambda _: None,
):
    """
    Un bucle generalizado para la validación de entradas de usuario.

    Parámetros:
    funcion_entrada (function): Una función para obtener la entrada del usuario.
    validador (function): Una función para validar la entrada. Debe
        devolver True si la entrada es válida.
    transformador (function): Una función para transformar la entrada
        antes de la validación.
    en_invalido (function): Una función para ejecutar cuando la
        entrada no es válida, recibe la entrada transformada.
    excepcion_manejo (Exception): Una excepción a manejar.
    en_error (function): Una función a ejecutar cuando se captura una
        excepción, recibe el objeto de excepción.

    Devuelve:
    La entrada de usuario validada y posiblemente transformada.
    """
    while True:
        try:
            recibido = funcion_entrada()
            recibido = transformador(recibido)
            if validador(recibido):
                return recibido
            else:
                en_invalido(recibido)
        except Exception as e:
            if (
                isinstance(e, KeyboardInterrupt)
                and excepcion_manejo is not KeyboardInterrupt
            ):
                raise

            if isinstance(e, excepcion_manejo):
                en_error(e)


def entrada_numero_ciclo(
    funcion_entrada=input,
    validador=lambda _: True,
    transformador=int,
    en_invalido=lambda _: None,
    excepcion_manejo=ValueError,
    en_error=lambda _: None,
):
    return entrada_ciclo(
        funcion_entrada=funcion_entrada,
        validador=validador,
        transformador=transformador,
        en_invalido=en_invalido,
        excepcion_manejo=excepcion_manejo,
        en_error=en_error,
    )


def iee_ciclo(mensaje):
    def f(_):
        imprimir_error_esperar(mensaje)

    return f


def ticeni_ciclo(mensaje):
    def f():
        return tic_entrada(mensaje, inmediato=False)

    return f


def tic_entrada_ciclo(
    entrada_texto="Ingresar un valor.",
    validador=lambda _: True,
    transformador=lambda x: x,
    en_invalido="Valor inválido.",
    excepcion_manejo=Exception,
    en_error=None,
):
    if en_error is None:
        en_error = en_invalido

    return entrada_ciclo(
        funcion_entrada=ticeni_ciclo(entrada_texto),
        validador=validador,
        transformador=transformador,
        en_invalido=iee_ciclo(en_invalido),
        excepcion_manejo=excepcion_manejo,
        en_error=iee_ciclo(en_error),
    )


def tic_entrada_numero_ciclo_inmediato(
    entrada_texto="Ingresar un número.",
    validador=lambda _: True,
    transformador=int,
    en_invalido="Número inválido.",
    excepcion_manejo=ValueError,
    en_error=None,
):
    if en_error is None:
        en_error = en_invalido

    return entrada_ciclo(
        funcion_entrada=lambda: tic_entrada(entrada_texto),
        validador=validador,
        transformador=transformador,
        en_invalido=iee_ciclo(en_invalido),
        excepcion_manejo=excepcion_manejo,
        en_error=iee_ciclo(en_error),
    )


def tic_entrada_numero_ciclo(
    entrada_texto="Ingresar un número.",
    validador=lambda _: True,
    transformador=int,
    en_invalido="Número inválido.",
    excepcion_manejo=ValueError,
    en_error=None,
):
    if en_error is None:
        en_error = en_invalido

    return entrada_ciclo(
        funcion_entrada=ticeni_ciclo(entrada_texto),
        validador=validador,
        transformador=transformador,
        en_invalido=iee_ciclo(en_invalido),
        excepcion_manejo=excepcion_manejo,
        en_error=iee_ciclo(en_error),
    )


def imprimir_encabezado(s):
    tic_imprimir(s)
    tic_imprimir("=" * len(s) + "\n")


def limpiar_pantalla():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def mensaje_error(s):
    return f"*** Error: {s}\n    Presionar <Enter> para continuar."


def imprimir_error_esperar(s):
    tic_entrada(mensaje_error(s))


def esperar_continuar():
    tic_entrada("Presionar <ENTER> para continuar.")


def es_si(s):
    return s.lower() in ("s", "si", "sí", "y", "yes")


def es_no(s):
    return s.lower() in ("n", "no")


def es_respuesta(s):
    return es_si(s) or es_no(s)
