1) Instalar gerenciador de pacotes do python (pip);
2) Instalar biblioteca Numpy, pelo seguinte comando: 
	sudo pip install numpy
3) Adicionar aquivo do grafo em .txt no diret�rio 'exemplo_de_grafos' e adicionar o nome do seu arquivo na linha 72;
	ex: arquivo = open("exemplos_de_grafos/nome_do_seu_arquivo.txt","r")
4) rodar o comando no mesmo diret�rio do c�digo:
	python grafo.py
5) caso na segunda linha do arqiovo .txt tenha apenas um valor a saida ser� todos os menores caminhos de s at� todos os outros v�rtices,
seguido das matrizes de menores caminhos obtidas por cada um dos algoritmos;
6) caso tenha dois valores a saida ser� o fluxo m�ximo de s at� t e as respectivas matrizes de fluxo obtidas por cada algoritmo.