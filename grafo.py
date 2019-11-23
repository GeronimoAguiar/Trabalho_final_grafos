'''
                    UNIVERSIDADE FEDERAL DO CEARÁ  
                            CAMPUS SOBRAL
                  CURSO DE ENGENHARIA DE COMPUTÇÃO
                TRABALHO FINAL DE ALGORITMOS E GRAFOS

                      SAMUEL HERICLES - 389118
                      GERÔNIMO AGUIAR - 385145
                      PEDRO RENOIR    - 389113
   
  Parte 1 -> Algoritmos de caminhos mínimos para todos os vértices

    Implementar os algoritmos de menores caminhos dentre todos os pares de
  vértices apresentados em sala. Cada algoritmo deve imprimir a matriz de
  menores caminhos e os menores a partir de vértice fixo fornecido como 
  entrada. Caso seu grafo tenha circuito negativo, seu algoritmo deverá
  ser capaz de identificar a sua existência.

  Parte 2 -> Algoritmos de fluxo máximo

    Considere os seguintes algoritmos para resolver o problema de fluxo
  máximo:

    • Ford-Fulkerson;
    • Push–relabel maximum flow algorithm.

    Implemente os algoritmos acima. Utilizando a ideia por trás de cada
  algoritmo acima, implemente uma forma eficiente, para cada algoritmo, de
  encontrar o corte mínimo do grafo fornecido. Seu algorítimo deverá 
  receber um grafo orientado com vértices fonte e sorvedouro explicitados
  e então retornar a função fluxo máximo para o grafo e as arestas que
  pertencem ao corte máximo.

'''

# Import da biblioteca math para valor 'infinito'
import math

# Import da bliblioteca numpy para criar matriz de zeros
import numpy as np

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>Carregar Matriz de Pesos<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

'''
@brief  Carrega a matriz de peso no qual se refere ao grafo que 
        será analisado.
        
        Exemplo:
          
                             _0____1____2_
                          0 | 0    1    1 | 
                          1 | inf  0    1 |
                          2 | 1   inf   0 |
      
      Esta matriz é interpretada assim:
        - A caminho do vértice 0->1 com peso 1
        - A caminho do vértice 0->2 com peso 1
        - A caminho do vértice 2->0 com peso 1
        - A caminho do vértice 1->1 com peso 1
        - Não há caminho do vértice 1->0 pois o peso é infinito

@return A matriz de pesos que representa o grafo direcionado.

'''

def matrizPesos():
  # Carrega o arquivo localizado na pasta 'exemplo_de_grafos'
  arquivo = open("exemplo_de_grafos/grafo_youtube.txt","r")    
  texto = arquivo.readlines()
  arquivo.close()

  # Trata os dados do arquivos
  nVertices = int(texto[0].split()[0])
  vPai = int(texto[1].split()[0])

  arestas = texto[2:]
  nArestas = len(arestas)
  w = np.zeros( (nVertices,nVertices) )
  
  for i in range(0,nVertices):
    for j in range(0,nVertices):
      if i != j:
        w[i,j] = math.inf
       
  for i in arestas:
    j = i.split()
    w[int(j[0]),int(j[1])] = float(j[2])

  print("\n>>>>>Matriz de Pesos<<<<<\n")
  print(w)
  return w
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>Busca em profunidade<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

'''
  @brief  Busca em profunidade para usar no algoritmo de ford-fulkerson,
          com ela podemos encontrar os pais do vértice raiz e poder realizar
          a busca pelo o menor caminho.

  @param[in] w Matriz de pesos que representa o grafo direcionado.
  @param[in] s Vértice raiz por onde a busca em profundidade irá percorrer.

  @return Vetor de descendência do vértice raiz ao mais profundo.

'''
def busca_em_profundidade(w,s):
  n = len(w)
  a = 0
  cor = [ 0 for i in range(n) ]
  pai = [ math.inf]*n
  BP_VISIT(w,s,pai,cor)

  return pai


'''
  @brief  BP_VISIT função no qual percorre cada vértice da aresta, armazena
          no vetor 'pai' de descendência e 'colore' o vetor 'cor' com preto ou
          cinza.

  @param[in] w   Matriz de pesos que representa o grafo direcionado.
  @param[in] i   Vértice no qual será verificado para ver seus descendentes.
  @param[in] pai Vetor que irá armazenar a descendência ao vértice raiz.
  @param[in] cor Vetor que irá mostrar um determinado vértices está percorrido
                 ou não, onde '0' representa a cor branca que indica que o vértice
                 não foi percorrido, '-1' representa a cor cinza que indica que o
                 vértice entrou em análise mas seus filhos não e '1' que representa
                 a cor preta que indica que o vértice já foi verifica junto com seus
                 descendentes.
  
'''
def BP_VISIT(w,i,pai,cor):
  
  n = len(w)
  cor[i] = -1
  for j in range(n):
    if(w[i,j] != math.inf and w[i,j] != 0):
      if(cor[j] == 0):
        pai[j] = i
        BP_VISIT(w,j,pai,cor)
  cor[i] = 1

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>Bellman-Ford<<<<<<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def init_single_source(w,s):

  d = [math.inf]*len(w)
  pai = [math.inf]*len(w)
  d[s] = 0
  return d,pai

def relax(d,pai,u,v,w):

  if d[v] > d[u] + w[u,v]:
    d[v] = d[u] + w[u,v]
    pai[v] = u

