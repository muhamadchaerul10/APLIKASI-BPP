# -*- coding: utf-8 -*-
"""
Aplikasi Prediksi BPP (Biaya Pokok Produksi)
PT. PLN Indonesia Power Suralaya Unit 8

@author: Mega Bagus Herlambang
"""

# Menyiapkan library
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import sklearn
from sklearn import set_config
import pickle
import plotly.graph_objects as go
import shap
from scipy.stats import gaussian_kde
import tensorflow as tf
import matplotlib.ticker as mtick
from tensorflow.keras.models import load_model
from style import (custom_style, nilai_kanan, 
                   garis_pemisah, sidebar_footer, custom_caption)
from config import apply_app_config


# Menerapkan fungsi apply_app_config
apply_app_config()


# File Spreadsheet
link_file_tampilan = 'https://docs.google.com/spreadsheets/d/16hZccWcjepE-Ac9Qd-9kBpJiJ8zhu2ON/export?format=csv'
link_file = 'https://docs.google.com/spreadsheets/d/16hZccWcjepE-Ac9Qd-9kBpJiJ8zhu2ON/export?format=xlsx'
df_tampilan = pd.read_csv(link_file_tampilan)
df = pd.read_excel(link_file)
df_selain_bulan = df.drop('Bulan', axis=1)

# Mengaktifkan
custom_style()


# Menentukan nilai indeks awal
n_awal = 5

# Nilai akurasi model
akurasi_keras = 94.40
akurasi_elastic = 93.88
akurasi_ridge = 93.16
akurasi_knn = 92.04

        
# Nilai error model
error_keras = 63.14
error_elastic = 68.52
error_ridge = 73.91
error_knn = 85.59


# Membuka model
modelku_elastic = pickle.load(open('model_bpp_elastic.pkl', 'rb'))
modelku_ridge = pickle.load(open('model_bpp_ridge.pkl', 'rb'))
modelku_knn = pickle.load(open('model_bpp_knn.pkl', 'rb')) 
modelku_keras = load_model('model_bpp.keras')
   
     
# Membuka scaler khusus untuk model keras
tf.keras.utils.set_random_seed(0)
scaler = pickle.load(open('preprocess_bpp_columntransformer.pkl', 'rb'))


# Membuka explainer shap
shap_values_keras = pickle.load(open('shap_values_keras.pkl', 'rb'))
shap_values_elastic = pickle.load(open('shap_values_elastic.pkl', 'rb'))
shap_values_ridge = pickle.load(open('shap_values_ridge.pkl', 'rb'))
shap_values_knn = pickle.load(open('shap_values_knn.pkl', 'rb'))


# Bagian Judul Halaman Utama
st.title('⚡ Aplikasi Simulasi BPP (Biaya Pokok Produksi)')
st.caption('Alat bantu pengambilan keputusan berbasis data untuk early warning system BPP')
tab1, tab2, tab3 = st.tabs(['🔍 Eksplorasi Data', '🤖 Simulasi & Insight Model', '📈 Penjelasan Model'])




#-------------------------------------------------------------------------------------------------------
#                                           MENU SEBELAH KIRI 
#-------------------------------------------------------------------------------------------------------

