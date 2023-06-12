import streamlit as st
import random
from PIL import Image
import streamlit_authenticator as stauth
from datetime import date
from datetime import datetime
from util import string_to_datetime
from util import string_to_list
import pandas as pd
import mysql.connector

conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='Colaboradores'
)
mycursor = conexao.cursor()


st.set_page_config(page_title="Nova Avaliação",  page_icon=Image.open('icon.png'), layout="wide")
image = Image.open(('logo.png'))
st.image(image, width = 180)


sql = '''SELECT parametro_macro.macroprocesso, parametro_processo.processo, parametro_procedimento.procedimento
        FROM parametro_procedimento
        JOIN parametro_macro ON parametro_procedimento.macroProcesso = parametro_macro.id
        JOIN parametro_processo ON parametro_procedimento.processo = parametro_processo.id;'''

mycursor.execute(sql)
listDadosCAVA1 = mycursor.fetchall()


def get_chart_30507421(df):
    import plotly.express as px
    fig = px.treemap(df, path=[px.Constant("Cadeia de valor"), 'Macroprocesso', 'Processo', 'Procedimento'])
    fig.update_traces(root_color="#06405C")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))


    st.plotly_chart(fig, theme="streamlit",use_container_width = True)


def F_DadosUsuarios():
    comandoUsuarios = 'SELECT * FROM Usuarios;'
    mycursor.execute(comandoUsuarios)
    UsuariosBD = list(mycursor.fetchall())

    return UsuariosBD


dadosUser = F_DadosUsuarios()

def F_listDados2():
    sql = 'SELECT * FROM Colaboradores;'
    mycursor.execute(sql)
    listDados2 = list(mycursor.fetchall())

    return listDados2


listDados2 = F_listDados2()


def F_listDadosMP():
    sql = 'SELECT macroProcesso FROM parametro_macro;'
    mycursor.execute(sql)
    listDadosMP = [x[0] for x in list(mycursor.fetchall())]

    return(listDadosMP)

listDadosMP = F_listDadosMP()


def F_listDadosPRO():
    sql = 'SELECT id, processo FROM parametro_processo;'
    mycursor.execute(sql)
    listDadosPRO = [[x[0], x[1]] for x in (mycursor.fetchall())]

    return(listDadosPRO)

listDadosPRO = F_listDadosPRO()



def F_listDadosPC():
    sql = 'SELECT processo, procedimento FROM parametro_procedimento;'
    mycursor.execute(sql)
    listDadosPC = [[x[0], x[1]] for x in mycursor.fetchall()]

    return listDadosPC

listDadosPC = F_listDadosPC()



def F_listDadosUnidad():
    sql = "SELECT unidade FROM parametro_unidade;"
    mycursor.execute(sql)
    listDadosUnidad = [x[0] for x in list(mycursor.fetchall())]

    return listDadosUnidad

listDadosUnidad = F_listDadosUnidad()


def tratar_periodc(periodo):
    if str(periodo[0]) == '0':
        periodos = ['Trimestral']

    else:   
        periodos = periodo
    
    return periodos


def tratar_compt(list):
    if 'Orientação p/ Pessoas' in list:
        index_compt = [x for x in range(len(list)) if str(list[x]) == 'Orientação p/ Pessoas'][0]
        index_compt2 = index_compt + 1

        ajust_comp = f'{list[index_compt]}'+', '+f'{list[index_compt2]}'
        
        list[index_compt] = ajust_comp
        del list[index_compt2]

    return list


def string_para_lista(string):
    # Remove os espaços em branco no início e no final da string maior
    string = string.strip()

    # Remove as aspas no início e no final da string maior
    string = string.replace("'", "").strip()

    # Separa as strings menores em uma lista utilizando a vírgula como separador
    lista_strings = string.split(", ")

    # Retorna a lista resultante
    return lista_strings


def limparProcedim(lista_de_listas):
    lista_limpa = []
    for a in lista_de_listas:
        for b in range(len(a)):
            lista_limpa.append(a[b])

    return lista_limpa
    

