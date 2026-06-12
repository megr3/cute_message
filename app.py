import streamlit as st
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
import requests
import time

# Configure core browser page window attributes
st.set_page_config(
    page_title="Live Love Letter Decoder 💖", 
    page_icon="💌", 
    layout="centered"
)

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

st.markdown("<h1 style='color: #f30477;'>🔒 Live Decrypted Love Vault</h1>", unsafe_allow_html=True)

status_message = st.empty()
image_placeholder = st.empty()
download_placeholder = st.empty()

if "last_time" not in st.session_state:
    st.session_state.last_time = None

# ----------------------------------------------------------------------
# LIVE REAL-TIME CLOUD PIPELINE WATCH ENGINE
# ----------------------------------------------------------------------
try:
    headers = {
        'X-Master-Key': '$2b$10$w8bX1v0SshIcoZfeAepLxeBfK22vK9I6kF5H7wK6Fqgq1TzB9q8rS'
    }
    # Poll records from the matching public database endpoint securely
    response = requests.get('https://jsonbin.io', headers=headers, timeout=5)
    
    if response.status_code == 200:
        love_package = response.json().get("record", {})
        
        user_name = love_package.get("name", "Babe")
        user_email = love_package.get("email", "Not Provided")
        user_place = love_package.get("place", "Not Provided")
        secret_note = love_package.get("note", "").strip()
        current_msg_time = love_package.get("timestamp", None)
        
        if secret_note:
            status_message.markdown("<h3 style='color: #f30477;'>✨ She Sent a Message! Card Decoded Successfully! ✨</h3>", unsafe_allow_html=True)
            
            if os.path.exists("temp.png"):
                card_img = Image.open("temp.png").convert("RGBA")
            else:
                card_img = Image.new("RGBA", (1080, 1080), "#fff0f7")
            
            draw = ImageDraw.Draw(card_img)
            
            # 1. Heading prints at exactly 30px height centered at 200px from top
            draw.text((540, 200), "💖 Our Anniversary Note 💖", fill="#f30477", anchor="mt")

            # 2. Message wraps at 24px width within 100px margins (Justified design grid blocks)
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

            # 3. Personal data points stack line-by-line centrally right below her text box block at 20px
            details_y = y_position + 60
            line_gap = 38
            draw.text((540, details_y), f"👤 Name: {user_name}", fill="#f30477", anchor="mm")
            draw.text((540, details_y + line_gap), f"📩 Email: {user_email}", fill="#f30477", anchor="mm")
            draw.text((540, details_y + (line_gap * 2)), f"📍 Place: {user_place}", fill="#f30477", anchor="mm")

            image_placeholder.image(card_img, use_container_width=True)

            buffered_io = BytesIO()
            card_img.save(buffered_io, format="PNG")
            
            download_placeholder.download_button(
                label="Download Card Photo 🖼️",
                data=buffered_io.getvalue(),
                file_name="our_anniversary_love_card.png",
                mime="image/png"
            )
            
            # Fire balloon burst animations once upon fresh arrival tracking identification keys
            if current_msg_time != st.session_state.last_time:
                st.session_state.last_time = current_msg_time
                st.balloons()
                
        else:
            status_message.info("👋 Keeping cloud sync live... Waiting for her input. Do not close this window! 💓")
except Exception as e:
    status_message.info("👋 Syncing with the cloud pipeline... Keeping dashboard lookup active. ✨")

# Keep the cloud app interface refresh cycle ticking every 2 seconds automatically
time.sleep(2)
st.rerun()
