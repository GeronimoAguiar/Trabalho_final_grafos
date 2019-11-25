'''
                    UNIVERSIDADE FEDERAL DO CEARÁ  
                            CAMPUS SOBRAL
                  CURSO DE ENGENHARIA DE COMPUTAÇÃO
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
  arquivo = open("exemplo_de_grafos/grafo_tcc.txt","r")    

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

  try:
      vSorv = int(texto[1].split()[1])
      return w,vPai,vSorv,nVertices
  except IndexError: 
      return w,vPai,nVertices
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

'''
  @brief  Função que cria o vetor de descendência 'pai' para armazenar os filhos
          vértice raiz e o vetor 'd' que armazena os pesos das arestas.

  @param[in] w   Matriz de pesos que representa o grafo direcionado.
  @param[in] s   Vértice raiz.

  return pai  Vetor de descendência do vértice 's' até o ultimo ou mais profundo.
  return  d   Vetor de peso dos vértices que auxilía na procura de circuitos negativos.
  
'''
def init_single_source(w,s):

  d = [math.inf]*len(w)
  pai = [math.inf]*len(w)
  d[s] = 0
  return d,pai


'''
  @brief  Função que aplica o relaxamento dos vértices no algoritmo de bellman-ford.

  @param[in]  d    Vetor de peso dos vértices que auxilía na procura de circuitos negativos.
  @param[in] pai   Vetor de descendência do vértice 's' até o ultimo ou mais profundo.
  @param[in]  u    Vértice de 'inicio' para reprensentar a aresta (u,v)
  @param[in]  v    Vértice de 'fim' para representar a aresta (u,v)
  @param[in]  w    Matriz de pesos que representa o grafo direcionado.

  
'''
def relax(d,pai,u,v,w):

  if d[v] > d[u] + w[u,v]:
    d[v] = d[u] + w[u,v]
    pai[v] = u

'''
  @brief  Algoritmo de Bellman-Ford para busca de menor caminho a partir de um grafos com pesos
          negativos ou positivos. Caso haja circutos negativos, o procedimento eh capaz de noti-
          ficar.

  @param[in]  w    Matriz de pesos que representa o grafo direcionado.
  @param[in]  s   Vértice raiz.

  return Booleano 'True' para caso o algoritmo não possua ciclo negativo.
                  'False' para caso o algoritmos possua ciclo negativo.
'''
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

  print("----------------------------")
  print("Caminhos a partir do vértice '{}' ".format(s))
 
  for i in range(len(w)):
    if i!=s and pai[i] != math.inf:
      aux = pai[i]
      p = []
      p.append(i)

      while aux != s:
        p.append(aux)
        aux = pai[aux]
      p.append(s)
      p = p[::-1] 
      aux = p
      for i in range(len(aux)):
        if i == len(aux)-1:
          print("{}".format(aux[i]))
        else:
          print("{}->".format(aux[i]),end="")
        
  return True

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

'''
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||
||||||||| ALGORITMOS DE CAMINHOS MINIMOS PARA |||||||||||
||||||||||   TODOS OS PARES DE VÉRTICES |||||||||||||||||
|||||||||||||||||||||||||||||||||||||||||||||||||||||||||
'''

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>Floyed-WarShall<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

'''

  @brief  Algoritmo que resolve o problema de calcular o
          caminho mais curto entre todos os pares de vértices
          em um grafo orientado (com direção) e valorado (com
          peso). 

  @param[in]  w  Matriz de pesos que representa o grafo direcionado.

  return d A matriz de menores distância para todos os pares
           de vértices.
'''
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


'''
  @brief   Função para multiplicação das matrizes.

  @param[in]  w  Matriz de pesos que representa o grafo direcionado.
  @param[in]  i  Vértice de 'inicio' que representa junto com j a aresta (i,j).
  @param[in]  j  Vértice de 'fim' que representa junto com i a aresta (i,j).
  @param[in]  m  Número de interações do algortimo.

  return c  Constante que armazena o valor do menor pesos da aresta do caminho
  de i -> j
