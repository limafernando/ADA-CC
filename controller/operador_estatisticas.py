# Biblioteca para centralizar requisições de cálculos estatísticos

from statistics import mean, median, mode, stdev, variance

def exibe_estatisticas(conteudo):
    """Dada uma lista de dados, por exemplo, tempo ou cra, exibe os dados estatísticos
    
    Arguments:
        conteudo {list} -- lista de dados, por exemplo, tempo ou cra
    """
    
    print('mínimo: {} \nmáximo: {}'.format(min(conteudo), max(conteudo)))
    
    try:
        print('média: {} \nmediana: {}  \nmoda: {} \ndesvia padrão: {} \nvariância: {}'.format(mean(conteudo), median(conteudo), mode(conteudo), stdev(conteudo), variance(conteudo)))
    except:
        print('!mais de um valor pra moda!')
        print('média: {} \nmediana: {}  \ndesvio padrão: {} \nvariância: {}'.format(mean(conteudo), median(conteudo), stdev(conteudo), variance(conteudo)))


def calcula_porcentagem(universo, amostra):
    """Função "genérica" para calcular a porcentagem
    
    Arguments:
        universo {int} -- universo da probabilidade
        amostra {int} -- amostra da probabilidade

    Returns:
        float -- retorna a porcentagem calculada entre a amostra e o universo
    """

    return amostra/universo