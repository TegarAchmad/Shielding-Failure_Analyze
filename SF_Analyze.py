import streamlit as st
from streamlit_option_menu import option_menu
import math as  m
import numpy as np
import pandas as pd
import plotly_express as px
import base64
import plotly.graph_objects as go
from streamlit_extras.mention import mention

with open("design.css") as source_des:
    st.markdown(f"<style>{source_des.read()}</style>", unsafe_allow_html=True)

@st.cache_data
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()
img = get_img_as_base64("image2.jpg")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"]{{
background-image: url("data:image/png;base64,{img}");
background-size: cover;
}}
[data-testid="stForm"]{{
background-color: white;
border-radius: 25px;
padding: 20px;
box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
}}
[data-testid="stHeader"]
{{
background:rgba(0,0,0,0);
}}
[data-testid="stMarkdownContainer"]{{
font-family: 'Times New Roman', Times, serif;
}}
css-10trblm e16nr0p30{{
font-family:'Times New Roman', Times, serif;
}}
[data-testid="stTable"]{{
font-family: 'Times New Roman', Times, serif;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)
with st.sidebar:
    page_bg_img = f"""
    <style>
    [data-testid="stMarkdownContainer"]{{
    font-family: 'Times New Roman', Times, serif;
    }}
    [data-testid="stImage"]{{
    width: 70%;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    st.image("logofix.png")

    selected = option_menu(
        menu_title="SITUS WEB ANALISA PERISAI",
        options=["Keandalan & Optimasi Perisaian", "Simulasi Sambaran", "Kontak"],
        icons=["shield-shaded", "lightning-charge-fill", "envelope"],
        menu_icon="cast",
        styles=
        {
    "container": {"background-color": "white", },
        "nav-link": {"font": "#31333f"},
        "icon": {"color": "#38A5D4"}, 
        "nav-link-selected": {"background-color": "#38A5D4"},
        }
    )

if selected == "Keandalan & Optimasi Perisaian":
    page_bg_img = f"""
    <style>
    [data-testid="stMarkdownContainer"]{{
    font-family: 'Times New Roman', Times, serif;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    #inputan
    with st.form("Data Tower"):
        st.markdown("<h1 style='text-align: center; text-color:#31333f;font-family: 'Times New Roman', Times, serif;background-color: white;border-radius: 25px;padding: 20px;'>KEANDALAN & OPTIMASI PERISAIAN</h1>", unsafe_allow_html=True)
        st.markdown("---")
        st.subheader("Data Tower")
        JenisTower = st.selectbox("Tentukan Jenis Tower Transmisi!", options=("SUTT", "SUTET", "SUTUT"))
        kol1,kol2,kol3=st.columns(3)
        htower = kol1.number_input("Tinggi Tower (meter)", 0.00)
        hfasa= kol2.number_input("Tinggi Kawat Fasa (m)")
        fg = kol3.number_input("Tinggi Travers Fasa-GSW (Meter)", 0.00)
        col3,col4=st.columns(2)
        fasa = col3.number_input("Panjang Travers Fasa (Meter)")
        pgsw = col4.number_input("Panjang Travers GSW (Meter)")
        col1,col2=st.columns(2)
        rtowerhi = col1.number_input("Lebar Kaki-Kaki Tower (m)") #panjang kakiAkeB
        rtower = rtowerhi/2
        DiameterKawatFasa= col2.number_input("Diameter Kawat Fasa (mm)")
        cola,colb,colc=st.columns(3)
        BIL = cola.number_input("BIL (kV)")
        PrentengIsolator = colb.number_input("Panjang Isolator (m)")
        IKL = colc.number_input("IKL")
    
        file_csv = st.file_uploader("Upload File Sambaran -- Contoh : [Format File](https://drive.google.com/file/d/1XqsDXSEtugAOfEqKX-YVkgLPUS5CQufd/view?usp=sharing) ", type=['csv'])
        if file_csv is not None:
            df = pd.read_csv("TabelSambaran.csv",";")
            df['new_column'] = df['Arus Petir (kA)']*df['Jumlah Sambaran']
            total_mean = df['new_column'].sum()
            total = df['Jumlah Sambaran'].sum()
            meanpetir = round((total_mean/total),2)
            def mencari_persen(masukan):
                    hasil = df.loc[df['Arus Petir (kA)'] > masukan, 'Jumlah Sambaran'].sum()
                    return (hasil/total*100)

        def form_submit_button(*args, key=None, **kwargs):
            if key is None:
                raise ValueError("Must pass key")
            if key not in st.session_state:
                st.session_state[key] = False
            if st.form_submit_button(*args, **kwargs):
                st.session_state[key] = not st.session_state[key]
            return st.session_state[key]

        if form_submit_button('Uji Keandalan', key="sentiment_button"):
            #Impedansi
            Ztower = round(30*m.log((2*(htower**2 + rtower**2))/(rtower**2)), 2)
            LebarTraversGSW = pgsw*2
            rKawatFasa = (DiameterKawatFasa/2)/1000
            Zc = 60*(m.log((2*hfasa/rKawatFasa)))
        
            AD2 = round(pow((hfasa/6.7), (1/0.8)), 2)
            B2 = round(m.degrees(m.atan((fasa-pgsw)/fg)),2) #hitung sudut eksisting
            
            #ELEKTROGEOMETRI
            def ELEKTROGEOMETRI(alfa, Isf, pgswexpand):
                global Smaks
                teta = 0
                traversfasagsw = fasa - pgswexpand
                F = m.sqrt(fg**2 + traversfasagsw**2 )
                S = hfasa 
                w = m.degrees(m.acos((F/(2*S))))
                Xs = S*((m.cos(teta)+m.sin(m.radians(alfa-w))))

                #Arus minimum yang dapat menyebabkan kegagalan perisai
                VlompatApi = ((0.4*PrentengIsolator)+((0.71*PrentengIsolator)/(6**0.75)))*10**3
                Imin = 2*VlompatApi/Zc
                #Jarak sambaran untuk arus minimum
                Smin = 6.7*Imin**0.8
                if JenisTower=="SUTT":
                    Betta = 1
                elif JenisTower=="SUTET":
                    Betta = 0.8
                elif JenisTower=="SUTUT":
                    Betta = 0.67
                BettaS = Betta*Smin
                Wmin = m.degrees(m.acos((F/(2*Smin))))
                if BettaS < hfasa:
                    XsMin = Smin*((1+m.sin(m.radians(alfa-Wmin))))
                else:
                    teta2=(BettaS-hfasa)/hfasa
                    XsMin = Smin*((m.cos(teta2)+m.sin(m.radians(alfa-Wmin))))

                #Jarak Sambaran Maksimum
                mm = (fasa-pgswexpand)/(htower-hfasa)
                Y0 = (htower+hfasa)/2
                As = mm**2-mm**2*Betta-Betta**2
                Bs = Betta*(mm**2+1)
                Cs = mm**2+1
                Smaks = Y0*((-Bs-m.sqrt(Bs**2+As*Cs))/As)
                Imaks = (Smaks/6.7)**(1/0.8)

                #probabilitas Gangguan
                Pmin = m.exp((-Imin/34))
                Pmax = m.exp((-Imaks/34))

                #Gangguan Petir Karena Kegagalan Perisai
                NSF = 0.015*IKL*Xs*(Pmin-Pmax)
                VSF = Zc*(Isf/2)

                if VSF > BIL:
                    huhuhu = ("FLASHOVER!!!")
                else:
                    huhuhu = ("TIDAK TERJADI FLAHSOVER")
                #HASIL
                global dataE
                dataE = {"Sudut": [alfa],
                        "VFlashover":[VlompatApi],
                        "Xs (m)" : [Xs],
                        #"Smin (m)": [Smin],
                        "Smaks (m)": [Smaks],
                        "Imin Flashover (kA)":[Imin],
                        "Imaks SF (kA)": [Imaks],
                        #"Pmin": [Pmin],
                        #"Pmax":[Pmax],
                        "Gangguan Petir (km-tahun)":[NSF],
                        "VSF (kV)":[VSF],
                        "status" : [huhuhu]
                        }
                return alfa, Isf, pgswexpand
            if ELEKTROGEOMETRI(B2,AD2, pgsw):
                C2 = round(Smaks, 2) #radius rolling sphere
            D2 = round(pow((C2/6.7), (1/0.8)), 2) #kemampuan min petir
            F2 = mencari_persen(D2) #kemampuan proteksi petir
            F22 = 100 - F2
            
            ArusKritis = round((pow(((C2 + 3)/6.7), (1/0.8))), 3)
            RSAK = round(6.7*(ArusKritis**0.8), 3)

            st.markdown("<h3 style='text-align: center; text-color:#31333f;'>UJI KEANDALAN PERISAIAN</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("Sudut Perisaian: ",B2, "derajat")
                st.write("Arus maks Kegagalan Perisaian: ",D2, "kA")
                st.write("- Radius Rolling Sphere: ",C2, "meter")
                st.write("Arus Kritis: ", ArusKritis, " kA")
                st.write("- Radius Rolling Sphere: ", RSAK, "meter")
                #st.write("Kemampuan Proteksi: ",F2, "%")
                st.image("zrsout22.png")
            with col2:
                fig = px.pie(values=[F22, F2], names=['tak terproteksi', 'terproteksi'],
                            title=f'Kemampuan Perisaian',
                            height=200, width=100)
                fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
                st.plotly_chart(fig, use_container_width=True)
                st.image("RS22.png")
            if B2 > 18:
                st.error("PERISAIAN TIDAK ANDAL")
      
            if B2 > 18:
                if st.form_submit_button("Optimasi Perisaian"):
                    #optimasi sudut perisaian
                    B3 = 15 #sudut lindung idel dari SPLN
                    E3 = round(fasa-pgsw-(fg*m.tan(m.radians(B3))), 2) #penambahan panjang
                    pgswSPLN = pgsw + E3
                    if ELEKTROGEOMETRI(B3,AD2, pgswSPLN):
                    #C3 = round(htower/(1-m.sin(m.radians(B3))), 2) #radius rolling
                        C3 = round(Smaks, 2) #radius rolling
                    D3 = round(pow((C3/6.7), (1/0.8)), 2) #kemampuan min arus petir
                    RSAKPLN = round((C3+3), 3)
                    ArusKritisPLN = round((pow(((C3 + 3)/6.7), (1/0.8))), 3)

                    RataRataGangguan = float(meanpetir) #arus petir
                    RGangguan = round((6.7*(pow(RataRataGangguan, 0.8))), 2)
                    SudutLindungUji = round(m.degrees(m.asin(1-(htower/RGangguan))), 2) #hitung sudut lindung terhadap petir
                    print(SudutLindungUji, "SUUDTT")
                    if SudutLindungUji < 0:
                        B5 = 0
                    else:
                        B5 = SudutLindungUji
                    
                    E5 = round(fasa-pgsw-(fg*m.tan(m.radians(B5))), 2) #penambahan panjang GSW
                    pgswUJI = pgsw + E5
                    if ELEKTROGEOMETRI(B5,AD2, pgswUJI):    
                        RB5 = Smaks #radius rolling    
                    D5 = round(pow((RB5/6.7), (1/0.8)), 2) #kemampuan min arus petir
                    #C5 = RGangguan
                    C5 = round((6.7*(pow(D5, 0.8))), 2)
                    RSAKUji = round((C5+3), 3)
                    ArusKritisUji = round((pow(((RSAKUji)/6.7), (1/0.8))), 3)

                    F3 = mencari_persen(D3) #kemampuan proteksi ideal
                    F5 = mencari_persen(D5) #kemampuan proteksi trhdp petir
                   
                    
                    st.markdown("<h3 style='text-align: center; text-color:#31333f;'>OPTIMASI PERISAIAN</h3>", unsafe_allow_html=True)
                    colA, colB = st.columns(2)
                    with colA:
                        f35 = 100-F3
                        fig = px.pie(values=[f35, F3], names=['tak terproteksi', 'SPLN'],
                                    title=f'Kemampuan Perisaian',
                                    height=200, width=100)
                        fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
                        st.plotly_chart(fig, use_container_width=True)

                        st.markdown("**STANDAR IDEAL PT. PLN**")
                        st.write("Sudut Perisai\t =",B3, "derajat")
                        st.write("Arus Maks Kegagalan Perisai\t =",D3, "kA")
                        st.write("- Radius RS ImaksSF\t =", C3, "meter")
                        st.write("Arus Kritis\t =",ArusKritisPLN, "kA", )
                        st.write("- Radius RS Ic\t =", RSAKPLN, "meter")
                        st.write("Pertambahan Panjang\t\t =",E3, "meter")
                        #st.write("Kemampuan Proteksi\t :",F3, "%")
                        st.image("RS15.png")
                
                    with colB:
                        f36 = 100-F5
                        gambar = px.pie(values=[f36, F5], names=['tak terproteksi', 'uji coba'],
                                    title=f'Kemampuan Perisaian',
                                    height=200, width=100)
                        gambar.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
                        st.plotly_chart(gambar, use_container_width=True)

                        st.markdown("**UJI COBA BERDASARKAN PETIR**")
                        st.write("Arus Petir\t\t\t =", RataRataGangguan, "kA (Radius", RGangguan, "m)")
                        st.write("Sudut Perisai\t\t\t =",B5, "derajat")
                        st.write("- Radius Rolling Sphere\t =", C5, "meter")
                        st.write("Arus Kritis\t =",ArusKritisUji, "kA", )
                        st.write("- Radius RS Ic\t =", RSAKUji, "meter")
                        st.write("Pertambahan Panjang GSW\t =", E5, " m")
                        #st.write("Kemampuan Proteksi\t =",F5, "%")
                        st.image("RS0.png")
                    st.markdown("---")    
                    st.markdown("<h3 style='text-color:#31333f;'>Rincian</h3>", unsafe_allow_html=True)
                    def warnain(x):
                        if x > BIL:
                            color = 'red'
                        else:
                            color = 'blue'
                        return f'background: {color}'
                    
                    
                    if ELEKTROGEOMETRI(B2,D2, pgsw):
                        df1 = pd.DataFrame(dataE, index = ["Existing"])
                    if ELEKTROGEOMETRI(B3,D3, pgswSPLN):
                        df2 = pd.DataFrame(dataE, index =["SPLN"])
                    if ELEKTROGEOMETRI(B5,D5, pgswUJI):
                        df3 = pd.DataFrame(dataE, index =["Uji Coba"])
                    dataEL = pd.concat([df1,df2,df3])
                    dataEL.style.applymap(warnain,subset=['VSF (kV)'])
                    st.table(dataEL) 
            else:
                st.markdown("<h3 style='text-color:#31333f;'>Teori Elektrogeometri</h3>", unsafe_allow_html=True)
                AD2 = round(pow((hfasa/6.7), (1/0.8)), 2)
                if ELEKTROGEOMETRI(B2,AD2):
                    df1 = pd.DataFrame(dataE, index = ["existing"])
                st.table(df1) 
                st.success("PERISAIAN ANDAL")

if selected == "Simulasi Sambaran":
    with st.form("Towerdata"):
        st.markdown("<h1 style='text-align: center;'>SIMULASI SAMBARAN</h1>", unsafe_allow_html=True)
        st.markdown("---")
        SimulasiSambaran = st.selectbox("Tentukan Simulasi!", options=("Sambaran Langsung Pada Menara", "Sambaran langsung Pada Kawat Tanah"))
        st.subheader("Data Tower")
        col1,col2=st.columns(2)
        Vs = col1.number_input("Tegangan Sistem (kV)")#tegangan sistem sutt
        ht = col2.number_input("Tinggi Tower (m)") #tinggi gsw
        LebarTraversGSW = st.number_input("Panjang Antar Travers GSW (m)")
        col8,col9=st.columns(2)
        rtowerhi = col8.number_input("Lebar Kaki-kaki Tower (m)") #panjang kakiAkeB
        rtower = rtowerhi/2
        Ro = col9.number_input("Tahanan Kaki Tower (ohm)") #tahanan kaki menara tipikal
        col14,col15=st.columns(2)
        DiameterKawatTanah = col14.number_input("Diameter GSW (mm)")
        rKawatTanah = (DiameterKawatTanah/2)/1000 # gsw 55mm2
        BIL = col15.number_input("BIL Isolator (kV)")
        #st.markdown("---")
        st.subheader("Data Petir")
        col11,col12=st.columns(2)
        Ipuncak = col11.number_input("Arus Puncak Petir (kA)") #asumsi arus puncak petir 40 kA
        IcuramPetir = col12.number_input("Arus Curam Petir (kA/µs)")
        SimulasiBerjalan=st.form_submit_button("Submit!")

        if SimulasiBerjalan:
            #Impedansi
            Ztower = round(30*m.log((2*(ht**2 + rtower**2))/(rtower**2)), 2)
            print(Ztower)
            Zg = 60*m.log((2*ht)/m.sqrt(LebarTraversGSW*rKawatTanah))
            print(Zg)

            if SimulasiSambaran == "Sambaran Langsung Pada Menara":
                ZgAksen = 2*Zg*Ztower/(Zg+(2*Ztower))
                RoAksen = Ro*Ztower/(Ztower-Ro)

                #impedansi gelombang menara
                Zw = ((2*Zg**2*Ztower)/((Zg+2*Ztower)**2))*((Ztower-Ro)/(Ztower+Ro))

                #faktor damping menara
                psi = ((2*Ztower-Zg)/(2*Ztower+Zg))*((Ztower-Ro)/(Ztower+Ro))

                #Waktu tempuh gelombang petir di menara
                tPetir = ht/300 #kecepatan cahaya 300m/mikrodet

                #nilai induktansi menara
                Ltower = round(((ZgAksen+2*RoAksen)/ZgAksen)*((2*Zw*tPetir)/(1-psi)), 2)

                # tegangan yang akan timbul pada puncak menara
                VPuncakTower = Ipuncak*Ztower

                #besarnya tegangan pada titik percabangan
                Zek = 1/((1/Zg)+(1/Zg)+(1/Zg)+(1/Zg)+(1/Ztower)) #perhitungan tahanan paralel
                Uk = VPuncakTower*(1+((Zek-Ztower)/(Zek+Ztower)))

                #Nilai arus yang mengalir pada menara
                Itower = round(Uk/Ztower, 2)

                #tegangan yang akan timbul pada menara 
                Vtf = (Itower*Ro)+(Ltower*IcuramPetir)+(Vs*m.sqrt(2)/m.sqrt(3))

                st.markdown("---")
                st.subheader("SIMULASI SAMBARAN LANGSUNG PADA MENARA")
                st.write("- Impedansi Surja Menara (Ω): ", Ztower)
                st.write("- Impedansi Kawat tanah (Ω): ", Zg)
                st.write("- Impedansi Gelombang menara (Ω):", Zw)
                st.write("- Faktor Damping Menara: ", psi)
                st.write("- Waktu tempuh gelombang petir menara (µdet): ", tPetir)
                st.write("- Nilai Induktansi Menara (µH): ", Ltower)
                st.write("- tegangan yang akan timbul pada puncak menara(kV): ", VPuncakTower)
                st.write("- besarnya tegangan pada titik percabangan (kV): ", Uk)
                st.write("- Niilai arus yang mengalir pada menara(kA): ", Itower)
                st.write("- Tegangan Yang Timbul pada menara(kV): ", Vtf)
                if Vtf > BIL:
                    st.error(f"BACKFLASOVER!!!"+ "-->"+"VTF: "+str(Vtf)+ " > BIL: "+ str(BIL))
                else:
                    st.success(F"Tidak Terjadi BACKFLASHOVER")
                #GRAFIK SIMULASI
                def BasicInsulationLevel(BOL):
                    x = np.arange(0,100,0.1)
                    y = BOL-x*0
                    return x,y
                # 1. Membuat data
                def BackFlashover():
                    xp = np.arange(0,100,1)
                    VPuncakTower = xp*Ztower
                    Uk = VPuncakTower*(1+((Zek-Ztower)/(Zek+Ztower)))
                    Itower = Uk/Ztower
                    yp = (Itower*Ro)+(Ltower*IcuramPetir)+(Vs*m.sqrt(2)/m.sqrt(3))
                    return xp,yp

                def InduktansiMenara():
                    Induktansi = np.arange(0,100,1)
                    VtfInduk = (Itower*Ro)+(Induktansi*IcuramPetir)+(Vs*m.sqrt(2)/m.sqrt(3))
                    return Induktansi, VtfInduk
                
                def TahananKaki(IpuncakM):
                    RoT = np.arange(0, 25, 5)
                    ZgAksen = 2*Zg*Ztower/(Zg+(2*Ztower))
                    RoAksen = RoT*Ztower/(Ztower-RoT)
                    Zw = ((2*Zg**2*Ztower)/((Zg+2*Ztower)**2))*((Ztower-RoT)/(Ztower+RoT)) #impedansi gelombang menara
                    psi = ((2*Ztower-Zg)/(2*Ztower+Zg))*((Ztower-RoT)/(Ztower+RoT)) #faktor damping menara
                    tPetir = ht/300 #kecepatan cahaya 300m/mikrodet
                    Ltower = ((ZgAksen+2*RoAksen)/ZgAksen)*((2*Zw*tPetir)/(1-psi))
                    VPuncakTower = IpuncakM*Ztower  # tegangan yang akan timbul pada puncak menara
                    Zek = 1/((1/Zg)+(1/Zg)+(1/Zg)+(1/Zg)+(1/Ztower)) #perhitungan tahanan paralel #besarnya tegangan pada titik percabangan
                    Uk = VPuncakTower*(1+((Zek-Ztower)/(Zek+Ztower)))
                    Itower = Uk/Ztower #Nilai arus yang mengalir pada menara
                    VtfTahanan = (Itower*RoT)+(Ltower*IcuramPetir)+(Vs*m.sqrt(2)/m.sqrt(3)) #tegangan yang akan timbul pada menara 
                    return RoT, VtfTahanan
            
                # 2. Membuat plot
                x1,y1 = BasicInsulationLevel(BIL)
                xp1,yp2 = BackFlashover()

                Uk = Ztower*((BIL-(Ltower*IcuramPetir)-(Vs*m.sqrt(2)/m.sqrt(3)))/Ro)
                VPuncakTower = Uk/(1+((Zek-Ztower)/(Zek+Ztower)))
                a1 = round((VPuncakTower/Ztower), 3)
                # 3. Menampilkan plot
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=xp1,y=yp2, name="Pengaruh Petir", text=xp1, mode='lines+text', textposition='top left'))
                fig.add_trace(go.Scatter(x=x1, y=y1, name="Batas BIL", mode='lines', line = dict(color='firebrick')))
                fig.update_layout(
                    title={'text':"Grafik Pengaruh Sambaran Petir Terhadap Tegangan Pada Menara",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    },
                    title_font_family="Times New Roman",
                    xaxis_title="Arus Petir (kA)",
                    yaxis_title="Tegangan Pada menara (kV)",
                    font=dict(
                        family="Times New Roman",
                    )
                )
                st.plotly_chart(fig, use_container_width=True)

                #Simulasi Induktansi
                x1,y1 = BasicInsulationLevel(BIL)
                Induktansi, VtfInduk = InduktansiMenara()
                figInduktansi = go.Figure()
                figInduktansi.add_trace(go.Scatter(x=Induktansi,y=VtfInduk, name="Pengaruh Induktansi", text=Induktansi, mode='lines+text', textposition='top left'))
                figInduktansi.add_trace(go.Scatter(x=x1, y=y1, name="Batas BIL", mode='lines', line = dict(color='firebrick')))
                figInduktansi.update_layout(
                    title={'text':"Grafik Pengaruh induktansi menara Terhadap Tegangan Pada Menara",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    },
                    title_font_family="Times New Roman",
                    xaxis_title="Induktansi Menara (µH)",
                    yaxis_title="Tegangan Pada menara (kV)",
                    font=dict(
                        family="Times New Roman"
                    )
                )
                st.plotly_chart(figInduktansi, use_container_width=True)

                #Simulasi Tahanan Kaki
                def BasicInsulationLevelt(BOL):
                    xt = np.arange(-20,45,0.1)
                    yt = BOL-xt*0
                    return xt,yt
                xt,yt = BasicInsulationLevelt(BIL)
                figTahanan = go.Figure()
                RoT, VtfTahanan = TahananKaki(Ipuncak)
                figTahanan.add_trace(go.Scatter(x=RoT,y=VtfTahanan, name="Pengaruh Tahanan Kaki", text=RoT, mode='lines+text', textposition='top left'))
                figTahanan.update_layout(
                    title={'text':"Grafik Pengaruh Tahanan kaki menara Terhadap Tegangan Pada Menara",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    },
                    title_font_family="Times New Roman",
                    xaxis_title="Tahanan Pembumian Kaki Menara (Ω)",
                    yaxis_title="Tegangan Pada menara (kV)",
                    font=dict(
                        family="Times New Roman"
                    )
                )
                st.plotly_chart(figTahanan, use_container_width=True)

            elif SimulasiSambaran == "Sambaran langsung Pada Kawat Tanah":
                #Tegangan yang Terjadi pada Menara Akibat Sambaran pada Kawat Tanah 
                Ikebagi2 = Ipuncak/2
                Ug = Zg*Ikebagi2
                #Tegangan pada titik sambungan, K 
                ZekTanah = 1/((1/Zg)+(1/Zg)+(1/Zg)+(1/Ztower))
                UkTanah = Ug*(1+((ZekTanah-Zg)/(ZekTanah+Zg)))

                #Nilai arus yang mengalir pada tower
                ItowerTanah = UkTanah/Ztower

                ZgAksen = 2*Zg*Ztower/(Zg+(2*Ztower))
                RoAksen = Ro*Ztower/(Ztower-Ro)
                tPetir = ht/300 #kecepatan cahaya 300m/mikrodet
                psi = ((2*Ztower-Zg)/(2*Ztower+Zg))*((Ztower-Ro)/(Ztower+Ro))
                Zw = ((2*Zg**2*Ztower)/((Zg+2*Ztower)**2))*((Ztower-Ro)/(Ztower+Ro))
                Ltower = round(((ZgAksen+2*RoAksen)/ZgAksen)*((2*Zw*tPetir)/(1-psi)), 2)
                Ltower2 = round((((Zg+2*Ro)/Zg)**2)*((2*Zw*tPetir)/(1-psi)), 2)
                print(Ltower2, "Induksinihboss")
                VtfTanah = ItowerTanah*Ro+Ltower*IcuramPetir+(Vs*m.sqrt(2)/m.sqrt(3))
                
                st.subheader("SIMULASI SAMBARAN LANGSUNG PADA KAWAT TANAH")
                st.write("- Impedansi Surja Menara (Ω): ", Ztower)
                st.write("- Impedansi Kawat tanah (Ω): ", Zg)
                st.write("- Induktansi Menara (µH): ", Ltower)
                st.write("- Tegangan yang terjadi pada menara akibat sambaran pada gsw(kV):", Ug)
                st.write("- Impedansi pada titik sambung K (Ω): ", ZekTanah)
                st.write("- Tegangan Pada titik sambung K (Ω): ", UkTanah)
                st.write("- Arus Yang Mengalir pada tower (kA)", ItowerTanah)            
                st.write("- Tegangan Yang timbul pada menara (kV): ", VtfTanah)
                if VtfTanah > BIL:
                    st.error("BACKFLASOVER!!!")
                else:
                    st.success("Tidak Terjadi BFO")
                #GRAFIK SIMULASI SAMBARAN
                # 1. Membuat data
                def BasicInsulationLevel(BOL):
                    x = np.arange(0,100,0.1)
                    y = BOL-x*0
                    return x,y

                # 1. Membuat data
                def BackFlashover():
                    xp = np.arange(0,100,1)
                    Ikebagi2 = xp/2
                    Ug = Zg*Ikebagi2
                    ZekTanah = 1/((1/Zg)+(1/Zg)+(1/Zg)+(1/Ztower))
                    UkTanah = Ug*(1+((ZekTanah-Zg)/(ZekTanah+Zg)))
                    ItowerTanah = UkTanah/Ztower
                    tPetir = ht/300
                    psi = ((2*Ztower-Zg)/(2*Ztower+Zg))*((Ztower-Ro)/(Ztower+Ro))
                    Ltower = round(((ZgAksen+2*RoAksen)/ZgAksen)*((2*Zw*tPetir)/(1-psi)), 2)
                    yp = ItowerTanah*Ro+Ltower*IcuramPetir+(Vs*m.sqrt(2)/m.sqrt(3))
                    return xp,yp
                
                def InduktansiMenara():
                    Induktansi = np.arange(0,100,1)
                    VtfInduk = (ItowerTanah*Ro)+(Induktansi*IcuramPetir)+(Vs*m.sqrt(2)/m.sqrt(3))
                    return Induktansi, VtfInduk
                
                def TahananKakiMenara():
                    RoT = np.arange(0, 30, 5)
                    RoAksen = RoT*Ztower/(Ztower-RoT)
                    tPetir = ht/300 #kecepatan cahaya 300m/mikrodet
                    psi = ((2*Ztower-Zg)/(2*Ztower+Zg))*((Ztower-RoT)/(Ztower+RoT))
                    Zw = ((2*Zg**2*Ztower)/((Zg+2*Ztower)**2))*((Ztower-RoT)/(Ztower+RoT))
                    Ltower = ((ZgAksen+2*RoAksen)/ZgAksen)*((2*Zw*tPetir)/(1-psi))
                    VtfTanahTahanan = ItowerTanah*RoT+Ltower*IcuramPetir+(Vs*m.sqrt(2)/m.sqrt(3))
                    return RoT, VtfTanahTahanan

                # 2. Membuat plot
                x1,y1 = BasicInsulationLevel(BIL)
                xp1,yp2 = BackFlashover()
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=xp1,y=yp2, name="Pengaruh Petir", text=xp1,mode='lines+text', textposition='top left'))
                fig.add_trace(go.Scatter(x=x1, y=y1, name="Batas BIL", mode='lines', line = dict(color='firebrick')))
                fig.update_layout(
                    title={'text':"Grafik Pengaruh Sambaran Petir Terhadap Tegangan Pada Menara",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top'
                    },
                    title_font_family="Times New Roman",
                    xaxis_title="Arus Petir (kA)",
                    yaxis_title="Tegangan Pada menara (kV)",
                    font=dict(
                        family="Times New Roman",
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
                
                x1,y1 = BasicInsulationLevel(BIL)
                Induktansi, VtfInduk = InduktansiMenara()
                figInduktansi = go.Figure()
                figInduktansi.add_trace(go.Scatter(x=Induktansi,y=VtfInduk, name="Pengaruh Induktansi", text=Induktansi, mode='lines+text', textposition='top left'))
                figInduktansi.add_trace(go.Scatter(x=x1, y=y1, name="Batas BIL", mode='lines', line = dict(color='firebrick')))
                figInduktansi.update_layout(
                    title={'text':"Grafik Pengaruh induktansi menara Terhadap Tegangan Pada Menara",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    },
                    title_font_family="Times New Roman",
                    xaxis_title="Induktansi Menara (µH)",
                    yaxis_title="Tegangan Pada menara (kV)",
                    font=dict(
                        family="Times New Roman"
                    )
                )
                st.plotly_chart(figInduktansi, use_container_width=True)

                def BasicInsulationLevelt(BOL):
                    xt = np.arange(-20,45,0.1)
                    yt = BOL-xt*0
                    return xt,yt
                xt,yt = BasicInsulationLevelt(BIL)
                RoT, VtfTanahTahanan = TahananKakiMenara()
                figTahanan = go.Figure()
                figTahanan.add_trace(go.Scatter(x=RoT,y=VtfTanahTahanan, name="Pengaruh Tahanan Kaki", text=RoT, mode='lines+text', textposition='top left',))
                figTahanan.add_trace(go.Scatter(x=xt, y=yt, name="Batas BIL", mode='lines', line = dict(color='firebrick')))
                figTahanan.update_layout(
                    title={'text':"Grafik Pengaruh Tahanan kaki menara Terhadap Tegangan Pada Menara",
                    'y':0.9,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    },
                    title_font_family="Times New Roman",
                    xaxis_title="Tahanan Pembumian Kaki Menara (Ω)",
                    yaxis_title="Tegangan Pada menara (kV)",
                    font=dict(
                        family="Times New Roman"
                    )
                )
                st.plotly_chart(figTahanan, use_container_width=True)
if selected == "Kontak":
    @st.cache_data
    def get_img_as_base64(file):
        with open(file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    img = get_img_as_base64("BLprofil.jpg")
    PP = get_img_as_base64("poto.png")

    page_bg_img = f"""
    <style>
    [data-testid="stMarkdownContainer"]
    {{
    align: center;
    }}
    [data-testid="stButton"]
    {{
    width: 250px;
    }}
    button.css-kmfd61 edgvbvh10{{
    width : 50%;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
    header_html = "<img src='data:image/png;base64,{}' class='img-fluid' style='text-align: center;border-radius: 50%;padding: 1px;display: block;margin-right:auto;margin-left: auto;width: 40%;box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);'>".format(get_img_as_base64("poto.png"))
    st.markdown(header_html, unsafe_allow_html=True,)

    st.markdown("<h1 style='text-align: center; text-color:#31333f;font-family: 'Times New Roman', Times, serif;'>TEGAR ACHMAD YUSTIADI</h1>", unsafe_allow_html=True)
    st.info('Electrical Engineering, Data Scientist, Data Analyst, Power System Analyst, Autodesk Autocad Drafter, Graphic Designer and trying to be a proud child')
    st.markdown("---")
    KLM1, KLM2, KLM3 = st.columns(3)
    with KLM1:
        mention(label="Linkedin",icon= "🇱", url="https://id.linkedin.com/in/tegar-achmad-yustiadi-7b05bb274")
    with KLM2:
        mention(label="INSTAGRAM",icon= "📷", url="https://instagram.com/tegar_achmad23?igshid=MzNlNGNkZWQ4Mg==")
    with KLM3:
        mention(label="GITHUB",icon= "github", url="https://github.com/TegarAchmad")

    
