import streamlit as st
import pandas as pd
from util import converte_data
from PIL import Image
import streamlit_authenticator as stauth
from util import soma_basica
from util import string_to_list
from util import string_to_datetime
from random import randint
from util import converte_data
import string
from dateutil.relativedelta import relativedelta
from funcoesAvaliarColab import FuncaoProcessos, FuncaoProjetos, FuncaoProcediment, FuncaoPesosBSC, FuncaoCPA
from datetime import datetime
import mysql.connector


conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='Colaboradores'
)

mycursor = conexao.cursor()

st.set_page_config(page_title="Avaliar Colaborador",  page_icon=Image.open('icon.png'),layout="wide" )
image = Image.open(('logo.png'))
st.image(image, width = 180)


comando2 = 'SELECT * FROM Usuarios;'
mycursor.execute(comando2)
dadosUser = mycursor.fetchall()

sql = 'SELECT * FROM parametro_indicadores;'
mycursor.execute(sql)
listDadosIndicadores = mycursor.fetchall()

sql = 'SELECT * FROM parametro_procedimento;'
mycursor.execute(sql)
listDadosPC = (mycursor.fetchall())

sql = 'SELECT * FROM parametro_processo;'
mycursor.execute(sql)
listDadosProces = mycursor.fetchall()


def transform_to_string(lista):
    # Junta os elementos da lista em uma única string separada por vírgulas
    string_com_virgulas = ', '.join(map(str, lista))
    return string_com_virgulas


def processBD():
    comando = 'SELECT processo FROM parametro_processo;'
    mycursor.execute(comando)
    processosBD = mycursor.fetchall()

    return list(set([x[0] for x in processosBD]))


def data_formato_americano(data_str):
    from datetime import datetime

    data = datetime.strptime(data_str, '%d-%m-%Y')
    data_americana = data.strftime('%Y-%m-%d')
    return data_americana


