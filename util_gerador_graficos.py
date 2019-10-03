import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def plot_ditribuicao_alunos(alunos):
    
    alunos = list(map(lambda x: float(x*100), alunos))
    alunos = list(map(lambda x: round(x, 1), alunos))
    
    semestres = list(map(lambda x: alunos.index(x)+1, alunos))

    semestres = len(alunos)
    aux_list = []
    
    for i in range(semestres):
        aux_list.append(i+1)

    semestres = aux_list

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
    
    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 0),  
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)

    fig.tight_layout()

    plt.show()