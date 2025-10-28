import streamlit as st

# Setting CSS untuk mengubah warna selectbox
def custom_style():
    st.markdown("""
        <style>

        /* ---------------- SIDEBAR BACKGROUND ---------------- */
        section[data-testid="stSidebar"] {
            background-color: #A8D8FF !important;   /* Biru muda cerah */
            color: #003049 !important;              /* Warna teks opsional */
        }

        /* Jika ingin teks label ikut kontras */
        section[data-testid="stSidebar"] label {
            color: #003049 !important;              /* Biru tua */
            font-weight: bold;
        }

        /* ---------------- BUTTON ---------------- */
        div.stButton > button:first-child {
            background-color: #F57171;       
            color: white;                     
            border-radius: 8px;               
            padding: 10px 20px;               
            font-size: 16px;                  
            font-weight: bold;                
            border: none;                     
            transition: 0.25s;                
        }
        
        div.stButton > button:first-child:hover {
            background-color: #DC2626;        
            transform: scale(1.03);           
            cursor: pointer;
        }
        
        div.stButton > button:first-child:active {
            transform: scale(0.97);
        }


        /* ---------------- NUMBER INPUT ---------------- */
        div[data-baseweb="input"] > div {
            background-color: #585C63 !important;
            color: #DADE4E !important;             
            border-radius: 10px;                   
            padding: 5px 10px;                     
            font-size: 18px !important;            
            font-weight: bold;                     
            border: none !important;
        }

        input[type=number] {
            color: #FFFFFF !important;             
            font-size: 15px !important;
            background-color: transparent !important;
        }


        /* ---------------- LABEL ---------------- */
        label[data-testid="stWidgetLabel"] > div {
            font-size: 16px !important;
            color: #191924 !important;             
            font-weight: bold;
        }


        /* ---------------- SELECTBOX ---------------- */
        div.stSelectbox div[data-baseweb="select"] > div {
            background-color: #585C63 !important;
            color: #eeeeee !important;  
            border-radius: 10px !important;
            border: none !important;
            font-size: 16px !important;
            font-weight: bold !important;
            padding: 1px 10px !important;
        }
        
        /* Dropdown list */
        div.stSelectbox ul[role="listbox"] {
            background-color: #1f1f1f !important;
            font-size: 16px !important;
            border-radius: 10px !important;
        }
        
        /* Highlighted / hovered options */
        li[role="option"]:hover {
            background-color: #393E46 !important;
            color: #eeeeee !important;
            cursor: pointer;
        }
        
        /* Selected text only for selectbox */
        div.stSelectbox span[data-baseweb="select"] {
            color: #00ADB5 !important;
        }
        
        /* Tambahkan border di sisi kanan kolom pertama */
        div[data-testid="column"]:first-child {
            border-right: 3px solid #D3D3D3;
        }
        
        /* Tambahkan jarak antar kolom */
        div[data-testid="column"] {
            padding-right: 20px;
            padding-left: 20px;
        }


        </style>
    """, unsafe_allow_html=True)



# Fungsi garis pemisah
def garis_pemisah(warna="#AAAAAA", margin_atas=2, margin_bawah=2, tebal=1):
    """
    Menampilkan garis pemisah tipis di Streamlit dengan pengaturan fleksibel.
    
    Parameters:
    - warna: str → warna garis (default abu-abu #AAAAAA)
    - margin_atas: int → jarak atas dalam piksel
    - margin_bawah: int → jarak bawah dalam piksel
    - tebal: float → ketebalan garis dalam piksel
    """
    st.markdown(f"""
        <hr style="
            margin-top: {margin_atas}px;
            margin-bottom: {margin_bawah}px;
            border: none;
            border-top: {tebal}px solid {warna};
        ">
    """, unsafe_allow_html=True)


# Fungsi tampilan nilai rata kanan
def nilai_kanan(
    nilai,
    prefix="Rp",
    satuan="Milyar",
    pembagi=1_000_000_000,
    font_size=15,
    warna="#172761",
    bold=False,
    margin_top=0,
    margin_bottom=0
):
    """
    Menampilkan teks hasil perhitungan di Streamlit rata kanan dengan format khusus.

    Parameters:
    - nilai: float/int → angka yang ingin ditampilkan
    - prefix: str → teks di depan angka (default: 'Rp')
    - satuan: str → teks di belakang angka (default: 'Milyar')
    - pembagi: int/float → pembagi nilai untuk menampilkan dalam satuan tertentu (default: 1 milyar)
    - font_size: int → ukuran font
    - warna: str → warna teks (kode hex)
    - bold: bool → apakah teks dicetak tebal
    - margin_top, margin_bottom: int → jarak vertikal dalam piksel
    """

    # Format angka dan style
    formatted_value = f"{prefix} {nilai / pembagi:,.2f} {satuan}".replace(",", ".")
    font_weight = "bold" if bold else "normal"

    st.markdown(f"""
        <div style='
            text-align: right;
            font-size: {font_size}px;
            color: {warna};
            font-weight: {font_weight};
            margin-top: {margin_top}px;
            margin-bottom: {margin_bottom}px;
        '>
            {formatted_value}
        </div>
    """, unsafe_allow_html=True)
    
    garis_pemisah()

def custom_button(label, key, color="red"):
    # Warna-presets
    if color == "red":
        bg = "#EF4444"; bg_hover = "#DC2626"
    elif color == "blue":
        bg = "#1E3A8A"; bg_hover = "#1E40AF"
    else:
        bg = "#4B5563"; bg_hover = "#374151"

    st.markdown(f"""
        <style>
        .custom-btn-{key} > button {{
            background-color: {bg} !important;
            color: white !important;
            border-radius: 8px;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            transition: 0.25s;
        }}
        .custom-btn-{key} > button:hover {{
            background-color: {bg_hover} !important;
            transform: scale(1.03);
            cursor: pointer;
        }}
        .custom-btn-{key} > button:active {{
            transform: scale(0.97);
        }}
        </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<div class='custom-btn-{key}'>", unsafe_allow_html=True)
    clicked = st.button(label, key=key)
    st.markdown("</div>", unsafe_allow_html=True)
    return clicked

# Fungsi footer
def sidebar_footer():
    st.sidebar.markdown(
        """
        <div style="text-align: center; margin-top: 30px; opacity: 0.7;">
            <small>
            © 2025 - Div. Keuangan Suralaya 8 <br>
            PT. PLN Indonesia Power <br>
            </small>
        </div>
        """,
        unsafe_allow_html=True
    )

# Fungsi Custom Subheader
def custom_subheader(text, font_size="20px", color="#00ADB5", align="left"):
    st.markdown(
        f"""
        <h3 style="
            font-size: {font_size};
            font-weight: 600;
            color: {color};
            text-align: {align};
            margin-top: 10px;
            margin-bottom: 10px;
        ">
            {text}
        </h3>
        """,
        unsafe_allow_html=True
    )

# Fungsi custom_caption
def custom_caption(text, font_size="12px", color="#888888", align="left", italic=False):
    style_italic = "italic" if italic else "normal"

    st.markdown(
        f"""
        <p style="
            font-size: {font_size};
            font-weight: 500;
            color: {color};
            text-align: {align};
            font-style: {style_italic};
            margin-top: 4px;
            margin-bottom: 4px;
            opacity: 0.85;
        ">
            {text}
        </p>
        """,
        unsafe_allow_html=True
    )