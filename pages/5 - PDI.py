import streamlit as st
from datetime import datetime
from func_relatorio import novos_compromissos
from util import converte_data
import emoji
from func_relatorio import contador_basico
from util import displayInd
from datetime import date
import pandas as pd
from util import string_to_datetime
from PIL import Image
from random import randint
import streamlit_authenticator as stauth
import plotly.graph_objects as go
import mysql.connector


st.set_page_config(page_title="DashboardPDI", page_icon=Image.open('icon.png'), layout='wide')
image = Image.open(('logo.png'))
st.image(image, width = 180)

conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='Colaboradores'
)

mycursor = conexao.cursor()

def dadosColab_BD():
    mycursor = conexao.cursor()
    comando_sql = 'SELECT * FROM Colaboradores;'
    mycursor.execute(comando_sql)
    listDados2 = mycursor.fetchall()

    mycursor.close()

    return listDados2

listDados2 = dadosColab_BD()


def UsersBD():
    mycursor = conexao.cursor()
    comando2 = 'SELECT * FROM Usuarios;'
    mycursor.execute(comando2)
    dadosUser = mycursor.fetchall()

    mycursor.close()
    
    return dadosUser

dadosUser = UsersBD()


def sort_descending_by_index2(lst):
    return sorted(lst, key=lambda x: x[2], reverse=True)


def limpar_lista(lista_de_listas):
    lista_final = []
    for lista in lista_de_listas:
        for info in lista:
            lista_final.append(info)
    
    return lista_final


def maior_valor_dic(dicionario):
    maior = 0
    lista_maior = []

    for chave, valor in dicionario.items():
        if valor > maior:
            maior = valor
            primeir_chave_maior = chave
    
    lista_maior.append(primeir_chave_maior)
    lista_maior.append(maior)

    return lista_maior


def maiores_to_dic(dicionario):
    lista_maiores = []

    maior = 0
    segundo_maior = 0
    terceito_maior = 0

    #1° MAIOR
    for chave, valor in dicionario.items():
        if valor > maior:
            maior = valor
            primeir_chave_maior = chave
    
    lista_maiores.append([primeir_chave_maior, maior])

    del dicionario[f'{primeir_chave_maior}']

    #2° MAIOR
    if len(dicionario) > 0:
        for chave, valor in dicionario.items():
            if valor > segundo_maior:
                segundo_maior = valor
                segund_chave_maior = chave
        
        lista_maiores.append([segund_chave_maior, segundo_maior])
        del dicionario[f'{segund_chave_maior}']

    if len(dicionario) > 0:
        #3° MAIOR
        for chave, valor in dicionario.items():
            if valor > terceito_maior:
                terceito_maior = valor
                terceir_chave_maior = chave
        
        lista_maiores.append([terceir_chave_maior, terceito_maior])
    
    return lista_maiores
    

def gerar_HTML_Caixa(title,subtitulo,valores):    
    texto = ""    
    for i in range(len(subtitulo)):
        aux = f"""<div class="skill"><div class="skill-name">{subtitulo[i]}</div><div class="skill-level"><div class="skill-percent" style="width: {valores[i]}"></div></div><div class="skill-percent-number">{valores[i]}</div></div>"""
        texto += aux
    html = f"""<div class="card"><div class="header">{title}</div><div class="body">{texto}</div></div>"""
    return html


def gerar_HTML_Caixa_New(title, valores):    
    texto = ""
  
    for i in range(len(valores)):
        aux = f'<div class="skill-box"><span class="title">{title[i]}</span><div class="skill-bar"><span class="skill-per"style = width:{valores[i]}%;><span class="tooltip">{valores[i]}% </span></span></div></div>'
        texto += aux
            
    html = f'<body><div class="container">{texto}</div></body>'
        
    return html


def cardPlotNew(lista_titles, lista_values):
    styleNew = """
        <style>
            /* ===== Google Font Import - Poppins ===== */
            @import url('https://fonts.googleapis.com/css2?family=Bowlby+One+SC&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
            *{
                margin: 0;
                padding: 0;
            }
            body{
                height: 100vh;
                display: flex;
                background: #4070f4;
                align-items: center;
                justify-content: center;
                
            }
            .container{
                position: relative;
                max-width: 500px;
                width: 100%;
                background: #fff;
                margin: 0 auto;
                padding: 10px 20px;
                border-radius: 7px;
                display: flex; 
                justify-content: center; 
                align-items: center;
                max-width: 90vw;
            }
            .container .skill-box{
                width: 100%;
                margin: 10px 0;
            }
            .skill-box .title{
                display: block;
                font-size: 14px;
                font-weight: normal;
                color: #333;
                box-sizing: border-box;
                font-family: 'Poppins', sans-serif;
                margin-bottom: 27px; 
            }
            .skill-box .skill-bar{
                height: 8px;
                width: 100%;
                border-radius: 6px;
                margin-top: 6px;
                background: rgba(0,0,0,0.1);
                margin-bottom: 0px;
                
            }
            .skill-bar .skill-per{
                position: relative;
                display: block;
                height: 100%;
                border-radius: 6px;
                background-color: #D4AF37; 
                animation: progress 0.4s ease-in-out forwards;
                opacity: 0;
                
            }
            @keyframes progress {
                0%{
                    width: 0;
                    opacity: 1;
                }
                100%{
                    opacity: 1;
                }
            }
            .skill-per .tooltip{
                position: absolute;
                right: -14px;
                top: -28px;
                font-size: 9px;
                font-weight: normal;
                color: #fff;
                padding: 2px 6px;
                border-radius: 3px;
                background: #D4AF37;
                z-index: 1;
            }
            .tooltip::before{
                content: '';
                position: absolute;
                left: 50%;
                bottom: -2px;
                height: 10px;
                width: 10px;
                z-index: -1;
                background-color: #D4AF37;
                transform: translateX(-50%) rotate(45deg);
            }
        </style>
        """

    html_and_css = gerar_HTML_Caixa_New(lista_titles, lista_values)

    st.write(styleNew, unsafe_allow_html=True)
    st.markdown(html_and_css, unsafe_allow_html=True)