def bellman_ford(w,s):

  d,pai = init_single_source(w,s)

  for i in range(len(w)):
    for u in range(len(w)):
      for v in range(len(w)):
        relax(d,pai,u,v,w)

  for u in range(len(w)):
    for v in range(len(w)):
      if d[v] != math.inf:
        if d[v] > d[u] + w[u,v]:
            return False
  #print(pai)

  print("----------------------------")
  print("Caminhos a partir do vértice '0' ")

  for i in range(1,len(w)):
    aux = pai[i]
    p = []
    p.append(i)

    while aux != 0:
      p.append(aux)
      aux = pai[aux]
    p.append(0)
    p = p[::-1]
    #print(p)

    aux = p
    for i in range(len(aux)):
      if i == len(aux)-1:
        print("{}".format(aux[i]))
      else:
        print("{}->".format(aux[i]),end="")
        
  return True

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>Floyed-WarShall<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def floydWarshall(w):
  d = w.copy()
  n = len(w)

  for k in range(n):
    for i in range(n):
      for j in range(n):
        if (d[i,j] > (d[i,k] + d[k,j])):
          d[i,j] = d[i,k] + d[k,j]

  print("\n>>>>>FloydWarshall<<<<\n")
  print(d)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>Shortest-Fastest-Path<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def calcSTP(w,i,j,m):
  if i == j: return 0
  if m == 1: return w[i,j]
  c = math.inf

  for k in range(len(w)):
    if c > (calcSTP(w,i,k,m-1) + w[k,j]):
      c = calcSTP(w,i,k,m-1) + w[k,j]

  return c


def menorRecSTP(w):
  l = w.copy()

  for i in range(len(w)):
    for j in range(len(w)):
      l[i,j] = calcSTP(w,i,j,len(w))

  print("\n>>>>>menorRecSTP<<<<<\n")
  print(l)


def STP(l, w):
  nVertices = len(w)
  l2 = w.copy()
  
  for i in range(nVertices):
    for j in range(nVertices):
      if i != j:
        l2[i,j] = math.inf
      else:
        l2[i,j] = 0

  for i in range(nVertices):
    for j in range(nVertices):
      c = l[i,j]
      for k in range(nVertices):
        if c > (l[i,k] + l[k,j]):
          c = l[i,k] + l[k,j]
      l[i,j] = c

  return l    


def mainSTP(w):
  l = w.copy()

  for i in range(len(w)):
    l = STP(l,l)

  print("\n>>>>>mainSTP<<<<<<\n")
  print(l)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>Ford-Fulkerson<<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def fordfulkerson(w,s,t):
  f = w.copy()
  p = []
  fm = 0

  for i in range(len(w)):
    for j in range(len(w)):
      if f[i,j]==math.inf:
        f[i,j]=0

  while True:
    pai = []
    pai = busca_em_profundidade(f,s)

    if(pai[t] != math.inf):
      a = t
      p = []

      while(a != s): 
        p.append(a)
        a = pai[a]
      p.append(s)
      p = p[::-1]
      fc = math.inf

      for i in range(len(p)-1):
        if fc > f[p[i],p[i+1]]:
          fc = f[p[i],p[i+1]]
      fm+=fc

      for j in range(len(p)-1):
        f[p[j],p[j+1]]-=fc
        f[p[j+1],p[j]]+=fc

    else :
      break

  print("\n>>>>>>Ford-Fulkerson<<<<<<\n")
  print("\nFluxo máximo: {}\n".format(fm))
  print(np.transpose(f))      
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>Generic-Push-Relabel<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def push(c,f,e,u,v):
  d = min(e[u],c[u,v]-f[u,v])
  f[u,v] += d
  f[v,u] = -f[u,v]
  e[u] -= d
  e[v] += d

def relabel(c,f,h,u,n,):
  min_h = h[0]

  for v in range(n):
    if (c[u,v] - f[u,v]) != 0:
      if min_h > h[v]:
        min_h = h[v]
  h[u] = min_h+1      
  #print(h)

def init(w,s):
  f = w.copy()
  c = w.copy()
  n = len(w)
  h = [0]*n
  e = [0]*n

  for i in range(n):
    for j in range(n):
      f[i,j] = 0
      if c[i,j] == math.inf:
        c[i,j] = 0

  h[s] = n
  e[s] = math.inf

  for i in range(n):
    if c[s,i] != 0:
      f[s,i] = c[s,i]
      f[i,s] -= c[s,i]
      e[i] = c[s,i]
      e[s] -= c[s,i]

  return e,c,f,h,n

def generic(w,s,t):

  e,c,f,h,n = init(w,s)

  for j in range(n):
    for u in range(n):
      if e[u]>0 and u!=s and u!=t:
        relabel(c,f,h,u,n)
        for v in range(n):

          if (c[u,v]-f[u,v]) != 0:
            if h[u] == h[v] + 1:
              push(c,f,e,u,v)

  max_fluxo = 0
  for i in range(n):
    max_fluxo += f[i,t]

  print("\n>>>>>Generic-Push-Relabel<<<<<<\n")
  print("\nFluxo máximo: {}\n".format(max_fluxo))
  print(f)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>Função Principal<<<<<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

w = matrizPesos()

#Exibir os caminhos do grafo
print("\n")
if bellman_ford(w,0):
  print("O Grafo não possui circuito negativo")
else:
  print("O Grafo possui circuito negativo")

print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print("> ALGORITMOS DE CAMINHOS MÍNIMOS PARA VÁRIOS VÉRTICES <")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

floydWarshall(w)
mainSTP(w)
menorRecSTP(w)

print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
print(">>>>>>>>> ALGORITMOS DE FLUXO MÁXIMO <<<<<<<<<<<<<<")
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

fordfulkerson(w,0,5)
generic(w,0,5)