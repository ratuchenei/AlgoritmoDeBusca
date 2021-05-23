import networkx as nx
from itertools import count
from heapq import heappush, heappop

class Busca:
	def __init__(self, origem, objetivo): 
		self.grafo = nx.Graph()
		self.origem = origem
		self.objetivo = objetivo

	def criarGrafo(self, arquivo):
		f = open(arquivo, "r")
		for line in f.readlines():
			arestas = line.split()
			self.grafo.add_edge(arestas[0], arestas[1], weight = int(arestas[2]))

class BuscaSemInformacao(Busca):
	def __init__(self, origem, objetivo): 
		super().__init__(origem, objetivo)
	
	def buscaEmProfundidade(self):
		return self.buscaEmProfundidade0(self.grafo, self.origem, self.objetivo)

	def buscaEmProfundidade0(self, grafo, origem, objetivo):
		visitado = set()
		profundidade = len(grafo)
		visitado.add(origem)
		caminho = [origem]
		pilha = [(origem, profundidade, iter(grafo[origem]))]
		while pilha:		
			nodopai, profundidade, nodofilho = pilha[-1]
			try:
				filho = next(nodofilho)
				if filho not in visitado:
					caminho.append(filho)
					if filho == objetivo: 
						return caminho
					visitado.add(filho)
					if profundidade > 1:
						pilha.append((filho, profundidade - 1, iter(grafo[filho])))
			except StopIteration:
				pilha.pop()

	def buscaEmProfundidade1(self, grafo, origem, objetivo):
		visitado = set()
		profundidade = len(grafo)
		visitado.add(origem)
		pilha = [(origem, profundidade, iter(grafo[origem]))]
		while pilha:
			nodopai, profundidade, nodofilho = pilha[-1]
			try:
				filho = next(nodofilho)
				if filho not in visitado:
					yield nodopai, filho
					if filho == objetivo: return 
					visitado.add(filho)
					if profundidade > 1:
						pilha.append((filho, profundidade - 1, iter(grafo[filho])))
			except StopIteration:
				pilha.pop()


class BuscaComInformacao(Busca):
	def __init__(self, origem, objetivo): 
		super().__init__(origem, objetivo)
		self.heuristica = {}

	def criarHeuristica(self, arquivo):
		f = open(arquivo, "r")
		for line in f.readlines():
			distancias = line.split()
			self.heuristica[distancias[0]] = int(distancias[1])

	def buscaAEstrela(self):
		return self.buscaAEstrela0(self.grafo, self.origem, self.objetivo, self.heuristica)


	def buscaAEstrela0(self, grafo, origem, objetivo, heuristica):
		fila = [(0, origem, 0, None)]
		enfileirados = {}
		explorados = {}
		while fila:
			_, nodoatual, distancia, nodopai = heappop(fila)
			if nodoatual == objetivo:
				caminho = [nodoatual]
				nodo = nodopai
				while nodo is not None:
					caminho.append(nodo)
					nodo = explorados[nodo]
				caminho.reverse()				
				return caminho
			if nodoatual in explorados:
				if explorados[nodoatual] is None:
					continue
				qcusto, hcusto = enfileirados[nodoatual]
				if qcusto < distancia:
					continue
			explorados[nodoatual] = nodopai
			for vizinho, dv in grafo[nodoatual].items():
				ncusto = distancia + int(dv['weight'])
				if vizinho in enfileirados:
					qcusto, hcusto = enfileirados[vizinho]
					if qcusto <= ncusto:
						continue
				else:
					hcusto = heuristica[vizinho]
				enfileirados[vizinho] = ncusto, hcusto
				heappush(fila, (ncusto + hcusto, vizinho, ncusto, nodoatual))

	def buscaAEstrela1(self, grafo, origem, objetivo, heuristica):
		fila = [(0, origem, None)]
		enfileirados = {}
		explorados = {}
		while fila:
			_ , nodoatual, nodopai = heappop(fila)
			if nodoatual == objetivo:
				caminho = [nodoatual]
				nodo = nodopai
				while nodo is not None:
					caminho.append(nodo)
					nodo = explorados[nodo]
				caminho.reverse()
				return caminho
			if nodoatual in explorados:
				if explorados[nodoatual] is None:
					continue
			explorados[nodoatual] = nodopai
			for vizinho, w in grafo[nodoatual].items():
				hcusto = heuristica[vizinho]
				enfileirados[vizinho] = hcusto
				heappush(fila, (hcusto, vizinho, nodoatual))


buscaDfs = BuscaSemInformacao('Arad','Bucharest')
buscaDfs.criarGrafo('input.txt')
dfs = buscaDfs.buscaEmProfundidade()
print(list(dfs))

buscaAstar = BuscaComInformacao('Arad','Bucharest')
buscaAstar.criarGrafo('input.txt')
buscaAstar.criarHeuristica('heuristics.txt')
aStar = buscaAstar.buscaAEstrela()
print(list(aStar))