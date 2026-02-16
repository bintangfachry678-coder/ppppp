import streamlit as st
import assemblyai as aai
import os

st.set_page_config(page_title="AI Subtitle Generator", page_icon="🎬")
st.title("🎬 Bikin Subtitle Otomatis")

# Input API Key AssemblyAI
api_key = st.text_input("Masukkan API Key AssemblyAI Lo:", type="password")
uploaded_file = st.file_uploader("Upload Video (mp4, mov)", type=["mp4", "mov"])

if st.button("Proses Subtitle") and uploaded_file and api_key:
    aai.settings.api_key = api_key
    st.info("Lagi diproses AI, sabar ya Bro. Jangan di-refresh...")
    
    # Simpan file sementara
    with open("temp_video.mp4", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    try:
        # Konfigurasi AI untuk Bahasa Indonesia
        config = aai.TranscriptionConfig(
            speech_models=["universal-3-pro", "universal-2"], 
            language_code="id"
        )
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe("temp_video.mp4", config=config)
        
        if transcript.status == aai.TranscriptStatus.error:
            st.error(f"Error AI: {transcript.error}")
        else:
            # Export ke format SRT
            srt_data = transcript.export_subtitles_srt(chars_per_caption=30)
            st.success("✅ Mantap! Subtitle selesai.")
            st.download_button(
                label="⬇️ DOWNLOAD FILE .SRT",
                data=srt_data,
                file_name="hasil_subtitle.srt",
                mime="text/plain"
            )
    except Exception as e:
        st.error(f"Waduh ada error: {e}")
    finally:
        # Hapus file sampah biar hemat tempat
        if os.path.exists("temp_video.mp4"):
            os.remove("temp_video.mp4")
elif not api_key or not uploaded_file:
    st.warning("Jangan lupa masukin API Key dan videonya ya.")