def separar_valores(string):
    lista_valores = string.split(", ")
    lista_valores = [valor.strip("'") for valor in lista_valores]
    return lista_valores
    

def gerar_codAce():
    trava = True
    while trava:
        random_number = random.randrange(100, 999999)
        if random_number not in [x[11] for x in listDados2]:
            trava = False    

    return random_number


def transform_to_string(lista):
    # Junta os elementos da lista em uma única string separada por vírgulas
    string_com_virgulas = ', '.join(map(str, lista))
    return string_com_virgulas


names = [x[5] for x in dadosUser if x[5] != None]
usernames = [x[7] for x in dadosUser if x[7] != None]
hashed_passwords = [x[11] for x in dadosUser if x[8] != None]
funcao = [x[6] for x in dadosUser if x[6] != None]


def convert_to_dict(names, usernames, passwords):
    credentials = {"usernames": {}}
    for name, username, password in zip(names, usernames, passwords):
        user_credentials = {
            "email":username,
            "name": name,
            "password": password
        }
        credentials["usernames"][username] = user_credentials
    return credentials

credentials = convert_to_dict(names, usernames, hashed_passwords)
authenticator = stauth.Authenticate(credentials, "Teste", "abcde", 30)

col1, col2,col3 = st.columns([1,3,1])
with col2:
    name, authentication_status, username = authenticator.login('Acesse o sistema 9box', 'main')

if authentication_status == False:
    with col2:
        st.error('Email ou Senha Incorreto')
elif authentication_status == None:
    with col2:
        st.warning('Insira seu Email e Senha')
