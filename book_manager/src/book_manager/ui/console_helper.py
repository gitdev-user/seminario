import os
import re
import subprocess
from datetime import date


def mostrar_separador():
    """Imprime una línea de 60 guiones para separar secciones de la consola."""
    print("-" * 60)

def limpiar_pantalla():
    """Limpia la consola usando el comando correspondiente al sistema operativo."""
    if os.name == "nt":
        subprocess.run("cls", shell=True)
    else:
        subprocess.run(["clear"])

def mostrar_menu(titulo: str, opciones: dict[str, tuple[str, callable]]) -> str:
    """Muestra las opciones de un menú y solicita una selección.

    Args:
        titulo: Texto que encabeza el menú.
        opciones: Mapa de claves a tuplas con el texto y la acción asociada.
            La acción puede ser None para indicar una salida del menú.

    Returns:
        Opción ingresada sin espacios al inicio ni al final. Esta función no
        valida la selección ni ejecuta la acción asociada.
    """
    print(f"\n--- {titulo} ---")

    for numero, (texto, _) in opciones.items():
        print(f"{numero}. {texto}")

    return input("\nSeleccione una opción: ").strip()

def input_entero(prompt: str, valor_actual=None) -> int:
    """Solicita un entero y repite la entrada si no puede convertirlo.

    Args:
        prompt: Mensaje que acompaña la solicitud de entrada.
        valor_actual: Valor que se conserva al presionar Enter, si se proporciona.

    Returns:
        Entero ingresado o valor_actual si la entrada está vacía.
    """
    while True:
        try:
            valor = input(prompt).strip()
            if not valor and valor_actual is not None:
                return valor_actual
            return int(valor)
        except ValueError:
            print("Por favor, ingrese un número entero válido.")

def input_decimal(prompt: str, valor_actual=None) -> float:
    """Solicita un número usando punto decimal y repite entradas no numéricas.

    Args:
        prompt: Mensaje que acompaña la solicitud de entrada.
        valor_actual: Valor que se conserva al presionar Enter, si se proporciona.

    Returns:
        Número convertido a float o valor_actual sin convertirlo si la entrada
        está vacía. No valida límites ni descarta valores infinitos o NaN.
    """
    while True:
        try:
            valor = input(prompt).strip()
            if not valor and valor_actual is not None:
                return valor_actual
            return float(valor)
        except ValueError:
            print("Por favor, ingrese un número decimal válido.")

def input_fecha(prompt: str, valor_actual=None) -> str:
    """Solicita una fecha existente en formato AAAA-MM-DD y repite entradas inválidas.

    Args:
        prompt: Mensaje que acompaña la solicitud de entrada.
        valor_actual: Fecha que se conserva al presionar Enter, si se proporciona.
            Debe ser una fecha válida, ya que no se vuelve a validar.

    Returns:
        Fecha ingresada como texto o representación textual de valor_actual
        si la entrada está vacía.
    """
    while True:
        fecha = input(prompt).strip()
        if not fecha and valor_actual is not None:
            return str(valor_actual)
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", fecha):
            print("Por favor, ingrese la fecha en formato AAAA-MM-DD.")
            continue

        try:
            date.fromisoformat(fecha)
        except ValueError:
            print("La fecha no es válida. Verifique el año, mes y día.")
            continue

        return fecha
