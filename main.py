import math
import tracemalloc
import random

from collections import deque

class No:
    def __init__(self, estado, no_pai=None, acao=None, custoCaminho=0, profundidade=0, funcaoAvaliacao=0):
        self.estado = estado
        self.no_pai = no_pai
        self.acao = acao
        self.custoCaminho = custoCaminho
        self.profundidade = profundidade
        self.funcaoAvaliacao = funcaoAvaliacao

        

def heuristicaDistanciaManhathan(elemento, estadoAtual, estadoObjetivo):
    # h² = |x1-x2| + |y1-y2|
    # x = coluna
    # y = linha
    
    # x0 x1 x2 
    # 0  1  2     --> y = 0
    # 3  4  5     --> y = 1
    # 6  7  8     --> y = 2
    
    posicaoObjetivo = estadoObjetivo.index(elemento)
    posicaoAtual = estadoAtual.index(elemento)

    x1_mapping = {8: 2, 5: 2, 2: 2, 1: 1, 4: 1, 7: 1}
    y1_mapping = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2}

    x2_mapping = {8: 2, 5: 2, 2: 2, 1: 1, 4: 1, 7: 1}
    y2_mapping = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2}

    x1, y1 = x1_mapping.get(posicaoObjetivo, 0), y1_mapping.get(posicaoObjetivo, 0)
    x2, y2 = x2_mapping.get(posicaoAtual, 0), y2_mapping.get(posicaoAtual, 0)

    resultado = math.fabs(x1 - x2) + math.fabs(y1 - y2)
    return resultado

def heuristicaDistanciaEuclidiana(elemento, estadoAtual, estadoObjetivo):
     # h² = (x1 - x2)² + (y1 - y2)²
    # x = coluna
    # y = linha
    
    # x0 x1 x2 
    # 0  5  2     --> y = 0
    # 3  4  1     --> y = 1
    # 6  7  8     --> y = 2
    
    posicaoObjetivo = estadoObjetivo.index(elemento)
    posicaoAtual = estadoAtual.index(elemento)

    x1_mapping = {8: 2, 5: 2, 2: 2, 1: 1, 4: 1, 7: 1}
    y1_mapping = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2}

    x2_mapping = {8: 2, 5: 2, 2: 2, 1: 1, 4: 1, 7: 1}
    y2_mapping = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2}

    x1, y1 = x1_mapping.get(posicaoObjetivo, 0), y1_mapping.get(posicaoObjetivo, 0)
    x2, y2 = x2_mapping.get(posicaoAtual, 0), y2_mapping.get(posicaoAtual, 0)

    resultado = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    return resultado

def heuristicaQuantidadeDeElementosForaDoLugar(estadoAtual, estadoObjetivo):
    foraDoLugar = 0
    for elemento in estadoAtual:
        if(estadoAtual.index(elemento) != estadoObjetivo.index(elemento)):
            foraDoLugar += 1

    return foraDoLugar


def acoesPossiveis(estado):
    # Retorna as ações possíveis no estado (movimentos da peça vazia)
    linhas, colunas = 3, 3
    posicao_vazia = estado.index(0)
    linha_vazia, coluna_vazia = divmod(posicao_vazia, colunas)
    
    acoes_possiveis = []

    # Verificar se é possível mover a peça para cima
    if linha_vazia > 0:
        acoes_possiveis.append(('cima', (linha_vazia - 1, coluna_vazia)))

    # Verificar se é possível mover a peça para baixo
    if linha_vazia < linhas - 1:
        acoes_possiveis.append(('baixo', (linha_vazia + 1, coluna_vazia)))

    # Verificar se é possível mover a peça para a esquerda
    if coluna_vazia > 0:
        acoes_possiveis.append(('esquerda', (linha_vazia, coluna_vazia - 1)))

    # Verificar se é possível mover a peça para a direita
    if coluna_vazia < colunas - 1:
        acoes_possiveis.append(('direita', (linha_vazia, coluna_vazia + 1)))

    return acoes_possiveis


def gerarFilho(estado, acao):
    novo_estado = estado[:]
    posicao_vazia = novo_estado.index(0)
    nova_posicao = acao[1][0] * 3 + acao[1][1]
    novo_estado[posicao_vazia], novo_estado[nova_posicao] = novo_estado[nova_posicao], novo_estado[posicao_vazia]
    return novo_estado


def teste_De_Objetivo(EstadoAtual, EstadoObjetivo):
    return EstadoAtual == EstadoObjetivo



def imprimirCaminhoSolucao(no_solucao):
    caminho = []
    while no_solucao:
        caminho.append(no_solucao.estado)
        no_solucao = no_solucao.no_pai
    caminho.reverse()
    for estado in caminho:
        print("Estado:")
        print(estado[0], estado[1], estado[2])
        print(estado[3], estado[4], estado[5])
        print(estado[6], estado[7], estado[8])
        print()
    

def imprimirEstadosNaBorda(borda, arquivo_saida):
    with open(arquivo_saida, 'a') as arquivo:
        arquivo.write("Borda:\n")
        for elemento in borda:
            arquivo.write(str(elemento.estado) + "\n\n")
            

def quantidadeDeEstadosNaBorda(borda):
    return len(borda)



def pegarNoRandomico(borda):
    return random.randint(0, 10)