'''
def calcSTP(w,i,j,m):
  if i == j: return 0
  if m == 1: return w[i,j]
  c = math.inf

  for k in range(len(w)):
    if c > (calcSTP(w,i,k,m-1) + w[k,j]):
      c = calcSTP(w,i,k,m-1) + w[k,j]

  return c

'''
  @brief   Função que calcula o menor caminho de todos os pares de vértices,
           calcula os pesos de caminhos curtos estendendo os caminhos mais
           curtos aresta por aresta.

  @param[in]  w  Matriz de pesos que representa o grafo direcionado.

  return l Matriz que de atualização dos pesos das arestas para os
           menores caminhos.
'''
def menorRecSTP(w):
  l = w.copy()

  for i in range(len(w)):
    for j in range(len(w)):
      l[i,j] = calcSTP(w,i,j,len(w))

  for i in range(len(w)):
    for j in range(len(w)):
      l[i,j] = calcSTP(w,i,j,len(w))

  print("\n>>>>>menorRecSTP<<<<<\n")
  print(l)


'''
  @brief   

  @param[in]  l  Matriz que de atualização dos pesos das arestas
                 para os menores caminhos.
  @param[in]  w  Matriz de pesos que representa o grafo direcionado.
  
  return l Matriz que de atualização dos pesos das arestas para os
           menores caminhos.
'''
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

'''
  @brief   

  @param[in]  w  Matriz de pesos que representa o grafo direcionado.

  return l Matriz que de atualização dos pesos das arestas para os
           menores caminhos.
'''
def mainSTP(w):

  l = w.copy()
  for i in range(len(w)):
    l = STP(l,l)

  l = w.copy()

  for i in range(len(w)):
    l = STP(l,l)

  print("\n>>>>>mainSTP<<<<<<\n")
  print(l)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

'''
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||| ALGORITMOS DE FLUXO MÁXIMO ||||||||||||||||
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
'''

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>Ford-Fulkerson<<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

'''
  @brief   Algoritmo utilizado para resolver problemas de 
           fluxo em rede (network flow). O algoritmo é empregado 
           quando se deseja encontrar um fluxo de valor máximo 
           que faça o melhor uso possível das capacidades
           disponíveis na rede em questão.

  @param[in]  w  Matriz de pesos que representa o grafo direcionado.
  @param[in]  s  Vértice que simboliza a fonte do fluxo.
  @param[in]  t  Vértice que simboliza o sorverdouro do fluxo.

  return f    A matriz que representa os pesos das arestas e a orientação
              delas no grafo de fluxo.
  return fm   Variavel que armazena o fluxo máximo do grafo.
'''
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

'''
  @brief   A operação push se aplica uma aresta (u,v) de um
           vétice u em w. Move min {e[u], c[u,v] - f[u,v]}
           unidades de fluxo de u para v.

  @param[in]  c  Matriz de capacidade do grafo.
  @param[in]  f  Matriz de fluxo do grafo.
  @param[in]  e  Vetor de excesso dos vértices.
  @param[in]  u  Vértice de 'inicio' que representa junto com v uma aresta (u,v).
  @param[in]  v  Vértice de 'fim' que representa junto com u uma aresta (u,v).
'''
def push(c,f,e,u,v):
  d = min(e[u],c[u,v]-f[u,v])
  f[u,v] += d
  f[v,u] -= d
  e[u] -= d
  e[v] += d

'''
  @brief   A operação de relabel se aplica a um vértice u, 
           sem quaisquer arestas admissíveis em w. Ele modifica h[u]
           para ser o valor mínimo tal que uma aresta admissíveis é
           criada. Observe que isso sempre aumenta h[u] e nunca cria
           uma aresta 'ingreme', que é uma aresta [u,v] tal que c[u,v]>0
           e h[u]>h[v]+1.

  @param[in]  c  Matriz de capacidade do grafo.
  @param[in]  f  Matriz de fluxo do grafo.
  @param[in]  h  Vetor de altura do vértices.
  @param[in]  u  Vértice de 'inicio' que representa junto com v uma aresta (u,v).
  @param[in]  n  Número de vértice do grafo.
