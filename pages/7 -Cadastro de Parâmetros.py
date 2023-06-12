import streamlit as st
import datetime
import random
from PIL import Image
import streamlit_authenticator as stauth
import string
import mysql.connector


conexao = mysql.connector.connect(
    passwd='nineboxeucatur',
    port=3306,
    user='ninebox',
    host='nineboxeucatur.c7rugjkck183.sa-east-1.rds.amazonaws.com',
    database='Colaboradores'
)
mycursor = conexao.cursor()

st.set_page_config(page_title="Cadastro de Parâmetros",  page_icon=Image.open('icon.png'), layout="wide")
image = Image.open(('logo.png'))
st.image(image, width = 180)

comando2 = 'SELECT * FROM Usuarios;'
mycursor.execute(comando2)
dadosUser = mycursor.fetchall()

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
    st.title("Cadastro de Parâmetros")

    perfilUser = str([x[9] for x in dadosUser if x[7] == str(username) and x[7] != None])
    perfilUser = perfilUser.upper()
 
    if perfilUser[2] in ['B','C']:
        st.error("Visualização não disponível para seu perfil")
    else:
        # Adiciona uma caixa de entrada
        


        ParaCadastro = st.selectbox("Escolha o parâmetro", ["Unidades de Negócios", "Cadeia de valor","Indicadores"])

        




        if ParaCadastro == "Unidades de Negócios":

            "Macroprocesso", "Processo", "Procedimento"

            sql = 'SELECT * FROM parametro_unidade;'
            mycursor.execute(sql)
            listDadosUn = (mycursor.fetchall())


            st.subheader("Cadastro de Unidade")

            col1, col2 = st.columns((1,3))

            with col1:
                st.dataframe({ "ID" :[x[0] for x in listDadosUn],
                        "Unidade" : [x[1] for x in listDadosUn]
                })

            with col2:

                tab1, tab2, tab3 = st.tabs(["Adicionar", "Editar",  "Excluir"])

                with tab1:
                    st.subheader("Adicionar Unidade")

                    Unidade = st.text_input("Adicionar Unidade de negócio")

                    if st.button("Adicionar"):
                        sql = f'''INSERT INTO parametro_unidade 
                        (unidade , matricula ) 
                        VALUES ('{Unidade}','{username}');'''
                        mycursor.execute(sql)
                        conexao.commit()
                        st.success(f"Nova unidade adicionada com sucesso")


                with tab2:
                    st.subheader("Editar Unidade")

                    Unidade = st.selectbox("Unidade de negócio", [x[1] for x in listDadosUn])

                    UnidadeNova = st.text_input("Editar para")



                    if st.button("Editar"):

                        linrow = [UnidadeNova, Unidade]

                        colunas = ["unidade" , "matricula"]

                        for i in range(len(colunas)):
                            sql = f"UPDATE parametro_unidade SET {colunas[i]} = '{linrow[i]}'  WHERE unidade = '{Unidade}'"
                            mycursor.execute(sql)
                            conexao.commit()
                        st.success(f"Unidade editada com sucesso")

                with tab3:
                    st.subheader("Excluir Unidade")

                    Unidade = st.selectbox("Unidade de negócio ", [x[1] for x in listDadosUn])

                    if st.button("Excluir"):
                        sql = f"DELETE FROM parametro_unidade  WHERE unidade = '{Unidade}';"

                        mycursor.execute(sql)
                        conexao.commit()
                        st.success(f"Unidade excluida com sucesso")



        st.write("---")

        if ParaCadastro == 'Cadeia de valor':

            def get_chart_30507421(df):
                import plotly.express as px
                fig = px.treemap(df, path=[px.Constant("Cadeia de valor"), 'Macroprocesso', 'Processo', 'Procedimento'])
                fig.update_traces(root_color="#06405C")
                fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))


                st.plotly_chart(fig, theme="streamlit",use_container_width = True)



            #sql = '''SELECT parametro_processo.processo, parametro_macro.macroprocesso
            #         FROM parametro_processo
            #         JOIN parametro_macro ON parametro_processo.macroProcesso = parametro_macro.id;'''
            #mycursor.execute(sql)
            #listDadosCAVA = (mycursor.fetchall())

            #get_chart_30507421({ "Macroprocesso" :[x[1] for x in listDadosCAVA],  "Processo" : [x[0] for x in listDadosCAVA]})

            sql = '''SELECT parametro_macro.macroprocesso, parametro_processo.processo, parametro_procedimento.procedimento
                        FROM parametro_procedimento
                        JOIN parametro_macro ON parametro_procedimento.macroProcesso = parametro_macro.id
                        JOIN parametro_processo ON parametro_procedimento.processo = parametro_processo.id;'''
            mycursor.execute(sql)
            listDadosCAVA1 = (mycursor.fetchall())


            get_chart_30507421( { "Macroprocesso" :[x[0] for x in listDadosCAVA1],
                                    "Processo" : [x[1] for x in listDadosCAVA1],
                                    "Procedimento" : [x[2] for x in listDadosCAVA1]})

            ### CADASTRO DE MACRO ########################################################################################


            sql = 'SELECT * FROM parametro_macro;'
            mycursor.execute(sql)
            listDadosMP = (mycursor.fetchall())


            st.subheader("Cadastro de Macroprocesso")

            col1, col2 = st.columns((2,3))

            with col1:
                st.dataframe({ "ID" :[x[0] for x in listDadosMP],
                        "Macroprocesso" : [x[1] for x in listDadosMP]
                })

            with col2:

                tab1, tab2, tab3 = st.tabs(["Adicionar", "Editar",  "Excluir"])

                with tab1:
                    st.subheader("Adicionar Macroprocesso")

                    MacroProcesso = st.text_input("Adicionar Macroprocesso")

                    if st.button("Adicionar"):
                        sql = f'''INSERT INTO parametro_macro 
                        (macroProcesso , matricula_ult_edic ) 
                        VALUES ('{MacroProcesso}','{username}');'''
                        mycursor.execute(sql)
                        conexao.commit()
                        st.success(f"Novo macroprocesso adicionado com sucesso")


                with tab2:
                    st.subheader("Editar Macroprocesso")

                    MacroProcesso = st.selectbox("Macroprocesso", [x[1] for x in listDadosMP])

                    MacroProcessoNovo = st.text_input("Editar Macroprocesso para")



                    if st.button("Editar"):

                        linrow = [MacroProcessoNovo, Unidade]

                        colunas = ["macroProcesso" , "matricula_ult_edic"]

                        for i in range(len(colunas)):
                            sql = f"UPDATE parametro_macro SET {colunas[i]} = '{linrow[i]}'  WHERE macroProcesso = '{MacroProcesso}'"
                            mycursor.execute(sql)
                            conexao.commit()
                        st.success(f"Unidade editada com sucesso")

                with tab3:
                    st.subheader("Excluir Macroprocesso")

                    MacroProcesso = st.selectbox("Macroprocesso ", [x[1] for x in listDadosMP])

                    if st.button("Excluir"):
                        sql = f"DELETE FROM parametro_macro  WHERE macroProcesso = '{MacroProcesso}';"

                        mycursor.execute(sql)
                        conexao.commit()
                        st.success(f"Macroprocesso excluido com sucesso")

            ### CADASTRO DE PROCESSO ########################################################################################

            st.write("---")

            sql = 'SELECT * FROM parametro_macro;'
            mycursor.execute(sql)
            listDadosMP = (mycursor.fetchall())

            sql = 'SELECT * FROM parametro_processo;'
            mycursor.execute(sql)
            listDadosPRO = (mycursor.fetchall())


            st.subheader("Cadastro de Processo")

            col1, col2 = st.columns((2,3))

            with col1:
                st.dataframe({ "ID" :[x[0] for x in listDadosPRO],
                        "Processo" : [x[1] for x in listDadosPRO]
                })

            with col2:

                tab1, tab2, tab3 = st.tabs(["Adicionar", "Editar",  "Excluir"])

                with tab1:
                    st.subheader("Adicionar Processo")

                    Processo = st.text_input("Adicionar Processo")

                    MacroProcesso = st.selectbox("Macroprocesso ", [x[1] for x in listDadosMP], key = "1")

                    MPIndex = [x[0] for x in listDadosMP if x[1] == MacroProcesso][0]

                    if st.button("Adicionar Processo"):
                        sql = f'''INSERT INTO parametro_processo 
                        (processo , macroProcesso, matricula_ult_edic ) 
                        VALUES ('{Processo}', '{MPIndex}','{username}');'''
                        mycursor.execute(sql)
                        conexao.commit()
                        st.success(f"Novo processo adicionado com sucesso")


                with tab2:
                    st.subheader("Editar Processo")

                    Processo = st.selectbox("Processo", [x[1] for x in listDadosPRO])

                    ProcessoNovo = st.text_input("Editar Processo para")

                    MacroProcesso = st.selectbox("Macroprocesso ", [x[1] for x in listDadosMP], key = "2")
                    MPIndex = [x[0] for x in listDadosMP if x[1] == MacroProcesso][0]



                    if st.button("Editar Processo"):

                        linrow = [ProcessoNovo, username , MPIndex]

                        colunas = ["processo" , "matricula_ult_edic","macroProcesso"]

                        for i in range(len(colunas)):
                            sql = f"UPDATE parametro_processo SET {colunas[i]} = '{linrow[i]}'  WHERE processo = '{Processo}'"
                            mycursor.execute(sql)
                            conexao.commit()
                        st.success(f"Processo editado com sucesso")

                with tab3:
                    st.subheader("Excluir Processo")

                    Processo = st.selectbox("Processo ", [x[1] for x in listDadosPRO])

                    if st.button("Excluir Processo"):
                        sql = f"DELETE FROM parametro_processo  WHERE processo = '{Processo}';"

                        mycursor.execute(sql)
                        conexao.commit()
                        st.success(f"Processo excluido com sucesso")


            ### CADASTRO DE PROCEDIMENTO ########################################################################################
            st.write("---")

            sql = 'SELECT * FROM parametro_macro;'
            mycursor.execute(sql)
            listDadosMP = (mycursor.fetchall())

            sql = 'SELECT * FROM parametro_processo;'
            mycursor.execute(sql)
            listDadosPRO = (mycursor.fetchall())

            sql = 'SELECT * FROM parametro_procedimento;'
            mycursor.execute(sql)
            listDadosPC = (mycursor.fetchall())
            

            st.subheader("Cadastro de Procedimento")

            col1, col2 = st.columns((2,3))

            with col1:
                st.dataframe({ "ID" :[x[0] for x in listDadosPC],
                        "Procedimento" : [x[3] for x in listDadosPC]
                })

            with col2:

                tab1, tab2, tab3 = st.tabs(["Adicionar", "Editar",  "Excluir"])

                with tab1:
                    st.subheader("Adicionar Procedimento")

                    Procedimento = st.text_input("Adicionar Procedimento")

                    Processo = st.selectbox("Processo ", [x[1] for x in listDadosPRO], key = "11")

                    PROIndex = [x[0] for x in listDadosPRO if x[1] == Processo][0]

                    MacroProcesso = st.selectbox("Macroprocesso ", [x[1] for x in listDadosMP], key = "13")

                    MPIndex = [x[0] for x in listDadosMP if x[1] == MacroProcesso][0]

                    if st.button("Adicionar Procedimento"):
                        sql = f'''INSERT INTO parametro_procedimento 
                        ( macroProcesso, processo, procedimento, matricula_ult_edic ) 
                        VALUES ('{MPIndex}', '{PROIndex}','{Procedimento}', '{username}');'''
                        mycursor.execute(sql)
                        conexao.commit()
                        st.success(f"Novo Procedimento adicionado com sucesso")


                with tab2:
                    st.subheader("Editar Procedimento")

                    Procedimento = st.selectbox("Procedimento", [x[1] for x in listDadosPC])

                    ProcedimentoNovo = st.text_input("Editar Procedimento para")
                    
                    Processo = st.selectbox("Processo ", [x[1] for x in listDadosPRO], key = "22")

                    PROIndex = [x[0] for x in listDadosPRO if x[1] == Processo][0]


                    MacroProcesso = st.selectbox("Macroprocesso ", [x[1] for x in listDadosMP], key = "23")
                    MPIndex = [x[0] for x in listDadosMP if x[1] == MacroProcesso][0]



                    if st.button("Editar Procedimento"):

                        linrow = [ProcedimentoNovo, username , MPIndex, PROIndex]

                        colunas = [ "procedimento", "matricula_ult_edic","macroProcesso", "processo"]

                        for i in range(len(colunas)):
                            sql = f"UPDATE parametro_procedimento SET {colunas[i]} = '{linrow[i]}'  WHERE procedimento = '{Procedimento}'"
                            mycursor.execute(sql)
                            conexao.commit()
                        st.success(f"Procedimento editado com sucesso")

                with tab3:
                    st.subheader("Excluir Procedimento")

                    Procedimento = st.selectbox("Procedimento ", [x[1] for x in listDadosPC])

                    if st.button("Excluir Procedimento"):
                        sql = f"DELETE FROM parametro_procedimento  WHERE procedimento = '{Procedimento}';"

                        mycursor.execute(sql)
                        conexao.commit()
                        st.success(f"Procedimento excluido com sucesso")



        if ParaCadastro == "Indicadores":

            
            ### CADASTRO DE INDICADORES ########################################################################################

            sql = 'SELECT * FROM parametro_macro;'
            mycursor.execute(sql)
            listDadosMP = (mycursor.fetchall())

            sql = 'SELECT * FROM parametro_processo;'
            mycursor.execute(sql)
            listDadosPRO = (mycursor.fetchall())

            sql = 'SELECT * FROM parametro_procedimento;'
            mycursor.execute(sql)
            listDadosPC = (mycursor.fetchall())
            
            sql = 'SELECT * FROM parametro_indicadores;'
            mycursor.execute(sql)
            listDadosIND = (mycursor.fetchall())

            st.subheader("Cadastro de Indicadores")

            col1, col2 = st.columns((2,3))

            with col1:
                st.dataframe({ "ID" :[x[0] for x in listDadosIND],
                        "Indicadores" : [x[4] for x in listDadosIND]
                })

            with col2:

                tab1, tab2, tab3 = st.tabs(["Adicionar", "Editar",  "Excluir"])

                with tab1:
                    st.subheader("Adicionar Indicadores")

                    Indicador = st.text_input("Adicionar Indicador")


                    MacroProcesso = st.selectbox("Macroprocesso ", [x[1] for x in listDadosMP], key = "13")

                    MPIndex = [x[0] for x in listDadosMP if x[1] == MacroProcesso][0]

                    Processo = st.selectbox("Processo ", [x[1] for x in listDadosPRO if x[2] == MPIndex], key = "11")

                    PROIndex = [x[0] for x in listDadosPRO if x[1] == Processo][0]

                    Procedimento = st.selectbox("Procedimento ", [x[3] for x in listDadosPC if x[2] == PROIndex], key = "12")

                    PCIndex = [x[0] for x in listDadosPC if x[3] == Procedimento][0]


                    if st.button("Adicionar Indicadores"):
                        sql = f'''INSERT INTO parametro_indicadores 
                        ( macroProcesso, processo, procedimento, indicador, matricula_ult_edic ) 
                        VALUES ('{MPIndex}', '{PROIndex}','{PCIndex}', '{Indicador}','{username}');'''
                        mycursor.execute(sql)
                        conexao.commit()
                        st.success(f"Novo Indicador adicionado com sucesso")

                with tab2:
                    st.subheader("Editar Indicadores")

                    Indicador = st.selectbox("Indicador", [x[4] for x in listDadosIND])
                    IndicadorDATA = [x for x in listDadosIND if x[4] == Indicador][0]

                    IndicadorNovo = st.text_input("Editar Indicador para")


                    MacroProcesso = st.selectbox("Macroprocesso ", [x[1] for x in listDadosMP],IndicadorDATA[1]-1,  key = "23")

                    MPIndex = [x[0] for x in listDadosMP if x[1] == MacroProcesso][0]

                    Processo = st.selectbox("Processo ", [x[1] for x in listDadosPRO if x[2] == MPIndex], IndicadorDATA[2] - 1, key = "21")

                    PROIndex = [x[0] for x in listDadosPRO if x[1] == Processo][0]

                    Procedimento = st.selectbox("Procedimento ", [x[3] for x in listDadosPC if x[2] == PROIndex], IndicadorDATA[3] - 1 , key = "22")

                    PCIndex = [x[0] for x in listDadosPC if x[3] == Procedimento][0]
                    

                    if st.button("Editar Indicadores"):

                        linrow = [IndicadorNovo,PCIndex, username , MPIndex, PROIndex]

                        colunas = [ "indicador","procedimento", "matricula_ult_edic","macroProcesso", "processo"]

                        for i in range(len(colunas)):
                            sql = f"UPDATE parametro_indicadores SET {colunas[i]} = '{linrow[i]}'  WHERE indicador = '{Indicador}'"
                            mycursor.execute(sql)
                            conexao.commit()
                        st.success(f"Indicador editado com sucesso")


                with tab3:
                    st.subheader("Excluir Indicadores")

                    Indicador = st.selectbox("Excluir Indicador", [x[4] for x in listDadosIND])

                    if st.button("Excluir Indicador"):
                        sql = f"DELETE FROM parametro_indicadores  WHERE indicador = '{Indicador}';"

                        mycursor.execute(sql)
                        conexao.commit()
                        st.success(f"Indicador excluido com sucesso")
