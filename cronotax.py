import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import os

def load_excel_data():
    """Load all sheets from the Excel file into a dictionary of DataFrames."""
    try:
        # Ruta al archivo Excel en la carpeta Dataframes
        excel_path = os.path.join('Dataframes', 'cronotax.xlsx')
        
        if not os.path.exists(excel_path):
            st.error(f"No se encontró el archivo Excel en: {excel_path}")
            return None
            
        sheets = {
            'declarantes': pd.read_excel(excel_path, sheet_name='declarantes', dtype={'Nit': str}),
            'ivabim': pd.read_excel(excel_path, sheet_name='ivabim'),
            'ivacua': pd.read_excel(excel_path, sheet_name='ivacua'),
            'rstivaan': pd.read_excel(excel_path, sheet_name='rstivaan'),
            'retefte': pd.read_excel(excel_path, sheet_name='retefte'),
            'parafiscales': pd.read_excel(excel_path, sheet_name='parafiscales'),
            'impocons': pd.read_excel(excel_path, sheet_name='impocons'),
            'rtapn': pd.read_excel(excel_path, sheet_name='rtapn'),
            'rtapj': pd.read_excel(excel_path, sheet_name='rtapj'),
            'exogenaDIANngc': pd.read_excel(excel_path, sheet_name='exogenaDIANngc'),
            'exogenaTULUA': pd.read_excel(excel_path, sheet_name='exogenaTULUA'),
            'exogenaDOSQUEBRADAS': pd.read_excel(excel_path, sheet_name='exogenaDOSQUEBRADAS'),
            'exogenaPEREIRA': pd.read_excel(excel_path, sheet_name='exogenaPEREIRA'),
            'exogenaBOGOTA': pd.read_excel(excel_path, sheet_name='exogenaBOGOTA'),
            'icabogotac': pd.read_excel(excel_path, sheet_name='icabogotac'),
            'icabogotaa': pd.read_excel(excel_path, sheet_name='icabogotaa'),
            'reteicabogota': pd.read_excel(excel_path, sheet_name='reteicabogota'),
            'icadosquebradas': pd.read_excel(excel_path, sheet_name='icadosquebradas'),
            'reteicadosquebradas': pd.read_excel(excel_path, sheet_name='reteicadosquebradas'),
            'icapereira': pd.read_excel(excel_path, sheet_name='icapereira'),
            'reteicapereira': pd.read_excel(excel_path, sheet_name='reteicapereira'),
            'icasantarosa': pd.read_excel(excel_path, sheet_name='icasantarosa'),
            'reteicasantarosa': pd.read_excel(excel_path, sheet_name='reteicasantarosa'),
            'icatulua': pd.read_excel(excel_path, sheet_name='icatulua'),
            'reteicatulua': pd.read_excel(excel_path, sheet_name='reteicatulua'),
            'nomelect': pd.read_excel(excel_path, sheet_name='nomelect'),
            'ipat': pd.read_excel(excel_path, sheet_name='ipat'),
            'rst': pd.read_excel(excel_path, sheet_name='rst'),
            'supersoc': pd.read_excel(excel_path, sheet_name='supersoc'),
            'actextpn': pd.read_excel(excel_path, sheet_name='actextpn')
        }
        return sheets
    except Exception as e:
        st.error(f"Error al cargar el archivo Excel: {str(e)}")
        return None

def process_declarantes(df):
    """Process the declarantes DataFrame to add UDN and DDN columns."""
    try:
        # Mostrar las columnas disponibles
        st.write("Columnas disponibles en el DataFrame:", df.columns.tolist())
        
        # Asegurarse de que Nit sea string
        df['Nit'] = df['Nit'].astype(str)
        # Extraer UDN y DDN
        df['udn'] = df['Nit'].str[-1]
        df['ddn'] = df['Nit'].str[-2:]
        return df
    except Exception as e:
        st.error(f"Error al procesar los declarantes: {str(e)}")
        return None

def filter_declarantes(df):
    """Filter declarantes based on different tax types."""
    try:
        # Verificar si la columna First Name existe
        if 'First Name' not in df.columns:
            st.warning("La columna 'First Name' no existe en el archivo. Usando solo NIT.")
            columns_to_show = ['Nit', 'udn', 'ddn']
        else:
            columns_to_show = ['Nit', 'First Name', 'udn', 'ddn']

        return {
            'iva_bim': df[df['IVA'] == 'B'][columns_to_show],
            'iva_cua': df[df['IVA'] == 'C'][columns_to_show],
            'rft': df[df['RFT'] == 'X'][columns_to_show],
            'ico': df[df['ICO'] == 'X'][columns_to_show]
        }
    except Exception as e:
        st.error(f"Error al filtrar los declarantes: {str(e)}")
        return None

def main():
    # Set page config for Streamlit
    st.set_page_config(
        page_title="Cronograma Legal y Tributario",
        page_icon="📅",
        layout="wide"
    )

    # Title and author
    st.title("Cronograma Legal y Tributario")
    st.caption("Autor: EDINSON PARRA BAHOS")

    # Load data directly from Dataframes folder
    sheets = load_excel_data()
    
    if sheets is not None:
        # Process declarantes
        declarantes = process_declarantes(sheets['declarantes'])
        
        if declarantes is not None:
            filtered_declarantes = filter_declarantes(declarantes)
            
            if filtered_declarantes is not None:
                # Display data tables
                st.subheader("Declarantes IVA Bimestral")
                st.dataframe(filtered_declarantes['iva_bim'])

                st.subheader("Declarantes IVA Cuatrimestral")
                st.dataframe(filtered_declarantes['iva_cua'])

                st.subheader("Declarantes RFT")
                st.dataframe(filtered_declarantes['rft'])

                st.subheader("Declarantes ICO")
                st.dataframe(filtered_declarantes['ico'])

if __name__ == "__main__":
    main() 