# Untuk Menu Sidebar (Sisi Sebelah Kiri)
with st.sidebar:
    st.image('https://www.megabagus.id/wp-content/uploads/2025/10/logo-pln-ip.jpg', use_container_width=True)
    st.title('Panel Kontrol')
    
    # Tombol reset
    #custom_style()
    if st.button("🔄 Reset Aplikasi"):
        st.session_state.clear()
        st.rerun()
    
    # Garis pemisah    
    st.divider()
    
    # Keterangan akurasi tiap model
    st.markdown(f"""
    <div style="font-size:15px; color:#1a3e6f; font-weight:600;">
    ⭐ Akurasi 4 model terbaik:
    <ol style="margin-left: 15px;">
        <li>Neural Network = <span style="color:#1a3e6f;">{akurasi_keras}%</span></li>
        <li>Elastic Net = <span style="color:#1a3e6f;">{akurasi_elastic}%</span></li>
        <li>Ridge Regression = <span style="color:#1a3e6f;">{akurasi_ridge}%</span></li>
        <li>KNN = <span style="color:#1a3e6f;">{akurasi_knn}%</span></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Garis pemisah
    st.divider()
    
    # Keterangan Data Simulasi
    st.markdown("""
    <div style="text-align:left; font-size:15px; color:#1a3e6f; font-weight:600;">
    ⚙️ Data Simulasi
    <ul style="margin-left: 15px;">
        <li>Masukkan data sebagai dasar prediksi.</span></li>
        <li>Nilai yang muncul di tampilan awal adalah nilai bulan terakhir.</span></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Dua enter
    st.write('')
    st.write('')
    
    # Nilai Beban Pembelian Tenaga Listrik
    b_ptl = st.number_input(str(df.columns[n_awal+1]), value=df.iloc[-1,n_awal+1], step=1)
    nilai_kanan(b_ptl)
    
    # Nilai Beban Sewa
    b_sewa = st.number_input(str(df.columns[n_awal+2]), value=df.iloc[-1,n_awal+2], step=1)
    nilai_kanan(b_sewa)
    
    # Nilai Beban Biosolar
    b_biosolar = st.number_input(str(df.columns[n_awal+3]), value=df.iloc[-1,n_awal+3], step=1)
    nilai_kanan(b_biosolar)

    # Nilai Beban Batubara
    b_batubara = st.number_input(str(df.columns[n_awal+4]), value=df.iloc[-1,n_awal+4], step=1)
    nilai_kanan(b_batubara)
    
    # Nilai Beban Biomassa
    b_biomassa = st.number_input(str(df.columns[n_awal+5]), value=df.iloc[-1,n_awal+5], step=1)
    nilai_kanan(b_biomassa)
 
    # Nilai Beban Kimia
    b_kimia = st.number_input(str(df.columns[n_awal+6]), value=df.iloc[-1,n_awal+6], step=1)
    nilai_kanan(b_kimia)
    
    # Nilai Beban Minyak
    b_minyak = st.number_input(str(df.columns[n_awal+7]), value=df.iloc[-1,n_awal+7], step=1)
    nilai_kanan(b_minyak)
    
    # Nilai Beban Pemeliharaan
    b_pemeliharaan = st.number_input(str(df.columns[n_awal+8]), value=df.iloc[-1,n_awal+8], step=1)
    nilai_kanan(b_pemeliharaan)
    
    # Nilai Beban Kepegawaian
    b_kepegawaian = st.number_input(str(df.columns[n_awal+9]), value=df.iloc[-1,n_awal+9], step=1)
    nilai_kanan(b_kepegawaian)
    
    # Nilai Beban Penyusutan Aset Tetap
    b_penyusutan = st.number_input(str(df.columns[n_awal+10]), value=df.iloc[-1,n_awal+10], step=1)
    nilai_kanan(b_penyusutan)    

    # Nilai Beban Penyusutan Aset Tetap (Sewa)
    b_penyusutan_s = st.number_input(str(df.columns[n_awal+11]), value=df.iloc[-1,n_awal+11], step=1)
    nilai_kanan(b_penyusutan_s)      
    
    # Nilai Beban Administrasi
    b_administrasi = st.number_input(str(df.columns[n_awal+12]), value=df.iloc[-1,n_awal+12], step=1)
    nilai_kanan(b_administrasi)  
    
    # Nilai Beban Emisi Carbon
    b_emisi = st.number_input(str(df.columns[n_awal+13]), value=df.iloc[-1,n_awal+13], step=1)
    nilai_kanan(b_emisi)    

    # Nilai Fee EPI
    b_fee = st.number_input(str(df.columns[n_awal+14]), value=df.iloc[-1,n_awal+14], step=1)
    nilai_kanan(b_fee)  

    # Nilai Lain-lain
    b_lain = st.number_input(str(df.columns[n_awal+15]), value=df.iloc[-1,n_awal+15], step=1)
    nilai_kanan(b_lain)   

    # Nilai Penjualan
    b_penjualan = st.number_input(str(df.columns[n_awal-3]), value=df.iloc[-1,n_awal-3], step=1)
    nilai_kanan(b_penjualan)     
    
    # Spasi
    st.write('')
    
    # Bagian Copyright
    sidebar_footer()    



#-------------------------------------------------------------------------------------------------------
#                                       LAYAR UTAMA 
#-------------------------------------------------------------------------------------------------------

# Tab bagian pertama
with tab1:
    
    #----------------------
    #     MELIHAT TABEL
    #----------------------
    
    # Judul awal
    st.subheader('Eksplorasi Data')
    
    # Tampilan tabel
    st.dataframe(df_tampilan)
    
    # Catatan kecil untuk user
    st.caption('Note: Data ini diupdate melalui file spreadsheet, silakan lakukan update untuk data terbaru')
    
    # Garis pemisah
    st.divider()
    
    
    #----------------------
    #    SCATTER PLOT
    #----------------------
    
    # Judul awal
    st.subheader('Visualisasi Scatter Plot')
    
    # Pilihan variabel dari dataframe (jika dataset Anda besar)
    x_var = st.selectbox("Pilih variabel X", df_selain_bulan.columns)
    y_var = st.selectbox("Pilih variabel Y", df_selain_bulan.columns)
    
    st.write(' ')
    
    # Opsi garis regresi
    tampil_regresi = st.checkbox("Tampilkan garis regresi", value=False)
    
    # Penentuan jumlah kolom
    col1, col2 = st.columns([2,1], gap='large')
    
    # Kolom pertama
    with col1:
        
        # Style seaborn
        sns.set_style("white")
        
        # Menyiapkan canvasnya
        fig, ax = plt.subplots(figsize=(4, 3))

        # Scatter seaborn (lebih halus dan estetis)
        sns.scatterplot(
            data=df,
            x=x_var,
            y=y_var,
            s=15,                # ukuran marker kecil
            color="#2252F0",     # warna marker (bisa Anda ganti)
            ax=ax
        )
        
        # Jika user memilih, tampilkan garis regresi
        if tampil_regresi:
            sns.regplot(
                data=df,
                x=x_var,
                y=y_var,
                scatter=False,    # supaya tidak menggandakan scatter
                ax=ax,
                color="#e63946",  # warna garis regresi
                line_kws={"linewidth":1.2}
            )
        
        # Hilangkan border sisi atas & kanan
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Rapikan garis sumbu
        ax.spines['left'].set_linewidth(0.8)
        ax.spines['bottom'].set_linewidth(0.8)
        
        # Label
        ax.set_xlabel(f'{x_var}', fontsize=6)
        ax.set_ylabel(f'{y_var}', fontsize=6)
        ax.set_title(f'{x_var} vs {y_var}', fontsize=7)
        
        # ukuran tick
        ax.tick_params(axis='both', labelsize=6)
        
        # Kecilkan tulisan scientific notaion (misal: 1e10)
        ax.xaxis.offsetText.set_fontsize(6)
        ax.yaxis.offsetText.set_fontsize(6)    
        
        # Memunculkan visualisasinya
        st.pyplot(fig, use_container_width=False)
    
    # Kolom kedua
    with col2:
        
        # Penulisan variabel terpilih
        st.markdown("""
        <div style="
            padding: 18px;
            border-radius: 10px;
            background-color: #F8F9FA;
            border: 1px solid #E0E0E0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            ">
            <h4 style="margin-top: 0; margin-bottom: 10px; color:#1a3e6f;">📌 Variabel yang Dipilih</h4>
            <p style="font-size:14px; margin:0;">
            <b>Sumbu X:</b> <span style="color:#2c7be5;">{}</span><br>
            <b>Sumbu Y:</b> <span style="color:#e83e8c;">{}</span>
            </p>
        </div>
        """.format(x_var, y_var), unsafe_allow_html=True)
    
    # Garis pemisah
    st.divider()
    
       
    #----------------------
    #    LINE CHART
    #----------------------
    
    # Judul awal
    st.subheader('Visualisasi Line Chart')
    
    # Pilih variabel Y untuk line chart
    y_line = st.selectbox("Pilih variabel untuk Line Chart (Sumbu Y)", df_selain_bulan.columns)
    
    # Penentuan kolom
    col1, col2 = st.columns([2,1], gap="large")
    
    # Kolom pertama
    with col1:
    
        fig = px.line(
            df,
            x="Bulan",
            y=y_line,
            markers=True,     
        )
    
        # Ganti warna line & marker (optional)
        fig.update_traces(
            line=dict(color="#1f77b4", width=2),
            marker=dict(size=6, color="#CC7F3D")
        )
    
        # Hilangkan background grid agar clean
        fig.update_layout(
            showlegend=False,
            plot_bgcolor="white",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            margin=dict(l=20, r=20, t=30, b=20)
        )
    
        # Sumbu dengan garis halus
        fig.update_xaxes(showline=True, linewidth=1, linecolor="black", tickangle=45)
        fig.update_yaxes(showline=True, linewidth=1, linecolor="black")
        
        # Memunculkan visualnya
        st.plotly_chart(fig, use_container_width=True)
        
    # Kolom kedua
    with col2:
        
        # Keterangan variabel terpilih
        st.markdown(f"""
        <div style="
            padding: 18px;
            border-radius: 10px;
            background-color: #F8F9FA;
            border: 1px solid #E0E0E0;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        ">
            <h4 style="margin-top: 0; margin-bottom: 10px; color:#1a3e6f;">📊 Variabel Line Chart</h4>
            <p style="font-size:14px; margin:0;">
            <b>Sumbu X:</b> <span style="color:#2c7be5;">Bulan</span><br>
            <b>Sumbu Y:</b> <span style="color:#e83e8c;">{y_line}</span>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()


    #----------------------
    #    Histogram
    #----------------------

    # Judul awal
    st.subheader('Visualisasi Histogram')
    
    # Pilih variabel
    y_dist = st.selectbox("Pilih variabel untuk Distribution Plot", df_selain_bulan.columns)
    
    # Penentuan kolom
    col1, col2 = st.columns([2,1], gap="large")
    
    # Kolom pertama
    with col1:
        
        # Ambil data
        data = df_selain_bulan[y_dist].dropna()
    
        # Hitung KDE
        kde = gaussian_kde(data)
        x_range = np.linspace(data.min(), data.max(), 200)
        y_kde = kde(x_range)
    
        # Buat figure
        fig_hist_kde = go.Figure()
    
        # Histogram
        fig_hist_kde.add_trace(go.Histogram(
            x=data,
            nbinsx=20,
            marker_color="#1f77b4",
            opacity=0.6,
            name="Histogram"
        ))
    
        # Density Line
        fig_hist_kde.add_trace(go.Scatter(
            x=x_range,
            y=y_kde * len(data) * (data.max()-data.min())/20,  # skala supaya sebanding
            mode="lines",
            line=dict(color="#e63946", width=2),
            name="KDE Curve"
        ))
    
        # Styling
        fig_hist_kde.update_layout(
            plot_bgcolor="white",
            showlegend=True,
            margin=dict(l=20, r=20, t=30, b=20),
            yaxis_title="Frekuensi"
        )
        fig_hist_kde.update_xaxes(showline=True, linecolor="black")
        fig_hist_kde.update_yaxes(showline=True, linecolor="black")
    
        st.plotly_chart(fig_hist_kde, use_container_width=True)
    
    
    with col2:
        st.markdown(f"""
        <div style="
            padding:18px; border-radius:10px; background-color:#F8F9FA;
            border:1px solid #E0E0E0; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
            <h4 style="margin:0 0 10px 0; color:#1a3e6f;">📊 Distribution + KDE</h4>
            <p style="font-size:14px; margin:0;">
            <b>Variabel:</b> <span style="color:#2c7be5;">{y_dist}</span><br>
            Histogram menunjukkan frekuensi, dan kurva merah menunjukkan estimasi distribusi kontinu.
            </p>
        </div>
        """, unsafe_allow_html=True) 

    st.divider()

    
    #----------------------
    #    Boxplot
    #----------------------       

    # Judul awal
    st.subheader('Visualisasi Boxplot')
    
    # Pemilihan variabel
    y_box = st.selectbox("Pilih variabel untuk Boxplot", df_selain_bulan.columns)
    
    # Penentuan kolom
    col1, col2 = st.columns([2,1], gap="large")
    
    # Kolom pertama
    with col1:
        fig_box = px.box(df, y=y_box, color_discrete_sequence=["#e83e8c"])
        fig_box.update_layout(showlegend=False, plot_bgcolor="white")
        st.plotly_chart(fig_box, use_container_width=True)
    
    # Kolom kedua
    with col2:
        st.markdown(f"""
        <div style="padding:18px; border-radius:10px; background-color:#F8F9FA;
                    border:1px solid #E0E0E0; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
            <h4 style="margin:0 0 10px 0; color:#1a3e6f;">📦 Boxplot</h4>
            <p style="font-size:14px; margin:0;">
            <b>Sumbu Y:</b> <span style="color:#e83e8c;">{y_box}</span><br>
            <b>Insight:</b> Menemukan outlier dan penyebaran nilai.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    #----------------------
    #    Heatmap
    #----------------------       

    # Judul awal
    st.subheader('Korelasi Heatmap')
    
    # Penentuan kolom
    col1, col2 = st.columns([2,1], gap="large")
    
    # kolom pertama
    with col1:
        fig_corr, ax_corr = plt.subplots(figsize=(6,5))
        sns.heatmap(
            df_selain_bulan.corr(),
            cmap="coolwarm",
            annot=True,                 # tampilkan nilai korelasi
            fmt=".2f",                  # 2 angka desimal
            annot_kws={"size":4},       # ukuran font angka annotasi
            cbar=True,                  # menyalakan color bar
            cbar_kws={"shrink": 0.7},   # tinggi colorbar
            ax=ax_corr
        )
        cbar = ax_corr.collections[0].colorbar
        cbar.ax.tick_params(labelsize=4)
        ax_corr.tick_params(axis='both', labelsize=4)
        ax_corr.set_title("Correlation Heatmap", fontsize=8)
        st.pyplot(fig_corr, use_container_width=False)
    
    # Kolom kedua
    with col2:
        st.markdown("""
        <div style="padding:18px; border-radius:10px; background-color:#F8F9FA;
                    border:1px solid #E0E0E0; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
            <h4 style="margin:0 0 10px 0; color:#1a3e6f;">🔗 Korelasi Antar Variabel</h4>
            <p style="font-size:14px; margin:0;">
            <b>Insight:</b> Lihat variabel mana yang paling berpengaruh.
            </p>
        </div>
        """, unsafe_allow_html=True)


# Tab bagian kedua
with tab2:
    
    # Penentuan model
    pilihan_model = st.selectbox('Pilih Model', ('Neural Network', 'Elastic', 'Ridge', 'KNN'))
    
    # Penentuan kolom
    col1, col2 = st.columns([1, 2], gap='large', border=True)
    
    # Kolom pertama
    with col1:
        
        # Judul pertama
        st.subheader('Simulasi Prediksi BPP')
        
        # Keterangan instruksi
        st.write('Silakan atur nilai setiap beban di menu sebelah kiri untuk melakukan simulasi prediksi BPP')
        
        # Menggabungkan data input
        data = {
                str(df.columns[n_awal+1]) : b_ptl,
                str(df.columns[n_awal+2]) : b_sewa,
                str(df.columns[n_awal+3]) : b_biosolar,
                str(df.columns[n_awal+4]) : b_batubara,
                str(df.columns[n_awal+5]) : b_biomassa,
                str(df.columns[n_awal+6]) : b_kimia,
                str(df.columns[n_awal+7]) : b_minyak,
                str(df.columns[n_awal+8]) : b_pemeliharaan,
                str(df.columns[n_awal+9]) : b_kepegawaian,
                str(df.columns[n_awal+10]) : b_penyusutan,
                str(df.columns[n_awal+11]) : b_penyusutan_s,
                str(df.columns[n_awal+12]) : b_administrasi,
                str(df.columns[n_awal+13]) : b_emisi,
                str(df.columns[n_awal+14]) : b_fee,
                str(df.columns[n_awal+15]) : b_lain,
                str(df.columns[n_awal-3]) : b_penjualan,
                }

        kolom = list(data.keys())
        df_final = pd.DataFrame([data.values()], columns=kolom)        
        df_final_scaling = scaler.transform(df_final)
        
        # Memprediksi model
        if pilihan_model == 'Neural Network':
            hasil = round(float(modelku_keras.predict(df_final_scaling)),2)
            nilai_error = error_keras
        elif pilihan_model == 'Elastic':
            hasil = round(float(modelku_elastic.predict(df_final)),2)
            nilai_error = error_elastic
        elif pilihan_model == 'Ridge':
            hasil = round(float(modelku_ridge.predict(df_final)),2)
            nilai_error = error_ridge
        else:
            hasil = round(float(modelku_knn.predict(df_final)),2)
            nilai_error = error_knn            
                
        # Mengeluarkan prediksi
        st.metric(
            label="Estimasi Prediksi BPP",
            value=f"~ {hasil} ± {nilai_error}",
            help='Nilai ini merepresentasikan nilai BPP berdasarkan semua nilai variabel yang sudah diinput'
        )
        
        # Melihat detail data awal
        with st.expander('Lihat detail input mentah yang dikirim ke model'):
            st.dataframe(data)
        
        # Keterangan tips
        custom_caption('Tips: Perhatikan Plot SHAP Summary, naikkan nilai variabel yang berperan positif dan turunkan nilai yang berperan negatif untuk mendapatkan nilai BPP yang dikehendaki!',
                       font_size="16px", color="#8F4D21")
   
    
    # Kolom kedua
    with col2:
        
        # Tulisan teks
        st.write('Visualisasi berikut adalah hasil analisis dari semua rentang data yang ada sesuai model yang dipilih')

        # Jika dipilih model Neural Network
        if pilihan_model == 'Neural Network':
            
            # Plot pertama
            st.subheader("🔹 Plot SHAP Bar")
            fig1, ax1 = plt.subplots()
            shap.plots.bar(shap_values_keras, max_display=20, show=False)
            ax1.set_title("Model Neural Network - Urutan Bobot Pengaruh Setiap Variabel")
            st.pyplot(fig1)
            
            # Plot kedua
            st.subheader("🔹 Plot SHAP Summary")
            fig2, ax2 = plt.subplots()
            shap.summary_plot(shap_values_keras, show=False)
            ax2.set_title("Model Neural Network - Interaksi Variabel Terhadap BPP")
            st.pyplot(fig2)     
        
 
        # Jika dipilih model elastic
        elif pilihan_model == 'Elastic':
            
            # Plot pertama
            st.subheader("🔹 Plot SHAP Bar")
            fig1, ax1 = plt.subplots()
            shap.plots.bar(shap_values_elastic, max_display=20, show=False)
            ax1.set_title("Model Elastic - Urutan Bobot Pengaruh Setiap Variabel")
            st.pyplot(fig1)
            
            # Plot kedua
            st.subheader("🔹 Plot SHAP Summary")
            fig2, ax2 = plt.subplots()
            shap.summary_plot(shap_values_elastic, show=False)
            ax2.set_title("Model Elastic - Interaksi Variabel Terhadap BPP")
            st.pyplot(fig2)   
        
        # Jika dipilih model ridge
        elif pilihan_model == 'Ridge':
            
            # Plot pertama
            st.subheader("🔹 Plot SHAP Bar")
            fig1, ax1 = plt.subplots()
            shap.plots.bar(shap_values_ridge, max_display=20, show=False)
            ax1.set_title("Model Ridge - Urutan Bobot Pengaruh Setiap Variabel")
            st.pyplot(fig1)
            
            # Plot kedua
            st.subheader("🔹 Plot SHAP Summary")
            fig2, ax2 = plt.subplots()
            shap.summary_plot(shap_values_ridge, show=False)
            ax2.set_title("Model Ridge - Interaksi Variabel Terhadap BPP")
            st.pyplot(fig2)     
        
        # Jika dipilih knn
        else:
            
            # Plot pertama
            st.subheader("🔹 Plot SHAP Bar")
            fig1, ax1 = plt.subplots()
            shap.plots.bar(shap_values_knn, max_display=20, show=False)
            ax1.set_title("Model KNN - Urutan Bobot Pengaruh Setiap Variabel")
            st.pyplot(fig1)
            
            # Plot kedua
            st.subheader("🔹 Plot SHAP Summary")
            fig2, ax2 = plt.subplots()
            shap.summary_plot(shap_values_knn, show=False)
            ax2.set_title("Model KNN - Interaksi Variabel Terhadap BPP")
            st.pyplot(fig2)               
                              
# Tab ketiga    
with tab3:
    
    # Rentang waktu
    rentang_waktu = ['Jan 2023', 'Feb 2023', 'Mar 2023', 'Apr 2023', 'Mei 2023', 'Jun 2023', 'Jul 2023', 'Agu 2023', 'Sep 2023', 'Okt 2023', 'Nov 2023', 'Des 2023',
                     'Jan 2024', 'Feb 2024', 'Mar 2024', 'Apr 2024', 'Mei 2024', 'Jun 2024', 'Jul 2024', 'Agu 2024', 'Sep 2024', 'Okt 2024', 'Nov 2024', 'Des 2024',
                     'Jan 2025', 'Feb 2025', 'Mar 2025', 'Apr 2025', 'Mei 2025', 'Jun 2025', 'Jul 2025', 'Agu 2025', 'Sep 2025'] 
    
    # Pemilihan model
    pilihan_model2 = st.selectbox('Pilih Model', ('Neural Network (NN)', 'Elastic Net', 'Ridge Regression', 'K-Nearest Neighbors'))
    
    # pemilihan urutan waktu
    pilihan_waktu = st.selectbox('Pilih waktu yang mau diinvestigasi', (rentang_waktu))
    index_pilihan = rentang_waktu.index(pilihan_waktu)
    
    # Jika yang terpilih neural network
    if pilihan_model2 == 'Neural Network (NN)':
        
        # Plot Waterfall 
        st.write(f'Nilai BPP Asli = {df.BPP[index_pilihan]:.2f}')
        st.write(f'Error model {str(pilihan_model2)} = ± {error_keras}')
        st.subheader("🔹 Plot SHAP Bar")
        fig, ax = plt.subplots()
        shap.plots.waterfall(shap_values_keras[index_pilihan], max_display=20, show=False)
        ax.set_title("Model Neural Network - Pengaruh Setiap Variabel Terhadap BPP")
        st.pyplot(fig) 
        
        st.markdown(f'<b>Cara Kerja Model {pilihan_model2}</b>:', unsafe_allow_html=True)
        
        st.markdown('''
        Model Neural Network bekerja dengan meniru cara kerja otak manusia dalam mengenali pola. 
        Data input masuk ke dalam neurons pada input layer, kemudian diproses secara bertahap melalui beberapa hidden 
        layer yang masing-masing berisi node yang melakukan operasi matematika (perkalian bobot, penambahan bias, dan aktivasi). 
        Pada setiap layer, model belajar menyesuaikan bobot (weight) berdasarkan seberapa besar kesalahannya dalam memprediksi output, 
        proses ini disebut training dan dilakukan menggunakan metode backpropagation. Semakin sering model dilatih, bobot akan 
        menyesuaikan sehingga pola dan hubungan kompleks dalam data dapat dipelajari dan menghasilkan prediksi atau keputusan yang semakin akurat.
        ''')
    
    # Jika yang terpilih elastic
    elif pilihan_model2 == 'Elastic Net':
        
        # Plot Waterfall
        st.write(f'Nilai BPP Asli = {df.BPP[index_pilihan]:.2f}')
        st.write(f'Error model {str(pilihan_model2)} = ± {error_elastic}')
        st.subheader("🔹 Plot SHAP Bar")
        fig, ax = plt.subplots()
        shap.plots.waterfall(shap_values_elastic[index_pilihan], max_display=20, show=False)
        ax.set_title("Model Elastic Net - Pengaruh Setiap Variabel Terhadap BPP")
        st.pyplot(fig) 

        st.markdown(f'<b>Cara Kerja Model {pilihan_model2}</b>:', unsafe_allow_html=True)
        
        st.markdown('''
        Model Elastic Net Regression bekerja dengan menggabungkan dua metode regularisasi, 
        yaitu L1 (Lasso) dan L2 (Ridge), untuk menghasilkan model regresi yang stabil dan tidak mudah overfitting. 
        Dalam proses pelatihannya, Elastic Net mencari garis regresi yang paling sesuai dengan pola data, sambil menambahkan 
        penalti pada nilai koefisien agar tidak terlalu besar. Penalti L1 membantu menghilangkan atau mengecilkan beberapa 
        koefisien sehingga model menjadi lebih sederhana (feature selection), sedangkan penalti L2 membantu menjaga stabilitas 
        koefisien terutama ketika terdapat fitur yang saling berkorelasi. Dengan kombinasi kedua penalti ini, Elastic Net 
        mampu memberikan hasil prediksi yang baik pada dataset dengan banyak variabel dan hubungan antar fitur yang kompleks.
        ''')        
    
    # Jika yang terpilih ridge
    elif pilihan_model2 == 'Ridge Regression':
        
        # Plot Waterfall
        st.write(f'Nilai BPP Asli = {df.BPP[index_pilihan]:.2f}')
        st.write(f'Error model {str(pilihan_model2)} = ± {error_ridge}')
        st.subheader("🔹 Plot SHAP Bar")
        fig, ax = plt.subplots()
        shap.plots.waterfall(shap_values_ridge[index_pilihan], max_display=20, show=False)
        ax.set_title("Model Ridge Regression - Pengaruh Setiap Variabel Terhadap BPP")
        st.pyplot(fig) 
        
        st.markdown(f'<b>Cara Kerja Model {pilihan_model2}</b>:', unsafe_allow_html=True)
        
        st.markdown('''
        Ridge Regression bekerja dengan menambahkan penalti L2 pada proses pelatihan regresi linier untuk mencegah model 
        memiliki koefisien yang terlalu besar. Saat mencari hubungan terbaik antara variabel input dan output, Ridge tetap 
        meminimalkan error prediksi, namun juga menambahkan batasan agar koefisien tidak berkembang secara ekstrem, terutama 
        ketika data memiliki multikolinearitas (fitur saling berkorelasi). Dengan cara ini, model menjadi lebih stabil, tidak 
        mudah overfitting, dan mampu memberikan hasil prediksi yang lebih konsisten meskipun data input memiliki banyak variabel 
        atau data yang tersedia relatif sedikit.
        ''')    
    
    # Jika yang terpilih knn
    else:
        
        # Plot Waterfall
        st.write(f'Nilai BPP Asli = {df.BPP[index_pilihan]:.2f}')
        st.write(f'Error model {str(pilihan_model2)} = ± {error_knn}')
        st.subheader("🔹 Plot SHAP Bar")
        fig, ax = plt.subplots()
        shap.plots.waterfall(shap_values_knn[index_pilihan], max_display=20, show=False)
        ax.set_title("Model KNN - Pengaruh Setiap Variabel Terhadap BPP")
        st.pyplot(fig) 
        
        st.markdown(f'<b>Cara Kerja Model {pilihan_model2}</b>:', unsafe_allow_html=True)
        
        st.markdown('''
        KNN Regression bekerja dengan cara memprediksi nilai suatu data baru berdasarkan nilai dari k tetangga terdekat dalam 
        data pelatihan. Untuk melakukan prediksi, model akan menghitung jarak antara data baru dan semua data yang ada di dataset 
        (misalnya menggunakan jarak Euclidean), lalu memilih k data yang jaraknya paling dekat. Nilai prediksi akhir diperoleh dari 
        rata-rata nilai target dari tetangga-tetangga terpilih tersebut. Karena tidak ada proses pelatihan berbentuk penyesuaian parameter, 
        KNN disebut sebagai lazy learning, dan performanya sangat bergantung pada pemilihan nilai k serta skala data (sehingga normalisasi 
        biasanya penting). Model ini sederhana namun efektif, terutama ketika hubungan antar variabel bersifat lokal atau tidak linear.
        ''')        
    
    # Menambahkan garis pemisah
    garis_pemisah()
    
    # Keterangan tambahan
    st.markdown("""
    <div style="font-size:16px; color:#1a3e6f; font-weight:600;">
    Keterangan:
    <ul style="margin-left: 15px;">
        <li>Nilai yang ditampilkan di grafik merupakan nilai sesuai waktu yang dipilih.</li>
        <li>Nilai f(x) adalah nilai prediksi BPP yang dihasilkan oleh model.</li>
        <li>Nilai E[<i>f(X)</i>] adalah nilai rata-rata dari prediksi semua rentang waktu yang dihasilkan oleh model.</li>
        <li>Tanda - dan + adalah arah pengaruh dari setiap variabel dari nilai rata-rata dasarnya.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)       