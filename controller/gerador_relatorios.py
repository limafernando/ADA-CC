import sys

sys.path.insert(1, '/home/luiz/ufpb/tcc/ADA.CC/src/')

from controller import controlador_dados

def relatorio_repeticao_em_disciplinas(matriculas_discentes, codigos_disciplinas, relacao_discente_matriculas, disciplinas):
    
    relatorio = open('checagem de repetição em disciplina.txt', 'r+')

    if relatorio.readlines():
        print('ARQUIVO JÁ EXISTE!!!')
        relatorio.close()

    else:
        
        for matricula in matriculas_discentes:
            
            relatorio.write('Analisando matriculas do aluno {}\n\n'.format(matricula))

            relacao = relacao_discente_matriculas[matricula]

            for disciplina in codigos_disciplinas:

                aux = relacao[relacao['codigo_componente'] == disciplina]

                if not aux.empty:

                    nome = disciplinas[disciplinas['codigo'] == disciplina]['nome'].iloc[0]

                    relatorio.write('Matricula na disciplina {} de código {}\n\n'.format(nome, disciplina))

                    #print(aux)

                    relatorio.write('O aluno se matriculou {} vez(es)\n\n'.format(aux.count().iloc[0]))

                    relatorio.write(aux.to_string())

                    relatorio.write('\n\n')

            relatorio.write('-------------------------------------------------------\n\n')

        relatorio.close()

        print('Relatório gerado')

def relatorio_alunos_rec_nao_rec(discentes_depois, codigos_disciplinas, matriculas_realizadas, matriculas_discentes, disciplinas):
    
    relatorio = []

    for codigo in codigos_disciplinas:
        
        relatorio_disciplina = {'nome': None, 'rec': None, 'nao_rec': None, 'alunos_nao_rec': []}

        aux = matriculas_realizadas[matriculas_realizadas['codigo_componente'] == codigo]

        disciplina = disciplinas[disciplinas['codigo'] == codigo]['nome'].iloc[0]

        periodo_recomendado = int(disciplinas[disciplinas['codigo'] == codigo]['semestre'].iloc[0])

        relatorio_disciplina['nome'] = disciplina

        matriculas = aux.count().iloc[0]
            
        #matriculas = 1

        rec = 0
        nao_rec = 0
        
        alunos_nao_rec = []

        for row in aux.iterrows():

            #print(row[1])
            #print()

            aluno = row[1]['matricula']

            if aluno not in matriculas_discentes:
                matriculas -= 1
                continue

            else:
                    
                periodo_matricula = row[1]['periodo_matricula']
                periodo_ingresso = discentes_depois[discentes_depois['matricula'] == aluno]['periodo_ingresso'].iloc[0]

                periodo_cursou = controlador_dados.retorna_tempo_graduacao(periodo_ingresso, periodo_matricula)

                #print('rec: {} matri: {} ingre: {} cursou: {}'.format(periodo_recomendado, periodo_matricula, periodo_ingresso, periodo_cursou))

                if periodo_cursou == periodo_recomendado:
                    rec += 1

                else:
                    nao_rec += 1
                    alunos_nao_rec.append(aluno)
                        
                #matriculas += 1
        
        relatorio_disciplina['rec'] = rec/matriculas
        relatorio_disciplina['nao_rec'] = nao_rec/matriculas
        relatorio_disciplina['alunos_nao_rec'] = alunos_nao_rec
        print(matriculas)
        
        relatorio.append(relatorio_disciplina)

    return relatorio

def relatorio_alunos_disciplina(codigos_disciplinas, matriculas_realizadas, disciplinas, matriculas_discentes):
    
    relatorio = []

    for codigo in codigos_disciplinas:
        
        relatorio_disciplina = {'nome': None, 'alunos': []}

        aux = matriculas_realizadas[matriculas_realizadas['codigo_componente'] == codigo]

        disciplina = disciplinas[disciplinas['codigo'] == codigo]['nome'].iloc[0]

        relatorio_disciplina['nome'] = disciplina

        matriculas = aux.count().iloc[0]
        
        alunos = []

        for row in aux.iterrows():

            #print(row[1])
            #print()

            aluno = row[1]['matricula']

            if aluno not in matriculas_discentes:
                matriculas -= 1
                continue

            else:
                    
                alunos.append(aluno)

        relatorio_disciplina['alunos'] = alunos
        print(matriculas)
        
        relatorio.append(relatorio_disciplina)

    return relatorio