import streamlit as st
from util import plotarRadar
from util import listaCompNon0
from util import PlotDisperssao
from util import ListaCellNine
from util import plot_all_employees
from util import string_to_list
from util import converte_data
from PIL import Image
import pandas as pd
import re
import streamlit_authenticator as stauth
from func_relatorio import visualizaçao_processos, visualizacao_Projetos, visualizacao_competencias, visualizacao_geral, visualizacao_ninebox, visualizacao_Compromissos, comparar_periodos
from func_relatorio import visualizacao_CPA
import mysql.connector


conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='Colaboradores'
)
mycursor = conexao.cursor()


def list_to_string(lista):
    string = ''
    for a in lista:
        string += a



def limpar_lista(lista_de_listas):
    lista_final = []
    for lista in lista_de_listas:
        for info in lista:
            lista_final.append(info)
    
    return lista_final


def contador_basico(lista):
    cont = 0
    for dado in lista:
        cont += 1

    return cont


def media_bas(lista_to_lista):
    soma = 0
    contad = 0

    for lista in lista_to_lista:
        for number in lista:
            contad += 1
            soma += int(number)

    media = soma / contad
    return media


def conta_proced(lista):
    cont = 0
    for a in lista:
        cont += 1
    return cont


def soma_horas(lista_horas):
    soma = 0
    for numbers in lista_horas:
        soma += int(numbers)
    return soma


def soma_lista_to_lista(lista_to_lista):
    soma = 0
    for lista_horas in lista_to_lista:
        for numbers in lista_horas:
            soma += int(numbers)

    return soma


st.set_page_config(page_title="Relatório Funcional", page_icon=Image.open('icon.png'), layout="centered")
image = Image.open(('logo.png'))
st.image(image, width = 180)

comando2 = 'SELECT * FROM Usuarios;'
mycursor.execute(comando2)
dadosUser = mycursor.fetchall()


