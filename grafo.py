import math
import numpy as np

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>>>>>>>>Matriz de Pesos<<<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def matrizPesos():
  arquivo = open("grafo_exemplo.txt","r")    
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
  d = w.copy()
  n = len(w)

  for k in range(n):
    for i in range(n):
      for j in range(n):
        if (d[i,j] > (d[i,k] + d[k,j])):
          d[i,j] = d[i,k] + d[k,j]
  print("floydWarshall")
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
    if c > (calcSTP(w,i,k,m-1) + w[k,j]):
      c = calcSTP(w,i,k,m-1) + w[k,j]
  return c


def menorRecSTP(w):
  l = w.copy()
  for i in range(len(w)):
    for j in range(len(w)):
      l[i,j] = calcSTP(w,i,j,len(w))
  print("menorRecSTP")
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
  print("mainSTP")
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
  print(pai)
  for i in range(1,len(w)):
    aux = pai[i]
    p = []
    p.append(i)
    while aux != 0:
      p.append(aux)
      aux = pai[aux]
    p.append(0)
    p = p[::-1]
    print(p)
  
  return True










#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>>>>>>>>>>>>Função Principal<<<<<<<<<<<<<<<<<<<<<<<<
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
w = matrizPesos()
print("\n")

#1-
#floydWarshall(w)
#2-
#mainSTP(w)
#3-
#fordfulkerson(w,0,4)
#print(bellman_ford(w,0))
menorRecSTP(w)
mainSTP(w)