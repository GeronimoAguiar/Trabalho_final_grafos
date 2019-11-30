1) Instalar o gerenciador de pacotes do python3 (pip), segue o link abaixo:
			->https://sempreupdate.com.br/como-instalar-o-pip-no-ubuntu/
2) Instalar biblioteca Numpy, pelo seguinte comando: 
				->sudo pip install numpy
3) Adicionar aquivo do grafo em ".txt" no diretório "exemplo_de_grafos" e adicionar o nome do seu arquivo na linha 72;
	->ex: arquivo = open("exemplos_de_grafos/nome_do_seu_arquivo.txt","r")[se encontra na linha 72]
4) Rodar o comando no mesmo diretório do código:
		->python grafo.py
5) Caso na segunda linha do arquivo ".txt" exista apenas um valor, a saída serão todos os menores caminhos de "s" até todos os outros vértices, seguido das matrizes de menores caminhos obtidas por cada um dos algoritmos;
6) Caso tenham dois valores a saída seram o fluxo máximo de "s" até "t" e as respectivas matrizes de fluxo obtidas por cada algoritmo.
