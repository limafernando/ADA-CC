'''
Biblioteca para centralizar requisições recorrentes à base de dados
'''

from statistics import mean, median, mode, stdev, variance

def exibe_estatisticas(conteudo):
    '''
    dada uma lista de dados, por exemplo, tempo ou cra, exibe os dados estatísticos
    '''
    print('mínimo: {} \nmáximo: {}'.format(min(conteudo), max(conteudo)))
    
    try:
        print('média: {} \nmediana: {}  \nmoda: {} \ndesvia padrão: {} \nvariância: {}'.format(mean(conteudo), median(conteudo), mode(conteudo), stdev(conteudo), variance(conteudo)))
    except:
        print('!mais de um valor pra moda!')
        print('média: {} \nmediana: {}  \ndesvio padrão: {} \nvariância: {}'.format(mean(conteudo), median(conteudo), stdev(conteudo), variance(conteudo)))


def calcula_porcentagem(universo, amostra):
    '''
    função "genérica" para calcular a porcentagem
    '''
    
    return amostra/universo