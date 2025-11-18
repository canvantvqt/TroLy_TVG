import streamlit as st
import json
import base64

st.set_page_config(page_title="Trưng Vương Garden - Voice Assistant", layout="centered")

st.markdown("<h2 style='text-align:center;'>CHÀO MỪNG BẠN ĐẾN TRƯNG VƯƠNG GARDEN</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>TRỢ LÝ A.I BẰNG GIỌNG NÓI TVG</h4>", unsafe_allow_html=True)

# -----------------------------------------------------
# FAQ PROCESSING (Python ok)
# -----------------------------------------------------
def find_answer(user_text):
    try:
        with open("faq_garden.json", encoding="utf-8") as f:
            faq_data = json.load(f)
    except:
        return "Xin lỗi, hiện tại tôi không thể truy cập dữ liệu tư vấn."

    for item in faq_data.get("faq", []):
        for keyword in item.get("question", []):
            if keyword.lower() in user_text.lower():
                return item.get("answer", "")

    return "Xin lỗi, tôi chưa hiểu câu hỏi của bạn."

# -----------------------------------------------------
# AUDIO PLAYER (for intro.mp3)
# -----------------------------------------------------
def play_audio_file(file_path):
    audio_data = open(file_path, "rb").read()
    b64 = base64.b64encode(audio_data).decode()

    st.markdown(f"""
        <audio autoplay controls>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
    """, unsafe_allow_html=True)

# -----------------------------------------------------
# UI LAYOUT
# -----------------------------------------------------
col1, col2, col3 = st.columns([1,1,1])

# BUTTON 1: PLAY INTRO
with col1:
    if st.button("▶️ Phát lời chào"):
        play_audio_file("intro.mp3")

# BUTTON 2: RECORD (Browser Mic)
with col2:
    st.write("🎤 Bấm để hỏi (giọng nói)")

    st.markdown("""
        <button id="recBtn" style="
            width:100%; padding:10px;
            background:#2d6cdf; color:white;
            border:none; border-radius:6px;
            font-size:18px; cursor:pointer;">
            🎤 Ghi âm câu hỏi
        </button>

        <p id="result" style="margin-top:10px; font-size:17px; color:green;"></p>

        <script>
        const btn = document.getElementById("recBtn");
        const result = document.getElementById("result");

        btn.onclick = () => {
            const rec = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
            rec.lang = "vi-VN";
            rec.start();

            btn.innerHTML = "⏳ Đang nghe...";

            rec.onresult = (e) => {
                let text = e.results[0][0].transcript;
                result.innerHTML = "Bạn nói: " + text;

                // Gửi về Python
                fetch("/?q=" + encodeURIComponent(text));
            };

            rec.onerror = () => {
                btn.innerHTML = "🎤 Thử lại";
            };

            rec.onend = () => {
                btn.innerHTML = "🎤 Ghi âm câu hỏi";
            };
        };
        </script>
    """, unsafe_allow_html=True)

# BUTTON 3: END
with col3:
    if st.button("⏹ Kết thúc"):
        st.success("Cảm ơn bạn đã sử dụng Trợ lý Trưng Vương Garden!")

        st.markdown("""
            <script>
            let msg = new SpeechSynthesisUtterance("Cảm ơn bạn đã sử dụng trợ lý Trưng Vương Garden. Hẹn gặp lại bạn!");
            msg.lang = "vi-VN";
            speechSynthesis.speak(msg);
            </script>
        """, unsafe_allow_html=True)

# -----------------------------------------------------
# HANDLE SPEECH RESULT
# -----------------------------------------------------
query = st.query_params.get("q", None)

if query:
    st.info(f"Bạn nói: {query}")
    answer = find_answer(query)
    st.success(f"Trợ lý trả lời: {answer}")

    # Speak answer (TTS)
    st.markdown(f"""
        <script>
        let msg2 = new SpeechSynthesisUtterance("{answer}");
        msg2.lang = "vi-VN";
        speechSynthesis.speak(msg2);
        </script>
    """, unsafe_allow_html=True)
