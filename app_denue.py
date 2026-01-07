import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests

FILE_ID_JAL= '1LECafNe3t2VtN2NldtZwSrSMUUZOxQvq'
url_denue_jal = f'https://drive.google.com/uc?export=download&id={FILE_ID_JAL}'

latitude = 20.67622683590842
longitude = -103.34613656040588

ramos = ('Panificación industrial', 'Panificación tradicional',
        'Elaboración de galletas y pastas para sopa',
        'Comercio al por mayor de pan y pasteles',
        'Comercio al por mayor de leche y otros productos lácteos',
        'Comercio al por mayor de abarrotes',
        'Comercio al por mayor de dulces y materias primas para repostería',
        'Comercio al por menor de dulces y materias primas para repostería',
        'Comercio al por menor de leche, otros productos lácteos y embutidos',
        'Servicios de comedor para empresas e instituciones',
        'Servicios de preparación de alimentos para ocasiones especiales',
        'Servicios de preparación de alimentos en unidades móviles')

@st.cache_data(show_spinner = 'Cargando datos...')
def load_data():
    df_denue_jalisco = pd.read_csv(url_denue_jal)
    return df_denue_jalisco

df_denue_jal = load_data()

def main():
    st.title('Prospectos') #h1
    st.header('Unidades económicas') #h2
    
    st.set_page_config(
    page_title = 'Prospectos',
    page_icon = '🌐',
    layout = 'wide',
    initial_sidebar_state = 'expanded'
    )

    mapa, contacto = st.tabs(['Mapa', 'Contactos'])

    with mapa:  

        selection = ''
        if 'selection' not in st.session_state:
            st.session_state.selection = ramos

        with st.form('Actividad económica'):  
       
            st.session_state.seleccion = st.segmented_control('Clase de actividad', ramos, selection_mode="multi", label_visibility = 'collapsed')
            st.form_submit_button('Actualizar')
        
        fig = go.Figure()

        if st.session_state.seleccion:
            df = df_denue_jal[df_denue_jal['Nombre de clase de la actividad'].isin(st.session_state.seleccion)]
        else:
            df = df_denue_jal

        fig.add_trace(go.Scattermap(
            lat = df['Latitud'],
            lon = df['Longitud'],
            mode = 'markers',
            customdata = df[['Nombre de clase de la actividad', 'Descripcion estrato personal ocupado',
                'Nombre', 'Dirección', 'Colonia', 'Código Postal', 'Municipio', 'Número de teléfono']],
            hovertemplate =
                '<b>🏷️ </b> %{customdata[0]}<br>' +
                '<b>📊 </b> %{customdata[1]}<br>' +
                '<b>🏪 </b> %{customdata[2]}<br>' +
                '<b>📍 </b> %{customdata[3]}<br>' +
                '         %{customdata[4]} %{customdata[5]} %{customdata[6]}<br>' +
                '<b>⏰ </b> %{customdata[7]}<br>' +
                '<extra></extra>',
            marker = dict(size = 16, color = 'rgb(74,85,211,0.75)'),
            )
        )    

        fig.update_layout(showlegend = False)
        
        fig.update_layout(
            map = dict(
                style = 'open-street-map',  #'carto-positron',
                center = dict(lat = latitude, lon = longitude),  # 👈 tu centro
                zoom = 10                                # 👈 tu zoom
            ),
            height = 600,
            margin = dict(r = 0, t = 0, l = 0, b = 0)
        )
        
        st.plotly_chart(fig, use_container_width = True)
        st.write(len(df), 'establecimientos')
    
    with contacto:
        st.subheader('Datos de negocio')
        st.dataframe(df[['Nombre de clase de la actividad', 'Descripcion estrato personal ocupado',
                'Nombre', 'Dirección', 'Colonia', 'Código Postal', 'Municipio', 'Número de teléfono',
                 'Correo electrónico', 'Sitio en Internet', 'Tipo de establecimiento']])

if __name__ == '__main__':
    main()