import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

def run():
    st.title("🎧 Vaka 2: Dijital Parazit")

    # Vaka 1 Kontrolü
    if 'inventory_audio_file' not in st.session_state:
        st.error("⛔ ERİŞİM ENGELLENDİ: Önce Vaka 1'i tamamla.")
        return 
    st.success("✅ Dosya Yüklendi.")

    if 'math_mode_2' not in st.session_state: st.session_state['math_mode_2'] = False
    
    if not st.session_state['math_mode_2']:
        st.markdown("**Görev:** Gürültülü sesteki gizli frekansı (Koordinatı) bul.")
    else:
        st.markdown(r"### 📐 FFT: Fourier Dönüşümü $$ X_k = \sum_{n=0}^{N-1} x_n e^{-i 2\pi k n / N} $$")

    noise_level = st.slider("Gürültü Filtresi", 0.0, 5.0, 4.0)
    
    N = 600; T = 1.0 / 800.0
    x = np.linspace(0.0, N*T, N, endpoint=False)
    y = np.sin(42.0 * 2.0 * np.pi * x) + np.random.normal(0, noise_level, N)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Zaman (Kulak)")
        fig, ax = plt.subplots(); ax.plot(x, y); st.pyplot(fig)
    with col2:
        st.subheader("Frekans (Matematik)")
        yf = fft(y); xf = fftfreq(N, T)[:N//2]
        amp = 2.0/N * np.abs(yf[0:N//2])
        fig, ax = plt.subplots(); ax.plot(xf, amp, 'r'); st.pyplot(fig)
        
        peak = xf[np.argmax(amp)]
        st.metric("Tespit Edilen", f"{peak:.2f} Hz")
        
        if 40 < peak < 44:
            st.success("ŞİFRE ÇÖZÜLDÜ! Koordinat: 0.0")
            st.session_state['inventory_coordinates'] = 0.0

    st.divider()
    if st.button("🔴 Kırmızı Hap"):
        st.session_state['math_mode_2'] = not st.session_state['math_mode_2']
        if hasattr(st, "rerun"): st.rerun() 
        else: st.experimental_rerun()

if __name__ == "__main__":
    run()