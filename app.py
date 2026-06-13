import streamlit as st
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os

st.set_page_config(page_title="Love Letter Decoder 💖", page_icon="💌", layout="centered")

st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #f30477 !important;
        color: #ffdff2 !important;
        border: 2px solid #f30477 !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        width: 100%;
        height: 55px;
        font-size: 20px;
    }
    div.stButton > button:first-child:hover { background-color: #ffdff2 !important; color: #f30477 !important; }
    h1, h3 { text-align: center; font-family: sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='color: #f30477;'>🔒 Decrypted Love Vault</h1>", unsafe_allow_html=True)

status_message = st.empty()
image_placeholder = st.empty()
download_placeholder = st.empty()

if "balloon_fired" not in st.session_state:
    st.session_state.balloon_fired = False

# Read url parameters directly from browser address bar
query_params = st.query_params

if "note" in query_params:
    try:
        user_name = query_params.get("name", "Babe")
        user_email = query_params.get("email", "Not Provided")
        user_place = query_params.get("place", "Not Provided")
        secret_note = query_params.get("note", "").strip()

        if secret_note:
            status_message.markdown("<h3 style='color: #f30477;'>✨ Card Decoded Successfully! ✨</h3>", unsafe_allow_html=True)
            
            if os.path.exists("temp.png"):
                card_img = Image.open("temp.png").convert("RGBA")
            else:
                card_img = Image.new("RGBA", (1080, 1080), "#fff0f7")
            
            draw = ImageDraw.Draw(card_img)
            draw.text((540, 200), "💖 Our Anniversary Note 💖", fill="#f30477", anchor="mt")

            left_margin = 100
            max_content_width = 1080 - left_margin - 100 
            y_position = 290 
            line_height = 42

            words = secret_note.split(' ')
            lines = []
            current_line = ""

            for word in words:
                if len(current_line + word) * 13 < max_content_width:
                    current_line += word + " "
                else:
                    lines.append(current_line.strip())
                    current_line = word + " "
            lines.append(current_line.strip())

            for line_idx, line_text in enumerate(lines):
                is_last_line = (line_idx == len(lines) - 1)
                line_words = line_text.split(' ')

                if is_last_line or len(line_words) == 1:
                    draw.text((540, y_position), line_text, fill="#5c002a", anchor="ma")
                else:
                    total_chars_length = sum(len(w) for w in line_words)
                    approx_words_width = total_chars_length * 13 
                    total_spaces_needed = len(line_words) - 1
                    empty_space_pixels_remaining = max_content_width - approx_words_width
                    
                    if approx_words_width > max_content_width:
                         draw.text((540, y_position), line_text, fill="#5c002a", anchor="ma")
                    else:
                        current_x = left_margin
                        space_pixel_width = empty_space_pixels_remaining / total_spaces_needed
                        for word_text in line_words:
                            draw.text((current_x, y_position), word_text, fill="#5c002a")
                            current_x += (len(word_text) * 13) + space_pixel_width
                            
                y_position += line_height

            draw.text((540, y_position + 60), f"👤 Name: {user_name}", fill="#f30477", anchor="mm")
            draw.text((540, y_position + 98), f"📩 Email: {user_email}", fill="#f30477", anchor="mm")
            draw.text((540, y_position + 136), f"📍 Place: {user_place}", fill="#f30477", anchor="mm")

            image_placeholder.image(card_img, use_container_width=True)

            buffered_io = BytesIO()
            card_img.save(buffered_io, format="PNG")
            
            download_placeholder.download_button(
                label="Download Card Photo 🖼️",
                data=buffered_io.getvalue(),
                file_name="our_anniversary_love_card.png",
                mime="image/png"
            )
            
            if not st.session_state.balloon_fired:
                st.session_state.balloon_fired = True
                st.balloons()

    except Exception as e:
        status_message.error(f"Error compiling canvas layers: {e}")
else:
    st.info("👋 Security Vault Active... Type a note on your grid website to reveal the card! 💓")