def progress_bar(percentual,titulo):
    # Converter o valor percentual para uma porcentagem decimal
    progress_decimal = percentual / 100
    # Código HTML
    html_code = f'''
    <div class="container">
        <div class="circular-progress" style="background: conic-gradient(#D4AF37 {progress_decimal*360}deg, #ededed 0deg);">
            <span class="progress-value">{percentual}%</span>
        </div>
        <span class="text">{titulo}</span>
    </div>
    '''
    # Código CSS
    css_code = '''
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
        *{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            
        }
        body{
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #7d2ae8;
            
        }
        .container{
            display: flex;
            width: 100%;
            padding: 10px;
            border-radius: 15px;
            background: #fff;
            row-gap: 30px;
            flex-direction: column;
            align-items: center;
            box-sizing: border-box;
            font-family: 'Poppins', sans-serif; 
        }
        .circular-progress{
            position: relative;
            height: 150px;
            width: 150px;
            border-radius: 50%;
            background: conic-gradient(#7d2ae8 3.6deg, #ededed 0deg);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .circular-progress::before{
            content: "";
            position: absolute;
            height: 115px;
            width: 115px;
            border-radius: 50%;
            background-color: #fff;
        }
        .progress-value{
            position: relative;
            font-size: 30px;
            font-weight: 600;
            color: black;
        }
        .text{
            font-size: 15px;
            font-weight: 500;
            color: black;
        }
    </style>
    '''
    # Exibir o código HTML e CSS usando st.markdown()
    st.markdown(html_code, unsafe_allow_html=True)
    st.markdown(css_code, unsafe_allow_html=True)


def font_BowlbyOne_TITLE(texto):
    css1 = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Bowlby+One+SC&display=swap');
            .gold-text1 {
            font-family: 'Bowlby One SC', cursive;
            font-size: 40px;
            color: gold;}
        </style>"""
            

    st.markdown(css1, unsafe_allow_html=True)
    st.markdown(f'<p class="gold-text1">{texto}</p>', unsafe_allow_html=True)


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


def font_BowlbyOne_SUBTITLE(texto):
    css = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Bowlby+One+SC&display=swap');
            .gold-text {
            font-family: 'Bowlby One SC', cursive;
            font-size: 20px;
            color: gold;}
        </style>"""
    
    st.markdown(css, unsafe_allow_html=True)
    st.markdown(f'<p class="gold-text">{texto}</p>', unsafe_allow_html=True)