def font_BowlbyOne_TITLE_center(texto):
    css1 = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Bowlby+One+SC&display=swap');
            .gold-text1_center {
            font-family: 'Bowlby One SC', cursive;
            font-size: 40px;
            color: gold;
            text-align: center;}
        </style>"""
            

    st.markdown(css1, unsafe_allow_html=True)
    st.markdown(f'<p class="gold-text1_center">{texto}</p>', unsafe_allow_html=True)


def limpar_lista(lista_de_listas):
    lista_final = []
    for lista in lista_de_listas:
        for info in lista:
            lista_final.append(info)
    
    return lista_final


def mostrarIcon(image_url):
  st.markdown(
      f"""
      <style>
      .display-flex {{
          display: flex;
          justify-content: center;
          align-items: center;
      }}
      </style>
      <div class="display-flex">
          <img src="{image_url}" width="50%" height="50%">
      </div>
      """,
      unsafe_allow_html=True
  )


names = [x[5] for x in dadosUser if x[5] != None]
usernames = [x[7] for x in dadosUser if x[7] != None]
hashed_passwords = [x[11] for x in dadosUser if x[8] != None]
funcao = [x[6] for x in dadosUser if x[6] != None]

def creat_numberRandom():
    number = randint(1,300)
    return int(number)


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
    #QUALQUER UM VAI PODER RESPONDER A PARTE DE AVALIAR COLABORADOR
    sql = 'SELECT * FROM Colaboradores;'
    mycursor.execute(sql)
    listDados2 = (mycursor.fetchall())
    
    matriUser = [x[4] for x in dadosUser if x[7] == username]
    dados_user = [list(x) for x in dadosUser if x[4] == matriUser[0]]
    perfil_user = str(dados_user[0][9].upper())
    
    if perfil_user == 'A':
        sql = 'SELECT * FROM Colaboradores;'
        mycursor.execute(sql)
        listDados2 = mycursor.fetchall()

    elif perfil_user == 'B' or perfil_user == 'C':
        sql = f'SELECT * FROM Colaboradores WHERE (Mat_Gestor = {matriUser[0]}) OR (Mat_Avalidor = {matriUser[0]});'
        mycursor.execute(sql)
        listDados2 = mycursor.fetchall()
    
    else:
        unidadesBP = list(str([x[10] for x in dadosUser if str(x[4]) == str(matriUser[0])][0]).split(', '))
        
        texto_sql = ''
        for index_unid in range(len(unidadesBP)):
            if index_unid == 0:
                text_sql_1 = f'(Unidade = "{unidadesBP[index_unid]}")'
                texto_sql += text_sql_1
            else:
                texto_sql_2 = f' OR (Unidade = "{unidadesBP[index_unid]}")'
                texto_sql += texto_sql_2

        comando_sql = f'SELECT * FROM Colaboradores WHERE {texto_sql};'
        mycursor.execute(comando_sql)
        listDados2 = mycursor.fetchall()
        
    div1, div2 = st.tabs(['Avaliar Colaborador', 'Editar Avaliações'])

    with div1:
        st.text(' ')
        st.subheader("Avaliar Colaborador")
        st.text(' ')

        df1 = pd.read_excel("dadosAvaliação.xlsx", sheet_name="Avaliação")
        listDados1 = df1.values.tolist()

        liscod = [str(x[11]) for x in listDados2]
        col1, col2 = st.columns((2, 3))
        with col1:
            codA = st.text_input("Código de acesso da avaliação", type='password')
        if codA not in liscod:
            with col2:
                st.text_input("", "Avaliação não encontrada")
        else:
            linhaBD = [x for x in range(len(listDados2)) if str(listDados2[x][11]) == codA][0]
            st.write("---")
            col1, col2, col3, = st.columns((1, 2, 1))
            with col1:
                st.text_input('Matrícula', listDados2[linhaBD][0])
            with col2:
                st.text_input("Nome Colaborador", listDados2[linhaBD][1])
            with col3:
                anoQuadr = st.text_input("Período", f"{converte_data(str(listDados2[linhaBD][12]))} - {converte_data(str(listDados2[linhaBD][13]))}")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text_input('Função', listDados2[linhaBD][40])
            with col2:
                st.text_input("Unidade de negócio", listDados2[linhaBD][2])
            with col3:
                st.text_input('Macroprocesso', listDados2[linhaBD][3])
            st.text_input('Processo', listDados2[linhaBD][4])
            col1, col2 = st.columns(2)
            with col1:
                st.text_input('Gestor de Carreira', listDados2[linhaBD][7])
            with col2:
                st.text_input('Avaliador', listDados2[linhaBD][9])
            not_funcao = ['Dono de processo', "Líder de Processos", "Gestor de Processos"]
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                    ["Competências", "Desempenho | Processos", "Desempenho | Projetos", "PPC", "CPA"])
            with tab1:
                if listDados2[linhaBD][28] == 1:
                    st.error("Avaliação já foi preenchida")
                else:
                    with st.expander("Critérios para aplicar a nota", expanded=True):
                            st.info(
                                "1- Não executa \n\n 2-Executa Abaixo do Esperado \n\n 3-Executa Conforme o Esperado \n\n 4-Executa Algumas Atividades Acima do Esperado \n\n 5-Executa todas as atividades Acima do Esperado")
                    with st.form("my_form"):
                            compObg = ["Orientação para Pessoas, Processos e Resultados", "Pensamento Crítico e Criativo",
                                    "Comunicação", "Foco no cliente"]
                            optAval = ["1 - Não executa",
                                    "2 - Abaixo do Esperado",
                                    "3 - Conforme o Esperado",
                                    "4 - Acima do Esperado",
                                    "5 - Além do Esperado"]
                            lismediasObg = []
                            for i in compObg:
                                listmedia = []
                                st.subheader(i)
                                for j in listDados1:
                                    if j[0] == i:
                                        st.write("")
                                        nota = int([st.select_slider(j[1], options=optAval, value=optAval[2])][0][0:1])
                                        listmedia.append(nota)
                                        # st.slider(j[1], 1,5,3,step=1)
                                        # st.selectbox(j[1], options=optAval,)
                                        st.write("---")
                                lismediasObg.append(int(sum(listmedia) / len(listmedia) * 100 / 5))
                            competenEspEucatur = ["Inteligência Emocional", "Autonomia e Proatividade", "Relacionamento e Network",
                                                "Futurabilidade", "Raciocínio Analítico", "Empreendedorismo",
                                                "Tomada de Decisão", "Visão Estratégica", "Visão Inovadora", "Liderança", "Comprometimento", "Negociação", "Habilidades Interpessoais"]
                            compEsp_aux = listDados2[linhaBD][6].split(',')
                            compEsp = [str(x).strip() for x in compEsp_aux]

                            lismediasEsp = []
                            for i in competenEspEucatur:
                                listmedia = []
                                if i not in compEsp:
                                    lismediasEsp.append(None)
                                else:
                                    st.subheader(i)
                                    for j in listDados1:
                                        if j[0] == i:
                                            nota = int([st.select_slider(j[1], options=optAval, value=optAval[2])][0][0:1])
                                            listmedia.append(nota)
                                            # st.slider(j[1], 1,5,3,step=1)
                                            # st.selectbox(j[1], options=optAval,)
                                            st.write("---")
                                    lismediasEsp.append(int(sum(listmedia) / len(listmedia) * 100 / 5))
                            lismedias = lismediasObg + lismediasEsp + [1]
                            submitted = st.form_submit_button("Registrar Avaliação do Colaborador")
                            if submitted:
                                if listDados2[linhaBD][28] == 1:
                                    st.error("Avaliação já foi preenchida")
                                else:
                                    linrow = ['(NULL)' if str(x) == "None" else x for x in lismedias]
                                    colunas = ["C_OPPR",
                                        "C_PCC",
                                        "C_Com",
                                        "C_FC",
                                        "C_IntEmo",
                                        "C_AutPro",
                                        "C_RelNet",
                                        "C_FutTen",
                                        "C_RacAna",
                                        "C_Emp",
                                        "C_TomDec",
                                        "C_VisEst",
                                        "C_VisIno",
                                        "C_Lid",
                                        "C_Compr",
                                        "C_Negoc",
                                        "C_Hab_Inter",
                                        "C_Check"]
                                    for i in range(len(colunas)):
                                        sql = f"UPDATE Colaboradores SET {colunas[i]} = {linrow[i]} WHERE CódAce = {int(codA)}"
                                        mycursor.execute(sql)
                                        conexao.commit()
                                    st.info(f"Colaborador Avaliado com Sucesso")
                with tab2:
                    if listDados2[linhaBD][33] == 1:
                        st.error("Registro do processo já foi realizado")
                    else:                        
                        procCola = listDados2[linhaBD][4].split(",")

                        L_ind = []
                        L_met = []
                        L_Des = []
                        L_Pol = []
                        number_indicadores = []
                        st.write(' ')
                        col1, col2, col3 = st.columns((1.2, 1, 0.9))
                        with col2:
                            st.subheader('Desempenho Processos')
                        st.text(' ')
                    
                        procedimentos_BD = [[x[2],x[3]] for x in listDadosPC]
                        indicadores_BD = [[x[2], x[4]] for x in listDadosIndicadores]
                        
                        periodicidade = listDados2[linhaBD][41]
                        if periodicidade == 'Trimestral':
                            vezes_periodo = 3
                        elif periodicidade == 'Bimestral':
                            vezes_periodo = 2
                        else:                               
                            vezes_periodo = 1

                        cont = [[x] for x in range(len(procCola))]
                
                        st.text(' ')
                        cont = 0
                        lista_indicadores_aux = []
                        lista_indicadores_escolha_user = []

                        qntd_indicadr = []
                        for procin in range(len(procCola)):
                            st.caption(procCola[procin])
                            col1, col2 = st.columns((1,3))
                            with col1:
                                qntd_indicadr.append(st.number_input('Indicador', min_value=0, step=1, key= f'Number {procin}'))

                            for a in range(qntd_indicadr[procin]):
                                cont += 1
                                with col2:    
                                    lista_indicadores_aux.append(st.text_input('Nome Indicador', key = f'Nome Indicador {cont}'))    


                            number_proc = [x[0] for x in listDadosProces if str(x[1]).upper().strip() == str(procCola[procin]).upper().strip()][0]

                            indicador_do_proc = [x[4] for x in listDadosIndicadores if int(x[2]) == int(number_proc)]
                            
                            #ESCOLHA DE INDICADORES DO USER
                            escolha_user_indicad = st.multiselect('Escolha de Indicadores', indicador_do_proc, key = f'{procCola[procin]}')
                            
                            lista_indicadores_escolha_user.append(escolha_user_indicad)
                            
                            st.write('---')
                        
                        name_newIndicador = [] 
                        for a in range(len(procCola)):
                            lista = [lista_indicadores_aux[x] for x in range(int(qntd_indicadr[a]))]

                            name_newIndicador.append(lista)
                        
                        with st.form("my_form1"):
                            cont = 0
                            for proc in range(len(procCola)):
                                titulo_proc = f'<div style="text-align:center; color:White;font-size:20px">{procCola[proc]}</div>'
                                st.markdown(titulo_proc, unsafe_allow_html=True)
                                st.text(' ')
                                
                                procedimentos = []
                                
                                if string_to_list(listDados2[linhaBD][49])[proc] != '[]' and string_to_list(listDados2[linhaBD][49])[proc] != '' and string_to_list(listDados2[linhaBD][49])[proc] != None:
                                    for a in (string_to_list(listDados2[linhaBD][49])[proc]):
                                        procedimentos.append(a)
                                
                                procedimentos_numbers = [x[0] for x in procedimentos_BD if x[1] in procedimentos]

                                #INDICADORES DOS PROCEDIMENTOS DAQUELE PROCESSO
                                #indicadores_to_proc = [x[1] for x in indicadores_BD if x[0] in procedimentos_numbers]
                                
                                indicadores_to_proc = list(lista_indicadores_escolha_user[proc])

                                if len(name_newIndicador[proc])> 0:
                                    indicadores_to_proc.extend(name_newIndicador[proc])
                
                                number_indicadores = len(indicadores_to_proc)
                                
                                col1, col2, col3, col4 = st.columns((1.20, 0.4, 0.5, 0.5))
                                with col1:
                                    st.info(f"Indicadores")
                                with col2:
                                    st.info("Meta")
                                with col3:
                                    st.info("Realizado")
                                with col4:
                                    st.info("Polaridade")
                                L_aux1 = []
                                L_aux2 = []
                                L_aux3 = []
                                L_aux4 = []

                                polarid = ['Positivo', 'Negativo']

                                for index_indic in range(number_indicadores):
                                    periodo_inicial = string_to_datetime(listDados2[linhaBD][12])

                                    for a in range(vezes_periodo):
                                        dias = relativedelta(months=a)
                                        periodo_ind = periodo_inicial + dias
                                        
                                        cont+=1
                                        with col1:
                                            L_aux1.append(st.text_input(f'a{proc} {a + 1}', f'{indicadores_to_proc[index_indic]}({converte_data(str(periodo_ind))})', label_visibility="hidden",key=f'{cont+1000}'))
                                        with col2:
                                            L_aux2.append(st.number_input(f'b{proc} {a + 1}', label_visibility="hidden", min_value=(0.00), step=0.01, key=f'{cont+23}'))
                                        with col3:
                                            L_aux3.append(st.number_input(f'c{proc} {a + 1}', label_visibility="hidden", min_value=(0.00), step=0.01, key=f'{cont+100}'))
                                        with col4:
                                            L_aux4.append(st.selectbox(f'd{proc} {a + 1}', polarid, label_visibility="hidden", key=f'{cont+300}'))
                                
                                L_ind.append(L_aux1)
                                L_met.append(L_aux2)
                                L_Des.append(L_aux3)
                                L_Pol.append(L_aux4)
                                st.text(" ")

                            submitted1 = st.form_submit_button("Registrar Desempenho Processos")
                            if submitted1:
                                if listDados2[linhaBD][33] == 1:
                                    st.error("Avaliação já foi preenchida")
                                else:
                                    
                                    #DESCOBRINDO SE O USUÁRIO PREENCHEU A AVALIAÇÃO
                                    lista_zerada = False
                                    for index in range(len(L_met)):
                                        if len(L_met[index]) < 1 or len(L_Des[index]) < 1:
                                            lista_zerada = True
                                    
                                    #DESCOBRINDO SE O CAMPO META E REALIZADO ESTÃO ZERADOS

                                    tem_zero = False
                                    for index in range(len(L_met)):
                                        if 0 in L_met[index] or 0 in L_Des[index]:
                                            tem_zero = True

                                    if lista_zerada:
                                        st.warning('Todos os campos devem ser preenchidos corretamente antes de concluir a avaliação.')                                            
                                    elif tem_zero:
                                        st.warning('Os campos Meta e Realizado não podem conter o valor Zero.')
                                    else:
                                        linrow = [L_ind, L_met, L_Des, L_Pol, 1]
                                        colunas = ["N_IPROC", "M_IPROC", "D_IPROC", "P_IPROC", "DPROC_Check"]
                                        for i in range(len(colunas)):
                                            sql = f'UPDATE Colaboradores SET {colunas[i]} = "{linrow[i]}"  WHERE CódAce = {int(codA)}'
                                            mycursor.execute(sql)
                                            conexao.commit()
                                        st.success('Registro realizado')

                    # REGISTRO DE PROCEDIMENTOS DE PROCESSOS
                    if listDados2[linhaBD][51] == '1':
                        st.error("Registro de Procedimento já foi realizado")
                    else:
                        if listDados2[linhaBD][40] == "Líder de Processos":
                            procCola = [listDados2[linhaBD][3]]
                        else:
                            procCola = listDados2[linhaBD][4].split(",")

                        procedimentos_BD = [[x[2],x[3]] for x in listDadosPC]
                        
                        procediment_BD_colab = list(string_to_list(listDados2[linhaBD][49]))

                        st.write(' ')
                        st.write(' ')
                        col1, col2, col3 = st.columns((1.1, 1, 0.9))
                        with col2:
                            st.subheader('Carga Horária Processos')
                        new_number_procedim = []
                        st.write(' ')
                        colun1, colun2, colun3 = st.columns((3, 1, 1))
                        for proc in range(len(procCola)):
                            with colun1:
                                new_number_procedim.append(st.number_input(f'Procedimentos - {procCola[proc]}', min_value=(0), step=(1)))

                                for a in range(int(new_number_procedim[0])):
                                    var_aux = list(procediment_BD_colab[proc])
                                    var_aux.extend([' '])
                                    procediment_BD_colab[proc] = var_aux


                        lista_final_proced = []
                        lista_final_horas = []
                        with st.form('form_proced'):
                            for proc in range(len(procCola)):
                                colP1, colP2 = st.columns((3, 1))
                                with colP1:
                                    st.markdown(f'Procedimentos - {procCola[proc]}')
                                with colP2:
                                    st.markdown(f'Horas')
                                lista_procedimentos = []
                                lista_horas_proced = []
                                
                                number_total_proced = len(procediment_BD_colab[proc])

                                for a in range(number_total_proced):
                                    coluna1, coluna2 = st.columns((3, 1))
                                    with coluna1:
                                        proced = st.text_input(f'Procedimentos {a + 1}', f'{procediment_BD_colab[proc][a]}', key=f'Procedimentos {a + 1} - {procCola[proc]}', label_visibility='hidden')
                                        lista_procedimentos.append(proced)
                                    with coluna2:
                                        horas_proced = st.number_input(f'Horas {a + 1}', min_value=(1), step=(1), key=f'Horas {a + 1} - {procCola[proc]}', label_visibility='hidden')
                                        lista_horas_proced.append(horas_proced)
                                lista_final_proced.append(lista_procedimentos)
                                lista_final_horas.append(lista_horas_proced)
                
                            proced_button = st.form_submit_button("Registrar Procedimentos de Processos")
                            if proced_button:
                                if listDados2[linhaBD][33] == '1':
                                    st.error("Avaliação já foi preenchida")
                                else:
                                    linrow = [lista_final_proced, lista_final_horas, 1]
                                    colunas = ["Procedimento", "hrs_procedim", "Check_proced"]
                                    for i in range(len(colunas)):
                                        sql = f'UPDATE Colaboradores SET {colunas[i]} =  "{linrow[i]}"  WHERE CódAce = {int(codA)}'
                                        mycursor.execute(sql)
                                        conexao.commit()
                                    st.success('Registro realizado')
                with tab3:
                    if listDados2[linhaBD][38] == 1:
                        st.error("Registro já foi realizado")
                    else:
                        from datetime import date
                        list_processos = processBD()

                        st.subheader('Desempenho em projetos')
                        qnt_projeto = st.number_input('Quantidade Projetos', min_value=1, step=1)


                        final_ProjName = []
                        final_ProjHora = []
                        final_ProjType = []
                        final_ProjDateIni = []
                        final_ProjDateFim = []
                        final_ProjQntSpri = []
                        final_ProjProc = []
                        final_ProjPerfi = []
                        final_ProjStat = []

                        final_IndcName = []
                        final_IndcMeta = []
                        final_IndcReal = []
                        final_IndcPolr = []

                        st.text(' ')
                        st.text(' ')
                        st.subheader('Projetos')
                        for a in range(qnt_projeto):
                            with st.expander(f'Projeto {a + 1}'):
                                col1, col2 = st.columns((5,1))
                                with col1:
                                    final_ProjName.append(st.text_input('Nome Projeto', value='', key=f'name proj {a}'))
                                with col2:
                                    final_ProjHora.append(st.number_input('Horas', min_value=1, step=1, key=f'Horas {a}'))

                                col1, col2, col3, col4 = st.columns((3,1,1,1.05))

                                with col1:
                                    final_ProjType.append(st.selectbox('Tipo', ['Estratégico', 'OKR', 'Implantação'], key=f'Tipo {a}'))
                                with col2:
                                    final_ProjDateIni.append(str(st.date_input('Início', date.today(), key =f'Inicio {a}')))
                                with col3:
                                    final_ProjDateFim.append(str(st.date_input('Fim', date.today(), key=f'fim {a}')))
                                with col4:
                                    final_ProjQntSpri.append(st.number_input('Sprint', min_value=1, step=1, key=f'Sprint {a}'))
                                
                                col1, col2, col3 = st.columns((3.5,1.5,1.03))

                                with col1:
                                    final_ProjProc.append(st.selectbox('Processo do Projeto', list_processos, key=f'ProcProj {a}'))
                                with col2:
                                    final_ProjPerfi.append(st.selectbox('Papel', ['Gestor', 'Especialista', 'Squad'], key=f'Papel {a}'))
                                with col3:
                                    status_temp = st.selectbox('Status', ['Homologado', 'Não Homologado'], key=f'Status {a}')
                                    if status_temp == 'Homologado':
                                        status = '1'
                                    else:
                                        status = '0'

                                final_ProjStat.append(status)
                                
                                st.text(' ')
                                st.write('---')

                                col2, col3 = st.columns((4,2))
                                with col2:
                                    st.text(' ')
                                    st.markdown('Informações Indicadores')

                                with col3:
                                    qntd_indic = st.number_input('Quantidade', label_visibility='collapsed', min_value=1, step=1, key=f'qnts indic {a}')
                                st.text(' ')
                                
                                col1, col2, col3, col4 = st.columns((1.50, 0.5, 0.5, 0.75))

                                with col1:
                                    st.caption('Indicador')
                                with col2:
                                    st.caption('Meta')
                                with col3:
                                    st.caption('Realizado')
                                with col4:
                                    st.caption('Polaridade')
                                                                
                                Temp_IndcName = []
                                Temp_IndcMeta = []
                                Temp_IndcReal = []
                                Temp_IndcPolr = []

                                for qnt_ind in range(int(qntd_indic)):
                                    
                                    with col1:
                                        Temp_IndcName.append(st.text_input(f'Indicador',label_visibility='collapsed', key=f'Indicador {a} {qnt_ind}'))
                                    with col2:
                                        Temp_IndcMeta.append(st.number_input(f'Meta', label_visibility='collapsed',key=f'Meta {a} {qnt_ind}', min_value=(0.00), step=0.01))
                                    with col3:
                                        Temp_IndcReal.append(st.number_input(f'Realizado', label_visibility='collapsed', key=f'Realizado {a} {qnt_ind}',min_value=(0.00), step=0.01))
                                    with col4:
                                        Temp_IndcPolr.append(st.selectbox(f'Polaridade', ['Positivo', 'Negativo' ], label_visibility='collapsed', key=f'Polaridade {a} {qnt_ind}'))
                                
                            final_IndcName.append(Temp_IndcName)
                            final_IndcMeta.append(Temp_IndcMeta)
                            final_IndcReal.append(Temp_IndcReal)
                            final_IndcPolr.append(Temp_IndcPolr)


                        botaoProj = st.button('Registrar Desempenho Projetos')
                        if botaoProj:
                            if listDados2[linhaBD][38] == 1:
                                st.error("Registro já foi realizado")
                            else:
                                #DESCOBRINDO SE O CAMPO META E REALIZADO ESTÃO ZERADOS
                                tem_zero_proj = False
                                for index in range(len(final_IndcMeta)):
                                    if 0 in final_IndcMeta[index] or 0 in final_IndcReal[index]:
                                        tem_zero_proj = True

                                if tem_zero_proj:
                                    st.warning('Os campos meta e realizado não podem conter o valor Zero.')
                                else:
                                    linrow = [final_IndcName, final_IndcMeta, final_IndcReal, final_IndcPolr, 1, final_ProjName, final_ProjHora, final_ProjType, final_ProjDateIni, final_ProjDateFim, final_ProjProc, final_ProjStat, final_ProjQntSpri, final_ProjPerfi]

                                    colunas = ["N_IPROJ", "M_IPROJ", "D_IPROJ", "P_IPROJ", "DPROJ_Check", "NAME_PROJ", "HORAS_PROJ", "PROJ_TYPE", "PROJ_INIC", "PROJ_FIM",
                                               "PROJ_PROC", "PROJ_STATUS", "PROJ_SPRINT", "PROJ_PAPEL"]
                                   
                                    for i in range(len(colunas)):
                                        sql = f'UPDATE Colaboradores SET {colunas[i]} = "{linrow[i]}"  WHERE CódAce = {int(codA)}'
                                        mycursor.execute(sql)
                                        conexao.commit()
                                    
                                    st.success('Registro do colaborador encaminhado.')

                lista_pesos = ['Peso de Competências','Peso de Processos', 'Peso de Projetos']
                with tab4:
                    if listDados2[linhaBD][56] == '1':
                        st.error("Registro já foi realizado")
                    else:
                        pesos = []
                        st.header('Pesos PPC')
                        st.text(' ')
                        with st.form('PPC'):
                            for a in lista_pesos:
                                coluna1, coluna2 = st.columns((3,1))
                                with coluna1:
                                    st.text(' ')
                                    st.text(' ')
                                    st.markdown(f'{a}')
                                with coluna2:
                                    peso_user = st.number_input('Porcetagem',max_value=100, step=1, key=f'{a}')
                            
                                st.write('---')
                                pesos.append(peso_user)
                            submitted = st.form_submit_button("Registrar pesos")  
                            
                            if submitted:
                                soma = soma_basica(pesos)
                                if soma != 100:
                                    st.warning('Impossível prosseguir! A soma dos campos deve ser 100%.')
                                else:
                                    pesos.append(1)
                                    coluna = ['BSC_Peso_Compr', 'BSC_Peso_Proces', 'BSC_Peso_Proj', 'BSC_check']
                                    for a in range(len(pesos)):    
                                        comando = f'UPDATE Colaboradores SET {coluna[a]} = "{pesos[a]}"  WHERE CódAce = {int(codA)}'
                                        mycursor.execute(comando)
                                        conexao.commit()
                                    st.success('Informações armazenadas com sucesso')
                
                with tab5:
                    if str(listDados2[linhaBD][28]) == '1':
                        if str(listDados2[linhaBD][60]) != '1':
                            competencias_bd = list(listDados2[linhaBD][14:28]) + list(listDados2[linhaBD][43:46])
                
                            competencias = [x for x in competencias_bd if x != None]
                            mediaC = sum(competencias) / len(competencias)

                            st.header('CPA')
                            st.text(' ')
                            lista_valores = []
                            topicos = ['Conhecimento', 'Perfil']

                            with st.form('CPA'):
                                for top in topicos:
                                    col_CPA, col_CPA1 = st.columns((3,1))
                                    with col_CPA:
                                        st.text(' ')
                                        st.text(' ')
                                        st.markdown(f'{top}')
                                    
                                    with col_CPA1: 
                                        valores = st.number_input('Porcetagem',max_value=100, step=1, key=f'{top}')
                                    
                                    st.write('---')
                                    lista_valores.append(valores)

                                col_CPA, col_CPA1 = st.columns((3,1))
                                with col_CPA:
                                    st.text(' ')
                                    st.text(' ')
                                    st.markdown(f'Atitude')
                                
                                with col_CPA1: 
                                    atitude = st.number_input('Porcetagem',value=int(mediaC),max_value=100, step=1)

                                lista_valores.append(int(mediaC))
                                lista_valores.append(1)

                                submittedCPA = st.form_submit_button("Registrar CPA")
                                if submittedCPA: 
                                    for a in range(len(lista_valores)):
                                        coluna = ['CPA_Perfil', 'CPA_Capacit', 'CPA_Atitude', 'CPA_Check']
                                        comando = f'UPDATE Colaboradores SET {coluna[a]} = "{lista_valores[a]}"  WHERE CódAce = {int(codA)}'
                                        mycursor.execute(comando)
                                        conexao.commit()
                                    st.success('Informações armazenadas com sucesso')
                        else:
                            st.error('Registro de CPA já realizado.')
                    else:
                        st.warning('Preencha o campo Avaliação de Competências para prosseguir com o preenchimento do CPA.')


################################################# EDITAR OS DADOS DO USER #####################################################
    with div2:
        perfil_user = [x[9] for x in dadosUser if x[7] == str(username) and x[7] != None][0]
        perfil_user = ('{}'.format(perfil_user)).upper()
        matricula_user = [x[4] for x in dadosUser if x[7] == str(username) and x[7] != None][0]
        
        if perfil_user == 'A' or perfil_user == 'BP':
            linhaBD = 0        
            
            dados_colaboradors = listDados2

            
            st.text(' ')
            st.subheader('Editar Avaliações')
            st.text(' ')
            
            col1, col2 = st.columns((2, 3))
            with col1:
                matricula_user = st.text_input('Matricula')

            matriculasBD = list(set([str(x[0]) for x in dados_colaboradors if x[1] != 'ZERO']))
            if matricula_user not in matriculasBD:
                with col2:   
                    st.text_input('', 'Colaborador não encontrado')         
            else:
                dados_colab = [x for x in dados_colaboradors if int(x[0]) == int(matricula_user)]
                
                #st.info(len(dados_colab))
                name_avaliacoes = [f'{x + 1}° Avaliação | {converte_data(dados_colab[x][12])} - {converte_data(dados_colab[x][13])}' for x in range(len(dados_colab))]
                st.text(' ')
                st.text(' ')
                st.write('---')
                st.text(' ')
                st.subheader('Avaliações')
                for rang in range(len(name_avaliacoes)):
                    with st.expander(f'{name_avaliacoes[rang]}'):
                        
                        tabs1, tabs2, tabs3, tabs4, tabs5, tabs6 = st.tabs(['Dados Gerais', 'Desempenho em Competências', 'Desempenho em Processos', 'Desempenho em Projetos', 'Pesos BSC', 'CPA'])
                        with tabs1:
                            if str(dados_colab[rang][28]) == '1': 
                                with st.form(f'Forms DadosGerais Atualizado {rang}'):
                                    st.text('')

                                    col1, col2, col3 = st.columns((0.6, 1.25, 1.1))
                                    with col1:
                                        mat_colab_atualizado = st.text_input("Matricula", dados_colab[rang][0], key=f'MATRICULA {rang}')

                                    with col2:   
                                        name_atualizado = st.text_input("Nome Colaborador", dados_colab[rang][1], key=f'NOME {rang}')
                                        
                                    with col3:
                                        periodo_atualizado = f'{converte_data(dados_colab[rang][12])} - {converte_data(dados_colab[rang][13])}'
                                        anoQuadr_atualizado = st.text_input('Período', periodo_atualizado, key=f'PERIODO {rang}')
                                    
                                    col1, col2, col3 = st.columns(3)
                                    with col1:
                                        funcao_atualizado = st.text_input('Função', dados_colab[rang][40], key=f'FUNÇÃO {rang}')
                                    with col2:
                                        unidade_atualizado = st.text_input("Unidade de negócio", dados_colab[rang][2], key = f'UNIDADE {rang}')
                                    with col3:
                                        macro_atualizado = st.text_input('Macroprocesso', dados_colab[rang][3], key= f'MACRO {rang}')
                                    processo_atualizado = st.text_input('Processo', dados_colab[rang][4], key = f'PROCESSO {rang}')
                                    col1, col2 = st.columns((3,1))
                                    with col1:
                                        gestor_atualizado = st.text_input('Gestor de Carreira', dados_colab[rang][7], key = f'GESTOR {rang}')
                                    with col2:
                                        mat_gestor_atualizado = st.text_input('Matricula Gestor', dados_colab[rang][8], key = f' MAT GESTOR {rang}')
                                    with col1:
                                        avaliador_atualizado = st.text_input('Avaliador', dados_colab[rang][9], key = f'AVALIADOR {rang}') 
                                    with col2:
                                        mat_avaliador_atualizado = st.text_input('Matricula Avaliador', dados_colab[rang][10], key = f' MAT AVALIADOR {rang}')

                                    data_inicio_atualizado = str(data_formato_americano(str(anoQuadr_atualizado[:10]).replace('/', '-')))
                                    data_fim_atualizado = str(data_formato_americano(str(anoQuadr_atualizado[13:]).replace('/', '-')))
                                    
                                    butao1 = st.form_submit_button("Atualizar")

                                    if butao1:
                                        linrow = [mat_colab_atualizado, name_atualizado, data_inicio_atualizado, data_fim_atualizado, funcao_atualizado, unidade_atualizado, macro_atualizado, processo_atualizado, gestor_atualizado, mat_gestor_atualizado, avaliador_atualizado, mat_avaliador_atualizado]
                                        colunas = ["Matricula", "Nome", "Data_Inic", "Data_fim", "funcao", "Unidade", "Macroprocesso", "Processo", "Gestor_de_Carreira", "Mat_Gestor", "Avaliador", "Mat_Avalidor"]
                                        for i in range(len(colunas)):
                                            sql = f'UPDATE Colaboradores SET {colunas[i]} = "{linrow[i]}"  WHERE CódAce = {int(dados_colab[rang][11])}'
                                            mycursor.execute(sql)
                                            conexao.commit()
                                        st.success('Registro realizado')

                            else:
                                st.error("Desempenho em Competências ainda não preenchido")

                        with tabs2:
                            if str(dados_colab[rang][28]) != '1':
                                st.error("Avaliação ainda não preenchida.")
                            else:
                                st.subheader("Renicializar o preenchimento da Avaliação")
                                botao_renecializ = st.button('Renecializar', key=f'Renecializar {rang}')
                                
                                if botao_renecializ:
                                    comando = f'UPDATE Colaboradores SET C_Check = "0"  WHERE CódAce = {int(dados_colab[rang][11])}'
                                    mycursor.execute(comando)
                                    conexao.commit()

                                    st.success('Avaliação disponível novamente!') 


                        with tabs3:
                            #EDITAR PROCESSOS
                            if str(dados_colab[rang][33]) != '1':
                                st.error("Desempenho em Processos ainda não preenchido")
                            else:
                                FuncaoProcessos(dados_colab, rang, dados_colab[rang][11])
                            
                            #EDITAR PROCEDIMENTOS
                            if str(dados_colab[rang][51]) != '1':
                                st.error("Registro de Procedimentos ainda não realizado!")
                            else:
                                FuncaoProcediment(dados_colab, rang, dados_colab[rang][11])

                        with tabs4:
                            #EDITAR PROJETOS
                            if str(dados_colab[rang][38]) != '1':
                                st.error("Registro ainda não realizado!")
                            else:
                                FuncaoProjetos(dados_colab, rang, dados_colab[rang][11])

                        with tabs5:
                            #EDITAR BSC
                            if dados_colab[rang][56] != '1':
                                st.error("Registro ainda não realizado!")
                            else:
                                FuncaoPesosBSC(dados_colab[rang][11], rang)
                        
                        with tabs6:
                            #EDITAR CPA
                            if str(dados_colab[rang][60]) != '1':
                                st.error("Registro ainda não realizado!")
                            else:
                                FuncaoCPA(dados_colab[rang][11], rang, dados_colab)                                               
                            
                                   
