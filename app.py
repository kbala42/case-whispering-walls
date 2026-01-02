import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

def run():
    st.title("🎧 Vaka 2: Dijital Parazit (Sinyaller)")

    # --- BAĞLANTI KONTROLÜ ---
    if 'inventory_audio_file' not in st.session_state:
        st.error("⛔ ERİŞİM ENGELLENDİ: Önce Vaka 1'deki 'Sıfırıncı Hasta'yı bulup ses dosyasını ele geçirmelisin.")
        return 

    st.success(f"✅ Dosya Yüklendi: {st.session_state['inventory_audio_file']}")

    # --- HİKAYE MODU ---
    if 'math_mode_2' not in st.session_state:
        st.session_state['math_mode_2'] = False

    if not st.session_state['math_mode_2']:
        st.markdown("""
        **Görev:** Ele geçirdiğimiz ses dosyasında, Moriarty'nin saklandığı yerin koordinatları var. 
        Ama dosya "Beyaz Gürültü" ile örtülmüş. Gürültüyü silip o ince frekansı bulmalısın.
        """)
    else:
        st.markdown("""
        ### 📐 MATEMATİKSEL YÜZLEŞME
        **Konu:** Fourier Dönüşümü (Signal Processing)
        
        Mennan Usta'nın "Gürültüyü soyup içini görmek" dediği şey, **Discrete Fourier Transform (DFT)** işlemidir:
        $$ X_k = \\sum_{n=0}^{N-1} x_n e^{-i 2\\pi k n / N} $$
        """)

    # --- SİMÜLASYON ---
    noise_level = st.slider("Gürültü Filtresi (Noise Level)", 0.0, 5.0, 4.0)
    
    N = 600
    T = 1.0 / 800.0
    x = np.linspace(0.0, N*T, N, endpoint=False)
    y = np.sin(42.0 * 2.0 * np.pi * x) + np.random.normal(0, noise_level, N)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Kulak (Zaman Alanı)")
        fig1, ax1 = plt.subplots()
        ax1.plot(x, y)
        st.pyplot(fig1)

    with col2:
        st.subheader("Matematik (Frekans Alanı)")
        yf = fft(y)
        xf = fftfreq(N, T)[:N//2]
        amp = 2.0/N * np.abs(yf[0:N//2])
        
        fig2, ax2 = plt.subplots()
        ax2.plot(xf, amp, color='red')
        st.pyplot(fig2)
        
        peak_freq = xf[np.argmax(amp)]
        st.metric("Tespit Edilen Frekans", f"{peak_freq:.2f} Hz")
        
        if 40 < peak_freq < 44:
            st.success("ŞİFRE ÇÖZÜLDÜ!")
            st.markdown("### 📍 Koordinat: Vadi Tabanı (x = 0)")
            st.session_state['inventory_coordinates'] = 0.0
            st.toast("🎒 Envantere Eklendi: Hedef Koordinat (0.0)")

    st.divider()
    
    if st.button("🔴 Kırmızı Hap: Analojiyi Kır"):
        st.session_state['math_mode_2'] = not st.session_state['math_mode_2']
        st.rerun() # GÜNCELLENDİ

    with st.expander("🛠️ Kod Müdahalesi (Reality Check)"):
        st.write("**Soru:** Kodda `np.sin` fonksiyonundaki `42.0` değerini `100.0` yaparsan, kırmızı grafikteki 'diken' (peak) nereye kayar?")
        ans = st.radio("Cevap:", ["Sola (0'a yaklaşır)", "Sağa (İleri gider)", "Kaybolur"])
        if ans == "Sağa (İleri gider)":
            st.success("Doğru!")
        elif ans:
            st.error("Yanlış. Frekans artarsa grafik sağa gider.")

if __name__ == "__main__":
    run()