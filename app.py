import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Mental Health Dashboard", layout="wide")
st.title("SafeMind: Dashboard")
st.markdown("""
Dibuat oleh Tim CC26-PRU474 | Samuel Sahata Sitompul | Intan Kurniasih | Mutia Ramadani | Muhammad Hendrik Ridwan (inact.)
""")
st.divider()

# 2. Fungsi Data Wrangling dengan Caching
# Dekorator ini memastikan data hanya di-unduh dan di-bersihkan sekali saat aplikasi pertama kali dibuka
@st.cache_data  
def load_and_clean_data():
    url = "https://drive.google.com/uc?export=download&id=1RBs4qfgFFhl0DJwh5FZbUipMZVKh6Oo5"
    df = pd.read_csv(url)
    
    # Cleaning: Datetime
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    
    # Cleaning: Boolean mapping
    binary_map = {'Yes': True, 'No': False}
    df['family_history'] = df['family_history'].map(binary_map)
    df['treatment'] = df['treatment'].map(binary_map)
    df['Coping_Struggles'] = df['Coping_Struggles'].map(binary_map)
    
    # Cleaning: Missing values pada self_employed
    df['self_employed'] = df['self_employed'].fillna("No")
    
    # Cleaning: Duplicate data
    df = df.drop_duplicates()
    
    return df

# Memanggil fungsi yang sudah di-cache
df = load_and_clean_data()

# 3. Sidebar untuk Interaktivitas
st.sidebar.header("Filter Data")
selected_gender = st.sidebar.multiselect("Pilih Gender:", options=df['Gender'].unique(), default=df['Gender'].unique())
filtered_df = df[df['Gender'].isin(selected_gender)]

# 4. Eksplorasi & Visualisasi Data (EDA)
st.header("Analisis berdasarkan Data")

# Menggunakan Tabs agar visualisasi rapi dan tidak menumpuk ke bawah
tab1, tab2, tab3 = st.tabs(["Univariate Analysis", "Bivariate Analysis", "Multivariate Analysis"])

with tab1:
    st.subheader("Distribusi Variabel Tunggal")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_gender = px.histogram(filtered_df, x="Gender", color="Gender", title="Jumlah Pengguna Berdasarkan Gender")
        st.plotly_chart(fig_gender, use_container_width=True)
        
        fig_treatment = px.histogram(filtered_df, x="treatment", color="treatment", title="Distribusi Treatment (Target)")
        st.plotly_chart(fig_treatment, use_container_width=True)
        
        fig_stress = px.histogram(filtered_df, x="Growing_Stress", color="Growing_Stress", title="Distribusi Growing Stress")
        st.plotly_chart(fig_stress, use_container_width=True)

    with col2:
        fig_indoors = px.histogram(filtered_df, x="Days_Indoors", color="Days_Indoors", title="Distribusi Days Indoors")
        st.plotly_chart(fig_indoors, use_container_width=True)
        
        fig_occ = px.histogram(filtered_df, x="Occupation", color="Occupation", title="Distribusi Occupation")
        st.plotly_chart(fig_occ, use_container_width=True)
        
        fig_habits = px.histogram(filtered_df, x="Changes_Habits", color="Changes_Habits", title="Distribusi Changes Habits")
        st.plotly_chart(fig_habits, use_container_width=True)

with tab2:
    st.subheader("Pertanyaan Bisnis 1: Days Indoors vs Stress & Habits")
    col3, col4 = st.columns(2)
    
    with col3:
        fig_q1_stress = px.histogram(filtered_df, x="Days_Indoors", color="Growing_Stress", barmode="group", 
                                     title="Days Indoors vs Growing Stress")
        st.plotly_chart(fig_q1_stress, use_container_width=True)
        
    with col4:
        fig_q1_habits = px.histogram(filtered_df, x="Days_Indoors", color="Changes_Habits", barmode="group", 
                                     title="Days Indoors vs Changes Habits")
        st.plotly_chart(fig_q1_habits, use_container_width=True)

    st.subheader("Pertanyaan Bisnis 2: Occupation vs Treatment")
    fig_q2 = px.histogram(filtered_df, x="Occupation", color="treatment", barmode="group", 
                          title="Occupation vs Treatment")
    st.plotly_chart(fig_q2, use_container_width=True)

with tab3:
    st.subheader("Correlation Heatmap")
    corr_matrix = filtered_df.corr(numeric_only=True)
    fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto", 
                         color_continuous_scale='RdBu_r', title="Heatmap Korelasi")
    st.plotly_chart(fig_corr, use_container_width=True)

# 5. Kesimpulan
st.divider()
st.header("Kesimpulan")
st.markdown("""
- **Konklusi Pertanyaan 1:** *(Isi dengan ringkasan temuan korelasi Days Indoors)*
- **Konklusi Pertanyaan 2:** *(Isi dengan ringkasan pengaruh Occupation terhadap Treatment)*
""")