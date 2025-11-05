import os
import pandas as pd
from dash import Dash, html, dcc, dash_table
import plotly.express as px

#Cargar datos
DATA_DIR = 'data'

df_mortalidad = pd.read_excel(os.path.join(DATA_DIR, 'Anexo1.NoFetal2019_CE_15-03-23.xlsx'))
df_codigos = pd.read_excel(os.path.join(DATA_DIR, 'Anexo2.CodigosDeMuerte_CE_15-03-23.xlsx'))
df_divipola = pd.read_excel(os.path.join(DATA_DIR, 'Divipola_CE_.xlsx'))

#  Limpieza básica de los datos
df_mortalidad['SEXO'] = df_mortalidad['SEXO'].replace({1: 'Hombre', 2: 'Mujer'})
df_mortalidad['GRUPO_EDAD1'] = df_mortalidad['GRUPO_EDAD1'].fillna(0).astype(int)

# Unir con Divipola para obtener nombres de departamento y municipio
df = df_mortalidad.merge(df_divipola, on=['COD_DEPARTAMENTO', 'COD_MUNICIPIO'], how='left')


# Agregaciones necesarias

# Total de muertes por departamento
muertes_departamento = df.groupby('DEPARTAMENTO').size().reset_index(name='TOTAL')

# Total de muertes por mes
muertes_mes = df.groupby('MES').size().reset_index(name='TOTAL')

# 5 ciudades más violentas (filtrando homicidios por arma de fuego X95)
ciudades_violentas = (
    df[df['COD_MUERTE'].astype(str).str.startswith('X95')]
    .groupby('MUNICIPIO')
    .size()
    .reset_index(name='TOTAL')
    .sort_values('TOTAL', ascending=False)
    .head(5)
)

# 10 ciudades con menor mortalidad
ciudades_menor = (
    df.groupby('MUNICIPIO')
    .size()
    .reset_index(name='TOTAL')
    .sort_values('TOTAL', ascending=True)
    .head(10)
)

# 10 principales causas de muerte
causas = (
    df.groupby('COD_MUERTE')
    .size()
    .reset_index(name='TOTAL')
    .sort_values('TOTAL', ascending=False)
    .head(10)
)

# Muertes por sexo y departamento
sexo_departamento = df.groupby(['DEPARTAMENTO', 'SEXO']).size().reset_index(name='TOTAL')

# Distribución por grupo de edad
grupo_edad = df.groupby('GRUPO_EDAD1').size().reset_index(name='TOTAL')

# Coordenadas para el mapa
coords = {
    'AMAZONAS': (-4.2153, -69.9406), 'ANTIOQUIA': (7.1986, -75.3412), 'ARAUCA': (6.551, -71.002),
    'ATLÁNTICO': (10.696, -74.874), 'BOLÍVAR': (9.395, -74.736), 'BOYACÁ': (5.550, -73.367),
    'CALDAS': (5.298, -75.247), 'CAQUETÁ': (0.870, -73.841), 'CASANARE': (5.333, -71.584),
    'CAUCA': (2.348, -76.51), 'CESAR': (9.65, -73.51), 'CHOCÓ': (5.694, -76.66),
    'CÓRDOBA': (8.401, -75.90), 'CUNDINAMARCA': (5.00, -74.26), 'GUAINÍA': (2.55, -68.90),
    'GUAVIARE': (1.89, -72.78), 'HUILA': (2.80, -75.29), 'LA GUAJIRA': (11.54, -72.91),
    'MAGDALENA': (10.15, -74.19), 'META': (3.50, -73.25), 'NARIÑO': (1.28, -77.39),
    'NORTE DE SANTANDER': (7.86, -72.78), 'PUTUMAYO': (0.43, -76.05), 'QUINDÍO': (4.55, -75.66),
    'RISARALDA': (5.10, -75.88), 'SANTANDER': (6.64, -73.73), 'SUCRE': (9.20, -75.14),
    'TOLIMA': (4.21, -75.17), 'VALLE DEL CAUCA': (3.80, -76.52),
    'VAUPÉS': (0.66, -70.74), 'VICHADA': (4.90, -69.78), 'BOGOTÁ, D.C.': (4.71, -74.07)
}

muertes_departamento['lat'] = muertes_departamento['DEPARTAMENTO'].map(
    lambda x: coords.get(str(x).upper(), (None, None))[0]
)
muertes_departamento['lon'] = muertes_departamento['DEPARTAMENTO'].map(
    lambda x: coords.get(str(x).upper(), (None, None))[1]
)


# Gráficas con Plotly

# Mapa
fig_mapa = px.scatter_geo(
    muertes_departamento.dropna(subset=['lat', 'lon']),
    lat='lat', lon='lon',
    size='TOTAL',
    text='DEPARTAMENTO',
    hover_name='DEPARTAMENTO',
    hover_data={'TOTAL': True, 'lat': False, 'lon': False},
    projection='natural earth',
    title='Distribución total de muertes por departamento (2019)'
)
fig_mapa.update_layout(margin=dict(l=0, r=0, t=50, b=0))

# Línea de tiempo (muertes por mes)
fig_mes = px.line(
    muertes_mes, x='MES', y='TOTAL',
    markers=True,
    title='Total de muertes por mes (2019)'
)
fig_mes.update_xaxes(dtick=1)

# Barras: ciudades más violentas
fig_violentas = px.bar(
    ciudades_violentas, x='MUNICIPIO', y='TOTAL',
    title='5 ciudades más violentas (códigos X95)'
)

# Circular: ciudades con menor mortalidad
fig_pie_menor = px.pie(
    ciudades_menor, names='MUNICIPIO', values='TOTAL',
    title='10 ciudades con menor mortalidad (total de muertes)'
)

# Barras apiladas: sexo por departamento
fig_sexo = px.bar(
    sexo_departamento, x='DEPARTAMENTO', y='TOTAL', color='SEXO',
    barmode='stack', title='Muertes por sexo en cada departamento'
)
fig_sexo.update_layout(xaxis={'categoryorder': 'total descending'})

# Histograma por grupo de edad
fig_edad = px.bar(
    grupo_edad, x='GRUPO_EDAD1', y='TOTAL',
    title='Distribución de muertes por grupo de edad'
)


# Construcción del Dashboard Dash
app = Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1('Mortalidad en Colombia 2019', style={'textAlign': 'center'}),
    html.P('Fuente: Certificados de Defunción No Fetal - DANE (2019)', style={'textAlign': 'center'}),

    dcc.Tabs([
        dcc.Tab(label='Mapa de Mortalidad por Departamento', children=[dcc.Graph(figure=fig_mapa)]),
        dcc.Tab(label='Muertes por Mes', children=[dcc.Graph(figure=fig_mes)]),
        dcc.Tab(label='5 Ciudades Más Violentas (X95)', children=[dcc.Graph(figure=fig_violentas)]),
        dcc.Tab(label='10 Ciudades con Menor Mortalidad', children=[dcc.Graph(figure=fig_pie_menor)]),
        dcc.Tab(label='Top 10 Causas de Muerte', children=[
            dash_table.DataTable(
                data=causas.to_dict('records'),
                columns=[{'name': i, 'id': i} for i in causas.columns],
                style_table={'overflowX': 'auto'},
                page_size=10
            )
        ]),
        dcc.Tab(label='Muertes por Sexo y Departamento', children=[dcc.Graph(figure=fig_sexo)]),
        dcc.Tab(label='Distribución por Grupo de Edad', children=[dcc.Graph(figure=fig_edad)])
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
