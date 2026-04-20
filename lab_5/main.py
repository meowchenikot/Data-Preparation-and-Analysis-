import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="NOAA Data Dashboard", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

@st.cache_data
def load_data():
    df = pd.read_csv('vhi_data.csv') 
    df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Week'].astype(str) + '-1', format="%Y-%W-%w", errors='coerce')
    regions = df['Region'].dropna().unique().tolist()
    return df, sorted(regions)

df, region_list = load_data()

if 'init' not in st.session_state:
    st.session_state.c_indicator = 'VHI'
    st.session_state.c_region = 'Київська'
    st.session_state.c_week_range = (1, 52)
    st.session_state.c_year_range = (1981, 2024)
    st.session_state.c_sort_asc = False
    st.session_state.c_sort_desc = False
    st.session_state.init = True

def reset_filters():
    st.session_state.c_indicator = 'VHI'
    st.session_state.c_region = 'Київська'
    st.session_state.c_week_range = (1, 52)
    st.session_state.c_year_range = (1981, 2024)
    st.session_state.c_sort_asc = False
    st.session_state.c_sort_desc = False

col_controls, col_content = st.columns([1, 3], gap="large")

with col_controls:
    st.header("⚙️ Панель керування")
    st.markdown("---")
    
    indicator = st.selectbox("Оберіть індекс:", options=['VCI', 'TCI', 'VHI'], key='c_indicator')
    region = st.selectbox("Оберіть область:", options=region_list, key='c_region')
    week_range = st.slider("Інтервал тижнів:", min_value=1, max_value=52, key='c_week_range')
    year_range = st.slider("Інтервал років:", min_value=1981, max_value=2024, key='c_year_range')
    
    st.markdown("---")
    st.subheader("Сортування даних")
    
    sort_asc = st.checkbox(f"За зростанням ({indicator})", key='c_sort_asc')
    sort_desc = st.checkbox(f"За спаданням ({indicator})", key='c_sort_desc')
    
    st.markdown("---")
    
    st.button("🔄 Скинути фільтри", on_click=reset_filters, type="primary", width="stretch")


mask = (
    (df['Region'] == region) &
    (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) &
    (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1])
)
filtered_df = df[mask].copy()

if sort_asc and sort_desc:
    st.warning("⚠️ Увага: Увімкнено обидва чекбокси сортування! Дані залишено в хронологічному порядку.")
elif sort_asc:
    filtered_df = filtered_df.sort_values(by=indicator, ascending=True)
elif sort_desc:
    filtered_df = filtered_df.sort_values(by=indicator, ascending=False)

with col_content:
    st.title(f"📊 Аналіз даних: {region} область")
    st.markdown(f"**Індекс:** {indicator} | **Період:** {year_range[0]}-{year_range[1]} (Тижні: {week_range[0]}-{week_range[1]})")
    
    tab_table, tab_plot1, tab_plot2 = st.tabs(["📋 Таблиця даних", "📈 Графік часового ряду", "📊 Порівняння областей"])
    
    with tab_table:
        st.subheader("Відфільтровані дані")

        st.dataframe(filtered_df[['Year', 'Week', 'Region', 'VCI', 'TCI', 'VHI']], width="stretch", height=500)
        
    with tab_plot1:
        st.subheader(f"Динаміка {indicator} ({region})")
        plot_data = df[mask].sort_values(by=['Year', 'Week']) 
        
        fig1 = px.line(
            plot_data, 
            x='Date', 
            y=indicator, 
            color_discrete_sequence=['#00e5ff'],
            hover_data=['Year', 'Week'],
            render_mode='svg' 
        )
        fig1.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Час (Роки-Тижні)",
            yaxis_title=f"Значення {indicator}"
        )
        st.plotly_chart(fig1, width="stretch")
        
    with tab_plot2:
        st.subheader(f"Порівняння {indicator} серед усіх областей")
        st.markdown(f"*Середнє значення за обраний період ({year_range[0]}-{year_range[1]}, тижні {week_range[0]}-{week_range[1]})*")
        
        mask_all_regions = (
            (df['Year'] >= year_range[0]) & (df['Year'] <= year_range[1]) &
            (df['Week'] >= week_range[0]) & (df['Week'] <= week_range[1])
        )
        compare_df = df[mask_all_regions].groupby('Region')[indicator].mean().reset_index()
        compare_df = compare_df.sort_values(by=indicator, ascending=False)
        
        compare_df['Color'] = np.where(compare_df['Region'] == region, '#ff0055', '#007acc')
        
        fig2 = go.Figure(data=[
            go.Bar(
                x=compare_df['Region'],
                y=compare_df[indicator],
                marker_color=compare_df['Color'],
                text=compare_df[indicator].round(1),
                textposition='auto'
            )
        ])
        fig2.update_layout(
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45,
            yaxis_title=f"Середній {indicator}",
            height=600
        )
        st.plotly_chart(fig2, width="stretch")


