import streamlit as st
import streamlit_authenticator as stauth
from PIL import Image
from util import listaCompNon0, calculoDesempenho, ListaCellNineTodos2, ListaCellNineTodos, plot_all_employees1, plot_all_employees2, PlotDisperssao1, plotarRadar
from numpy import mean
import pandas as pd
import pymysql
from func_relatorio import contador_basico
from util import string_to_datetime
import plotly.graph_objects as go
from util import string_to_list
from util import displayInd2, displayInd, displayInd3, displayInd4
from dateutil.relativedelta import relativedelta
import mysql.connector

st.set_page_config(page_title="Dashboard", page_icon=Image.open('icon.png'),layout="wide")


def limpar_porc(number_string):
    number = ''
    for a in number_string:    
        if a == '.':
            break 

        elif a.isdigit():
            number = number + a
            
    return int(number)


def obter_mes(data):
    return int(data.month)


def grafico_pizza(nomes, valores):
    #NOMES E VALORES SÃO LISTAS
    colors = ['#0077B6', '#60B9CC', '#FDB813', '#F77737']
    
    fig = go.Figure(data=[go.Pie(labels=nomes, values=valores, hole=.3, marker=dict(colors=colors))])

    fig.update_traces(hole=.5, hoverinfo="label+percent+name")
    fig.update_layout(margin=dict(l=0, r=370, t=100, b=100),
                    legend=dict(orientation='h', yanchor='top', y=1.25, xanchor='left', x=0.1))  
                    # Define a margem esquerda como zero

    st.plotly_chart(fig, theme="streamlit")


def font_BowlbyOne_TITLE_center(texto):
    css1 = """
        <style>
            @import url('https://fonts.google.com/specimen/Bebas+Neue?query=Ryoichi+Tsunekawa');
            .gold-text1_center {
            font-family: 'Bowlby One SC', cursive;
            font-size: 40px;
            color: gold;
            text-align: center;}
        </style>"""
            

    st.markdown(css1, unsafe_allow_html=True)
    st.markdown(f'<p class="gold-text1_center">{texto}</p>', unsafe_allow_html=True)


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


def sort_descending_by_index2(lst):
    return sorted(lst, key=lambda x: x[1], reverse=True)


def font_BowlbyOne_SUBTITLE_center(texto):
    css = """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
            .gold-text_ {
            font-family: 'Poppins', sans-serif;
            font-size: 17px;
            color: white;
            text-align: center;}
        </style>"""
            

    st.markdown(css, unsafe_allow_html=True)
    st.markdown(f'<p class="gold-text_">{texto}</p>', unsafe_allow_html=True)

#def font_BowlbyOne_SUBTITLE_center_menor(texto):
#    css = """
#        <style>
#            @import url('https://fonts.googleapis.com/css2?family=Bowlby+One+SC&display=swap');
#            .gold-text_MENOR {
#            font-family: 'Bowlby One SC', cursive;
#            font-size: 20px;
#            color: gold;
#            }
#        </style>"""
#            
#
#    st.markdown(css, unsafe_allow_html=True)
#    st.markdown(f'<p class="gold-text_MENOR">{texto}</p>', unsafe_allow_html=True)           
#

def limpar_lista(lista_de_listas):
    lista_final = []
    for lista in lista_de_listas:
        for info in lista:
            lista_final.append(info)
    
    return lista_final


def divisaoSecao2(title):
  style23 = """
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600&display=swap');
  .card233 {
    width: 100%;
    background-color: #D4AF37;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    border-radius: 10px;
    overflow: hidden;
    border: none; /* Adiciona esta propriedade para remover a borda */
    font-family: 'Poppins', sans-serif;
  }
  .header233 {
    background-color:#D4AF37;
    color: White;
    padding: 4px;
    text-align: center;
    font-size: 22px;
    font-weight: bold;
  }
  """
  html23 = f"""<div class="card233"><div class="header233">{title}</div>"""
  st.write(f'<style>{style23}</style>', unsafe_allow_html=True)
  st.write(f'<div>{html23}</div>', unsafe_allow_html=True)
  st.write("")


def limparNomesForGrafics(nome):
    name_split = list(nome.split(' '))

    if len(name_split) >= 2:
        name_final = f'{name_split[0]} {name_split[1]}'

    else:
        name_final = f'{name_split[0]}'

    return name_final


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


conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='Colaboradores'
)

mycursor = conexao.cursor()
comando2 = 'SELECT * FROM Usuarios;'
mycursor.execute(comando2)
dadosUser = mycursor.fetchall()


names = [x[5] for x in dadosUser if x[5] != None]
usernames = [x[7] for x in dadosUser if x[7] != None]
hashed_passwords = [x[11] for x in dadosUser if x[8] != None]
funcao = [x[6] for x in dadosUser if x[6] != None]


#def convert_to_dict(names, usernames, passwords):
#    credentials = {"usernames": {}}
#    for name, username, password in zip(names, usernames, passwords):
#        user_credentials = {
#            "email":username,
#            "name": name,
#            "password": password
#        }
#        credentials["usernames"][username] = user_credentials
#    return credentials
#
#credentials = convert_to_dict(names, usernames, hashed_passwords)
#authenticator = stauth.Authenticate(credentials, "Teste", "abcde", 30)
#
#col1, col2,col3 = st.columns([1,3,1])
#with col2:
#    name, authentication_status, username = authenticator.login('Acesse o sistema 9box', 'main')
#
#if authentication_status == False:
#    with col2:
#        st.error('Email ou Senha Incorreto')
#elif authentication_status == None:
#    with col2:
#        st.warning('Insira seu Email e Senha')
#elif authentication_status:
sql = 'SELECT * FROM Colaboradores;'
mycursor.execute(sql)
listDados2 = (mycursor.fetchall())

sql = 'SELECT * FROM compromissos_9box;'
mycursor.execute(sql)
listDados3 = (mycursor.fetchall())

comando = 'SELECT * FROM feedbacks_on_compromissos;'
mycursor.execute(comando)
feedbacksBD = mycursor.fetchall()

sql_user = 'SELECT * FROM Usuarios;'
mycursor.execute(sql_user)
dados_userBD = mycursor.fetchall()

matriUser = [x[4] for x in dados_userBD if x[7] == 'processos4.eucatur@gmail.com']

