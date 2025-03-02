import random

def monty_hall_simulacion(n_rondas=100000):
    """
    Simula el experimento del Problema de Monty Hall para dos estrategias:
    - No cambiar de puerta.
    - Cambiar de puerta.
    Retorna la probabilidad de ganar para cada estrategia.
    """
    
    # Contadores de victorias para cada estrategia
    victorias_no_cambiar = 0
    victorias_cambiar = 0

    for _ in range(n_rondas):
        # 1. Se coloca el premio al azar detrás de una de las tres puertas.
        puertas = [0, 1, 2]
        premio = random.choice(puertas)

        # 2. El concursante elige una puerta al azar.
        eleccion_concursante = random.choice(puertas)

        # 3. El presentador (que sabe dónde está el premio) abre otra puerta
        #    que NO contiene el premio.
        #    - Para abrir la puerta, primero filtramos las que no son la elegida
        #      y no tienen el premio.
        puertas_restantes = [p for p in puertas if p != eleccion_concursante]
        puertas_posibles_para_abrir = [p for p in puertas_restantes if p != premio]
        
        # El presentador abre una puerta al azar de las posibles (aunque en el juego real
        # típicamente solo habría una opción posible, si el concursante eligió la puerta correcta).
        puerta_abierta = random.choice(puertas_posibles_para_abrir)
        
        # 4. Se determinan los resultados bajo cada estrategia:
        
        # Estrategia 1: No cambiar de puerta
        # Gana si la elección inicial es la puerta con el premio
        if eleccion_concursante == premio:
            victorias_no_cambiar += 1
        
        # Estrategia 2: Cambiar de puerta
        # Para cambiar, se elige la otra puerta cerrada que no es ni la elegida originalmente
        # ni la que abrió el presentador.
        puerta_para_cambiar = [p for p in puertas
                               if p != eleccion_concursante and p != puerta_abierta][0]
        
        if puerta_para_cambiar == premio:
            victorias_cambiar += 1
    
    # Calcular las probabilidades de ganar
    prob_no_cambiar = victorias_no_cambiar / n_rondas
    prob_cambiar = victorias_cambiar / n_rondas
    
    return prob_no_cambiar, prob_cambiar

if __name__ == "__main__":
    # Número de simulaciones
    N = 100000
    
    prob_nc, prob_c = monty_hall_simulacion(N)
    
    print(f"Resultados tras {N} rondas:")
    print(f"Probabilidad de ganar SIN cambiar: {prob_nc:.4f}")
    print(f"Probabilidad de ganar CAMBIANDO de puerta: {prob_c:.4f}")
