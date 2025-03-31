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

        # Crear máscaras para cada tipo de declarante
        iva_bim_mask = df['IVA'] == 'B'
        iva_cua_mask = df['IVA'] == 'C'
        rft_mask = df['RFT'] == 'X'
        ico_mask = df['ICO'] == 'X'
        
        # Máscaras para los nuevos filtros
        rst_mask = df['RST'].notna() & (df['RST'] != '')
        rti_mask = df['RTI'].notna() & (df['RTI'] != '')
        seg_mask = df['SEG'].notna() & (df['SEG'] != '')
        rt1_mask = df['RT1'].notna() & (df['RT1'] != '')
        rt2_mask = df['RT2'].notna() & (df['RT2'] != '')
        ipa_mask = df['IPA'].notna() & (df['IPA'] != '')
        supervig_mask = df['SUPERVIG'].notna() & (df['SUPERVIG'] != '')
        exo_mask = df['EXO'].notna() & (df['EXO'] != '')
        exica_mask = df['EXICA'].notna() & (df['EXICA'] != '')
        actextpn_mask = df['ActExtPn'].notna() & (df['ActExtPn'] != '')
        ica_mask = df['ICA'].notna() & (df['ICA'] != '')

        # Filtrar RTI por ciudad
        rti_df = df[rti_mask].copy()
        rti_ciudades = {}
        if not rti_df.empty:
            for ciudad in rti_df['RTI'].unique():
                if pd.notna(ciudad) and ciudad != '':
                    rti_ciudades[ciudad] = rti_df[rti_df['RTI'] == ciudad][columns_to_show]

        # Filtrar ICA por ciudad (usando la columna RTI)
        ica_df = df[ica_mask].copy()
        ica_ciudades = {}
        if not ica_df.empty:
            for ciudad in ica_df['RTI'].unique():
                if pd.notna(ciudad) and ciudad != '':
                    ica_ciudades[ciudad] = ica_df[ica_df['RTI'] == ciudad][columns_to_show]

        # Filtrar EXICA por ciudad (usando la columna RTI)
        exica_df = df[exica_mask].copy()
        exica_ciudades = {}
        if not exica_df.empty:
            for ciudad in exica_df['RTI'].unique():
                if pd.notna(ciudad) and ciudad != '':
                    exica_ciudades[ciudad] = exica_df[exica_df['RTI'] == ciudad][columns_to_show]

        # Filtrar RT1 por tipo de persona
        rt1_df = df[rt1_mask].copy()
        rt1_tipos = {}
        if not rt1_df.empty:
            for tipo in rt1_df['TP'].unique():
                if pd.notna(tipo) and tipo != '':
                    if tipo == 'PN':
                        rt1_tipos['Persona Natural'] = rt1_df[rt1_df['TP'] == tipo][columns_to_show]
                    elif tipo == 'PJ':
                        rt1_tipos['Persona Jurídica'] = rt1_df[rt1_df['TP'] == tipo][columns_to_show]
                    else:
                        rt1_tipos[tipo] = rt1_df[rt1_df['TP'] == tipo][columns_to_show]

        return {
            'iva_bim': df[iva_bim_mask][columns_to_show],
            'iva_cua': df[iva_cua_mask][columns_to_show],
            'rft': df[rft_mask][columns_to_show],
            'ico': df[ico_mask][columns_to_show],
            'rst': df[rst_mask][columns_to_show],
            'rti': df[rti_mask][columns_to_show],
            'rti_ciudades': rti_ciudades,
            'seg': df[seg_mask][columns_to_show],
            'rt1': df[rt1_mask][columns_to_show],
            'rt1_tipos': rt1_tipos,
            'rt2': df[rt2_mask][columns_to_show],
            'ipa': df[ipa_mask][columns_to_show],
            'supervig': df[supervig_mask][columns_to_show],
            'exo': df[exo_mask][columns_to_show],
            'exica': df[exica_mask][columns_to_show],
            'exica_ciudades': exica_ciudades,
            'actextpn': df[actextpn_mask][columns_to_show],
            'ica': df[ica_mask][columns_to_show],
            'ica_ciudades': ica_ciudades
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

                st.subheader("Declarantes ReteFTE")
                st.dataframe(filtered_declarantes['rft'])

                st.subheader("Declarantes ImpoConsumo")
                st.dataframe(filtered_declarantes['ico'])

                st.subheader("Declarantes Régimen Simple de Tributación")
                st.dataframe(filtered_declarantes['rst'])

                # Mostrar RTI general y por ciudad
                st.subheader("Declarantes ReteICA - General")
                st.dataframe(filtered_declarantes['rti'])

                if filtered_declarantes['rti_ciudades']:
                    st.subheader("Declarantes ReteICA por Ciudad")
                    for ciudad, df_ciudad in filtered_declarantes['rti_ciudades'].items():
                        st.write(f"**Ciudad: {ciudad}**")
                        st.dataframe(df_ciudad)

                st.subheader("Pago de Aportes de Seguridad Social")
                st.dataframe(filtered_declarantes['seg'])

                # Mostrar RT1 general y por tipo de persona
                st.subheader("Declarantes Renta Cuota 1 - General")
                st.dataframe(filtered_declarantes['rt1'])

                if filtered_declarantes['rt1_tipos']:
                    st.subheader("Declarantes Renta Cuota 1 por Tipo de Persona")
                    for tipo, df_tipo in filtered_declarantes['rt1_tipos'].items():
                        st.write(f"**Tipo de Persona: {tipo}**")
                        st.dataframe(df_tipo)

                st.subheader("Declarantes Renta Cuota 2")
                st.dataframe(filtered_declarantes['rt2'])

                st.subheader("Declarantes Impuesto al Patrimonio")
                st.dataframe(filtered_declarantes['ipa'])

                st.subheader("Reporte de Supervigilancia")
                st.dataframe(filtered_declarantes['supervig'])

                st.subheader("Reportantes de Exógena DIAN")
                st.dataframe(filtered_declarantes['exo'])

                # Mostrar EXICA general y por ciudad
                st.subheader("Reportantes de Exógena ICA - General")
                st.dataframe(filtered_declarantes['exica'])

                if filtered_declarantes['exica_ciudades']:
                    st.subheader("Reportantes de Exógena ICA por Ciudad")
                    for ciudad, df_ciudad in filtered_declarantes['exica_ciudades'].items():
                        st.write(f"**Ciudad: {ciudad}**")
                        st.dataframe(df_ciudad)

                st.subheader("Declarantes Activos en el Exterior Persona Natural")
                st.dataframe(filtered_declarantes['actextpn'])

                # Mostrar ICA general y por ciudad
                st.subheader("Declarantes Industria y Comercio - General")
                st.dataframe(filtered_declarantes['ica'])

                if filtered_declarantes['ica_ciudades']:
                    st.subheader("Declarantes Industria y Comercio por Ciudad")
                    for ciudad, df_ciudad in filtered_declarantes['ica_ciudades'].items():
                        st.write(f"**Ciudad: {ciudad}**")
                        st.dataframe(df_ciudad)

if __name__ == "__main__":
    main() 