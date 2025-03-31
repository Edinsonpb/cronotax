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
            'ivabim': pd.read_excel(excel_path, sheet_name='ivabim', parse_dates=True)
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

def filter_iva_bimestral(df):
    """Filter declarantes IVA Bimestral."""
    try:
        # Verificar si la columna First Name existe
        if 'First Name' not in df.columns:
            columns_to_show = ['Nit', 'udn', 'ddn']
        else:
            columns_to_show = ['Nit', 'First Name', 'udn', 'ddn']

        # Filtrar declarantes IVA Bimestral
        iva_bim_mask = df['IVA'] == 'B'
        return df[iva_bim_mask][columns_to_show]
    except Exception as e:
        st.error(f"Error al filtrar los declarantes IVA Bimestral: {str(e)}")
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

def main():
    # Set page config for Streamlit
    st.set_page_config(
        page_title="IVA Bimestral con Fechas",
        page_icon="📅",
        layout="wide"
    )

    # Title and author
    st.title("IVA Bimestral con Fechas")
    st.caption("Autor: EDINSON PARRA BAHOS")

    # Load data directly from Dataframes folder
    sheets = load_excel_data()
    
    if sheets is not None:
        # Process declarantes
        declarantes = process_declarantes(sheets['declarantes'])
        
        if declarantes is not None:
            # Filtrar declarantes IVA Bimestral
            iva_bim_declarantes = filter_iva_bimestral(declarantes)
            
            if iva_bim_declarantes is not None and not iva_bim_declarantes.empty:
                # Mostrar las columnas disponibles en ivabim para debugging
                st.write("Columnas disponibles en ivabim:", sheets['ivabim'].columns.tolist())
                
                # Asegurarse de que UDN sea string en ambos DataFrames
                iva_bim_declarantes['udn'] = iva_bim_declarantes['udn'].astype(str)
                
                # Verificar si la columna existe como 'UDN' o 'udn'
                if 'UDN' in sheets['ivabim'].columns:
                    sheets['ivabim']['UDN'] = sheets['ivabim']['UDN'].astype(str)
                    right_on = 'UDN'
                elif 'udn' in sheets['ivabim'].columns:
                    sheets['ivabim']['udn'] = sheets['ivabim']['udn'].astype(str)
                    right_on = 'udn'
                else:
                    st.error("No se encontró la columna UDN en la pestaña ivabim")
                    return
                
                # Realizar el merge usando UDN como clave
                merged_df = pd.merge(
                    iva_bim_declarantes,
                    sheets['ivabim'],
                    left_on='udn',
                    right_on=right_on,
                    how='left'
                )
                
                # Formatear las fechas
                merged_df = format_dates(merged_df)
                
                # Mostrar la tabla combinada
                st.subheader("Declarantes IVA Bimestral con Fechas")
                st.dataframe(merged_df)
            else:
                st.warning("No se encontraron declarantes IVA Bimestral")
        else:
            st.error("Error al procesar los declarantes")
    else:
        st.error("Error al cargar los datos")

if __name__ == "__main__":
    main()