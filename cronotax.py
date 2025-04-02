import pandas as pd
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
            'ivabim': pd.read_excel(excel_path, sheet_name='ivabim', parse_dates=True),
            'ivacua': pd.read_excel(excel_path, sheet_name='ivacua', parse_dates=True),
            'retefte': pd.read_excel(excel_path, sheet_name='retefte', parse_dates=True),
            'rst': pd.read_excel(excel_path, sheet_name='rst', parse_dates=True),
            'parafiscales': pd.read_excel(excel_path, sheet_name='parafiscales', parse_dates=True)
        }
        return sheets
    except Exception as e:
        st.error(f"Error al cargar el archivo Excel: {str(e)}")
        return None

def process_declarantes(df):
    """Process the declarantes DataFrame to add UDN and DDN columns."""
    try:
        # Asegurarse de que Nit sea string
        df['Nit'] = df['Nit'].astype(str)
        # Extraer UDN y DDN
        df['udn'] = df['Nit'].str[-1]
        df['ddn'] = df['Nit'].str[-2:]
        return df
    except Exception as e:
        st.error(f"Error al procesar los declarantes: {str(e)}")
        return None

def filter_declarantes(df, tipo):
    """Filter declarantes por tipo (IVA Bimestral, Cuatrimestral, RFT, RST o SEG)."""
    try:
        # Verificar si la columna First Name existe
        if 'First Name' not in df.columns:
            columns_to_show = ['Nit', 'udn', 'ddn']
        else:
            columns_to_show = ['Nit', 'First Name', 'Apl', 'udn', 'ddn']

        # Filtrar declarantes según el tipo
        if tipo == 'B':
            mask = df['IVA'] == 'B'
        elif tipo == 'C':
            mask = df['IVA'] == 'C'
        elif tipo == 'RFT':
            mask = df['RFT'].notna() & (df['RFT'] != '')
        elif tipo == 'RST':
            mask = df['RST'].notna() & (df['RST'] != '')
        elif tipo == 'SEG':
            mask = df['SEG'].notna() & (df['SEG'] != '')
        else:
            st.error(f"Tipo de declarante no válido: {tipo}")
            return None

        return df[mask][columns_to_show]
    except Exception as e:
        st.error(f"Error al filtrar los declarantes {tipo}: {str(e)}")
        return None

def format_dates(df):
    """Format all date columns to YYYY-MM-DD format."""
    try:
        # Identificar columnas de fecha
        date_columns = df.select_dtypes(include=['datetime64']).columns
        
        # Formatear cada columna de fecha
        for col in date_columns:
            df[col] = df[col].dt.strftime('%Y-%m-%d')
        
        return df
    except Exception as e:
        st.error(f"Error al formatear las fechas: {str(e)}")
        return df

def merge_with_dates(declarantes_df, dates_df, tipo, use_ddn=False):
    """Merge declarantes with their corresponding dates."""
    try:
        # Asegurarse de que las columnas sean string
        if use_ddn:
            # Formatear DDN en declarantes para asegurar dos dígitos
            declarantes_df['ddn'] = declarantes_df['ddn'].astype(str).str.zfill(2)
            
            if 'DDN' in dates_df.columns:
                # Formatear DDN en fechas para asegurar dos dígitos
                dates_df['DDN'] = dates_df['DDN'].astype(str).str.zfill(2)
                right_on = 'DDN'
            elif 'ddn' in dates_df.columns:
                # Formatear DDN en fechas para asegurar dos dígitos
                dates_df['ddn'] = dates_df['ddn'].astype(str).str.zfill(2)
                right_on = 'ddn'
            else:
                st.error(f"No se encontró la columna DDN en la pestaña {tipo}")
                return None
            left_on = 'ddn'
        else:
            declarantes_df['udn'] = declarantes_df['udn'].astype(str)
            if 'UDN' in dates_df.columns:
                dates_df['UDN'] = dates_df['UDN'].astype(str)
                right_on = 'UDN'
            elif 'udn' in dates_df.columns:
                dates_df['udn'] = dates_df['udn'].astype(str)
                right_on = 'udn'
            else:
                st.error(f"No se encontró la columna UDN en la pestaña {tipo}")
                return None
            left_on = 'udn'
        
        # Realizar el merge
        merged_df = pd.merge(
            declarantes_df,
            dates_df,
            left_on=left_on,
            right_on=right_on,
            how='left'
        )
        
        # Formatear las fechas
        merged_df = format_dates(merged_df)
        
        return merged_df
    except Exception as e:
        st.error(f"Error al combinar declarantes con fechas de {tipo}: {str(e)}")
        return None

def main():
    # Set page config for Streamlit
    st.set_page_config(
        page_title="Plazos por responsabilidad y contribuyentes",
        page_icon="📅",
        layout="wide"
    )

    # Title and author
    st.title("Plazos por responsabilidad y contribuyentes")
    st.caption("Autor: EDINSON PARRA BAHOS")

    # Load data directly from Dataframes folder
    sheets = load_excel_data()
    
    if sheets is not None:
        # Process declarantes
        declarantes = process_declarantes(sheets['declarantes'])
        
        if declarantes is not None:
            # Filtrar y mostrar declarantes IVA Bimestral
            iva_bim_declarantes = filter_declarantes(declarantes, 'B')
            if iva_bim_declarantes is not None and not iva_bim_declarantes.empty:
                merged_bim_df = merge_with_dates(iva_bim_declarantes, sheets['ivabim'], 'ivabim')
                if merged_bim_df is not None:
                    st.subheader("Declarantes IVA Bimestral con Fechas")
                    st.dataframe(merged_bim_df)
            
            # Filtrar y mostrar declarantes IVA Cuatrimestral
            iva_cua_declarantes = filter_declarantes(declarantes, 'C')
            if iva_cua_declarantes is not None and not iva_cua_declarantes.empty:
                merged_cua_df = merge_with_dates(iva_cua_declarantes, sheets['ivacua'], 'ivacua')
                if merged_cua_df is not None:
                    st.subheader("Declarantes IVA Cuatrimestral con Fechas")
                    st.dataframe(merged_cua_df)
            
            # Filtrar y mostrar declarantes RFT
            rft_declarantes = filter_declarantes(declarantes, 'RFT')
            if rft_declarantes is not None and not rft_declarantes.empty:
                merged_rft_df = merge_with_dates(rft_declarantes, sheets['retefte'], 'retefte')
                if merged_rft_df is not None:
                    st.subheader("Declarantes ReteFTE con Fechas")
                    st.dataframe(merged_rft_df)
            
            # Filtrar y mostrar declarantes RST
            rst_declarantes = filter_declarantes(declarantes, 'RST')
            if rst_declarantes is not None and not rst_declarantes.empty:
                merged_rst_df = merge_with_dates(rst_declarantes, sheets['rst'], 'rst')
                if merged_rst_df is not None:
                    st.subheader("Declarantes Régimen Simple de Tributación con Fechas")
                    st.dataframe(merged_rst_df)
            
            # Filtrar y mostrar declarantes SEG
            seg_declarantes = filter_declarantes(declarantes, 'SEG')
            if seg_declarantes is not None and not seg_declarantes.empty:
                merged_seg_df = merge_with_dates(seg_declarantes, sheets['parafiscales'], 'parafiscales', use_ddn=True)
                if merged_seg_df is not None:
                    st.subheader("Declarantes Parafiscales con Fechas")
                    st.dataframe(merged_seg_df)
        else:
            st.error("Error al procesar los declarantes")
    else:
        st.error("Error al cargar los datos")

if __name__ == "__main__":
    main()