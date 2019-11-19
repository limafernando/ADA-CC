# Biblioteca para centralizar requisições de geração de gráficos

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def autolabel(rects, ax):
    """Função auxiliar para gerar os gráficos de barra
    
    Arguments:
        rects -- Atributo bar do objeto ax
        ax -- Objeto plt.subplots()
    """

    #Attach a text label above each bar in *rects*, displaying its height

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 0),  
                    textcoords="offset points",
                    ha='center', va='bottom')

def plot_distruicao_disciplinas(disciplinas, iacrs):
    """Função para gerar o gráfico que mostra os IACRs das disciplinas, por semestre recomendado
    
    Arguments:
        disciplinas {list} -- Lista de disciplinas recomendadas em um semestre
        iacrs {list} -- Lista de IACRs para cada disciplina 
        Os índices da lista de disciplinas devem ser correspondentes aos índices da lista de IACRs
    """

    x = np.arange(len(disciplinas))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()

    rects1 = ax.bar(x , iacrs, width)#, label='Men')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('IACRs (%)')
    ax.set_title('IACRs por disciplina')
    ax.set_xticks(x)
    ax.set_xticklabels(disciplinas)
    ax.set(ylim=(0, 100))
    #ax.legend()

    autolabel(rects1, ax)

    fig.tight_layout()

    plt.show()

def plot_ditribuicao_alunos(alunos):
    """Função para gerar o gráfico que mostra a distribuição que os alunos fazem das 
    disciplinas pelos semestres diferentes do semestre recomendado
    
    Arguments:
        alunos {list} -- Lista com a proporção de alunos por semestre, cada índice representa um semestre (ínidice 0 = semestre 1)
    """

    alunos = list(map(lambda x: float(x*100), alunos))
    alunos = list(map(lambda x: round(x, 1), alunos))
    
    semestres = list(map(lambda x: alunos.index(x)+1, alunos))

    x = np.arange(len(semestres))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()

    rects1 = ax.bar(x , alunos, width)#, label='Men')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Quantidade de alunos (%)')
    ax.set_title('Quantidade de alunos por semestre')
    ax.set_xticks(x)
    ax.set_xticklabels(semestres)
    ax.set(ylim=(0, 100))
    #ax.legend()

    autolabel(rects1, ax)

    fig.tight_layout()

    plt.show()