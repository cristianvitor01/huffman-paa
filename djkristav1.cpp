#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define INF INT_MAX

typedef struct Grafo {
    int numVertices;
    int **matriz; // Matriz de adjacência
} Grafo;

// Função para inicializar o grafo
Grafo* inicializaGrafo(int vertices) {
    Grafo *g = (Grafo *)malloc(sizeof(Grafo));
    g->numVertices = vertices;

    g->matriz = (int **)malloc(vertices * sizeof(int *));

    for (int i = 0; i < vertices; i++) {
        g->matriz[i] = (int *)malloc(vertices * sizeof(int));
        for (int j = 0; j < vertices; j++) {
            g->matriz[i][j] = INF; // Inicializa todos com infinito
        }
    }
    return g;
}

// Função para adicionar uma aresta ao grafo
void adicionarAresta(Grafo *g, int origem, int destino, int peso) {
    g->matriz[origem][destino] = peso;
    g->matriz[destino][origem] = peso; // Somente grafos não direcionados
}

// Função para encontrar o vértice com a menor distância ainda não visitado
int menorDistancia(int dist[], int visitados[], int vertices) {
    int min = INF, minIndex = -1;

    for (int i = 0; i < vertices; i++) {
        if (!visitados[i] && dist[i] <= min) {
            min = dist[i];
            minIndex = i;
        }
    }
    return minIndex;
}

// Algoritmo de Dijkstra
void dijkstra(Grafo *g, int origem, int destino) {
    int vertices = g->numVertices;
    int dist[vertices];        // Distâncias mínimas
    int visitados[vertices];   // Marca vértices já visitados
    int anterior[vertices];    // Armazena o caminho

    for (int i = 0; i < vertices; i++) {
        dist[i] = INF;
        visitados[i] = 0;
        anterior[i] = -1; // Sem caminho anterior
    }

    dist[origem] = 0;

    // Encontra o caminho mais curto para todos os vértices
    for (int count = 0; count < vertices - 1; count++) {
        int u = menorDistancia(dist, visitados, vertices);
        if (u == -1) break; // Não há mais vértices alcançáveis

        visitados[u] = 1;

        for (int v = 0; v < vertices; v++) {
            if (!visitados[v] && g->matriz[u][v] != INF && dist[u] != INF &&
                dist[u] + g->matriz[u][v] < dist[v]) {
                dist[v] = dist[u] + g->matriz[u][v];
                anterior[v] = u;
            }
        }
    }

    // Exibe o caminho mais curto
    if (dist[destino] == INF) {
        printf("Não há caminho entre os vértices %d e %d.\n", origem, destino);
    } else {
        printf("Caminho mais curto de %d para %d tem peso %d.\n", origem, destino, dist[destino]);
        printf("Caminho: ");
        int caminho[vertices], tam = 0, atual = destino;

        while (atual != -1) {
            caminho[tam++] = atual;
            atual = anterior[atual];
        }
        for (int i = tam - 1; i >= 0; i--) {
            printf("%d ", caminho[i]);
            if (i > 0) printf("-> ");
        }
        printf("\n");
    }
}

// liberar a memória alocada
void liberaGrafo(Grafo *g) {
    for (int i = 0; i < g->numVertices; i++) {
        free(g->matriz[i]);
    }
    free(g->matriz);
    free(g);
}

int main() {
    int vertices, arestas, origem, destino;

    printf("Digite o número de vértices: ");
    scanf("%d", &vertices);

    Grafo *g = inicializaGrafo(vertices);

    printf("Digite o número de arestas: ");
    scanf("%d", &arestas);

    printf("Digite as arestas no formato (origem destino peso):\n");
    for (int i = 0; i < arestas; i++) {
        int v1, v2, peso;
        scanf("%d %d %d", &v1, &v2, &peso);
        adicionarAresta(g, v1, v2, peso);
    }

    printf("Digite o vértice de origem: ");
    scanf("%d", &origem);

    printf("Digite o vértice de destino: ");
    scanf("%d", &destino);

    dijkstra(g, origem, destino);

    liberaGrafo(g);
    return 0;
}