matriUser = [56126]
matricula_dados = [x[0] for x in listDados2 if x[0] != None or x[0] != '']
matricula_dados_usuarios = [x[4] for x in dados_userBD if x[4] != None and x[4] != ' ']

liscod = [str(int(x[8])) for x in listDados2 if str(x[8]) != "None"] + [str(int(x[10])) for x in listDados2 if
                                                                        str(x[10]) != "None"] + ["admin"]

if matriUser != None and matriUser != '':
    if matriUser[0] in matricula_dados_usuarios:
        dados = [x for x in listDados2 if int(matriUser[0]) == x[8] or int(matriUser[0]) == x[10]]
        dados_user = [list(x) for x in dados_userBD if x[4] == matriUser[0]]

        perfil_user = str(dados_user[0][9].upper())
        
        perfil_user = 'B'
        if perfil_user == 'A' or perfil_user == 'BP':
            if perfil_user == 'BP':
                unidadesPerfil = list(str([x[10] for x in dados_userBD if str(x[4]) == str(matriUser[0])][0]).split(', '))
                listDados2 = [x for x in listDados2 if str(x[2]) in unidadesPerfil]

            divisaoSecao2("DASHBOARD ADMINISTRATIVO")

            col1,col2,col3,col4 = st.columns(4)
            
    
            with col1:
                st.write("")
                st.write("")
                st.image(Image.open(('logo.png')), width = 180)

            with col2:
                colaboComRelFuncional = len(set([x[0] for x in [y for y in listDados2 if y[28] == 1 and y[33] == 1 ]]))
                TotalColabEmpresa = 1914

                displayInd("Colab. com Rel. Funcional", str(colaboComRelFuncional), 0, TotalColabEmpresa)
            
            with col3:
                displayInd("Total de avaliações Criadas", str(len(listDados2)), 0, len(listDados2))

            with col4:
                displayInd("Avaliações Realizadas", str(len([x[28] for x in listDados2 if x[28] == 1 and x[33] == 1 ])), 0, len(listDados2))


            col1,col2 = st.columns([1,3]) 
            with col1:

                st.write("")
                percRelFunc = round((colaboComRelFuncional/TotalColabEmpresa)*100,2)

                progress_bar(percRelFunc, "% Rel. Funcional")

                colaboComPDI = len(set([x[2] for x in  listDados3]))
                percPDI = round((colaboComPDI/TotalColabEmpresa)*100, 2)

                progress_bar(percPDI, "% PDI")

            with col2:
                uniDades = ["CEEM Boa Vista - Manaus","CEEM Cacoal","CEEM Campo Grande","CEEM Cascavel","CEEM Curitiba","CEEM Goiânia","CEEM Ji-Paraná","CEEM Mato Grosso","CEEM Porto Alegre","CEEM Porto Velho","CEEM Pres. Prudente","CEEM Rio Branco","CEEM São Paulo","CEEM Vilhena","Corporativo Cascavel","Corporativo Ji-Paraná"]
                ColPorUni = [158, 125, 116,149,59,39,405,212,73,197,27,47,63,70,103,71]

                dadosGraf = [[uniDades[y],round((sum([1 for z in listDados2 if z[2] == uniDades[y] and z[28] == 1 and z[33] == 1]) * 100 /ColPorUni[y]),2)] for y in range(len(uniDades))]

                import plotly.express as px

                df = {
                    "Unidades": [x[0] for x in dadosGraf],
                    "% Rel. Funcional": [x[1] for x in dadosGraf]
                }

                fig = px.bar(df, x="Unidades", y="% Rel. Funcional", text_auto=True)

                # Atualizar o layout do gráfico
                fig.update_layout(
                    title_text='% Rel. Funcional por Unidades',
                    title_x=0.35,  # Centralizar título horizontalmente
                    title_y=0.95,
                    title_font=dict(color='black', size=18),
                    # Definir o fundo como branco
                    paper_bgcolor='white',
                    # Definir a cor de fundo do gráfico como branco
                    plot_bgcolor='ghostwhite',
                    # Definir a altura do gráfico como 495 pixels
                    height=495,
                )

                fig.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
                fig.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
                fig.update_traces(marker_color='#D4AF37')  # Definir cor das colunas

                # Renderizar o gráfico no Streamlit
                st.write(" ")
                st.plotly_chart(fig, use_container_width=True)

                
            #######################
                
            Gestores = set([x[8] for x in listDados2 if x[8] != 0 and x[8] in [y[4] for y in dadosUser if y[4] != None]])

            GestoresNomes = [ [y[5] for y in dadosUser if y[4] ==  x][0] for x in Gestores]

            ColPorGestor = []

            dadosGrafGestor = [sum([ 1 for x in listDados2 if x[8] == y ]) for y in Gestores]

            df = {"Gestores":GestoresNomes,
            "Nº Rel. Funcional": dadosGrafGestor}

            fig = px.bar(df, x="Gestores", y="Nº Rel. Funcional", text_auto=True)
            # Atualizar o layout do gráfico
            fig.update_layout(
                title_text='Nº Rel. Funcional por Gestores',
                title_x=0.40,  # Centralizar título horizontalmente
                title_y=0.95,
                title_font=dict(color='black', size=18),
                # Definir o fundo como branco
                paper_bgcolor='white',
                # Definir a cor de fundo do gráfico como branco
                plot_bgcolor='ghostwhite',
                # Definir a altura do gráfico como 600 pixels
                height=490,
                    )
            fig.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
            fig.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
            fig.update_traces(marker_color='#D4AF37')  # Definir cor das colunas
            # Renderizar o gráfico no Streamlit
            st.write(" ")
            st.plotly_chart(fig, use_container_width=True)

            macroProcessos = ["Relacionamento com Cliente - Pessoas","Relacionamento com Cliente - Cargas","Administrar","Operar","Formulação Estratégica"]              

            #MATRICULA DOS AVALIADORES
            matricula_gestores = list(set([x[8] for x in listDados2]))

            matriculas_UsersBD = list(set([(x[4]) for x in dados_userBD]))

            matricula_comum = list(set(matricula_gestores) & set(matriculas_UsersBD))

            dados_geridos = [x for x in listDados2 if (x[8]) in matricula_comum]

            soma = 0
            convers_por_avaliador = {}
            for index in range(len(matricula_comum)):
                geridos_daquele_avaliador = [x for x in dados_geridos if x[8] == matricula_comum[index]]
                
                soma += len(geridos_daquele_avaliador)
                #TOTAL DE AVALIAÇÕES CONCLUIDAS DAQUELE GESTOR
                ava_complet = len([x for x in geridos_daquele_avaliador if str(x[28]) == '1' and str(x[33]) == '1'])
                
                convers_por_avaliador[f'{[x[5] for x in dados_userBD if x[4] == matricula_comum[index]][0]}'] = (ava_complet / len(geridos_daquele_avaliador)) * 100
            

            df_to_grafic = pd.DataFrame({'Avaliadores':[limparNomesForGrafics(x) for x in convers_por_avaliador.keys()],
                                        'Conversão': [round(x, 2) for x in convers_por_avaliador.values()]})

            fig = px.bar(df_to_grafic, x="Avaliadores", y="Conversão", text_auto=True)

            # Atualizar o layout do gráfico
            fig.update_layout(
                title_text='% Rel. Funcional por Gestor',
                title_x=0.40,  # Centralizar título horizontalmente
                title_y=0.95,
                title_font=dict(color='black', size=18),
                # Definir o fundo como branco
                paper_bgcolor='white',
                # Definir a cor de fundo do gráfico como branco
                plot_bgcolor='ghostwhite',
                # Definir a altura do gráfico como 600 pixels
                height=495,
                    )

            fig.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
            fig.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
            fig.update_traces(marker_color='#D4AF37')  # Definir cor das colunas


            # Renderizar o gráfico no Streamlit
            st.write(" ")
            st.plotly_chart(fig, use_container_width=True)

            divisaoSecao2("Gestão do Desempenho")

            #OPÇÕES UNIDADES
            unidList = list(set([x[2] for x in listDados2 if x[28] == 1]))
            unidList.append('Todos')
            Unidade = st.multiselect("Unidade de negócio", unidList, ['Todos'])
            
            if 'Todos' in Unidade:
                Unidade = unidList

            if len(Unidade) < 1:
                st.info("Não há uma unidade selecionada")
            else:
                #OPÇÕES MACROPROCESSOS     
                mplist = set([x[3] for x in listDados2 if x[2] in Unidade and x[28] == 1])
                macroprocesso = st.multiselect('Macroprocesso', mplist, mplist)
                if len(macroprocesso) < 1:
                    st.info("Não há um macroprocesso selecionado")
                else:
                    #OPÇÕES PROCESSOS
                    pclist_aux = [str(x[4]).split(', ') for x in listDados2 if x[2] in Unidade and x[28] == 1 and x[3] in macroprocesso]
                    
                    pclist = list(set([str(x).replace("'", '') for x in list(sum(pclist_aux, []))]))
                    pclist.append('Todos')

                    processo = st.multiselect('Processo', pclist, ['Todos'])
                    if 'Todos' in processo:
                        processo = pclist

                    if len(processo) < 1:
                        st.info("Não há um processo selecionado")
                    else:
                        #OPÇÕES GESTORES
                        GestList = [[str([n[5] for n in dados_userBD if n[4] == x[8]]).replace("['", "").replace("']", "").replace("[","").replace("]",""), x[8]] for x in listDados2 if x[2] in Unidade and x[28] == 1 and x[3] in macroprocesso and len([w for w in [str(y).replace("'", '') for y in list(str(x[4]).split(', '))] if w in processo]) > 0]                            
                        
                        GestList.append(['Todos', None])
                        gestor = st.multiselect('Gestor', list(set([x[0] for x in GestList if len(x[0]) > 0])), ['Todos']) 
                        if 'Todos' in gestor:   
                            gestor = list(set([x[0] for x in GestList if len(x[0]) > 0]))
                    
                        if len(gestor) < 1:
                            st.info('Não há um gestor selecionado')
                        else:
                            #OPÇÕES FUNÇÕES
                            FuncList = list(set([x[40] for x in listDados2 if x[2] in Unidade and x[28] == 1 and x[3] in macroprocesso and len([w for w in [str(y).replace("'", '') for y in list(str(x[4]).split(', '))] if w in processo]) > 0 and x[8] in list(set([y[1] for y in GestList if y[0] in gestor]))] ))
                            FuncList.append('Todos')

                            funcao = st.multiselect('Função', FuncList, ['Todos'])
                            
                            if 'Todos' in funcao:
                                funcao = FuncList

                            if len(funcao) < 1:
                                st.info("Não há uma função selecionada")
                            else:
                                #OPÇÕES COLABORADORES
                                gclist = [x[1] for x in listDados2 if x[2] in Unidade and x[28] == 1 and x[3] in macroprocesso and len([w for w in [str(y).replace("'", '') for y in list(str(x[4]).split(', '))] if w in processo]) > 0 and x[8] in list(set([y[1] for y in GestList if y[0] in gestor])) and x[40] in funcao]                                     
                                
                                gclist.append('Todos')
                                gclist = set(gclist)

                                colaborador = st.multiselect('Colaborador', gclist, ['Todos'])
                                if 'Todos' in colaborador:
                                    colaborador = gclist

                                if len(colaborador) < 1:
                                    st.info("Não há um colaborador selecionado")
                                else:
                                    if 'Todos' in colaborador:
                                        listDadosAux =  [x for x in listDados2 if
                                                        x[2] in Unidade and x[3] in macroprocesso and x[1] in gclist and x[28] == 1]
                                    else:
                                        listDadosAux = [x for x in listDados2 if
                                                        x[2] in Unidade and x[3] in macroprocesso and x[1] in colaborador and x[28] == 1]
                                    
                                    listDadosAux = [[date for date in listDadosAux if date[0] == matrc][-1] for matrc in list(set([x[0] for x in listDadosAux]))]

                                    competenEucatur = ["OPPR", "Pensamento Crítico e Criativo", "Comunicação", "Foco no Cliente"]
                                    competenEspEucatur = ["Inteligência Emocional", "Autonomia e Proatividade", "Relacionamento e Network",
                                                            "Futurabilidade", "Raciocínio Analítico", "Empreendedorismo",
                                                            "Tomada de Decisão",
                                                            "Visão Estratégica", "Visão Inovadora", "Liderança", "Comprometimento", "Negociação", "Habilidades Interpessoais"]

                                    data = [[0 if str(y) == "None" else y for y in list(x[14:28])+list(x[43:46])] for x in listDadosAux]
                                    categories = competenEucatur + competenEspEucatur
                                    Nomes = [x[1] for x in listDadosAux]
                                    uniDadesAux = [x[2] for x in listDadosAux]
                                    macroProcessosAux = [x[3] for x in listDadosAux]
                                    processosAux = [x[4].replace("'","").split(",") for x in listDadosAux]
                                    data, categories = listaCompNon0(data, categories)

                                    divisaoSecao2("9Box")

                                    tab1, tab2, tab3 = st.tabs(["Unidades", "Macroprocessos", "Colaboradores"])
                                    
                                    with tab1:
                                        col1,col2,col3 = st.columns([1,6,1])
                                        with col2:
                                            divisaoSecao2("9Box Unidades")
                                            dadosNineboxAux1 = [[listDadosAux[x][1], uniDadesAux[x],macroProcessosAux[x], processosAux[x], calculoDesempenho(x, listDadosAux), int(sum(data[x]) / (len(data[x]) - data[x].count(0) - data[x].count("None")))]
                                                                for x in
                                                                range(len(listDadosAux))]
                                            dadosNineboxAuxUni = [[y,mean([x[4] for x in dadosNineboxAux1 if x[1] == y ]),mean([x[5] for x in dadosNineboxAux1 if x[1] == y ])] for y in uniDades]
                                            dadosNineboxUni = ListaCellNineTodos(dadosNineboxAuxUni)
                                            plot_all_employees2(dadosNineboxUni[0], dadosNineboxUni[1])

                                    with tab2:
                                        col1,col2,col3 = st.columns([1,6,1])
                                        with col2:
                                            divisaoSecao2("9Box Macroprocessos")
                                            dadosNineboxAuxMac = [[y,mean([x[4] for x in dadosNineboxAux1 if x[2] == y ]),mean([x[5] for x in dadosNineboxAux1 if x[2] in y ])] for y in macroProcessos]
                                            dadosNineboxMac = ListaCellNineTodos(dadosNineboxAuxMac)
                                            plot_all_employees2(dadosNineboxMac[0], dadosNineboxMac[1])

                                    with tab3:
                                        col1,col2,col3 = st.columns([1,6,1])
                                        with col2:
                                            divisaoSecao2("9Box Colaboradores")
                                            dadosNineboxAux = [[listDadosAux[x][1], calculoDesempenho(x, listDadosAux), int(sum(data[x]) / (len(data[x]) - data[x].count(0) - data[x].count("None")))]
                                                                for x in
                                                                range(len(listDadosAux))]
                                            dadosNinebox = ListaCellNineTodos(dadosNineboxAux)
                                            plot_all_employees2(dadosNinebox[0], dadosNinebox[1])
                                            

                                    divisaoSecao2("Comparar Competências Comportamentais")

                                    if len(listDadosAux) > 3:
                                        st.info("Selecione no máximo 3 colaboradores para comparar as competências comportamentais")
                                    else:
                                        lista_medias = []
                                        tab1, tab2 = st.tabs(["Radar", "Desempenho"])
                                        with tab2:
                                            st.subheader("Média de Competências")
                                            for i in range(len(Nomes)):
                                                med = int(sum(data[i]) / (len(data[i]) - data[i].count(0) - data[i].count("None")))
                                                lista_medias.append([Nomes[i], med])

                                            lista_medias = sort_descending_by_index2(lista_medias)  
                                            cardPlotNew([x[0] for x in lista_medias], [x[1] for x in lista_medias])

                                        with tab1:
                                            st.subheader("Gráfico Radar")
                                            st.pyplot(plotarRadar(data, categories, Nomes))

        elif perfil_user == 'B':
            from datetime import date

            st.image(Image.open(('logo.png')), width = 180)

            TotalColabEmpresa = 600
            
            cursor = conexao.cursor()
            comando = 'SELECT * FROM compromissos_9box;'
            cursor.execute(comando)
            compromissos_BD = cursor.fetchall()
                
            geridos_by_gestor = [x for x in listDados2 if x[10] == int(matriUser[0]) or x[8] == int(matriUser[0])]
            
            colaborador = ''

            st.text(' ')
            with st.expander('Filtro de Dados'):
                if len(geridos_by_gestor) > 0:
                    unidList = list(set([x[2] for x in geridos_by_gestor]))
                    unidList.append('Todos')
                    Unidade = st.multiselect("Unidade de negócio", unidList, ['Todos'])
                    
                    if 'Todos' in Unidade:
                        Unidade = unidList

                    if len(Unidade) < 1:
                        st.info("Não há uma unidade selecionada")
                    else:
                        #OPÇÕES MACROPROCESSOS     
                        mplist = set([x[3] for x in geridos_by_gestor if x[2] in Unidade])
                        macroprocesso = st.multiselect('Macroprocesso', mplist, mplist)
                        if len(macroprocesso) < 1:
                            st.info("Não há um macroprocesso selecionado")
                        else:
                            #OPÇÕES PROCESSOS
                            pclist_aux = [str(x[4]).split(', ') for x in geridos_by_gestor if x[2] in Unidade and x[3] in macroprocesso]
                            
                            pclist = list(set([str(x).replace("'", '') for x in list(sum(pclist_aux, []))]))
                            pclist.append('Todos')

                            processo = st.multiselect('Processo', pclist, ['Todos'])
                            if 'Todos' in processo:
                                processo = pclist

                            if len(processo) < 1:
                                st.info("Não há um processo selecionado")
                            else:
                                #OPÇÕES GESTORES
                                AvalidList = [[str([n[5] for n in dados_userBD if n[4] == x[10]]).replace("['", "").replace("']", "").replace("[","").replace("]",""), x[10]] for x in geridos_by_gestor if x[2] in Unidade and x[3] in macroprocesso and len([w for w in [str(y).replace("'", '') for y in list(str(x[4]).split(', '))] if w in processo]) > 0]                            
                                
                                AvalidList.append(['Todos', None])
                                gestor = st.multiselect('Avaliador', list(set([x[0] for x in AvalidList if len(x[0]) > 0])), ['Todos']) 
                                if 'Todos' in gestor:   
                                    gestor = list(set([x[0] for x in AvalidList if len(x[0]) > 0]))
                            
                                if len(gestor) < 1:
                                    st.info('Não há um avaliador selecionado')
                                else:
                                    #OPÇÕES FUNÇÕES
                                    FuncList = list(set([x[40] for x in geridos_by_gestor if x[2] in Unidade and x[3] in macroprocesso and len([w for w in [str(y).replace("'", '') for y in list(str(x[4]).split(', '))] if w in processo]) > 0 and x[8] in list(set([y[1] for y in AvalidList if y[0] in gestor]))] ))
                                    FuncList.append('Todos')

                                    funcao = st.multiselect('Função', FuncList, ['Todos'])
                                    
                                    if 'Todos' in funcao:
                                        funcao = FuncList

                                    if len(funcao) < 1:
                                        st.info("Não há uma função selecionada")
                                    else:
                                        #OPÇÕES COLABORADORES
                                        gclist = [x[1] for x in geridos_by_gestor if x[2] in Unidade and x[3] in macroprocesso and len([w for w in [str(y).replace("'", '') for y in list(str(x[4]).split(', '))] if w in processo]) > 0 and x[10] in list(set([y[1] for y in AvalidList if y[0] in gestor])) and x[40] in funcao]                                     
                                        
                                        gclist.append('Todos')
                                        gclist = set(gclist)

                                        colaborador = st.multiselect('Colaborador', gclist, ['Todos'])
                                        if 'Todos' in colaborador:
                                            colaborador = gclist
                                        
                                        if len(colaborador) < 1:
                                            st.info("Não há um colaborador selecionado")
                                        else:
                                            horariosList_aux = [string_to_datetime(x[12]) for x in geridos_by_gestor if x[2] in Unidade and x[3] in macroprocesso and len([w for w in [str(y).replace("'", '') for y in list(str(x[4]).split(', '))] if w in processo]) > 0 and x[10] in list(set([y[1] for y in AvalidList if y[0] in gestor])) and x[40] in funcao and x[1] in colaborador]

                                            horariosList_aux.extend([string_to_datetime(x[13]) for x in geridos_by_gestor if x[2] in Unidade and x[3] in macroprocesso and len([w for w in [str(y).replace("'", '') for y in list(str(x[4]).split(', '))] if w in processo]) > 0 and x[10] in list(set([y[1] for y in AvalidList if y[0] in gestor])) and x[40] in funcao and x[1] in colaborador])
                                            horariosList = sorted(list(set(horariosList_aux)), key=lambda x: x)

                                            #options_horario_ini, options_horario_fin = st.select_slider('Período', options=horariosList,  value=(horariosList[0], horariosList[-1]))
                                            
                                            col1, col2 = st.columns(2)
                                            with col1:
                                                options_data_inic = st.date_input('Início', date.today())
                                            with col2:
                                                options_data_fim = st.date_input('Fim', date.today() + relativedelta(months=3))

                                            if 'Todos' in colaborador:
                                                listDadosAux1 = [x for x in geridos_by_gestor if x[2] in Unidade and x[3] in macroprocesso and x[1] in gclist]
                                            else:
                                                listDadosAux1 = [x for x in geridos_by_gestor if x[2] in Unidade and x[3] in macroprocesso and x[1] in colaborador]

                                            listDadosAux = []

                                            for a in listDadosAux1:
                                                if string_to_datetime(a[12]) >= options_data_inic and string_to_datetime(a[12]) <= options_data_fim:
                                                    listDadosAux.append(a)
                                                else: 
                                                    if string_to_datetime(a[13]) >= options_data_inic and string_to_datetime(a[13]) <= options_data_fim:
                                                        listDadosAux.append(a)

                                            meses_periodo = list(range(obter_mes(options_data_inic), obter_mes(options_data_fim) + 1))

            if len(listDadosAux) < 1 and len(colaborador) > 0:
                st.warning("Ausência de dados dos colaborados e período selecionado.")
            elif len(listDadosAux) > 0:
                avaliaCriadasGestor = [y[0] for y in listDadosAux if y[8] == matriUser[0]]
                colaboComRelFuncional = len(set([x[0] for x in [y for y in listDadosAux if y[28] == 1 and y[33] == 1 and y[8] == matriUser[0]]]))
            
                compromissos_BD = [x for x in compromissos_BD if x[2] in list(set([y[0] for y in listDadosAux]))]          
            ##################### TRATAMENTO DOS DADOS ######################
                #st.write(listDadosAux)

                horas_por_colab = {}
                for date_user in listDadosAux: 
                    processos_user = list(str(date_user[4]).split(', '))

                    if date_user[50] != '' and date_user[50] != None:
                        lista_horas_user = string_to_list(date_user[50])
                        
                        #CALCULANDO HORAS POR PROCESSO
                        horas_por_process = {}
                        for rang_proc in range(len(lista_horas_user)):
                            horas_por_process[f'{processos_user[rang_proc]}'] = sum(lista_horas_user[rang_proc])

                        horas_por_colab[str(date_user[11])] = horas_por_process

                                
                #CALCULANDO AS HORAS MENSAIS DE PROCESSOS
                horas_mes_aux_proc = {}
                for x in meses_periodo:
                    horas_mes_proc = sum([sum(limpar_lista(string_to_list(y[50]))) for y in listDadosAux if x in list(range(obter_mes(string_to_datetime(y[12])), obter_mes(string_to_datetime(y[13]))+1)) and y[50] != '' and y[50] != None])

                    horas_mes_aux_proc[F'mês {x}'] = horas_mes_proc
                
                
                #CALCULANDO AS HORAS MENSAIS DE PROJETOS
                horas_mes_aux_proj = {}    
                for data in meses_periodo:
                    
                    lista_horas = []
                    for dados_user in listDadosAux:
                        if dados_user[38] == 1:
                            periodos_inc = [string_to_datetime(x) for x in string_to_list(dados_user[47])]
                            periodos_fim = [string_to_datetime(x) for x in string_to_list(dados_user[48])]
                            
                            indic_proj_doMes = [x for x in range(len(periodos_inc)) if data in list(range(obter_mes(periodos_inc[x]), obter_mes(periodos_fim[x])+1))]

                            horas_do_colab = [string_to_list(dados_user[52])[x] for x in indic_proj_doMes]
                        
                            lista_horas.append(sum(horas_do_colab))
                                        

                    horas_mes_aux_proj[f'mês {data}'] = sum(lista_horas)    

                HORAS_MES = {'Processos': horas_mes_aux_proc,
                            'Projetos': horas_mes_aux_proj}
                
                ############################# APRESENTAÇÃO DOS DADOS ################################
                T_horasProces = sum([sum(horas_por_colab[x].values()) for x in horas_por_colab.keys()])
                T_horasProjes = sum(([sum(string_to_list(x[52])) for x in listDadosAux if x[52] != None]))
                
                divisaoSecao2('Relatório Funcional')

                import plotly.express as px
                macroProcessos = ["Relacionamento com Cliente - Pessoas","Relacionamento com Cliente - Cargas","Administrar","Operar","Formulação Estratégica"]                
            
                #MATRICULA DOS AVALIADORES
                matricula_avaliadores = list(set([(x[10]) for x in listDadosAux if x[8] == matriUser[0]]))

                matriculas_UsersBD = list(set([(x[4]) for x in dados_userBD]))

                matricula_comum = list(set(matricula_avaliadores) & set(matriculas_UsersBD))

                dados_geridos = [x for x in listDadosAux if x[10] in matricula_comum]

                soma = 0
                convers_por_avaliador = {}
                for index in range(len(matricula_comum)):
                    geridos_daquele_avaliador = [x for x in dados_geridos if x[10] == matricula_comum[index]]
                    
                    soma += len(geridos_daquele_avaliador)
                    #TOTAL DE AVALIAÇÕES CONCLUIDAS DAQUELE GESTOR
                    ava_complet = len([x for x in geridos_daquele_avaliador if str(x[28]) == '1' and str(x[33]) == '1'])
                    
                    convers_por_avaliador[f'{[x[5] for x in dados_userBD if x[4] == matricula_comum[index]][0]}'] = (ava_complet / len(geridos_daquele_avaliador)) * 100

                df_to_grafic1 = pd.DataFrame({'Avaliadores':[limparNomesForGrafics(x) for x in convers_por_avaliador.keys()],
                                            'Conversão': [round(x, 2) for x in convers_por_avaliador.values()]})

                fig = px.bar(df_to_grafic1, x="Avaliadores", y="Conversão", text_auto=True)

                # Atualizar o layout do gráfico
                fig.update_layout(
                    title_text='% Rel. Funcional por Avaliador',
                    title_x=0.5,  # Centralizar título horizontalmente
                    title_y=0.95,
                    title_font=dict(color='black', size=18),
                    # Definir o fundo como branco
                    paper_bgcolor='white',
                    # Definir a cor de fundo do gráfico como branco
                    plot_bgcolor='ghostwhite',
                    # Definir a altura do gráfico como 600 pixels
                    height=495,
                        )

                fig.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
                fig.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
                fig.update_traces(marker_color='#D4AF37')  # Definir cor das colunas

                # Renderizar o gráfico no Streamlit
                col1, col2 = st.columns([1.5,3])
                with col1:
                    st.text(" ")
                    st.text(" ")
                    st.text(" ")
                    title = 'Base Colaboradores'
                    valor_base = '120'
                    min_val = 0
                    max_val = float(120)
                    displayInd(title, valor_base, min_val, max_val)

                    title = 'N° Relatórios'
                    valor = f'{len(listDadosAux)}'
                    min_val = 0
                    max_val = float(valor_base)
                    displayInd(title, valor, min_val, max_val)
                    st.text(" ")

                    progress_bar(round((len([x for x in listDadosAux if str(x[28]) == '1' and str(x[33]) == '1']) / len(listDadosAux)) * 100, 1), "% Rel. Funcional")

                    
                with col2:
                    tab1, tab2 = st.tabs(['Unidade', 'Avaliador']) 
                    
                    with tab2:
                        st.text(" ")
                        st.plotly_chart(fig, use_container_width=True)

                    with tab1:
                        uniDades = list(set([x[2] for x in listDadosAux]))
                        ColPorUni = [158,125,116,149,59,39,405,212,73,197,27,47,63,70,103,71]

                        #dadosGraf = [[uniDades[y],round(((sum([1 for z in listDados2 if z[2] == uniDades[y] and z[28] == 1 and z[33] == 1 and z[8] == matriUser[0]]) /ColPorUni[y])) * 100,2)] for y in range(len(uniDades))]
                        dadosGraf = [[uniDades[y] ,round((sum([1 for x in listDadosAux if str(x[2]) == uniDades[y] and str(x[28]) == '1' and str(x[33]) == '1']) / len([x for x in listDadosAux if str(x[2]) == uniDades[y]])) * 100,2)] for y in range(len(uniDades))]

                        import plotly.express as px
                        df = {"Unidades":[x[0] for x in dadosGraf],
                        "% Rel. Funcional": [x[1] for x in dadosGraf]}

                        fig = px.bar(df, x="Unidades", y="% Rel. Funcional", text_auto=True)


                        # Atualizar o layout do gráfico
                        fig.update_layout(
                            title_text='% Rel. Funcional por Unidades',
                            title_x=0.5,  # Centralizar título horizontalmente
                            title_y=0.95,
                            title_font=dict(color='black', size=18),
                            # Definir o fundo como branco
                            paper_bgcolor='white',
                            # Definir a cor de fundo do gráfico como branco
                            plot_bgcolor='ghostwhite',
                            # Definir a altura do gráfico como 600 pixels
                            height=495,
                                )

                        fig.update_xaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
                        fig.update_yaxes(title_font=dict(color='black'), tickfont=dict(color='black'))
                        fig.update_traces(marker_color='#D4AF37')  # Definir cor das colunas


                        # Renderizar o gráfico no Streamlit
                        st.text(" ")
                        st.plotly_chart(fig, use_container_width=True)



                col1,col2 = st.columns([1,3]) 

                divisaoSecao2('PDI')
                col1, col2, col3, col4 = st.columns(4)

                if len(compromissos_BD) > 0:
                    with col1:
                        title = '% PDI'
                        valor = len([y for y in list(set([x[0] for x in listDadosAux])) if y in list(set([x[2] for x in compromissos_BD]))]) / len(list(set([x[0] for x in listDadosAux]))) * 100
                        porc = ''
                        min_val = 0
                        max_val = float(valor)
                        #displayInd3(title, valor, min_val, max_val)
                        st.text(' ')
                        progress_bar(float(valor), title)

                    #COMPROMISSOS EXECUTADOS
                    with col4:
                        title = 'Ações Finalizadas'
                        #str(round(float(contador_basico([x for x in compromissos_BD if x[10] == '1'])), 1))
                        valor = str((len([x for x in compromissos_BD if x[10] == '1']) / len(compromissos_BD)) * 100)
                        max_val = 100
                        displayInd2(title, valor, min_val, max_val)
                        

                    #COMPROMISSOS PENDENTES
                    with col2:
                        title = 'Ações no Prazo'
                        valor = str((len([x for x in compromissos_BD if x[10] != '1' and date.today() <= string_to_datetime(x[9])])/ len(compromissos_BD)) * 100)
                        displayInd2(title, valor, min_val, max_val)
                        

                    #COMPROMISSOS VENCIDOS
                    with col3:
                        title = 'Ações Vencidas'
                        valor = str((len([x for x in compromissos_BD if x[10] != '1' and date.today() > string_to_datetime(x[9])]) / len(compromissos_BD)) * 100)
                        displayInd2(title, valor, min_val, max_val)
                
                col1,col2 = st.columns([1,3]) 
                #with col1:
                #    porc_comp = (len(list(set([x[3] for x in feedbacksBD if x[3] in list(set([x[0] for x in compromissos_BD]))]))) / len(list(set([x[0] for x in compromissos_BD])))) * 100
                #
                #    progress_bar(porc_comp, 'ONE ON ONE')


                with col2:
                    columns_grafic = ['Processos', 'Projetos', 'Competências']

                    dados_for_grafic = {}
                    for name_colum in columns_grafic:
                        dados_for_grafic[f'{name_colum}'] = len([x for x in compromissos_BD if x[11] == name_colum])

                    dados_series = pd.Series(dados_for_grafic)
                    dados_DF = pd.DataFrame({'Áreas': dados_series})
                    
                    st.bar_chart(dados_DF)
            

                divisaoSecao2('Processos e Projetos')
                col1, col2, col3, col4 = st.columns([0.6,1, 0.2, 2])

                with col1: 
                    st.text('')
                    st.text('')
                    st.text('')

                    soma_proc = sum(list(HORAS_MES['Processos'].values()))
                    st.text('')
                    st.metric('Processos', f'{soma_proc} hrs')
                    st.text('')

                    soma_proj = sum(list(HORAS_MES['Projetos'].values()))
                    st.metric('Projetos', f'{soma_proj} hrs')
                                            
                    st.text('')
                    st.metric('Horas Totais', f'{int(soma_proc) + int(soma_proj)} hrs')

                with col2:

                    grafico_pizza(['Processos', 'Projetos'], [soma_proc, soma_proj])
                
                with col4:
                    df = pd.DataFrame(HORAS_MES)

                    fig = go.Figure()
                    for col in df.columns:
                        fig.add_trace(go.Scatter(x=df.index, y=df[col], mode='lines+markers', name=col))
                    fig.update_layout(xaxis_title='Data', yaxis_title='Valores')
                    #st.dataframe(df, use_container_width=True)
                    st.plotly_chart(fig, use_container_width=True)
                
                divisaoSecao2('9Box')
                listDadosAux = [x for x in listDadosAux if str(x[28]) == '1']

                listDadosAux4 = [[date for date in listDadosAux if date[0] == matrc][-1] for matrc in list(set([x[0] for x in listDadosAux]))]
                
                uniDades = ["CEEM Boa Vista - Manaus","CEEM Cacoal","CEEM Campo Grande","CEEM Cascavel","CEEM Curitiba","CEEM Goiânia","CEEM Ji-Paraná","CEEM Mato Grosso","CEEM Porto Alegre","CEEM Porto Velho","CEEM Pres. Prudente","CEEM Rio Branco","CEEM São Paulo","CEEM Vilhena","Corporativo Cascavel","Corporativo Jí-Parana"]
                macroProcessos = ["Relacionamento com Cliente - Pessoas","Relacionamento com Cliente - Cargas","Administrar","Operar","Formulação Estratégica"]              


                competenEucatur = ["OPPR", "Pensamento Crítico e Criativo", "Comunicação", "Foco no Cliente"]
                competenEspEucatur = ["Inteligência Emocional", "Autonomia e Proatividade", "Relacionamento e Network",
                                        "Futurabilidade", "Raciocínio Analítico", "Empreendedorismo",
                                        "Tomada de Decisão",
                                        "Visão Estratégica", "Visão Inovadora", "Liderança", "Comprometimento", "Negociação", "Habilidades Interpessoais"]

                data = [[0 if str(y) == "None" else y for y in list(x[14:28])+list(x[43:46])] for x in listDadosAux4]
                categories = competenEucatur + competenEspEucatur
                Nomes = [x[1] for x in listDadosAux4]
                uniDadesAux = [x[2] for x in listDadosAux4]
                macroProcessosAux = [x[3] for x in listDadosAux4]
                processosAux = [x[4].replace("'","").split(",") for x in listDadosAux4]

                data, categories = listaCompNon0(data, categories)

                tab1, tab2, tab3 = st.tabs(["Unidades", "Macroprocessos", "Colaboradores"])
                
                with tab1:
                    col1,col2,col3 = st.columns([1,6,1])
                    with col2:
                        divisaoSecao2("9Box Unidades")
                        dadosNineboxAux1 = [[listDadosAux4[x][1], uniDadesAux[x],macroProcessosAux[x], processosAux[x], calculoDesempenho(x, listDadosAux4), int(sum(data[x]) / (len(data[x]) - data[x].count(0) - data[x].count("None")))]
                                            for x in
                                            range(len(listDadosAux4))]
                        dadosNineboxAuxUni = [[y,mean([x[4] for x in dadosNineboxAux1 if x[1] == y ]),mean([x[5] for x in dadosNineboxAux1 if x[1] == y ])] for y in uniDades]
                        dadosNineboxUni = ListaCellNineTodos(dadosNineboxAuxUni)

                        plot_all_employees2(dadosNineboxUni[0], dadosNineboxUni[1])

                with tab2:
                    col1,col2,col3 = st.columns([1,6,1])
                    with col2:
                        divisaoSecao2("9Box Macroprocessos")
                        dadosNineboxAuxMac = [[y,mean([x[4] for x in dadosNineboxAux1 if x[2] == y ]),mean([x[5] for x in dadosNineboxAux1 if x[2] in y ])] for y in macroProcessos]
                        dadosNineboxMac = ListaCellNineTodos(dadosNineboxAuxMac)
                        plot_all_employees2(dadosNineboxMac[0], dadosNineboxMac[1])

                with tab3:
                    col1,col2,col3 = st.columns([1,6,1])
                    with col2:
                        divisaoSecao2("9Box Colaboradores")

                        dadosNineboxAux = [[listDadosAux4[x][1], calculoDesempenho(x, listDadosAux4), int(sum(data[x]) / (len(data[x]) - data[x].count(0) - data[x].count("None")))]
                                            for x in
                                            range(len(listDadosAux4))]

                        dadosNinebox = ListaCellNineTodos(dadosNineboxAux)
                        plot_all_employees2(dadosNinebox[0], dadosNinebox[1])
                        


                ########################## EVOLUÇÃO 9BOX ##################################       
                st.text(' ')
                st.text(' ')

                divisaoSecao2('Evolução 9Box')
        
                #ATUAL
                listDadosAuxAT = [[date for date in listDadosAux if date[0] == matrc][-1] for matrc in list(set([x[0] for x in listDadosAux]))]

                dadosNineboxAuxEVO = [[listDadosAuxAT[x][1], calculoDesempenho(x, listDadosAuxAT), int(sum(data[x]) / (len(data[x]) - data[x].count(0) - data[x].count("None")))]
                                    for x in
                                    range(len(listDadosAuxAT))]
                
                desem_geral_atual = ((sum([w[1] for w in dadosNineboxAuxEVO])  / len(dadosNineboxAuxEVO)) + (sum([comp[2] for comp in dadosNineboxAuxEVO]) / len(dadosNineboxAuxEVO))) / 2
                dadosNineboxEVO1 = ListaCellNineTodos2(dadosNineboxAuxEVO)

                #ANTIGO
                list_aux = [[dados for dados in listDadosAux if dados[0] == matrc] for matrc in list(set([x[0] for x in listDadosAux]))]
                listDadosAuxAN = [x[len(x) - 2] for x in list_aux]

                dadosNineboxAuxEVOAN = [[listDadosAuxAN[x][1], calculoDesempenho(x, listDadosAuxAN), int(sum(data[x]) / (len(data[x]) - data[x].count(0) - data[x].count("None")))]
                                    for x in
                                    range(len(listDadosAuxAN))]
                
                desem_geral_antig = ((sum([w[1] for w in dadosNineboxAuxEVOAN])  / len(dadosNineboxAuxEVOAN)) + (sum([comp[2] for comp in dadosNineboxAuxEVOAN]) / len(dadosNineboxAuxEVOAN))) / 2
                dadosNineboxEVO2 = ListaCellNineTodos2(dadosNineboxAuxEVOAN)

                ########### METRICS ###########
                
                col_metric1, col_metric2, col_metric3 = st.columns(3)
                
                with col_metric1:
                    title = 'Desempenho Geral Anterior'
                    valor = str(desem_geral_antig)
                    max_val = 100
                    displayInd4(title, valor, min_val, max_val)

                with col_metric2:
                    title = 'Desempenho Geral Atual'
                    valor = str(desem_geral_atual)
                    displayInd4(title, valor, min_val, max_val)
                
                with col_metric3:
                    title = 'Evolução'
                    valor = str(round(((desem_geral_atual - desem_geral_antig) / desem_geral_antig)*100, 1))
                    displayInd2(title, valor, min_val, max_val)

                #EVOLUÇÃO
            
                st.text(' ')
                st.text(' ')
                col_grafic1, col_grafic2, col_grafic3 = st.columns(3)
                
                with col_grafic2:
                    font_BowlbyOne_SUBTITLE_center('Ciclo Atual')
                    st.pyplot(plot_all_employees1(dadosNineboxEVO1[0], dadosNineboxEVO1[2]))

                with col_grafic1:
                    font_BowlbyOne_SUBTITLE_center('Ciclo Anterior')
                    st.pyplot(plot_all_employees1(dadosNineboxEVO2[0], dadosNineboxEVO2[2]))
                
                with col_grafic3:
                    import altair as alt
                    font_BowlbyOne_SUBTITLE_center('Desempenho Geral')
                    
                    dataf = pd.DataFrame({
                        'Médias': ['Anterior', 'Atual'],
                        'Pontuação': [desem_geral_antig, desem_geral_atual]
                    })
                    
                    # Criação do gráfico de barras usando o Vega-Lite com cores personalizadas
                    chart = alt.Chart(dataf).mark_bar().encode(
                        x='Médias',
                        y='Pontuação',
                        color=alt.Color('Médias',
                                        scale=alt.Scale(domain=['Anterior', 'Atual'],
                                                        range=['lightblue', 'goldenrod']))
                    )

                    # Mostra o gráfico usando o Streamlit
                    st.altair_chart(chart, use_container_width=True)

                with st.expander('Desempenho Individual', expanded=False):
                    st.subheader("Média de Competências")
                    
                    lista_medias = []
                    for i in range(len(Nomes)):
                        med = int(sum(data[i]) / (len(data[i]) - data[i].count(0) - data[i].count("None")))
                        lista_medias.append([Nomes[i], med])

                    lista_medias = sort_descending_by_index2(lista_medias)  
                    cardPlotNew([x[0] for x in lista_medias], [x[1] for x in lista_medias])

                divisaoSecao2("Comparar Competências Comportamentais")
                if len(listDadosAux) > 3:
                    st.info("Selecione no máximo 3 colaboradores para comparar as competências comportamentais")
                else:
                    lista_medias = []
                    
                    st.subheader("Gráfico Radar")
                    st.pyplot(plotarRadar(data, categories, Nomes))
            

        else:
            st.error('Visualização não disponível para seu perfil.')