'''
def relabel(c,f,h,u,n):
  min_h = math.inf

  for v in range(n):
    if (c[u,v] - f[u,v]) > 0:
      if min_h > h[v]:
        min_h = h[v]
  h[u] = min_h+1      


'''
  @brief  O algoritmo genérico de push-relabel utiliza a sub-rotina a seguir
          para criar um pré-fluxo inicial no fluxo em rede.

  @param[in]  w  Matriz de pesos que representa o grafo direcionado.
  @param[in]  s  Vértice que simboliza a fonte do fluxo.

  return  c  Matriz de capacidade do grafo.
  return  f  Matriz de fluxo do grafo.
  return  e  Vetor de excesso dos vértices.
  return  h  Vetor de altura do vértices.
  return  n  Número de vértice do grafo.
'''
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

'''
  @brief   Algoritmo para calcular fluxos máximos em uma rede de fluxo.
           O nome "push-relabel" vem das duas operações básicas usadas 
           no algoritmo. Ao longo de sua execução, o algoritmo mantém um 
           "pré-fluxo" e gradualmente o converte em um fluxo máximo, movendo 
           o fluxo localmente entre nós vizinhos, usando operações push, sob 
           a orientação de uma rede admissível mantida por operações de remarcação.

  @param[in]  w  Matriz de pesos que representa o grafo direcionado.
  @param[in]  s  Vértice que simboliza a fonte do fluxo.
  @param[in]  t  Vértice que simboliza o sorvedouro do fluxo.
  
  return f           A matriz que representa os pesos das arestas e a orientação
                     delas no grafo de fluxo.
  return max_fluxo   Variavel que armazena o fluxo máximo do grafo.
'''
def generic_pushRelabel(w,s,t):

  e,c,f,h,n = init(w,s)
  for j in range(n*n):
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
  m = f.copy()
  print("\n>>>>>Generic-Push-Relabel<<<<<<\n")
  print("\nFluxo máximo: {}\n".format(max_fluxo))
  print(f)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

'''
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
|||||||||||||||||||||| FUNÇÃO PRINCIPAL ||||||||||||||||||||||
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
'''

#Armazenar a matriz de pesos e orientação do grafo

try:
  w,vPai,vSorv,nVertices = matrizPesos()
  print(">>>>>>>Matriz de Pesos<<<<<<<<")
  print("\nNúmero de vértices-> {}".format(nVertices))
  print("Vértice fonte-> {}".format(vPai))
  print("Vértice soverdouro-> {}\n".format(vSorv))
  print(w)
  
  print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
  print(">>>>>>>>> ALGORITMOS DE FLUXO MÁXIMO <<<<<<<<<<<<<<")
  print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

  fordfulkerson(w,vPai,vSorv)
  generic_pushRelabel(w,vPai,vSorv)

except:
  w,vPai,nVertices = matrizPesos()
  print(">>>>>>>Matriz de Pesos<<<<<<<<")
  print("\nNúmero de vértices-> {}".format(nVertices))
  print("Vértice raiz-> {}\n".format(vPai))
  
  print(w)  
  
  if bellman_ford(w,vPai):
    print("O Grafo não possui circuito negativo")

    print("\n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("> ALGORITMOS DE CAMINHOS MÍNIMOS PARA VÁRIOS VÉRTICES <")
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    floydWarshall(w)
    mainSTP(w)
    menorRecSTP(w)

  else:
    print("O Grafo possui circuito negativo")


print("\n")