elif authentication_status:

    perfilUser = str([x[9] for x in dadosUser if x[7] == str(username) and x[7] != None])
    matricu_user = [x[4] for x in dadosUser if x[7] == str(username) and x[7] != None]
    perfilUser = perfilUser.upper()
                        
    tab1, tab2 = st.tabs(['Nova Avaliação', 'Avaliações Pendentes'])
    # Adiciona uma caixa de entrada
    st.write("---")
    
    with tab1:
        st.text(' ')
        st.subheader("Nova Avaliação")
        st.text(' ')

        col1, col2 = st.columns([4, 1])
        with col1:
            matricula = st.text_input("Nº Matrícula")
        st.text(' ')    
        st.text(' ')    
        st.text(' ')
        with col2:
            st.text(' ')    
            st.text(' ')
            #botao_new_avaliac = st.button('Criar Avaliação')
        
        if len(matricula) > 0:
    
            with st.expander('Cadeia de Valor'):
                get_chart_30507421({ "Macroprocesso" :[x[0] for x in listDadosCAVA1],
                                     "Processo" : [x[1] for x in listDadosCAVA1],
                                     "Procedimento" : [x[2] for x in listDadosCAVA1]})

            codAce = gerar_codAce()

            if matricula in [str(x[0]) for x in listDados2]:
                linhaBD = [x for x in range(len(listDados2)) if str(listDados2[x][0]) == matricula][0]
                dados_colab = listDados2[linhaBD]

                lista_padrão = [[dados_colab[1]] , [dados_colab[40]], [dados_colab[2]], [dados_colab[3]], separar_valores(dados_colab[4]), tratar_compt(string_para_lista(dados_colab[5])), separar_valores(dados_colab[6]), [dados_colab[7]], [dados_colab[9]], [dados_colab[8]], [dados_colab[10]], [date.today()], [date.today()], limparProcedim(string_to_list(dados_colab[49])), tratar_periodc([dados_colab[41]])]
                
                lista_padrão2 = [[' '],["Executor de Processos","Líder de Processos", "Dono de processo", "Gestor de Processos"],
                        listDadosUnidad,
                        listDadosMP,
                        [x[1] for x in listDadosPRO],
                        ["Orientação p/ Pessoas, Processos e Resultados", "Pensamento Crítico e Criativo",
                                        "Comunicação", "Foco no Cliente"],
                        ["Inteligência Emocional", "Autonomia e Proatividade", "Relacionamento e Network",
                                            "Futurabilidade", "Raciocínio Analítico", "Empreendedorismo", "Tomada de Decisão",
                                            "Visão Estratégica", "Visão Inovadora", "Liderança", "Comprometimento", "Negociação", "Habilidades Interpessoais"],
                        [''], [''], [''], [''],[date.today()], [date.today()], list(set([x[1] for x in listDadosPC])), ['Trimestral', 'Bimestral', 'Mensal']]
            elif matricula not in [str(x[0]) for x in listDados2]:
                lista_padrão = [[' '], 
                        ["Executor de Processos", "Líder de Processos", "Dono de processo", "Gestor de Processos"],
                        listDadosUnidad,
                        listDadosMP,
                        [],
                        ['Orientação p/ Pessoas, Processos e Resultados', 'Pensamento Crítico e Criativo', 'Comunicação', 'Foco no Cliente'],
                        [],
                        [''], [""], [""], [""],[date.today()], [date.today()], [], ['Trimestral', 'Bimestral', 'Mensal']]
                
                proces = [x[1] for x in listDadosPRO]
                proces.append("")
                
                proced = list(set([x[1] for x in listDadosPC]))
                proced.append('')
                
                comptObr = ["Orientação p/ Pessoas, Processos e Resultados", "Pensamento Crítico e Criativo",
                                        "Comunicação", "Foco no Cliente"]
                comptEsp = ["Inteligência Emocional", "Autonomia e Proatividade", "Relacionamento e Network",
                                            "Futurabilidade", "Raciocínio Analítico", "Empreendedorismo", "Tomada de Decisão",
                                            "Visão Estratégica", "Visão Inovadora", "Liderança", "Comprometimento", "Negociação", "Habilidades Interpessoais"]
                lista_padrão2 = [[' '],["Executor de Processos", "Líder de Processos", "Dono de processo", "Gestor de Processos"],
                        listDadosUnidad,
                        listDadosMP,
                        proces,comptObr,
                        comptEsp,
                        [''], [''], [''], [''],[date.today()], [date.today()], proced , ['Trimestral', 'Bimestral', 'Mensal']]
                            
            with st.form('Forms_new_avaliação'):
                col1, col2 = st.columns([2,1])
                colu1, colu2 = st.columns(2)


                with col1:
                    name = st.text_input("Nome Colaborador", lista_padrão[0][0])
                with col2:
                    funcao = st.selectbox('Função', lista_padrão2[1], [x for x in range(len(lista_padrão2[1])) if lista_padrão2[1][x] == lista_padrão[1][0]][0])
                with colu1:
                    Unidade = st.selectbox("Unidade de negócio", lista_padrão2[2], [x for x in range(len(lista_padrão2[2])) if lista_padrão2[2][x] == lista_padrão[2][0]][0])
                with colu2:
                    macroprocesso = st.selectbox('Macroprocesso', lista_padrão2[3], [x for x in range(len(lista_padrão2[3])) if lista_padrão2[3][x] == lista_padrão[3][0]][0], help="Em caso de dúvidas, Cadeia de Valor disponível na parte superior da página.")

                processo = st.multiselect('Processo', lista_padrão2[4], lista_padrão[4], help="Em caso de dúvidas, Cadeia de Valor disponível na parte superior da página.")
                procediment_padrão_total = list(lista_padrão2[13])
            
                var_aux = [procediment_padrão_total.append(x) for x in list(lista_padrão[13]) if x not in procediment_padrão_total]   
                procedimentos = st.multiselect('Procedimento',procediment_padrão_total, lista_padrão[13], help="Em caso de dúvidas, Cadeia de Valor disponível na parte superior da página.")
                
                st.subheader("Competências")
                
                SelComObg = st.multiselect("Obrigatórias", lista_padrão2[5], lista_padrão[5])
                competenEspEucatur = lista_padrão[6]
                SelComEsp = st.multiselect("Específicas", lista_padrão2[6], lista_padrão[6])
                st.write("---")
                st.subheader("Gestor de Carreira")
                col1, col2 = st.columns((2, 1))
                with col1:
                    gestorCarreira = st.text_input('Gestor de Carreira', lista_padrão[7][0])
                    avaliadorCarreira = st.text_input('Avaliador', lista_padrão[8][0])
                with col2:
                    matriculaGC = st.text_input("Nº Matrícula Gestor", lista_padrão[9][0])
                    matriculaAval = st.text_input("Nº Matrícula Avaliador", lista_padrão[10][0])
                
                periodicidad = st.selectbox('Periodicidade',lista_padrão2[14], index = int([x for x in range(len(lista_padrão2[14])) if lista_padrão2[14][x] in lista_padrão[14]][0]))
                if periodicidad == 'Trimestral':
                    day = 90
                elif periodicidad == 'Bimestral':
                    day = 60
                else: 
                    day = 30
                col1, col2 = st.columns(2)
                with col1:
                    dataIni = st.date_input('Data Inicio', lista_padrão[11][0])
                with col2:
                    dataFim = st.date_input('Data Fim', lista_padrão[12][0])
                butaoNovoAvaliac = st.form_submit_button('Criar')
                
                import datetime
    ############################ TRATAMENTO DOS DADOS ##########################################3##
                Data_Prox_Avalia = dataFim + datetime.timedelta(days=int(day))
                        
                processos_total = [[x[0], x[1]] for x in listDadosPRO if x[1] in processo]#FILTRO DE PROCESSOS DO USER
                
                number_processos_total = list(set([x[0] for x in processos_total]))                
                
                #TODOS OS PROCEDIMENTOS DOS PROCESSOS SELECIONADOS
                procedimentos_total = [[x[0], x[1]] for x in listDadosPC if x[0] in number_processos_total]#TODOS OS PROCEDIMENTOS REFERENTE AO PROCESSOS SELECIONADOS
                #NUMERO DE PROCEDIMENTOS
                number_procd_total = list(set([x[0] for x in procedimentos_total]))
                #NOME PROCEDIMENTO
                name_procedimentos_total = list(set([x[1] for x in procedimentos_total]))
                
                #PROCEDIMENTOS NÃO PRESENTES NOS PROCESSOS SELECIONADOS
                proced_not_in_process = [x for x in procedimentos if x not in name_procedimentos_total]
                #PROCEDIMENTOS PRESENTES
                proced_in_process = [x for x in procedimentos_total if x[1] in procedimentos]
                
                ####### FILTRANDO OS PROCESSOS PARA CASO TENHA ALGUM PROCESSO SEM PROCEDIMENTO#######
                numbers_procss_de_procd = [x[0] for x in procedimentos_total if x[1] in procedimentos]
                number_processos_not_proced = []
                for a in range(len(number_processos_total)):
                    if number_processos_total[a] not in numbers_procss_de_procd:
                        number_processos_not_proced.append(number_processos_total[a])
                
                #NOMES DE PROCESSOS SEM PROCEDIMENTOS
                nomes_proces_n_presents = [x[1] for x in processos_total if x[0] in number_processos_not_proced]
                ########PREPARANDO DF DE PROCEDIMENTOS VÁLIDOS
                procedimentos_validos = []
                for a in processos_total:
                    procd_valid_aux = [[a[1], x[1]] for x in procedimentos_total if x[0] == a[0]]
                            
                    procedimentos_validos.extend(procd_valid_aux)
                df_procd_validos = pd.DataFrame({'Processo Referência':
                                                        [x[0] for x in procedimentos_validos],
                                                        'Procedimento':[x[1] for x in procedimentos_validos]})
                #################################################################
                
                if butaoNovoAvaliac: 
                    st.write('---')  
                    data_avaliações = list(set([string_to_datetime(x[12]) for x in listDados2 if str(x[0]) == matricula]))    
                    if dataIni in data_avaliações: 
                        codAcessos_antigo = [int(x[11]) for x in listDados2 if int(x[0]) == int(matricula)]
                        
                        for linha in range(len(listDados2)):
                            if listDados2[linha][11] in codAcessos_antigo:
                                if str(listDados2[linha][12]) == str(dataIni):
                                    linha_Antig = linha
                        st.warning(f'Avaliação já criada para essa data. Realize a avaliação do colaborador com o código *{listDados2[linha_Antig][11]}*')
                    #SE A QUANTIDADE DE PROCEDIMENTOS ESCOLHIDOS FOR MAIOR QUE A QUANTIDADE DE PROCEDIMENTOS CORRETOS SABEMOS QUE TEM ALGO ERRADO
                    elif len([x for x in procedimentos if x != '']) > len(proced_in_process):
                        st.warning('No espaço *Procedimentos*, preencha o formulário com procedimentos que são referentes aos processos selecionados.')
                        st.text(' ')
                        procedimentos_invalidos = [x for x in proced_not_in_process if x != '']
                        
                        st.subheader('Procedimentos Incorretos:')
                        df_procd_invalidos = pd.DataFrame({
                        'Procedimentos':procedimentos_invalidos
                        })
                        st.table(df_procd_invalidos)
                        st.text(' ')
                        st.subheader('Opções de Procedimentos:')
                        st.table(df_procd_validos)
                    elif len(nomes_proces_n_presents) > 0:
                        if len(nomes_proces_n_presents) > 1:
                            st.warning(f'Os processos {transform_to_string(nomes_proces_n_presents)} não tem procedimentos vinculados. \nPor favor, antes de concluir a criação de uma avaliação, vincule um procedimento aos processos mencionados')
                        else:
                            st.warning(f'O processo {transform_to_string(nomes_proces_n_presents)} não tem procedimentos vinculados. \nPor favor, antes de concluir a criação de uma avaliação vincule um procedimento ao processo mencionado')
                        
                        st.text(' ')
                        st.subheader('Opções de Procedimentos:')
                        st.table(df_procd_validos)
                    elif int(0) in [len(processo), len(proced_in_process), len(SelComEsp), len(SelComEsp)]:
                        st.warning(f'Por favor, preencha todos os campos do formulário antes de finalizar a criação da avaliação.')
                    
                    else:
                        proced_for_bd = []
                        for a in number_processos_total:
                            list_aux = [x[1] for x in proced_in_process if x[0] == a]
                            proced_for_bd.append(list_aux)
                        
                        processo_for_bd = [x for x in processo if x != '']
                        obrigat_for_bd = [x for x in SelComObg if x != '']
                        especf_for_bd =  [f'{x}' for x in SelComEsp if x != '']
                        linrow = [matricula, str(name), str(Unidade), str(macroprocesso), str(transform_to_string(processo_for_bd)),
                                    str(transform_to_string(obrigat_for_bd)),
                                    f"{transform_to_string(especf_for_bd)}", gestorCarreira, matriculaGC,
                                    avaliadorCarreira, matriculaAval, codAce, str(dataIni), str(dataFim), funcao, f'{proced_for_bd}', periodicidad, (Data_Prox_Avalia)]

                        sql = f'INSERT INTO Colaboradores (Matricula ,Nome ,Unidade ,Macroprocesso ,Processo ,Comp_Obrigatória ,Comp_Específica ,Gestor_de_Carreira ,Mat_Gestor ,Avaliador ,Mat_Avalidor ,CódAce ,Data_Inic ,Data_Fim, funcao, Procedimento, Periodicidade_avaliação, Data_Prox_Avalia) VALUES ({linrow[0]}, "{linrow[1]}", "{linrow[2]}", "{linrow[3]}", "{linrow[4]}", "{linrow[5]}", "{linrow[6]}", "{linrow[7]}", "{linrow[8]}", "{linrow[9]}", "{linrow[10]}", "{linrow[11]}", "{linrow[12]}", "{linrow[13]}", "{linrow[14]}", "{linrow[15]}" , "{linrow[16]}" , "{linrow[17]}");'

                        mycursor.execute(sql)
                        conexao.commit()

                        st.info(f"""
                                Instruções para fazer a avaliação de Competências do Colaborador
                                ----------------------------------------------------------------
                                ----------------------------------------------------------------
                                Nome: **{name}**
                                Matrícula: **{matricula}**
                                Unidade: **{Unidade}**
                                Macroprocesso: **{macroprocesso}**
                                Processo: **{str(processo).replace("[", "").replace("]", "")}**
                                Gestor de Carreira: **{gestorCarreira}**
                                Avaliador: **{avaliadorCarreira}**
                                ----------------------------------------------------------------
                                Insira o código de acesso 
                                **{codAce}** 
                                ----------------------------------------------------------------
                                No seguinte link:
                                
                                https://9box.eucatur.com.br/Avaliar_Colaborador
                                
                                
                                ----------------------------------------------------------------
                                """)
                    
    with tab2:
        st.text(' ')
        st.subheader("Avaliações Pendentes")
        st.text(' ')        
        Unidade = st.multiselect("Unidade de negócio", list(set([x[2] for x in listDados2 if x[2] != '' and x[2] != None and x[2] != 'Zero'])), [])
                                                        
        if len(Unidade) < 1:
            st.write("Não há uma unidade selecionada.")
        else:
            mplist = set([x[3] for x in listDados2 if x[2] in Unidade])
            macroprocesso = st.multiselect('Macroprocesso', mplist, mplist)
            if len(macroprocesso) < 1:
                st.write("Não há um macroprocesso selecionado")
            else:
                FuncList = set([x[40] for x in listDados2 if x[2] in Unidade and x[3] in macroprocesso])
                funcao = st.multiselect('Função', FuncList, FuncList)
                if len(funcao) < 1:
                    st.info("Não há uma função selecionada")

        st.text(' ')
        st.text(' ')
        st.text(' ')
        st.text(' ')
   
        botao_pendentes = st.button('Procurar Avaliações Pendentes')


        if botao_pendentes:
            dados_do_filtro = [x for x in listDados2 if x[3] in macroprocesso and x[2] in Unidade and x[40] in funcao and x[1] != 'ZERO']

            matricu_user = list(set([x[4] for x in dadosUser if x[7] == username]))[0]

            if perfilUser[2] == 'A':
                avaliacao_complet = [list(x) for x in dados_do_filtro if str(x[28]) == '1' and str(x[33]) == '1']
                avaliacao_incom = [list(x) for x in dados_do_filtro if str(x[28]) != '1' or str(x[33]) != '1'] 
                
                                    #[COD_ACES, MATRICUL, NOME_COLAB, UNIDADE, MACRO, PROCESSO, GESTOR, AVALIADOR, PERIODO_AVALIAÇÃO]
                colaboradores_incom = [[x[11] ,x[0], x[1], x[2], x[3], x[4], x[7], x[9], f'{x[12]} - {x[13]}'] for x in avaliacao_incom if x[0] != 0]
            else:
                avaliacao_incom2 = [list(x) for x in dados_do_filtro if str(x[28]) != '1' or str(x[33]) != '1']
                                    #[COD_ACES, MATRICUL, NOME_COLAB, UNIDADE, MACRO, PROCESSO, GESTOR, AVALIADOR, PERIODO_AVALIAÇÃO]
                colaboradores_incom = [[x[11] ,x[0], x[1], x[2], x[3], x[4], x[7], x[9], f'{x[12]} - {x[13]}'] for x in avaliacao_incom2 if x[0] != 0 and str(x[8]) == str(matricu_user) or str(x[10]) == str(matricu_user)]
            df_users_incom = pd.DataFrame({'COD_ACES' : [x[0] for x in colaboradores_incom],
                                        'NOME_COLAB':[x[2] for x in colaboradores_incom],
                                        'UNIDADE':[x[3] for x in colaboradores_incom],
                                        'MACRO':[x[4] for x in colaboradores_incom],
                                        'GESTOR':[x[6] for x in colaboradores_incom],
                                        'AVALIADOR':[x[7] for x in colaboradores_incom],
                                        'PERIODO_AVALIAÇÃO':[x[8] for x in colaboradores_incom]
                                        })
            st.dataframe(df_users_incom)
