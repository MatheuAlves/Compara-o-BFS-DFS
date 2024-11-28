from collections import deque
from time import perf_counter
import tracemalloc

matriz = [
    ['A', 'B', 'C', 'D', 'E'],
    ['F', 'G', 'H', 'I', 'J'],
    ['K', 'L', 'M', 'N', 'O'],
    ['P', 'Q', 'R', 'S', 'T'],
    ['U', 'V', 'X', 'Y', 'Z']
]

barreiras = [
    ((0, 1), (0, 2)), # B - C
    ((0, 2), (0, 1)), # C - B
    ((0, 1), (1, 1)), # B - G
    ((1, 1), (0, 1)), # G - B
    ((0, 3), (1, 3)), # D - I
    ((1, 3), (0, 3)), # I - D
    ((1, 3), (1, 4)), # I - J
    ((1, 4), (1, 3)), # J - I
    ((1, 0), (2, 0)), # F - K
    ((2, 0), (1, 0)), # K - F
    
    ((1, 1), (2, 1)), # G - L
    ((2, 1), (1, 1)), # L - G
    ((1, 2), (2, 2)), # H - M
    ((2, 2), (1, 2)), # M - H
    ((1, 4), (2, 4)), # J - O
    ((2, 4), (1, 4)), # O - J
    ((2, 0), (2, 1)), # K - L
    ((2, 1), (2, 0)), # L - K
    ((2, 3), (3, 3)), # N - S
    ((3, 3), (2, 3)), # S - N
    
    ((2, 4), (3, 4)), # O - T
    ((3, 4), (2, 4)), # T - O
    ((3, 0), (3, 1)), # P - Q
    ((3, 1), (3, 0)), # Q - P
    ((3, 1), (3, 2)), # Q - E
    ((3, 2), (3, 1)), # E - Q
    ((3, 2), (4, 2)), # E - X
    ((4, 2), (3, 2)), # X - E
    ((3, 3), (4, 3)), # S - Y
    ((4, 3), (3, 3)), # Y - S
]


inicio = (4, 0) 
fim = (0, 4) 
movimentos = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def tem_barreira(matriz, pos_atual, prox_pos):
    coordenadas = (pos_atual, prox_pos)
    for i in barreiras:
        if coordenadas == i:
            return True
    return False

def bfs(matriz, inicio, fim, movimentos):
    inicio_tempo_bfs = perf_counter()
    tracemalloc.start()
    fila = deque([inicio])
    
    # Dicionário para armazenar os pais das posições (para reconstruir o caminho)
    pais = {inicio: None}

    while fila:
        pos_atual = fila.popleft()
        
        if pos_atual == fim:
            print("BFS Resolvido!")
            fim_tempo_bfs = perf_counter()
            tempo_total_bfs = fim_tempo_bfs - inicio_tempo_bfs
            
            
            caminho = []
            caminho_valores = []
            
            while pos_atual is not None:
                caminho.append(pos_atual)
                caminho_valores.append(matriz[pos_atual[0]][pos_atual[1]])
                pos_atual = pais[pos_atual]
            caminho.reverse()
            caminho_valores.reverse()
            
            # Relatório de memória
            memoria, pico_memoria = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            imprime_bfs(caminho, caminho_valores, tempo_total_bfs, memoria, pico_memoria)
            
            return caminho
        
        for movimento in movimentos:
            prox_pos = (pos_atual[0] + movimento[0], pos_atual[1] + movimento[1])
            
            # Verifica se a posição está dentro dos limites da matriz e não tem barreira
            if 0 <= prox_pos[0] < len(matriz) and 0 <= prox_pos[1] < len(matriz[0]):
                if prox_pos not in pais and not tem_barreira(matriz, pos_atual, prox_pos):
                    fila.append(prox_pos)
                    pais[prox_pos] = pos_atual 
                    
    print("Matriz não tem solução!")
    tracemalloc.stop()
    return None

def imprime_bfs(caminho, caminho_valores, tempo_bfs, memoria, pico_memoria):
    print(f'Caminho BFS: {caminho}')
    print(f'Caminho BFS: {caminho_valores}')
    print(f'Tempo total BFS: {tempo_bfs:.10f}')
    print(f"Consumo de Memória BFS: {memoria / 1024:.2f} KB; Pico: {pico_memoria / 1024:.2f} KB")

def dfs(matriz, inicio, fim, movimentos):
    inicio_tempo_dfs = perf_counter()
    tracemalloc.start()
    pilha = [inicio]
    
    # Dicionário para armazenar os pais das posições (para reconstruir o caminho)
    pais = {inicio: None}
    
    while pilha:
        pos_atual = pilha.pop()
        
        if pos_atual == fim:
            print("DFS Resolvido!")
            fim_tempo_dfs = perf_counter()
            tempo_total_dfs = fim_tempo_dfs - inicio_tempo_dfs
            
            caminho = []
            caminho_valores = []
            while pos_atual is not None:
                caminho.append(pos_atual)
                caminho_valores.append(matriz[pos_atual[0]][pos_atual[1]])
                pos_atual = pais[pos_atual]
            caminho.reverse()
            caminho_valores.reverse()
            
            # Relatório de memória
            memoria, pico_memoria = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            imprime_dfs(caminho, caminho_valores, tempo_total_dfs, memoria, pico_memoria)
            
            return caminho
        
        for movimento in movimentos:
            prox_pos = (pos_atual[0] + movimento[0], pos_atual[1] + movimento[1])
            
            # Verifica se a posição está dentro dos limites da matriz e não tem barreira
            if 0 <= prox_pos[0] < len(matriz) and 0 <= prox_pos[1] < len(matriz[0]):
                if prox_pos not in pais and not tem_barreira(matriz, pos_atual, prox_pos):
                    pilha.append(prox_pos)
                    pais[prox_pos] = pos_atual 
                    
    print("Matriz não tem solução!")
    tracemalloc.stop()
    return None

def imprime_dfs(caminho, caminho_valores, tempo_dfs, memoria, pico_memoria):
    print(f'Caminho DFS: {caminho}')
    print(f'Caminho DFS: {caminho_valores}')
    print(f'Tempo total DFS: {tempo_dfs:.10f}')
    print(f"Consumo de Memória DFS: {memoria / 1024:.2f} KB; Pico: {pico_memoria / 1024:.2f} KB")

print(f"Início: {matriz[inicio[0]][inicio[1]]}")
print(f"Fim: {matriz[fim[0]][fim[1]]}")


print('-----------BFS-----------')
pos_atual = inicio
bfs(matriz, pos_atual, fim, movimentos)

print('-----------DFS-----------')
pos_atual = inicio
dfs(matriz, pos_atual, fim, movimentos)