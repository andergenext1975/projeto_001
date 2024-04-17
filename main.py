import pandas as pd

import streamlit as st

import plotly.express as px

df = pd.read_csv('covid19_variants.csv')
list(df)

paises = list(df['area'].unique())
variantes = list(df['variant_name'].unique())
periodos = list(pd.to_datetime(df['date'],format='%Y').unique())

df['date'] = pd.to_datetime(df['date'],format='%Y-%m-%d')


pais = st.sidebar.selectbox('Escolha o pais',['Todos'] + paises)
variante = st.sidebar.selectbox('Escolha a variante',['Todas'] + variantes)
periodo = st.sidebar.selectbox('Escolha a Data',['Todas'] + periodos)


if(periodo != 'Todas') :
    st.header('Mostrando resultado de ' + periodo)
    df = df[pd.to_datetime(df['date'],format='%Y')==periodo]
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


dfShow = df.groupby(by = ['date']).sum()  


fig = px.line(dfShow,x=dfShow.index, y='specimens')
fig.update_layout(title='Casos diarios de Covid-19')
st.plotly_chart(fig,use_container_width=True)