def buscaEmProfundidade(estado_inicial, estado_objetivo, limite_profundidade=33):
    borda = [No(estado_inicial)]
    explorados = set()
    passo = 0
    nos_expandidos = 0
    
    while borda:
        nos_expandidos += 1
        passo += 1        
        no_atual = borda.pop()
        explorados.add(tuple(no_atual.estado))

        if( no_atual.profundidade == limite_profundidade):
            indice_aleatorio = pegarNoRandomico(borda)
            no_aleatorio = borda[indice_aleatorio]
            no_aleatorio.profundidade = 0
            borda.clear()
            borda.append(no_aleatorio)
            explorados.clear()
            passo = 0
            print(no_aleatorio.estado)
            continue

        if teste_De_Objetivo(no_atual.estado, estado_objetivo):
            return no_atual, passo, quantidadeDeEstadosNaBorda(borda), nos_expandidos  # Retorna o nó solução

        for acao, posicao in acoesPossiveis(no_atual.estado):
            filho_estado = gerarFilho(no_atual.estado, (acao, posicao))
            if tuple(filho_estado) not in explorados:
                filho = No(filho_estado, no_atual, acao, profundidade=no_atual.profundidade + 1)
                borda.append(filho)
                explorados.add(tuple(filho_estado))

        imprimirEstadosNaBorda(borda, 'output.txt')

    return None, None, None, None  # Se não encontrou solução



def buscaEmLargura(estado_inicial, estado_objetivo):
    borda = deque([No(estado_inicial)])
    explorados = set()
    passo = 0

    while borda:
        passo += 1
        #print(f"Passo {passo}:")

        no = borda.popleft()
        explorados.add(tuple(no.estado))

        if teste_De_Objetivo(no.estado, estado_objetivo):
            return no, passo, quantidadeDeEstadosNaBorda(borda)  # Retorna o nó solução

        for acao, posicao in acoesPossiveis(no.estado):
            filho_estado = gerarFilho(no.estado, (acao, posicao))
            if tuple(filho_estado) not in explorados:
                filho = No(filho_estado, no, acao)
                borda.append(filho)
                explorados.add(tuple(filho_estado))

        imprimirEstadosNaBorda(borda, 'output.txt')

    return None, None, None  # Se não encontrou solução


def funcaoAvaliacao(estado, custoCaminho, estadoAtual, estadoObjetivo): 
    # f(n)= g(n) + h(n)
    # A* = profundidade do nó + heuristica
    h = 0
    g = custoCaminho
    for indice in estado:
        h += heuristicaDistanciaManhathan(indice, estadoAtual, estadoObjetivo)
    return (g + h)

def a_estrela(estado_inicial, estado_objetivo):
    borda = [No(estado_inicial)]
    explorados = set()
    passo = 0

    while borda:
        passo += 1
        #print(f"Passo {passo}:")
        borda.sort(key=lambda x: x.funcaoAvaliacao)  # Ordena a borda pela heurística pelo menor custoTotal
        no = borda.pop(0)
        explorados.add(tuple(no.estado))

        if teste_De_Objetivo(no.estado, estado_objetivo):
            return no, passo, quantidadeDeEstadosNaBorda(borda)  # Retorna o nó solução

        for acao, posicao in acoesPossiveis(no.estado):
            filho_estado = gerarFilho(no.estado, (acao, posicao))
            if tuple(filho_estado) not in explorados:
                filho = No(filho_estado, no, acao, custoCaminho=passo, profundidade=passo, funcaoAvaliacao = funcaoAvaliacao(estado= filho_estado, custoCaminho= passo, estadoAtual= filho_estado, estadoObjetivo= estado_objetivo))
                borda.append(filho)
                explorados.add(tuple(filho_estado))

        imprimirEstadosNaBorda(borda, 'output.txt')

    return None, None, None  # Se não encontrou solução


def heuristicaGulosa(estadoAtual, estadoObjetivo):
    valor_heuristico_total = 0
    for elemento in estadoAtual:
        if elemento != 0:
           #valor_heuristico_total += heuristicaQuantidadeDeElementosForaDoLugar(estadoAtual, estadoObjetivo)
           #valor_heuristico_total += heuristicaDistanciaEuclidiana(elemento, estadoAtual, estadoObjetivo)
           valor_heuristico_total += heuristicaDistanciaManhathan(elemento, estadoAtual, estadoObjetivo)
    return valor_heuristico_total



def buscaGulosa_algoritmo(estado_inicial, estado_objetivo):
    borda = [No(estado_inicial)]
    explorados = set()
    passo = 0

    while borda:
        passo += 1
        #print(f"Passo {passo}:")

        borda.sort(key=lambda x: heuristicaGulosa(x.estado, estado_objetivo))  # Ordena a borda pela heurística pelo menor custoTotal

        no = borda.pop(0)
        explorados.add(tuple(no.estado))

        if teste_De_Objetivo(no.estado, estado_objetivo):
            return no, passo, quantidadeDeEstadosNaBorda(borda)  # Retorna o nó solução

        for acao, posicao in acoesPossiveis(no.estado):
            filho_estado = gerarFilho(no.estado, (acao, posicao))
            if tuple(filho_estado) not in explorados:
                filho = No(filho_estado, no, acao)
                borda.append(filho)
                explorados.add(tuple(filho_estado))

        imprimirEstadosNaBorda(borda, 'output.txt')

    

    return None, None, None  # Se não encontrou solução

