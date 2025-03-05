import simpy
import numpy as np
import random

class SistemaOperativo:
    def __init__(self, env, memoria_total, instrucciones_cpu, num_cpus):
        self.env = env
        self.memoria = simpy.Container(env, init=memoria_total, capacity=memoria_total)
        self.cpu = simpy.Resource(env, capacity=num_cpus)
        self.instrucciones_cpu = instrucciones_cpu
        self.tiempos_finalizacion = []

    def registrar_tiempo(self, tiempo):
        self.tiempos_finalizacion.append(tiempo)

class Proceso:
    def __init__(self, env, nombre, sistema):
        self.env = env
        self.nombre = nombre
        self.sistema = sistema
        self.memoria_requerida = random.randint(1, 10)
        self.instrucciones_restantes = random.randint(1, 10)
        self.tiempo_inicio = env.now

    def run(self):
        yield self.sistema.memoria.get(self.memoria_requerida)
        
        while self.instrucciones_restantes > 0:
            with self.sistema.cpu.request() as req:
                yield req
                yield self.env.timeout(1)
                self.instrucciones_restantes -= min(self.sistema.instrucciones_cpu, self.instrucciones_restantes)
                
                if self.instrucciones_restantes == 0:
                    self.sistema.registrar_tiempo(self.env.now - self.tiempo_inicio)
                    self.sistema.memoria.put(self.memoria_requerida)

def ejecutar_simulacion(num_procesos, intervalo_llegada, memoria_total, instrucciones_cpu, num_cpus):
    env = simpy.Environment()
    sistema = SistemaOperativo(env, memoria_total, instrucciones_cpu, num_cpus)

    for i in range(num_procesos):
        proceso = Proceso(env, f"Proceso-{i+1}", sistema)
        env.process(proceso.run())
        env.timeout(random.expovariate(1.0 / intervalo_llegada))

    env.run()

    if len(sistema.tiempos_finalizacion) > 0:
        media = np.mean(sistema.tiempos_finalizacion)
        desviacion = np.std(sistema.tiempos_finalizacion)
    else:
        media, desviacion = 0, 0

    return media, desviacion