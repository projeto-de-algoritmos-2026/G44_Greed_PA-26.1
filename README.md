# Rota Solidaria

Conteudo da Disciplina: Algoritmos Ambiciosos

## Sobre

Rota Solidaria e um projeto em Python/Tkinter sobre uma cozinha comunitaria que precisa entregar marmitas em bairros da cidade com combustivel limitado.

Cada bairro tem uma quantidade de familias esperando atendimento. A pergunta principal e simples:

> Para onde o caminhao deve ir agora para ajudar mais gente gastando menos combustivel?

O algoritmo ambicioso responde escolhendo sempre o bairro com a melhor relacao:

```txt
familias atendidas / distancia ate o bairro
```

Assim, a cada passo o sistema toma uma decisao local que parece a melhor naquele momento.

## Por que e facil de explicar

- O caminhao tem combustivel limitado.
- Cada bairro tem uma demanda visivel no mapa.
- Cada rua tem uma distancia.
- O algoritmo escolhe o bairro que entrega mais impacto por custo.
- A interface mostra a rota escolhida, o combustivel gasto e o diario das decisoes.

## Tecnica utilizada

O projeto usa uma estrategia gulosa inspirada em mochila/beneficio por custo:

1. Calcula a menor distancia da posicao atual ate cada bairro ainda nao atendido.
2. Remove candidatos que nao cabem no combustivel restante.
3. Ordena os bairros por maior `familias / distancia`.
4. Escolhe o melhor candidato.
5. Move o caminhao, gasta combustivel e marca o bairro como atendido.

O calculo da menor distancia usa Dijkstra como apoio, pois o mapa tem ruas com pesos. A decisao principal do projeto, porem, e ambiciosa: escolher sempre o melhor beneficio imediato.

## Funcionalidades

- Interface grafica em Tkinter.
- Mapa com bairros, ruas e distancias.
- Modo manual com setas, WASD e botoes direcionais.
- Botao para executar um passo guloso.
- Botao para resolver a rota inteira.
- Painel com combustivel, familias atendidas, proxima melhor escolha e diario.
- Modo terminal para apresentacao rapida.
- Testes unitarios da logica.

## Como executar

Linguagem: `Python 3.8+`

Biblioteca: `Tkinter`, normalmente incluida no Python.

```bash
python main.py
```

Modo terminal:

```bash
python main.py --terminal
```

Testes:

```bash
python -m unittest discover -v
```

## Controles

- `Setas` ou `W`, `A`, `S`, `D`: movem o caminhao manualmente pelas ruas.
- `Espaco`: executa um passo guloso.
- `R`: reinicia a simulacao.
- Botoes direcionais na tela: alternativa para jogar com mouse.

## Estrutura

```text
.
|-- main.py
|-- src
|   |-- algorithms.py
|   |-- config.py
|   |-- data.py
|   |-- models.py
|   |-- planner.py
|   |-- ui.py
|   `-- __init__.py
`-- tests
    |-- test_algorithms.py
    `-- __init__.py
```
