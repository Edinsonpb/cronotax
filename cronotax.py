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
            'parafiscales': pd.read_excel(excel_path, sheet_name='parafiscales', parse_dates=True),
            'reteicatulua': pd.read_excel(excel_path, sheet_name='reteicatulua', parse_dates=True),
            'reteicabogota': pd.read_excel(excel_path, sheet_name='reteicabogota', parse_dates=True),
            'reteicapereira': pd.read_excel(excel_path, sheet_name='reteicapereira', parse_dates=True),
            'reteicadosquebradas': pd.read_excel(excel_path, sheet_name='reteicadosquebradas', parse_dates=True),
            'rtapj': pd.read_excel(excel_path, sheet_name='rtapj', parse_dates=True),
            'rtapn': pd.read_excel(excel_path, sheet_name='rtapn', parse_dates=True),
            'supersoc': pd.read_excel(excel_path, sheet_name='supersoc', parse_dates=True)
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
    """Filter declarantes por tipo (IVA Bimestral, Cuatrimestral, RFT, RST, SEG o RTI)."""
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
        elif tipo == 'RTI_TULUA':
            mask = df['RTI'].notna() & (df['RTI'] != '') & (df['RTI'].str.contains('TULUA', case=False, na=False))
        elif tipo == 'RTI_BOGOTA':
            mask = df['RTI'].notna() & (df['RTI'] != '') & (df['RTI'].str.contains('BOGOTA', case=False, na=False))
        elif tipo == 'RTI_PEREIRA':
            mask = df['RTI'].notna() & (df['RTI'] != '') & (df['RTI'].str.contains('PEREIRA', case=False, na=False))
        elif tipo == 'RTI_DOSQUEBRADAS':
            mask = df['RTI'].notna() & (df['RTI'] != '') & (df['RTI'].str.contains('DOSQUEBRADAS', case=False, na=False))
        elif tipo == 'RT1_PJ':
            mask = df['RT1'].notna() & (df['RT1'] != '') & (df['TP'] == 'PJ')
        elif tipo == 'RT1_PN':
            mask = df['RT1'].notna() & (df['RT1'] != '') & (df['TP'] == 'PN')
        elif tipo == 'SUPERVIG_SUPERSOC':
            mask = df['SUPERVIG'].notna() & (df['SUPERVIG'] != '') & (df['SUPERVIG'].str.contains('SUPERSOC', case=False, na=False))
        elif tipo == 'RT2':
            mask = df['RT2'].notna() & (df['RT2'] != '')
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
            
            # Filtrar y mostrar declarantes RTI de Tuluá
            rti_tulua_declarantes = filter_declarantes(declarantes, 'RTI_TULUA')
            if rti_tulua_declarantes is not None and not rti_tulua_declarantes.empty:
                merged_rti_tulua_df = merge_with_dates(rti_tulua_declarantes, sheets['reteicatulua'], 'reteicatulua')
                if merged_rti_tulua_df is not None:
                    st.subheader("Declarantes ReteICA Tuluá con Fechas")
                    st.dataframe(merged_rti_tulua_df)
            
            # Filtrar y mostrar declarantes RTI de Bogotá
            rti_bogota_declarantes = filter_declarantes(declarantes, 'RTI_BOGOTA')
            if rti_bogota_declarantes is not None and not rti_bogota_declarantes.empty:
                merged_rti_bogota_df = merge_with_dates(rti_bogota_declarantes, sheets['reteicabogota'], 'reteicabogota')
                if merged_rti_bogota_df is not None:
                    st.subheader("Declarantes ReteICA Bogotá con Fechas")
                    st.dataframe(merged_rti_bogota_df)
            
            # Filtrar y mostrar declarantes RTI de Pereira
            rti_pereira_declarantes = filter_declarantes(declarantes, 'RTI_PEREIRA')
            if rti_pereira_declarantes is not None and not rti_pereira_declarantes.empty:
                merged_rti_pereira_df = merge_with_dates(rti_pereira_declarantes, sheets['reteicapereira'], 'reteicapereira')
                if merged_rti_pereira_df is not None:
                    st.subheader("Declarantes ReteICA Pereira con Fechas")
                    st.dataframe(merged_rti_pereira_df)
            
            # Filtrar y mostrar declarantes RTI de Dosquebradas
            rti_dosquebradas_declarantes = filter_declarantes(declarantes, 'RTI_DOSQUEBRADAS')
            if rti_dosquebradas_declarantes is not None and not rti_dosquebradas_declarantes.empty:
                merged_rti_dosquebradas_df = merge_with_dates(rti_dosquebradas_declarantes, sheets['reteicadosquebradas'], 'reteicadosquebradas')
                if merged_rti_dosquebradas_df is not None:
                    st.subheader("Declarantes ReteICA Dosquebradas con Fechas")
                    st.dataframe(merged_rti_dosquebradas_df)
            
            # Filtrar y mostrar declarantes RT1 de tipo Persona Jurídica
            rt1_pj_declarantes = filter_declarantes(declarantes, 'RT1_PJ')
            if rt1_pj_declarantes is not None and not rt1_pj_declarantes.empty:
                merged_rt1_pj_df = merge_with_dates(rt1_pj_declarantes, sheets['rtapj'], 'rtapj', use_ddn=True)
                if merged_rt1_pj_df is not None:
                    st.subheader("Declarantes RT1 Persona Jurídica con Fechas")
                    st.dataframe(merged_rt1_pj_df)
            
            # Filtrar y mostrar declarantes RT1 de tipo Persona Natural
            rt1_pn_declarantes = filter_declarantes(declarantes, 'RT1_PN')
            if rt1_pn_declarantes is not None and not rt1_pn_declarantes.empty:
                merged_rt1_pn_df = merge_with_dates(rt1_pn_declarantes, sheets['rtapn'], 'rtapn', use_ddn=True)
                if merged_rt1_pn_df is not None:
                    st.subheader("Declarantes RT1 Persona Natural con Fechas")
                    st.dataframe(merged_rt1_pn_df)
            
            # Filtrar y mostrar declarantes SUPERVIG con SUPERSOC
            supervig_supersoc_declarantes = filter_declarantes(declarantes, 'SUPERVIG_SUPERSOC')
            if supervig_supersoc_declarantes is not None and not supervig_supersoc_declarantes.empty:
                merged_supervig_supersoc_df = merge_with_dates(supervig_supersoc_declarantes, sheets['supersoc'], 'supersoc', use_ddn=True)
                if merged_supervig_supersoc_df is not None:
                    st.subheader("Declarantes SUPERVIG SUPERSOC con Fechas")
                    st.dataframe(merged_supervig_supersoc_df)
            
            # Filtrar y mostrar declarantes RT2
            rt2_declarantes = filter_declarantes(declarantes, 'RT2')
            if rt2_declarantes is not None and not rt2_declarantes.empty:
                merged_rt2_df = merge_with_dates(rt2_declarantes, sheets['rtapj'], 'rtapj')
                if merged_rt2_df is not None:
                    st.subheader("Declarantes RT2 con Fechas")
                    st.dataframe(merged_rt2_df)
        else:
            st.error("Error al procesar los declarantes")
    else:
        st.error("Error al cargar los datos")

if __name__ == "__main__":
    main()