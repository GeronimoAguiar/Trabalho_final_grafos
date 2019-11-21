import math
import numpy as np

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>Matriz de Pesos<<<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def matrizPesos():
  arquivo = open("grafo_youtube.txt","r")    
  texto = arquivo.readlines()
  arquivo.close()
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

  print(w)
  return w
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>Floyed-WarShall<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def floydWarshall(w):
  d = w
  n = len(w)

  for k in range(n):
    for i in range(n):
      for j in range(n):
        if (d[i,j] > (d[i,k] + d[k,j])):
          d[i,j] = d[i,k] + d[k,j]
  print(d)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>Shortest-Fastest-Path<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def calcSTP(w,i,j,m):
  if i == j: return 0
  if m == 1: return w[i,j]
  c = math.inf
  for k in range(len(w)):
    if c > (calcSTP(w,k,j,m-1) + w[k,j]):
      c = calcSTP(w,k,j,m-1) + w[k,j]
  return c


def menorRecSTP(w):
  l = w
  for i in range(len(w)):
    for j in range(len(w)):
      l[i,j] = calcSTP(w,i,j,len(w))
  return l


def STP(l, w):
  nVertices = len(w)
  l2 = np.zeros( (nVertices,nVertices) )
  for i in range(0,nVertices):
    for j in range(0,nVertices):
      if i != j:
        l2[i,j] = math.inf

  for i in range(nVertices):
    for j in range(nVertices):
      c = math.inf
      for k in range(nVertices):
        if c > (l[i,k] + w[k,i]):
          c = l[i,k] + w[k,i]
    l2[i,j] = c

  return l2    


def mainSTP(w):
  l = w
  for i in range(1, len(w)):
    l = STP(l,w)
  print(l)
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>>>Ford-Fulkerson<<<<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
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
      print(p)
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
  print(fm)
  print(np.transpose(f))      
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>Busca em profunidade<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def busca_em_profundidade(w,s):
  n = len(w)
  a = 0
  cor = [ 0 for i in range(n) ]
  pai = [ math.inf]*n
  BP_VISIT(w,s,pai,cor)

  return pai

def BP_VISIT(w,i,pai,cor):
  n = len(w)
  cor[i] = -1
  for j in range(n):
    if(w[i,j] != math.inf and w[i,j] != 0):
      if(cor[j] == 0):
        pai[j] = i
        BP_VISIT(w,j,pai,cor)
  cor[i] = 1

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>Função Principal<<<<<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
w = matrizPesos()
print("\n")

#1-
floydWarshall(w)
#2-
mainSTP(w)
#3-
fordfulkerson(w,0,4)