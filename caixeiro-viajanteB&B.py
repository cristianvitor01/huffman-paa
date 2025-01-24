# Implemente uma resolução para o problema do
# Caixeiro Viajante (TSP) utilizando Branch-and-Bound. O
# programa deve receber uma matriz , onde
# representa a quantidade de cidades e cada elemento
# corresponde ao custo entre elas.

import math

maxsize = float('inf') # Infinito


# Função para copiar o caminho atual para a solução final
def copiarParaFinal(caminho_atual):
    caminho_final[:N + 1] = caminho_atual[:]
    caminho_final[N] = caminho_atual[0]


# Função para encontrar o custo mínimo da aresta com um fim no vértice i
def primeiroMin(adj, i):
    minimo = maxsize
    for k in range(N):
        if adj[i][k] < minimo and i != k:
            minimo = adj[i][k]
    return minimo


# Função para encontrar o segundo custo mínimo da aresta com um fim no vértice i
def segundoMin(adj, i):
    primeiro, segundo = maxsize, maxsize
    for j in range(N):
        if i == j:
            continue
        if adj[i][j] <= primeiro:
            segundo = primeiro
            primeiro = adj[i][j]
        elif (adj[i][j] <= segundo and adj[i][j] != primeiro):
            segundo = adj[i][j]
    return segundo


# Função recursiva que resolve o problema do TSP utilizando a técnica Branch and Bound
def TSPRec(adj, limite_atual, peso_atual, nivel, caminho_atual, visitado):
    global resultado_final

    # Caso base: quando todos os vértices foram visitados
    if nivel == N:
        if adj[caminho_atual[nivel - 1]][caminho_atual[0]] != 0:
            resultado_atual = peso_atual + adj[caminho_atual[nivel - 1]] \
                [caminho_atual[0]]
            if resultado_atual < resultado_final:
                copiarParaFinal(caminho_atual)
                resultado_final = resultado_atual
        return

    # Recursão para explorar todas as possibilidades de caminho
    for i in range(N):
        if (adj[caminho_atual[nivel - 1]][i] != 0 and visitado[i] == False):
            temp = limite_atual
            peso_atual += adj[caminho_atual[nivel - 1]][i]

            # Cálculo do limite inferior para o nó atual
            if nivel == 1:
                limite_atual -= ((primeiroMin(adj, caminho_atual[nivel - 1]) +
                                  primeiroMin(adj, i)) / 2)
            else:
                limite_atual -= ((segundoMin(adj, caminho_atual[nivel - 1]) +
                                  primeiroMin(adj, i)) / 2)

            # Se o limite inferior mais o peso atual for menor que o resultado final,
            # prosseguir com a busca
            if limite_atual + peso_atual < resultado_final:
                caminho_atual[nivel] = i
                visitado[i] = True
                TSPRec(adj, limite_atual, peso_atual, nivel + 1, caminho_atual, visitado)

            # Caso contrário, desfazer as mudanças e explorar outras possibilidades
            peso_atual -= adj[caminho_atual[nivel - 1]][i]
            limite_atual = temp

            visitado = [False] * len(visitado)
            for j in range(nivel):
                if caminho_atual[j] != -1:
                    visitado[caminho_atual[j]] = True


# Função principal que configura a solução inicial e chama a recursão
def TSP(adj):
    limite_atual = 0
    caminho_atual = [-1] * (N + 1)
    visitado = [False] * N

    # Cálculo do limite inferior inicial para o nó raiz
    for i in range(N):
        limite_atual += (primeiroMin(adj, i) + segundoMin(adj, i))

    # Arredondamento do limite inferior para um número inteiro
    limite_atual = math.ceil(limite_atual / 2)

    # Começar a partir do vértice 0
    visitado[0] = True
    caminho_atual[0] = 0

    # Chama a função recursiva para explorar as possibilidades
    TSPRec(adj, limite_atual, 0, 1, caminho_atual, visitado)


adj = [[0, 10, 15, 20],
       [10, 0, 35, 25],
       [15, 35, 0, 30],
       [20, 25, 30, 0]]
N = 4

caminho_final = [None] * (N + 1)
visitado = [False] * N
resultado_final = maxsize

TSP(adj)

print("Custo mínimo:", resultado_final)
print("Caminho percorrido: ", end=' ')
for i in range(N + 1):
    print(caminho_final[i], end=' ')
