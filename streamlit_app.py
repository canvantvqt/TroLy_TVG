# -*- coding: utf-8 -*-
import streamlit as st
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment
import json
import base64
from gtts import gTTS
import time

# ======================
# PAGE SETUP
# ======================
st.set_page_config(page_title="Trưng Vương Garden - Voice Assistant", layout="centered")

st.markdown("<h2 style='text-align:center;'>CHÀO MỪNG BẠN ĐẾN TRƯNG VƯƠNG GARDEN</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>TRỢ LÝ A.I BẰNG GIỌNG NÓI TVG</h4>", unsafe_allow_html=True)

st.markdown("""
**Hướng dẫn ngắn:**  
1) Nhấn **Phát lời chào** để nghe giới thiệu.  
2) Nhấn **Bấm để hỏi**, ghi âm câu hỏi (upload file audio).  
3) Trợ lý trả lời bằng âm thanh.  
4) Nhấn **Kết thúc** để chào tạm biệt.  
""")


# ======================
# FAQ FINDER
# ======================
def find_answer(user_text):
    try:
        with open("faq_garden.json", encoding="utf-8") as f:
            faq_data = json.load(f)
    except Exception:
        return "Xin lỗi, hiện tại tôi không thể truy cập dữ liệu tư vấn."

    for item in faq_data.get("faq", []):
        for keyword in item.get("question", []):
            if keyword.lower() in user_text.lower():
                return item.get("answer", "")

    return ("Xin lỗi, tôi chưa hiểu câu hỏi của bạn. "
            "Bạn có thể hỏi về giờ mở cửa, giá vé, trải nghiệm, ẩm thực, khuyến mãi hoặc liên hệ.")


# ======================
# AUDIO PLAYER
# ======================
def play_audio_file(file_path):
    try:
        with open(file_path, "rb") as f:
            audio_data = f.read()

        b64 = base64.b64encode(audio_data).decode()
        audio_html = f"""
            <audio autoplay="true" controls>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except:
        st.error("Không phát được file âm thanh.")


# ======================
# SAFE TTS (no gTTSError)
# ======================
def safe_tts(text, file_path):
    for _ in range(3):    # thử 3 lần
        try:
            tts = gTTS(text=text, lang="vi")
            tts.save(file_path)
            return True
        except:
            time.sleep(1)
    return False


# ======================
# SPEECH RECOGNITION
# ======================
def transcribe_audio(uploaded_file):
    if uploaded_file is None:
        return None

    file_bytes = uploaded_file.read()

    try:
        audio = AudioSegment.from_file(BytesIO(file_bytes))
        audio = audio.set_frame_rate(16000).set_channels(1)
    except:
        return "Tôi không thể xử lý file âm thanh bạn tải lên."

    wav_io = BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(wav_io) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language='vi-VN')
            return text

    except sr.UnknownValueError:
        return "Tôi không nghe rõ, bạn vui lòng nói lại nhé!"
    except sr.RequestError:
        return "Không kết nối được dịch vụ nhận dạng giọng nói."


# ======================
# UI – 3 COLUMNS
# ======================
col1, col2, col3 = st.columns([1, 1, 1])

# STATE
if 'stop' not in st.session_state:
    st.session_state.stop = False

# ---- PLAY INTRO ----
with col1:
    if st.button("▶️ Phát lời chào"):
        play_audio_file("intro.mp3")

# ---- ASK ----
with col2:
    uploaded_audio = st.file_uploader("🎤 Bấm để hỏi", type=["wav", "mp3", "m4a", "webm"])

    if uploaded_audio is not None:
        user_text = transcribe_audio(uploaded_audio)
        st.info(f"Bạn nói: {user_text}")

        answer_text = find_answer(user_text)
        st.success(f"Trợ lý trả lời: {answer_text}")

        # TTS trả lời
        if safe_tts(answer_text, "answer.mp3"):
            play_audio_file("answer.mp3")
        else:
            st.error("Không tạo được âm thanh trả lời.")

# ---- END ----
with col3:
    if st.button("⏹ Kết thúc"):
        farewell_text = "Cảm ơn bạn đã sử dụng Trợ lý Trưng Vương Garden. Chào tạm biệt!"

        if safe_tts(farewell_text, "farewell.mp3"):
            play_audio_file("farewell.mp3")

        st.success(farewell_text)
        st.session_state.stop = True

st.markdown("<p style='text-align:center; color: gray;'>Sản phẩm do nhóm học sinh CLB Lập trình lớp 7C</p>", unsafe_allow_html=True)
