import os
import sys
from simulacion import ejecutar_simulacion

def menu():
    print("\n--- Simulacion de los procesos en el sistema operativo ---")
    print("1. Ejecutar una simulacion con los parametros personalizados")
    print("2. Ver graficos de rendimiento")
    print("3. Salir")
    return input("Selecciona una opcion: ")

def obtener_parametros():
    try:
        num_procesos = int(input("El numero de procesos (ejemplo: 25, 50, 100, 150, 200): "))
        intervalo_llegada = int(input("Intervalo de llegada de procesos (ejemplo: 10, 5, 1): "))
        memoria_total = int(input("Cantidad de memoria RAM total (ejemplo: 100 o 200): "))
        instrucciones_cpu = int(input("Cantidad de instrucciones por ciclo de CPU (ejemplo: 3 o 6): "))
        num_cpus = int(input("Los numero de CPUs disponibles (ejemplo: 1 o 2): "))
        return num_procesos, intervalo_llegada, memoria_total, instrucciones_cpu, num_cpus
    except ValueError:
        print("\n AAAAAAH ERROR, ingresa solo los valores numericos que te habia dicho.")
        return obtener_parametros()

def ejecutar_personalizado():
    num_procesos, intervalo_llegada, memoria_total, instrucciones_cpu, num_cpus = obtener_parametros()
    
    print("\nEjecutando tu simulacion... :D")
    media, desviacion = ejecutar_simulacion(num_procesos, intervalo_llegada, memoria_total, instrucciones_cpu, num_cpus)

    print(f"\nEstos fueron los resultados de la simulacion:")
    print(f"Tiempo promedio de la ejecucion: {media:.2f} unidades de tiempo")
    print(f"Desviación estandar del tiempo: {desviacion:.2f}")

def ver_graficos():
    os.system("python graficas.py")

    while True:
        opcion = menu()
        if opcion == "1":
            ejecutar_personalizado()
        elif opcion == "2":
            ver_graficos()
        elif opcion == "3":
            sys.exit()
        else:
            print(" Opcion no válida, intentalo de nuevo :(.")