def font_BowlbyOne_SUBTITLE_center(texto):
    css = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Bowlby+One+SC&display=swap');
            .gold-text_ {
            font-family: 'Bowlby One SC', cursive;
            font-size: 30px;
            color: gold;
            text-align: center;}
        </style>"""
            

    st.markdown(css, unsafe_allow_html=True)
    st.markdown(f'<p class="gold-text_">{texto}</p>', unsafe_allow_html=True)


def transform_to_string(lista):
    # Junta os elementos da lista em uma única string separada por vírgulas
    string_com_virgulas = ', '.join(map(str, lista))
    return string_com_virgulas


def visualizacao_Compromissos_PDI(listDados2, linhaBD, matricula):
  mycursor = conexao.cursor()
  st.text(' ')
  font_BowlbyOne_SUBTITLE_center("COMPROMISSOS")

  #CONEXÃO BD
  comando = f'SELECT * FROM compromissos_9box WHERE(matricula = {matricula});'
  mycursor.execute(comando)
  compromissos_user = mycursor.fetchall()
  
  mycursor.close()
  if len(compromissos_user) > 0:

    #declarar os valores title, valor, porc, min_val, max_val para usar a função "displayInd"
    col1, col2, col3, col4 = st.columns(4)
    #TOTAL DE COMPROMISSOS
    with col1:
      title = 'Todos'
      valor = str(contador_basico(compromissos_user))
      porc = ''
      min_val = 0
      max_val = int(valor)

      displayInd(title, valor, min_val, max_val)

    #COMPROMISSOS EXECUTADOS
    with col4:
      title = 'Concluídos'
      valor = str(contador_basico([x for x in compromissos_user if x[10] == '1']))
      displayInd(title, valor, min_val, max_val)

    #COMPROMISSOS PENDENTES
    with col2:
        title = 'Em andamento'
        valor = str(len([x for x in compromissos_user if x[10] != '1' and date.today() < string_to_datetime(x[9])]))
        displayInd(title, valor, min_val, max_val)

    #COMPROMISSOS VENCIDOS
    with col3:
        title = 'Vencidos'
        valor = str(len([x for x in compromissos_user if x[10] != '1' and date.today() > string_to_datetime(x[9])]))
        displayInd(title, valor, min_val, max_val)
    
    id = [x[0] for x in compromissos_user]
    comp_compt = [x[4] for x in compromissos_user]
    comp_Plan = [x[5] for x in compromissos_user]
    comp_Recurs = [x[6] for x in compromissos_user]
    comp_Result = [x[7] for x in compromissos_user]
    comp_dat_Inin = [x[8] for x in compromissos_user]
    comp_dat_Fim = [x[9] for x in compromissos_user]
    check_db = [x[10] for x in compromissos_user]
    compr_area = [x[11] for x in compromissos_user]

    
  
    st.text(' ')
    for a in range(len(comp_compt)):
        if str(check_db[a]) == '1':
            check_emoji = emoji.emojize(":heavy_check_mark:")
            check_forms = True
        elif str(check_db[a]) != '1' and date.today() <= string_to_datetime(comp_dat_Fim[a]):
            check_emoji = emoji.emojize(":hourglass_not_done: ")
            check_forms = False
        elif str(check_db[a]) != '1' and date.today() > string_to_datetime(comp_dat_Fim[a]):
            check_emoji = emoji.emojize(":warning:")
            check_forms = False
        
        
        #QUANDO FOR FAZER DOS ATRASADOS USAR O EMOJI ":warning:" OU "":exclamation:""

        
        if compr_area[a] != None and compr_area[a] != '': 
            name_expend = f'{comp_compt[a]} | {compr_area[a]} | {converte_data(comp_dat_Inin[a])} - {converte_data(comp_dat_Fim[a])}' + ' ' + check_emoji
        else:
            name_expend = f'{comp_compt[a]} | {converte_data(comp_dat_Inin[a])} - {converte_data(comp_dat_Fim[a])}' + ' ' + check_emoji

        with st.expander(f'{name_expend}'):

            tab1, tab2 = st.tabs(['Compromisso', 'Feedback'])

            ################## COMPROMISSOS #######################
            with tab1:
                st.text(' ')
                col1, col2, col3, col4 = st.columns((3.7, 2.0, 2.0, 2.0))
                with col1:
                    st.text_input(f'Área a melhorar', compr_area[a], key = f'area{a + 1}')

                with col2:
                    st.text_input(f'Inicio', converte_data(comp_dat_Inin[a]), key=f'Inicio {a + 1}')
                with col3:
                    st.text_input(f'Fim', converte_data(comp_dat_Fim[a]), key=f'Fim {a + 1}')
                with col4:
                    st.text(' ')
                    st.text(' ')
                    check_comp = st.checkbox('Concluído',value=check_forms, key = f'check{a}')

                    if check_comp == True:
                        check_for_bd = '1'
                    else:
                        check_for_bd = '0'

                #desempenho = st.slider('Desempenho no compromisso',0 , 100,(0, desem_daquele_compr), step=10,  key=f'Conclusão do compromisso {a + 1}')
                
                st.text_input(f'Comportamento a Melhorar', str(comp_compt[a]), key=f'Comportamento a Melhorar {a + 1}')
                st.text_area(f'Plano de Ação', str(comp_Plan[a]), key=f'Plano de Ação {a + 1}')
                st.text_area(f'Recursos Necessários | Acompanhamento', str(comp_Recurs[a]), key=f'Recursos Necessários | Acompanhamento {a + 1}')
                st.text_area(f'Resultado Previsto', str(comp_Result[a]), key=f'Resultado Previsto {a + 1}')
                st.write("---")

                botao = st.button('Atualizar Compromisso', key=f'Botão{comp_compt[a]} - {a}')
                
                if botao:  
                    cursor_update_comp = conexao.cursor()

                    comandBDCheck = f'UPDATE compromissos_9box SET check_conclui = {check_for_bd} WHERE (matricula = {matricula}) AND (id = "{id[a]}");'
                    cursor_update_comp.execute(comandBDCheck)
                    conexao.commit() 
                    st.success('Informações atualizadas com sucesso!')

                    cursor_update_comp.close()
            ###################### FEEDBACK ##########################
            with tab2:
                #DADOS DE FEEDBACKS DO COMPROMISSO
                mycursor = conexao.cursor()

                comando_sql = f'SELECT * FROM feedbacks_on_compromissos WHERE(id_compromisso = {id[a]});'
                mycursor.execute(comando_sql)
                feedbacks_bd = mycursor.fetchall()
                
                mycursor.close()
                hoje = date.today()
                if len(feedbacks_bd) > 0:
                    index_list_bd = len(feedbacks_bd) - 1
                    data_hora_bd = feedbacks_bd[index_list_bd][1]
                    data_bd = data_hora_bd.date().isoformat()

                else:
                    data_bd = None

                #DESEMPENHO FEEDBACK
                
                if len(feedbacks_bd) > 0:
                    maior = 0
                #
                    for feed in list(feedbacks_bd):
                        if feed[0] > maior:
                            maior = feed[0]
                            ultimo_feed = list(feed)
                            ultimo_desemp = ultimo_feed[4]
                else:
                    ultimo_desemp = 0

                st.text(' ')
                #desempenho = st.slider('Avanço no compromisso', 0, 100,(0, ultimo_desemp), step=10,  key=f'Conclusão do compromisso {a + 1}')
                
                st.text(' ')
                feedback = st.text_area('Feedback', key = f'feedback {a}')

                botao2 = st.button('Vincular feedback', key=f'Vincular feedback {a}')

                if botao2:
                    mycursor_feedback = conexao.close()
                    if str(hoje) == str(data_bd):
                        st.warning('Já foi dado um feedback a esse compromisso no dia de hoje.')
                    else:
                        comandFeed = f"INSERT INTO feedbacks_on_compromissos (feedback, id_compromisso) VALUES ('{feedback}', {id[a]});"
                        mycursor_feedback.execute(comandFeed)
                        conexao.commit() 
                        
                        st.success('Feedback salvo com sucesso!')

                        mycursor_feedback.close()
#######################################################################################################################################################################################3

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
    perfilUser = [x[9] for x in dadosUser if x[7] == str(username) and x[7] != None][0]
    perfilUser = ('{}'.format(perfilUser)).upper()
    
    matriculaUser = [x[4] for x in dadosUser if x[7] == str(username) and x[7] != None][0]
    
    #matric_gestores_avaliadores = list(set(limpar_lista([[x[8],x[10]] for x in listDados2])))
    tab1, tab2, tab3 = st.tabs(['PDI','One On One', 'Novos Compromissos'])

    with tab1:
        if perfilUser != 'C':
            #CONSULTANDO INFORMAÇÕES DO BANCO DE DADOS
            comando = 'SELECT * FROM compromissos_9box;'
            mycursor.execute(comando)
            compromissos_BD = mycursor.fetchall()
            
            font_BowlbyOne_TITLE_center('PDI')

            if str(perfilUser) == 'B':
                matric_geridos_by_gestor = [x[0] for x in listDados2 if int(x[8]) == int(matriculaUser) or int(x[10]) == int(matriculaUser)]
                
                compromissos_BD = [x for x in compromissos_BD if x[2] in matric_geridos_by_gestor]

            elif str(perfilUser) == 'BP':
                unidades_BP = [str(y).replace("['", "").replace("']", "") for y in (str([x[10] for x in dadosUser if str(x[4]) == f'{matriculaUser}']).split(', '))]
                matriColab_to_unidade = list(set([x[0] for x in listDados2 if x[2] in unidades_BP]))
                
                compromissos_BD = [x for x in compromissos_BD if x[2] in matriColab_to_unidade]

            if len(compromissos_BD) > 0:
                matriculas_with_compromiss = list(set([x[2] for x in compromissos_BD]))
                unidades_with_compromiss = list(set([x[2] for x in listDados2 if x[0] in matriculas_with_compromiss]))

    ##################################################################### TRATANDO OS DADOS #####################################################################
                if perfilUser != 'B':
                    total_andamento = {} 
                    total_vencido = {}
                    total_concluido = {}   
                    total_compromissos = {}
                
                    #SEPARANDO AS MATRICULAS POR UNIDADE QUE TEM COMPROMISSO
                    matric_por_unidade = {}

                    #SEPARANDO OS COMPROMISSOS POR UNIDADE 
                    compromissos_por_unidade = {}

                    #SEPARANDO A CONVERSÃO DE COMPROMISSOS POR UNIDADE
                    conversao_por_unidade = {}
                    #DESCOBRINDO QUAL COLABORADOR É DE QUAL UNIDADE
                    for unidade in unidades_with_compromiss:

                        matric_daquela_unidade_com_compromiss = []
                        for colab in listDados2:
                            if colab[0] in matriculas_with_compromiss and str(colab[2]) == str(unidade):
                                matric_daquela_unidade_com_compromiss.append(colab[0])
                            
                        matric_por_unidade[f'{unidade}'] = list(set(matric_daquela_unidade_com_compromiss))

                        comprom_daquela_unidad = [x for x in compromissos_BD if x[2] in matric_daquela_unidade_com_compromiss]
                        
                        #FAZENDO UM LOOP PARA SABER A TAXA DE CONVERSÃO DOS COMPROMISSOS DAQUELA UNIDADE
                        conversao = (len([x for x in comprom_daquela_unidad if str(x[10]) == '1']) / len(comprom_daquela_unidad)) * 100

                        conversao_por_unidade[f'{unidade}'] = conversao
                        compromissos_por_unidade[f'{unidade}'] = comprom_daquela_unidad

                        conversao_por_unidade['Todos'] = round((len([x for x in compromissos_BD if str(x[10]) == '1']) / len(compromissos_BD)) * 100, 1)
                        
                    for unidade in unidades_with_compromiss:
                        #VENCIDOS DAQUELA UNIDADE 
                        vencid = [x for x in compromissos_por_unidade[f'{unidade}'] if str(x[10]) != '1' and date.today() > string_to_datetime(x[9])]

                        #QUANDTIDADE EM ANDAMENTO DAQUELA UNIDADE
                        andamento = [x for x in compromissos_por_unidade[f'{unidade}'] if str(x[10]) != '1' and date.today() < string_to_datetime(x[9])]
                        
                        #QUANTIDADE CONCLUIDOS DAQUELA UNIDADE
                        concluidos = [x for x in compromissos_por_unidade[f'{unidade}'] if str(x[10]) == '1']

                        total_daquela_unidade = len(compromissos_por_unidade[f'{unidade}'])
                        total_compromissos[f'{unidade}'] = total_daquela_unidade
                        total_concluido[f'{unidade}'] = len(concluidos)
                        total_andamento[f'{unidade}'] = len(andamento)
                        total_vencido[f'{unidade}'] = len(vencid)

                if perfilUser == 'B':
                    avaliador_do_gestor = list(set([x[10] for x in listDados2 if str(x[8]) == str(matriculaUser)]))

                    avaliados_by_avaliador_with_comprom = {}
                    for matricula_aval in avaliador_do_gestor:
                        avaliados = list(set([x[0] for x in listDados2 if str(x[10]) == str(matricula_aval)]))    

                        name_avaliador = list(set([x[9] for x in listDados2 if int(x[10]) == int(matricula_aval)]))[0]

                        #COMPROMISSOS DOS COLABORADORES DAQUELE AVALIADOR
                        avaliados_by_avaliador_with_comprom[f'{name_avaliador}'] = [x for x in compromissos_BD if x[2] in avaliados]

                    
                    avaliadores = avaliados_by_avaliador_with_comprom.keys()

                    #MEDIA DE CONCLUSÃO DOS COMPROMISSOS 
                    media_avaliadores = {}
                    total_concluido = {}   
                    total_andamento = {}
                    total_vencido = {}
                    total_compromissos = {}

                    for name_aval in avaliadores:
                        if len(avaliados_by_avaliador_with_comprom[f'{name_aval}']) > 0:
                            total_comp = len(avaliados_by_avaliador_with_comprom[f'{name_aval}'])
                            total_comp_concl = len([x for x in avaliados_by_avaliador_with_comprom[f'{name_aval}'] if str(x[10]) == '1'])
                        
                            media_avaliadores[f'{name_aval}'] = (total_comp_concl / total_comp) * 100

                            #VENCIDOS DAQUELE AVALIADOR 
                            vencid = [x for x in avaliados_by_avaliador_with_comprom[f'{name_aval}'] if str(x[10]) != '1' and date.today() > string_to_datetime(x[9])]

                            #QUANDTIDADE EM ANDAMENTO DAQUELE AVALIADOR
                            andamento = [x for x in avaliados_by_avaliador_with_comprom[f'{name_aval}'] if str(x[10]) != '1' and date.today() <= string_to_datetime(x[9])]
                            
                            #QUANTIDADE CONCLUIDOS DAQUELE AVALIADOR
                            concluidos = [x for x in avaliados_by_avaliador_with_comprom[f'{name_aval}'] if str(x[10]) == '1']

                            #QUANTIDADE TOTAL DAQUELE AVALIADOR
                            total = [x for x in avaliados_by_avaliador_with_comprom[f'{name_aval}']]

                            total_vencido[f'{name_aval}'] = len(vencid)
                            total_andamento[f'{name_aval}'] = len(andamento)
                            total_concluido[f'{name_aval}'] = len(concluidos)
                            total_compromissos[f'{name_aval}'] = len(total)

                #TOTAL DE TODAS AS UNIDADES
                valor1 = str(contador_basico(compromissos_BD))
                total_compromissos['Todos'] = round(float(valor1), 1)

                #TODAS UNIDADE CONCLUIDOS
                valor2 = str(contador_basico([x for x in compromissos_BD if x[10] == '1']))
                total_concluido['Todos'] = round(float(valor2), 1)

                #TOTAL COMPROMISSOS ANDAMENTO
                valor3 = str(len([x for x in compromissos_BD if x[10] != '1' and date.today() <= string_to_datetime(x[9])]))
                total_andamento['Todos'] = round(float(valor3), 1)

                #TOTAL COMPROMISSOS VENCIDO
                valor4 = str(len([x for x in compromissos_BD if x[10] != '1' and date.today() > string_to_datetime(x[9])]))
                total_vencido['Todos'] = round(float(valor4), 1)

                if perfilUser == 'B':
                    #PORCENTAGEM COMPROMISSOS
                    media_avaliadores['Todos'] = round((float(total_concluido['Todos']) /float(total_compromissos['Todos'])) * 100, 2)
                

    ######################################################### APRESENTAÇÕES DO FRONT #########################################################
                col1, col2 = st.columns((1,4))
                
                
                #CASO O USUÁRIO SEJA "A" VÁRIAVEL ARMAZENARA UNIDADES
                if perfilUser != 'B':
                    unidade_or_avaliadr = st.selectbox('adwda', list(conversao_por_unidade.keys()), index=[x for x in range(len(list(conversao_por_unidade.keys()))) if list(conversao_por_unidade.keys())[x] == 'Todos'][0], label_visibility='hidden')
                    
                    if unidade_or_avaliadr != 'Todos':
                        matriculas_unidade_or_avaliadr = set([x[0] for x in listDados2 if str(x[2]) == str(unidade_or_avaliadr)])
                        matriculas_with_compromiss = list(set(matriculas_unidade_or_avaliadr) & set(matriculas_with_compromiss))
                    else:
                        matriculas_unidade_or_avaliadr = set([x[0] for x in listDados2])
                        matriculas_with_compromiss = list(set(matriculas_unidade_or_avaliadr) & set(matriculas_with_compromiss))

                
                #CASO O USUÁRIO SEJA "B" VÁRIAVEL ARMAZENARA AVALIADORES
                if perfilUser == 'B':
                    unidade_or_avaliadr = st.selectbox('adwda', list(total_compromissos.keys()),index=[x for x in range(len(list(total_compromissos.keys()))) if str(list(total_compromissos.keys())[x]) == 'Todos'][0], label_visibility='hidden')
                    
                    if unidade_or_avaliadr != 'Todos':
                        matriculas_unidade_or_avaliadr = [x[2] for x in avaliados_by_avaliador_with_comprom[f'{unidade_or_avaliadr}']]
                        matriculas_with_compromiss = list(set(matriculas_unidade_or_avaliadr) & set(matriculas_with_compromiss))
                    
                    else:
                        matriculas_unidade_or_avaliadr = set([x[0] for x in listDados2])
                        matriculas_with_compromiss = list(set(matriculas_unidade_or_avaliadr) & set(matriculas_with_compromiss))

                
                col1, col2, col3, col4 = st.columns(4)
                #TOTAL DE COMPROMISSOS

                if len(compromissos_BD) > 0:
                    with col1:
                        title = 'Total'
                        valor = str(total_compromissos[f'{unidade_or_avaliadr}'])
                        porc = ''
                        min_val = 0
                        max_val = float(valor)

                        displayInd(title, valor, min_val, max_val)
                        

                    #COMPROMISSOS EXECUTADOS
                    with col4:
                        title = 'Concluído'
                        valor = str(total_concluido[f'{unidade_or_avaliadr}'])
                        displayInd(title, valor, min_val, max_val)
                        

                    #COMPROMISSOS PENDENTES
                    with col2:
                        title = 'Em andamento'
                        valor = str(total_andamento[f'{unidade_or_avaliadr}'])
                        displayInd(title, valor, min_val, max_val)
                        

                    #COMPROMISSOS VENCIDOS
                    with col3:
                        title = 'Atrasado'
                        valor = str(total_vencido[f'{unidade_or_avaliadr}'])
                        displayInd(title, valor, min_val, max_val)
                        
            
                    #$$$$$$$$$$$$$$$$$$ GRÁFICOS $$$$$$$$$$$$$$$$$$$$
            
                    col1, col2 = st.columns((1.5,2.5))
                    
                    if perfilUser != 'B':
                        with col2:
                            st.text(' ')
                            st.text(' ')
                            st.text(' ')
                            font_BowlbyOne_SUBTITLE('Porcentual da Unidade')
                            progress_bar(conversao_por_unidade[f'{unidade_or_avaliadr}'], f'{unidade_or_avaliadr}')

                        with col1:
                            @st.cache_data
                            def grafico_pizza(nomes, valores):
                                #NOMES E VALORES SÃO LISTAS
                                colors = ['#0077B6', '#60B9CC', '#FDB813', '#F77737']
                                
                                fig = go.Figure(data=[go.Pie(labels=nomes, values=valores, hole=.3, marker=dict(colors=colors))])

                                fig.update_traces(hole=.5, hoverinfo="label+percent+name")
                                fig.update_layout(margin=dict(l=0, r=370, t=100, b=100),
                                                legend=dict(orientation='h', yanchor='top', y=1.25, xanchor='left', x=0.1))  
                                                # Define a margem esquerda como zero

                                st.plotly_chart(fig, theme="streamlit")

                            grafico_pizza(['Em Andamento', 'Atrasado', 'Concluido'], [total_andamento[f'{unidade_or_avaliadr}'], total_vencido[f'{unidade_or_avaliadr}'], total_concluido[f'{unidade_or_avaliadr}']])


                    if perfilUser == 'B':
                        with col2:
                            st.text(' ')                       
                            st.text(' ')
                            st.text(' ')
                            font_BowlbyOne_SUBTITLE('Porcentual do Avaliador')
                            
                            progress_bar(media_avaliadores[f'{unidade_or_avaliadr}'], f'{unidade_or_avaliadr}')

                        with col1:
                            @st.cache_data
                            def grafico_pizza(nomes, valores):
                                #NOMES E VALORES SÃO LISTAS
                                colors = ['#0077B6', '#60B9CC', '#FDB813', '#F77737']
                                
                                fig = go.Figure(data=[go.Pie(labels=nomes, values=valores, hole=.3, marker=dict(colors=colors))])

                                fig.update_traces(hole=.5, hoverinfo="label+percent+name")
                                fig.update_layout(margin=dict(l=0, r=370, t=100, b=100),
                                                legend=dict(orientation='h', yanchor='top', y=1.25, xanchor='left', x=0.1))  
                                                # Define a margem esquerda como zero

                                st.plotly_chart(fig, theme="streamlit")

                            grafico_pizza(['Em Andamento', 'Atrasado', 'Concluido'], [total_andamento[f'{unidade_or_avaliadr}'], total_vencido[f'{unidade_or_avaliadr}'], total_concluido[f'{unidade_or_avaliadr}']])


                ################################### GRÁFICO DE BARRAS ###################################                
                    if perfilUser != 'B':
                        name_grafic = 'Unidade'
                    elif perfilUser == 'B':
                        name_grafic = 'Avaliador'
                    
                    if unidade_or_avaliadr != 'Todos':
                        total_vencido = {'Todos':total_vencido['Todos'],
                                        f'{unidade_or_avaliadr}': total_vencido[f'{unidade_or_avaliadr}']}
                        total_concluido = {'Todos':total_concluido['Todos'],
                                        f'{unidade_or_avaliadr}': total_concluido[f'{unidade_or_avaliadr}']}
                        opcoes_grafics_user = [total_vencido, total_concluido]

                    else:
                        opcoes_grafics_user = [total_vencido, total_concluido]

                    font_BowlbyOne_SUBTITLE('Compromissos Concluidos')
                    grafic_barra = pd.DataFrame({f'{name_grafic}': opcoes_grafics_user[1]})
                    st.bar_chart(grafic_barra)
                                    

                    font_BowlbyOne_SUBTITLE('Compromissos Atrasados')
                    grafic_barra = pd.DataFrame({f'{name_grafic}': opcoes_grafics_user[0]})
                    st.bar_chart(grafic_barra)

                ################################### PORCENTUAL NOS COMPROMISSOS ################################### 
                    font_BowlbyOne_SUBTITLE_center('PORCENTUAL NOS COMPROMISSOS')
                    

                    media_compromissos_colabs = []
                    for matricula in matriculas_with_compromiss:
                        comprom_total = len([x[10] for x in compromissos_BD if str(x[2]) == str(matricula)])
                        comprom_check = len([x[10] for x in compromissos_BD if str(x[2]) == str(matricula) and str(x[10]) == '1'])
                            
                        porc = (comprom_check / comprom_total) * 100

                        media_compromissos_colabs.append([matricula, list(set([x[3] for x in compromissos_BD if str(x[2]) == str(matricula)]))[0], porc])

                    media_compromissos_colabs = sort_descending_by_index2(media_compromissos_colabs)
                    cardPlotNew([x[1] for x in media_compromissos_colabs],[x[2] for x in media_compromissos_colabs])
            else:
                st.warning('Visualização não disponível por ausência de dados.')
        
        elif perfilUser == 'C':
            #CONSULTANDO INFORMAÇÕES DO BANCO DE DADOS
            comando = 'SELECT * FROM compromissos_9box;'
            mycursor.execute(comando)
            compromissos_BD = mycursor.fetchall()
            
            matricula_avaliados = [str(x[0]) for x in listDados2 if str(x[10]) == str(matriculaUser)]
            compromissos_BD = [x for x in compromissos_BD if str(x[2]) in matricula_avaliados]

            font_BowlbyOne_TITLE_center('PDI')

            if len(compromissos_BD) > 0:
                matriculas_with_compromiss = list(set([x[2] for x in compromissos_BD]))
                unidades_with_compromiss = list(set([x[2] for x in listDados2 if x[0] in matriculas_with_compromiss]))

    ##################################################################### TRATANDO OS DADOS #####################################################################
                total_andamento = {} 
                total_vencido = {}
                total_concluido = {}   
                total_compromissos = {}
            
                #SEPARANDO AS MATRICULAS POR UNIDADE QUE TEM COMPROMISSO
                matric_por_unidade = {}

                #SEPARANDO OS COMPROMISSOS POR UNIDADE 
                compromissos_por_unidade = {}

                #SEPARANDO A CONVERSÃO DE COMPROMISSOS POR UNIDADE
                conversao_por_unidade = {}



                #DESCOBRINDO QUAL COLABORADOR É DE QUAL UNIDADE
                for unidade in unidades_with_compromiss:

                    matric_daquela_unidade_com_compromiss = []
                    for colab in listDados2:
                        if colab[0] in matriculas_with_compromiss and str(colab[2]) == str(unidade):
                            matric_daquela_unidade_com_compromiss.append(colab[0])
                        
                    matric_por_unidade[f'{unidade}'] = list(set(matric_daquela_unidade_com_compromiss))

                    comprom_daquela_unidad = [x for x in compromissos_BD if x[2] in matric_daquela_unidade_com_compromiss]
                    
                    #FAZENDO UM LOOP PARA SABER A TAXA DE CONVERSÃO DOS COMPROMISSOS DAQUELA UNIDADE
                    conversao = (len([x for x in comprom_daquela_unidad if str(x[10]) == '1']) / len(comprom_daquela_unidad)) * 100

                    conversao_por_unidade[f'{unidade}'] = conversao
                    compromissos_por_unidade[f'{unidade}'] = comprom_daquela_unidad

                    conversao_por_unidade['Todos'] = round((len([x for x in compromissos_BD if str(x[10]) == '1']) / len(compromissos_BD)) * 100, 1)
                    
                for unidade in unidades_with_compromiss:
                    #VENCIDOS DAQUELA UNIDADE 
                    vencid = [x for x in compromissos_por_unidade[f'{unidade}'] if str(x[10]) != '1' and date.today() > string_to_datetime(x[9])]

                    #QUANDTIDADE EM ANDAMENTO DAQUELA UNIDADE
                    andamento = [x for x in compromissos_por_unidade[f'{unidade}'] if str(x[10]) != '1' and date.today() < string_to_datetime(x[9])]
                    
                    #QUANTIDADE CONCLUIDOS DAQUELA UNIDADE
                    concluidos = [x for x in compromissos_por_unidade[f'{unidade}'] if str(x[10]) == '1']

                    total_daquela_unidade = len(compromissos_por_unidade[f'{unidade}'])
                    total_compromissos[f'{unidade}'] = total_daquela_unidade
                    total_concluido[f'{unidade}'] = len(concluidos)
                    total_andamento[f'{unidade}'] = len(andamento)
                    total_vencido[f'{unidade}'] = len(vencid)


                #TOTAL DE TODAS AS UNIDADES
                valor1 = str(contador_basico(compromissos_BD))
                total_compromissos['Todos'] = round(float(valor1), 1)

                #TODAS UNIDADE CONCLUIDOS
                valor2 = str(contador_basico([x for x in compromissos_BD if x[10] == '1']))
                total_concluido['Todos'] = round(float(valor2), 1)

                #TOTAL COMPROMISSOS ANDAMENTO
                valor3 = str(len([x for x in compromissos_BD if x[10] != '1' and date.today() <= string_to_datetime(x[9])]))
                total_andamento['Todos'] = round(float(valor3), 1)

                #TOTAL COMPROMISSOS VENCIDO
                valor4 = str(len([x for x in compromissos_BD if x[10] != '1' and date.today() > string_to_datetime(x[9])]))
                total_vencido['Todos'] = round(float(valor4), 1)

    ######################################################### APRESENTAÇÕES DO FRONT #########################################################
                            
                col1, col2, col3, col4 = st.columns(4)
                #TOTAL DE COMPROMISSOS

                if len(compromissos_BD) > 0:
                    with col1:
                        title = 'Total'
                        valor = str(total_compromissos[f'Todos'])
                        porc = ''
                        min_val = 0
                        max_val = float(valor)

                        displayInd(title, valor, min_val, max_val)
                        

                    #COMPROMISSOS EXECUTADOS
                    with col4:
                        title = 'Concluído'
                        valor = str(total_concluido[f'Todos'])
                        displayInd(title, valor, min_val, max_val)
                        

                    #COMPROMISSOS PENDENTES
                    with col2:
                        title = 'Em andamento'
                        valor = str(total_andamento[f'Todos'])
                        displayInd(title, valor, min_val, max_val)
                        

                    #COMPROMISSOS VENCIDOS
                    with col3:
                        title = 'Atrasado'
                        valor = str(total_vencido[f'Todos'])
                        displayInd(title, valor, min_val, max_val)
                        
            
                    #$$$$$$$$$$$$$$$$$$ GRÁFICOS $$$$$$$$$$$$$$$$$$$$
            
                    col1, col2 = st.columns((1.5,2.5))
                    
                    if perfilUser != 'B':
                        with col2:
                            st.text(' ')
                            st.text(' ')
                            st.text(' ')
                            font_BowlbyOne_SUBTITLE('Porcentual do Avaliador')
                            progress_bar(conversao_por_unidade[f'Todos'], f'Todos')

                        with col1:
                            @st.cache_data
                            def grafico_pizza(nomes, valores):
                                #NOMES E VALORES SÃO LISTAS
                                colors = ['#0077B6', '#60B9CC', '#FDB813', '#F77737']
                                
                                fig = go.Figure(data=[go.Pie(labels=nomes, values=valores, hole=.3, marker=dict(colors=colors))])

                                fig.update_traces(hole=.5, hoverinfo="label+percent+name")
                                fig.update_layout(margin=dict(l=0, r=370, t=100, b=100),
                                                legend=dict(orientation='h', yanchor='top', y=1.25, xanchor='left', x=0.1))  
                                                # Define a margem esquerda como zero

                                st.plotly_chart(fig, theme="streamlit")

                            grafico_pizza(['Em Andamento', 'Atrasado', 'Concluido'], [total_andamento[f'Todos'], total_vencido[f'Todos'], total_concluido[f'Todos']])



                        with col1:
                            @st.cache_data
                            def grafico_pizza(nomes, valores):
                                #NOMES E VALORES SÃO LISTAS
                                colors = ['#0077B6', '#60B9CC', '#FDB813', '#F77737']
                                
                                fig = go.Figure(data=[go.Pie(labels=nomes, values=valores, hole=.3, marker=dict(colors=colors))])

                                fig.update_traces(hole=.5, hoverinfo="label+percent+name")
                                fig.update_layout(margin=dict(l=0, r=370, t=100, b=100),
                                                legend=dict(orientation='h', yanchor='top', y=1.25, xanchor='left', x=0.1))  
                                                # Define a margem esquerda como zero

                                st.plotly_chart(fig, theme="streamlit")


                ################################### GRÁFICO DE BARRAS ###################################                
                    def obter_primeiro_e_segundo_nome(nome_completo):
                        nomes = nome_completo.split()
                        primeiro_nome = nomes[0]
                        segundo_nome = nomes[1] if len(nomes) > 1 else ""

                        return f'{primeiro_nome} {segundo_nome}'


                    #opcoes_grafics_user = [total_vencido, total_concluido]

                    col1, colE, col2 = st.columns([1,0.1, 1])

                    comprom_concluid = {}
                    comprom_atrasad = {}
                    for matrc in matriculas_with_compromiss:
                        qntd_concluid = len([x for x in compromissos_BD if x[2] == matrc and str(x[10]) == '1'])
                        qntd_atrasad = len([x for x in compromissos_BD if x[2] == matrc and string_to_datetime(x[9]) < date.today()])
                        
                        comprom_concluid[f'{[obter_primeiro_e_segundo_nome(x[1]) for x in listDados2 if x[0] == matrc][0]}'] = qntd_concluid
                        comprom_atrasad[f'{[obter_primeiro_e_segundo_nome(x[1]) for x in listDados2 if x[0] == matrc][0]}'] = qntd_atrasad
                    
                    with col1:
                        font_BowlbyOne_SUBTITLE('Compromissos Concluidos')
                        grafic_barra = pd.DataFrame({f'Avaliados': comprom_concluid})
                        st.bar_chart(grafic_barra)                                    
                    with col2:
                        font_BowlbyOne_SUBTITLE('Compromissos Atrasados')
                        grafic_barra = pd.DataFrame({f'Avaliados': comprom_atrasad})
                        st.bar_chart(grafic_barra)

                ################################### PORCENTUAL NOS COMPROMISSOS ################################### 
                    font_BowlbyOne_SUBTITLE_center('PORCENTUAL NOS COMPROMISSOS')
                    

                    media_compromissos_colabs = []
                    for matricula in matriculas_with_compromiss:
                        comprom_total = len([x[10] for x in compromissos_BD if str(x[2]) == str(matricula)])
                        comprom_check = len([x[10] for x in compromissos_BD if str(x[2]) == str(matricula) and str(x[10]) == '1'])
                            
                        porc = (comprom_check / comprom_total) * 100

                        media_compromissos_colabs.append([matricula, list(set([x[3] for x in compromissos_BD if str(x[2]) == str(matricula)]))[0], porc])

                    media_compromissos_colabs = sort_descending_by_index2(media_compromissos_colabs)
                    cardPlotNew([x[1] for x in media_compromissos_colabs],[x[2] for x in media_compromissos_colabs])
            else:
                st.warning('Visualização não disponível por ausência de dados.')
    with tab2:
        if perfilUser != 'C':
            linhaBD = 0

            
            #DESCOBRINDO O PERFIL DO USUÁRIO
            matricula_user = matriculaUser
            perfil_user = perfilUser
            
            if perfil_user == 'A':
                dados_colaboradors = listDados2
            elif perfil_user == 'BP':
                unidades_BP = [str(y).replace("['", "").replace("']", "") for y in (str([x[10] for x in dadosUser if str(x[4]) == f'{matricula_user}']).split(', '))]
                dados_colaboradors = [x for x in listDados2 if x[2] in unidades_BP]

            else:
                dados_colaboradors = [x for x in listDados2 if x[8] == matricula_user or x[10] == matricula_user] 

            col1, col2 = st.columns((3,1))  
            
            with col1:
                st.text(' ')
                font_BowlbyOne_TITLE('ONE ON ONE')
            
            with col2:    
                radio = st.radio("Pesquisar por:",['Matricula', 'Filtro'])

            st.text('')
            if radio == 'Filtro':
                Unidade = st.multiselect("Unidade de negócio", set([x[2] for x in dados_colaboradors if x[2] != '' and x[2] != None and x[2] != 'Zero']),
                                                                set([x[2] for x in dados_colaboradors if x[2] != '' and x[2] != None and x[2] != 'Zero']))
                if len(Unidade) < 1:
                    st.info("Não há uma unidade selecionada")
                else:
                    mplist = set([x[3] for x in dados_colaboradors if x[2] in Unidade])
                    macroprocesso = st.multiselect('Macroprocesso', mplist, mplist)
                    if len(macroprocesso) < 1:
                            st.info("Não há um macroprocesso selecionado")
                    else:
                        FuncList = set([x[40] for x in dados_colaboradors if x[2] in Unidade and x[3] in macroprocesso])
                        funcao = st.multiselect('Função', FuncList, FuncList)
                        if len(funcao) < 1:
                            st.info("Não há uma função selecionada")
                        else:
                            col1, col2 = st.columns((3,1))
                            with col1:
                                gclist = set([x[1] for x in dados_colaboradors if x[3] in macroprocesso and x[2] in Unidade and x[40] in funcao and x[1] != 'ZERO'])
                                name_colaborador = st.selectbox('Colaborador', gclist)
                            if len(name_colaborador) < 1:
                                st.info("Não há um colaborador selecionado")
                            else:
                                linhaBD = [x for x in range(len(dados_colaboradors)) if dados_colaboradors[x][1] == name_colaborador][0]
                                with col2:
                                    #matricula do colaborador escolhido
                                    matricula_user = st.text_input('Matricula', dados_colaboradors[linhaBD][0])

            elif radio == 'Matricula':
                st.text(' ')
                col1, col2, col3 = st.columns((0.34, 1.25, 1.1))
                with col1:
                    matricula_user = st.text_input('Matricula')
                
                matriculasBD = list(set([str(x[0]) for x in dados_colaboradors if x[1] != 'ZERO']))
                if matricula_user not in matriculasBD:
                    with col2:   
                        st.text_input('', 'Colaborador não encontrado')         
                else:
                    with col2:   
                        st.text_input("Nome Colaborador", list(set([x[1] for x in dados_colaboradors if str(x[0]) == matricula_user]))[0])
                    
                    with col3:
                        periodos = [f'{converte_data(x[12])} - {converte_data(x[13])}' for x in dados_colaboradors if str(x[0]) == matricula_user]
                        anoQuadr = st.selectbox('Período', periodos)
                        linhaBD = [x for x in range(len(dados_colaboradors)) if dados_colaboradors[x][0] == int(matricula_user) and f'{converte_data(dados_colaboradors[x][12])} - {converte_data(dados_colaboradors[x][13])}' == anoQuadr][0]    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.text_input('Função', dados_colaboradors[linhaBD][40])
                    with col2:
                        st.text_input("Unidade de negócio", dados_colaboradors[linhaBD][2])
                    with col3:
                        st.text_input('Macroprocesso', dados_colaboradors[linhaBD][3])
                    st.text_input('Processo', dados_colaboradors[linhaBD][4])
                    col1, col2 = st.columns(2)
                    with col1:
                        st.text_input('Gestor de Carreira', dados_colaboradors[linhaBD][7])
                    with col2:
                        st.text_input('Avaliador', dados_colaboradors[linhaBD][9])

            if linhaBD > 0:
                st.text(' ')
                st.text(' ')
                st.text(' ')
                st.text(' ')
                visualizacao_Compromissos_PDI(dados_colaboradors, linhaBD, matricula_user)
                st.text(' ')
                st.text(' ')
                st.text(' ')
                st.text(' ')
                st.text(' ')
                st.text(' ')


                font_BowlbyOne_SUBTITLE_center('DESENVOLVIMENTO DOS COMPROMISSOS')

                comando = f'SELECT * FROM compromissos_9box WHERE(matricula = {matricula_user});'
                mycursor.execute(comando)
                compromissos_user = mycursor.fetchall()

                st.text(' ')

                compromisso_escolhid = st.selectbox('Compromisso',list(set([x[4] for x in compromissos_user])))
                
                dados_compro = [x for x in compromissos_user if x[4] == compromisso_escolhid] 
                
                if len(dados_compro) > 0:
                    comandoSQL_feed = f'SELECT * FROM feedbacks_on_compromissos WHERE(id_compromisso = {dados_compro[0][0]});'
                    mycursor.execute(comandoSQL_feed)
                    feedbacks_BD = mycursor.fetchall()
                    st.text(' ')
                    st.text(' ')

                    font_link = "https://fonts.googleapis.com/css?family=Roboto"

                    font_style = """
                                <style>
                                @import url('"""+font_link+"""');
                                p {
                                    font-family: 'Roboto', sans-serif;
                                    font-size: 20px;
                                }
                                </style>
                                """

                    st.markdown(font_style, unsafe_allow_html=True)

                    if len(feedbacks_BD) > 0:
                        font_BowlbyOne_SUBTITLE("Feedbacks")
                        st.text(' ')

                        dic_for_df = {}
                        for rang in range(len(feedbacks_BD)):
                            data_hora_bd = feedbacks_BD[rang][1]
                            data_bd = str(data_hora_bd.date().isoformat())

                            with st.container():
                                st.caption(f'{rang + 1}° Feedback - {converte_data(data_bd)}')
                                #st.text_area('', feedbacks_BD[rang][2], key= f'{rang}')
                                st.write(feedbacks_BD[rang][2])
                            st.text(' ')  
                            st.text(' ')
                            st.write('---')

                            dic_for_df[f'{converte_data(data_bd)}'] = feedbacks_BD[rang][4]

                        #font_BowlbyOne_SUBTITLE("Desempenho")

                        #df_desemp = pd.DataFrame.from_dict(dic_for_df, orient='index', columns=['Desempenho'])

                        #st.line_chart(df_desemp)
                    else:
                        st.warning('Não há feedbacks vinculados ao compromisso selecionado.')  
        else:
            st.warning('Visualização não disponível para seu perfil.')

    with tab3:
        font_BowlbyOne_TITLE('Novos Compromissos')

        matricula = st.text_input('Matricula', key='Chaves')
        
        if perfilUser == 'A':
            listDados2 = listDados2
        elif perfilUser == 'BP':
            unidades_BP = [str(y).replace("['", "").replace("']", "") for y in (str([x[10] for x in dadosUser if str(x[4]) == f'{matricula_user}']).split(', '))]
            listDados2 = [x for x in listDados2 if x[2] in unidades_BP]
        else:
            listDados2 = [x for x in listDados2 if x[8] == matriculaUser or x[10] == matriculaUser] 

        if len(matricula) > 0: 
            linhaBD = [x for x in range(len(listDados2)) if str(listDados2[x][0]) == str(matricula)]
            
            if len(linhaBD) > 0:
                novos_compromissos(listDados2, linhaBD[0], 50, 'Processos')
            else:
                st.warning('Insira uma matricula válida')