def contador_list_to_list(lista_de_lista):
    cont = 0
    for lista in lista_de_lista:
        for dado in lista:
            cont += 1

    return cont



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

    col1, col2 = st.columns((3,1))
    
    with col1:
        st.title('Relatório Funcional')

    sql = 'SELECT * FROM Colaboradores;'
    mycursor.execute(sql)
    listDados2 = (mycursor.fetchall())
    
    matric_gestores_avaliadores = list(set(limpar_lista([[x[8],x[10]] for x in listDados2])))

    matriUser = [x[4] for x in dadosUser if x[7] == username][0]
    perfilUser = [x[9] for x in dadosUser if x[7] == username][0]
    st.text(' ')
    st.text(' ')
    st.text(' ')
    if perfilUser == 'A' or perfilUser == 'BP':
        if perfilUser == 'BP':
            unidadesBP = list(str([x[10] for x in dadosUser if str(x[4]) == str(matriUser)][0]).split(', '))
            listDados2 = [x for x in listDados2 if str(x[2]).strip() in unidadesBP]

        #CABEÇALHO PARA O ADMINISTRADOR
        linhaBD = 0
        with col2:
            radio = st.radio("Pesquisar por:",['Matricula', 'Filtro'])

        if radio == 'Filtro':
            Unidade = st.multiselect("Unidade de negócio", list(set([x[2] for x in listDados2 if x[2] != '' and x[2] != None and x[2] != 'Zero'])),
                                                        [])
            if len(Unidade) < 1:
                st.info("Não há uma unidade selecionada")
            else:
                mplist = set([x[3] for x in listDados2 if x[2] in Unidade])
                macroprocesso = st.multiselect('Macroprocesso', mplist, mplist)
                if len(macroprocesso) < 1:
                        st.info("Não há um macroprocesso selecionado")
                else:
                    FuncList = set([x[40] for x in listDados2 if x[2] in Unidade and x[3] in macroprocesso])
                    funcao = st.multiselect('Função', FuncList, FuncList)
                    if len(funcao) < 1:
                        st.info("Não há uma função selecionada")
                    else:
                        col1, col2 = st.columns((3,1))
                        with col1:
                            gclist = set([x[1] for x in listDados2 if x[3] in macroprocesso and x[2] in Unidade and x[40] in funcao and x[1] != 'ZERO'])
                            name_colaborador = st.selectbox('Colaborador', gclist)
                        if len(name_colaborador) < 1:
                            st.info("Não há um colaborador selecionado")
                        else:
                            linhaBD = [x for x in range(len(listDados2)) if listDados2[x][1] == name_colaborador][0]
                            with col2:
                                #matricula do colaborador escolhido
                                st.text_input('Matricula', listDados2[linhaBD][0])

        elif radio == 'Matricula':
            st.text(' ')
            col1, col2, col3 = st.columns((0.34, 1.25, 1.1))
            with col1:
                matricula_user = st.text_input('Matricula')
            
            matriculasBD = list(set([str(x[0]) for x in listDados2 if x[1] != 'ZERO']))
            if matricula_user not in matriculasBD:
                with col2:   
                    st.text_input('', 'Colaborador não encontrado')         
            else:
                with col2:   
                    st.text_input("Nome Colaborador", list(set([x[1] for x in listDados2 if str(x[0]) == matricula_user]))[0])
                
                with col3:
                    periodos = [f'{converte_data(x[12])} - {converte_data(x[13])}' for x in listDados2 if str(x[0]) == matricula_user]
                    anoQuadr = st.selectbox('Período', periodos, len(periodos) - 1)
                    linhaBD = [x for x in range(len(listDados2)) if listDados2[x][0] == int(matricula_user) and f'{converte_data(listDados2[x][12])} - {converte_data(listDados2[x][13])}' == anoQuadr][0]    

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
                

        #A PARTIR DO MOMENTO QUE "LINHAS BD" FOR MAIOR DOQUE "0" O RELATÓRIO FUNCIONAL VAI LIBERAR
        if linhaBD > 0:
            periodos = comparar_periodos(listDados2, linhaBD)
            st.text(' ')
            st.text(' ')
            st.text(' ')
            st.write('---')
            medProj = 0
            medProc = 0
            
            #VISUALIZAÇÃO DE PROCESSOS (PERFIL A)
            medProc = visualizaçao_processos(listDados2, linhaBD)
            
            #VISUALIZAÇÃO DE PROJETOS(PERFIL A)
            medProj = visualizacao_Projetos(listDados2, linhaBD)

            #VISUALIZAÇÃO DE COMPETÊNCIAS(PERFIL A)
            medComp = visualizacao_competencias(listDados2, linhaBD, periodos)
           
            #VISUALIZAÇÃO GERAL(PERFIL A)
            medDes = visualizacao_geral(listDados2, linhaBD, medProc, medProj, medComp, periodos)
            
            #VISUALIZAÇÃO CPA(PERFIL A)
            visualizacao_CPA(listDados2, linhaBD, medDes, medComp)
            st.text(' ')
            #VISUALIZAÇÃO NINEBOX(PERFIL A)
            visualizacao_ninebox(listDados2, linhaBD, medDes, medComp, periodos)
            
            
            #visualizacao_Compromissos(listDados2, linhaBD, listDados2[linhaBD][0])

    elif perfilUser == 'B':
        
        #CABEÇALHO PARA O GESTOR
        liscod = [str(x[0]) for x in listDados2]
     
        st.text(' ')
        col1, col2 = st.columns((3,1))


        geridos_by_gestor = [x for x in listDados2 if x[10] == matriUser or x[8] == matriUser]
        if len(geridos_by_gestor) < 1:
            st.warning('Ainda não foram realizadas avaliações ligadas ao seu perfil.')
        else:
            with col1:
                colab_gerido = st.selectbox("Colaboradores", [x[1] for x in geridos_by_gestor])

            matCola = [x[0] for x in listDados2 if x[1] == colab_gerido]
            
            linhaBD = [x for x in range(len(listDados2)) if str(listDados2[x][0]) == str(matCola[0])][0] 
            with col2:
                periodo_inicio = converte_data(str([x[12] for x in geridos_by_gestor if x[1] == colab_gerido][0]))
                periodo_fim = converte_data(str([x[13] for x in geridos_by_gestor if x[1] == colab_gerido][0]))    
                anoQuadr = st.text_input('Período', f'{periodo_inicio}  -  {periodo_fim}')
                                        
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text_input('Função', [x[40] for x in geridos_by_gestor if x[1] == colab_gerido][0])
            with col2:
                st.text_input("Unidade de negócio", [x[2] for x in geridos_by_gestor if x[1] == colab_gerido][0])
            with col3:
                st.text_input('Macroprocesso', [x[3] for x in geridos_by_gestor if x[1] == colab_gerido][0])
            st.text_input('Processo', [x[4] for x in geridos_by_gestor if x[1] == colab_gerido][0])
            col1, col2 = st.columns(2)
            with col1:
                st.text_input('Gestor de Carreira', [x[7] for x in geridos_by_gestor if x[1] == colab_gerido][0])
            with col2:
                st.text_input('Avaliador', [x[9] for x in geridos_by_gestor if x[1] == colab_gerido][0])

           
            medProj = 0
            medProc = 0

            if linhaBD > 0:
                periodos = comparar_periodos(listDados2, linhaBD)
                st.write("---")
                #VISUALIZAÇÃO DE PROCESSOS (PERFIL B)
                medProc = visualizaçao_processos(listDados2, linhaBD)
                
                #VISUALIZAÇÃO DE PROJETOS(PERFIL B)
                medProj = visualizacao_Projetos(listDados2, linhaBD)

                #VISUALIZAÇÃO DE COMPETÊNCIAS(PERFIL B)
                medComp = visualizacao_competencias(listDados2, linhaBD, periodos)
                
                #VISUALIZAÇÃO GERAL(PERFIL B)
                medDes = visualizacao_geral(listDados2, linhaBD, medProc, medProj, medComp, periodos)
                
                
                #VISUALIZAÇÃO CPA(PERFIL B)
                visualizacao_CPA(listDados2, linhaBD, medDes, medComp) 
                st.text(' ')
                #VISUALIZAÇÃO NINEBOX(PERFIL B)
                visualizacao_ninebox(listDados2, linhaBD, medDes, medComp, periodos)

                #VISUALIZAÇÃO DE COMPRIMISSOS(PERFIL B)
                #visualizacao_Compromissos(listDados2, linhaBD, listDados2[linhaBD][0])
    else:
        avaliados_by_avaliador = [x for x in listDados2 if x[10] == matriUser]
        
        col1, col2 = st.columns((3,1))
        if len(avaliados_by_avaliador) < 1:
            st.warning('Ainda não foram realizadas avaliações ligadas ao seu perfil.')
        else:
            with col1:
                    colab_gerido = st.selectbox("Colaboradores", [x[1] for x in avaliados_by_avaliador])
            
            matCola = [x[0] for x in listDados2 if x[1] == colab_gerido]
            
            linhaBD = [x for x in range(len(listDados2)) if str(listDados2[x][0]) == str(matCola[0])][0] 
            with col2:
                periodo_inicio = converte_data(str([x[12] for x in avaliados_by_avaliador if x[1] == colab_gerido][0]))
                periodo_fim = converte_data(str([x[13] for x in avaliados_by_avaliador if x[1] == colab_gerido][0]))    
                anoQuadr = st.text_input('Período', f'{periodo_inicio}  -  {periodo_fim}')
                                        
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text_input('Função', [x[40] for x in avaliados_by_avaliador if x[1] == colab_gerido][0])
            with col2:
                st.text_input("Unidade de negócio", [x[2] for x in avaliados_by_avaliador if x[1] == colab_gerido][0])
            with col3:
                st.text_input('Macroprocesso', [x[3] for x in avaliados_by_avaliador if x[1] == colab_gerido][0])
            st.text_input('Processo', [x[4] for x in avaliados_by_avaliador if x[1] == colab_gerido][0])
            col1, col2 = st.columns(2)
            with col1:
                st.text_input('Gestor de Carreira', [x[7] for x in avaliados_by_avaliador if x[1] == colab_gerido][0])
            with col2:  
                st.text_input('Avaliador', [x[9] for x in avaliados_by_avaliador if x[1] == colab_gerido][0])
            medProj = 0
            medProc = 0

            if linhaBD > 0:
                periodos = comparar_periodos(listDados2, linhaBD)
                st.write("---")
                #VISUALIZAÇÃO DE PROCESSOS (PERFIL C)
                medProc = visualizaçao_processos(listDados2, linhaBD)
                    
                #VISUALIZAÇÃO DE PROJETOS(PERFIL C)
                medProj = visualizacao_Projetos(listDados2, linhaBD)

                #VISUALIZAÇÃO DE COMPETÊNCIAS(PERFIL C)
                medComp = visualizacao_competencias(listDados2, linhaBD, periodos)

                #VISUALIZAÇÃO GERAL(PERFIL C)
                medDes = visualizacao_geral(listDados2, linhaBD, medProc, medProj, medComp, periodos)
                
                #VISUALIZAÇÃO CPA(PERFIL C)
                visualizacao_CPA(listDados2, linhaBD, medDes, medComp) 
                st.text(' ')
                    
                #VISUALIZAÇÃO NINEBOX(PERFIL C)
                visualizacao_ninebox(listDados2, linhaBD, medDes, medComp, periodos)
                    
                #VISUALIZAÇÃO DE COMPRIMISSOS(PERFIL C)
                #visualizacao_Compromissos(listDados2, linhaBD, listDados2[linhaBD][0])
