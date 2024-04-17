import pandas as pd
import streamlit as st
import plotly.express as px

# Lendo o arquivo
df = pd.read_csv('covid19_variants.csv')
df = df.loc[df['variant_name'] != 'Total']

# Convertendo a coluna 'data' para o tipo datetime
df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')

# Agrupando informações para criar os filtros
paises = list(df['area'].unique())
variantes = list(df['variant_name'].unique())
periodos = list(df['date'].dt.year.unique())

# Disponibilizando os Filtros para o Usuário
pais = st.sidebar.selectbox('Escolha o pais',['Todos'] + paises)
variante = st.sidebar.selectbox('Escolha a variante',['Todas'] + variantes)
periodo = st.sidebar.selectbox('Escolha o Ano',['Todos'] + periodos)

# Aplicando os Filtros
if(periodo != 'Todos') :
    df = df[df['date'].dt.year==periodo]
else:
    st.header('Mostrando resultados de todo período')
if(pais != 'Todos') :
    st.header('Mostrando resultado de ' + pais)
    df = df[df['area']==pais]
else:
    st.header('Mostrando todos os paises')
if(variante != 'Todas') :
    st.subheader('Mostrando resultado para variante ' + variante)
    df = df[df['variant_name']==variante]
else:
    st.subheader('Mostrando resultados para todas as variantes')

# Agrupando as Informações por Data
dfShow = df.groupby(by = ['date']).sum()  

# Definindo os Eixos X e Y
fig = px.line(dfShow,x=dfShow.index, y='specimens')

# Definindo o Título
fig.update_layout(title='Casos diarios de Covid-19')

# Publicando
st.plotly_chart(fig,use_container_width=True)
