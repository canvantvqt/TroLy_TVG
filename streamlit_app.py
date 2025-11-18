<<<<<<< HEAD
# -*- coding: utf-8 -*-
import streamlit as st
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment
import json
import base64

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

# ---- Load FAQ JSON ----
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

# ---- Phát lời chào bằng HTML5 audio (miễn phí, trình duyệt) ----
def play_audio_file(file_path):
    audio_file = open(file_path, "rb").read()
    b64_audio = base64.b64encode(audio_file).decode()
    audio_html = f"""
        <audio autoplay="true" controls>
        <source src="data:audio/mp3;base64,{b64_audio}" type="audio/mp3">
        Your browser does not support the audio element.
        </audio>
    """
    st.markdown(audio_html, unsafe_allow_html=True)

# ---- STT từ file audio ----
def transcribe_audio(uploaded_file):
    if uploaded_file is None:
        return None
    # Chuyển audio về WAV nếu cần
    file_bytes = uploaded_file.read()
    audio = AudioSegment.from_file(BytesIO(file_bytes))
    wav_io = BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)
    
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_io) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='vi-VN')
            return text
        except sr.UnknownValueError:
            return "Tôi không nghe rõ, bạn vui lòng nói lại nhé!"
        except sr.RequestError:
            return "Hiện tại không thể kết nối dịch vụ STT."

# ---- MAIN UI ----
col1, col2, col3 = st.columns([1,1,1])

# State
if 'stop' not in st.session_state:
    st.session_state.stop = False

with col1:
    if st.button("▶️ Phát lời chào"):
        # intro.mp3 phải có trong repo
        play_audio_file("intro.mp3")

with col2:
    uploaded_audio = st.file_uploader("🎤 Bấm để hỏi", type=["wav", "mp3", "m4a", "webm"])
    if uploaded_audio is not None:
        user_text = transcribe_audio(uploaded_audio)
        st.info(f"Bạn nói: {user_text}")
        answer_text = find_answer(user_text)
        st.success(f"Trợ lý trả lời: {answer_text}")
        # Phát bằng TTS trình duyệt
        tts_file = "temp_answer.mp3"
        from gtts import gTTS
        tts = gTTS(text=answer_text, lang="vi")
        tts.save(tts_file)
        play_audio_file(tts_file)

with col3:
    if st.button("⏹ Kết thúc"):
        farewell_text = "Cảm ơn bạn đã sử dụng Trợ lý Trưng Vương Garden. Chào tạm biệt!"
        st.success(farewell_text)
        tts = gTTS(text=farewell_text, lang="vi")
        tts.save("farewell.mp3")
        play_audio_file("farewell.mp3")
        st.session_state.stop = True

st.markdown("<p style='text-align:center; color: gray;'>Sản phẩm do nhóm học sinh CLB Lập trình lớp 7C</p>", unsafe_allow_html=True)
=======
# -*- coding: utf-8 -*-
import streamlit as st
import speech_recognition as sr
from io import BytesIO
from pydub import AudioSegment
import json, base64, os
from gtts import gTTS

st.set_page_config(page_title="Trưng Vương Garden - Voice Assistant", layout="centered")

st.markdown("<h2 style='text-align:center;'>CHÀO MỪNG BẠN ĐẾN TRƯNG VƯƠNG GARDEN</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>TRỢ LÝ A.I GIỌNG NÓI</h4>", unsafe_allow_html=True)

st.write("""
**Hướng dẫn:**
1) Nhấn **Phát lời chào**
2) Nhấn **🎤 Bấm để ghi âm**
3) Trợ lý tự trả lời bằng âm thanh
4) Nhấn **Kết thúc**
""")

# ====== LOAD FAQ ======
def find_answer(user_text):
    try:
        with open("faq_garden.json", encoding="utf-8") as f:
            faq_data = json.load(f)
    except:
        return "Xin lỗi, tôi không thể truy cập dữ liệu tư vấn."

    for item in faq_data.get("faq", []):
        for kw in item.get("question", []):
            if kw.lower() in user_text.lower():
                return item.get("answer", "")
    return "Xin lỗi, tôi chưa hiểu câu hỏi của bạn."

# ====== PHÁT ÂM THANH ======
def play_audio_file(path):
    audio_bytes = open(path, "rb").read()
    b64 = base64.b64encode(audio_bytes).decode()
    st.markdown(
        f"""
        <audio autoplay controls>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True,
    )

# ====== STT ======
def transcribe(data):
    audio = AudioSegment.from_file(BytesIO(data))
    wav_io = BytesIO()
    audio.export(wav_io, format="wav")
    wav_io.seek(0)

    rec = sr.Recognizer()
    with sr.AudioFile(wav_io) as src:
        audio_data = rec.record(src)
        try:
            return rec.recognize_google(audio_data, language="vi-VN")
        except:
            return "Tôi không nghe rõ, bạn nói lại nhé."

# ====== GIAO DIỆN 3 CỘT ======
col1, col2, col3 = st.columns([1,2,1])

# ====== BUTTON 1 ======
with col1:
    if st.button("▶️ Phát lời chào"):
        play_audio_file("intro.mp3")

# ====== BUTTON 2 — GHI ÂM MICRO ======
with col2:
    st.markdown("### 🎤 Bấm để ghi âm câu hỏi")

    audio_data = st.experimental_get_query_params().get("audio", [None])[0]

    # Nút ghi âm bằng Javascript
    st.markdown("""
    <button id="recBtn" style="padding:10px 20px; font-size:18px;">🎤 Bấm để hỏi</button>

    <script>
    let recBtn = document.getElementById('recBtn');
    let chunks = [];
    let recorder;

    recBtn.onclick = async function() {
        let stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        recorder = new MediaRecorder(stream);

        recorder.ondataavailable = e => chunks.push(e.data);

        recorder.onstop = async () => {
            let blob = new Blob(chunks, { type: 'audio/webm' });
            let reader = new FileReader();

            reader.onloadend = () => {
                let base64Audio = reader.result.split(',')[1];
                const query = new URLSearchParams(window.location.search);
                query.set("audio", base64Audio);
                window.location.search = query.toString();
            };

            reader.readAsDataURL(blob);
        };

        chunks = [];
        recorder.start();
        recBtn.innerText = "⏹ Dừng ghi";

        setTimeout(() => {
            recorder.stop();
            recBtn.innerText = "🎤 Bấm để hỏi";
        }, 3500); // Ghi 3.5 giây
    };
    </script>
    """, unsafe_allow_html=True)

    # Nếu có dữ liệu ghi âm
    if audio_data not in [None, ""]:
        audio_bytes = base64.b64decode(audio_data)
        user_text = transcribe(audio_bytes)
        st.info(f"Bạn nói: {user_text}")

        answer = find_answer(user_text)
        st.success(f"Trợ lý: {answer}")

        tts = gTTS(answer, lang="vi")
        tts.save("answer.mp3")
        play_audio_file("answer.mp3")

# ====== BUTTON 3 ======
with col3:
    if st.button("⏹ Kết thúc"):
        farewell = "Cảm ơn bạn đã trải nghiệm Trợ lý A.I của Trưng Vương Garden!"
        tts = gTTS(farewell, lang="vi")
        tts.save("farewell.mp3")
        st.success(farewell)
        play_audio_file("farewell.mp3")

st.markdown("<p style='text-align:center; color: gray;'>Sản phẩm CLB Lập trình 7C</p>", unsafe_allow_html=True)
>>>>>>> aeba1507bdfb064525c86015c84b5b1b37f0205d
