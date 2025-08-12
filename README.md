# Modelagem de Epidemias: Uma Abordagem com Autômatos Celulares e Análise Fractal

[![📄 Scientific Report](https://img.shields.io/badge/📄_Scientific_Report-Disponível-blue?style=for-the-badge)](https://github.com/rbrtotavio/EpidemCellAuto/tree/master/paper)

> **Nota:** O **artigo científico** completo deste projeto, no formato *Scientific Reports*, está disponível na pasta [`paper/`](https://github.com/rbrtotavio/EpidemCellAuto/tree/master/paper).

## Resumo

Este projeto de pesquisa acadêmica explora a dinâmica de epidemias utilizando um modelo de autômatos celulares (CA) baseado em agentes. Diferentemente de modelos compartimentais clássicos que assumem uma mistura populacional homogênea, esta abordagem simula a propagação de uma doença (modelo SEIR) em uma grade esparsa e dinâmica. Os indivíduos, que representam a população ativa, podem se mover de forma estocástica, permitindo a análise de interações locais e do impacto do distanciamento social.

A principal contribuição deste trabalho é a análise quantitativa da complexidade espacial da epidemia. Para isso, o modelo calcula a dimensão de box-counting no pico da infecção, uma métrica de geometria fractal que oferece um novo insight sobre a eficácia das intervenções não farmacêuticas.

## Estrutura do Projeto

O projeto está organizado na seguinte estrutura de diretórios para garantir a modularidade e a replicabilidade dos experimentos:


```
.
├── data/                  # Armazena dados de entrada e saída
    ├── processed/         # Amostras de simulações
│   ├── raw/               # Parâmetros de simulação (parameters.json)
│   └── results/           # Resultados de cada simulação (.csv, .gif, .json)
├── notebooks/             # Ambiente de trabalho principal (analysis.ipynb)
├── paper/                 # Arquivos para a redação do artigo científico (.tex, .bib)
├── src/                   # Código-fonte do modelo e das utilidades
│   ├── model.py           # Definição da classe EpidemiaCA e regras do modelo
│   ├── simulation.py      # Lógica para executar e salvar simulações
│   └── utils.py           # Funções de visualização e análise (box-counting)
├── venv/                  # Ambiente virtual do Python
├── .gitignore             # Arquivo de regras para o Git
└── requirements.txt       # Lista de dependências do Python
```

## Replicabilidade e Dependências

Para garantir a replicabilidade dos experimentos, o projeto utiliza um ambiente virtual e o controle explícito da aleatoriedade.

1. **Configurar o Ambiente Virtual**: Recomenda-se a criação de um ambiente virtual para isolar as dependências do projeto, como detalhado em `requirements.txt`.
    ```bash
    python -m venv venv
    ```
    Ative o ambiente virtual:
    - No Windows: `venv\Scripts\activate`
    - No macOS/Linux: `source venv/bin/activate`

2. **Instalar as Dependências**: As bibliotecas necessárias estão listadas no arquivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## Uso e Análise

A interface principal do projeto é o `Jupyter Notebook`, localizado em `notebooks/analysis.ipynb`.

1. **Executar a Simulação**: Abra o notebook e use os widgets interativos para ajustar os parâmetros do modelo. Ao clicar no botão "Iniciar Simulação", o notebook executará a simulação e exibirá os resultados.
2. **Análise de Resultados**: Após cada execução, os resultados são salvos de forma permanente no diretório `data/results/` com um identificador único. Os dados incluem um arquivo `.csv` com as contagens de estados e um arquivo `.json` com os parâmetros exatos e o valor da dimensão de box-counting. A animação da grade é salva como um arquivo `.gif`.

## Parâmetros-Chave do Modelo

O modelo permite a exploração de múltiplos cenários através dos seguintes parâmetros:

* `population_density`: Porcentagem da grade ocupada por indivíduos. Simula o impacto da densidade populacional.
* `movement_rate`: Probabilidade de um indivíduo se mover em cada passo de tempo. Simula a mobilidade na população.
* `exposed_time`: Duração do período latente (de exposição), uma característica do modelo SEIR.
* `random_seed`: Valor inicial para o gerador de números aleatórios, garantindo a replicabilidade dos experimentos.

---

**Licença:** Este projeto é distribuído sob a Licença MIT.
