import streamlit as st
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import os
import json
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# Set up browser layout dashboard configurations
st.set_page_config(page_title="Live Love Letter Decoder 💖", page_icon="💌", layout="centered")

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

if "received_data" not in st.session_state:
    st.session_state.received_data = None
if "last_processed_time" not in st.session_state:
    st.session_state.last_processed_time = None

# ----------------------------------------------------------------------
# LIGHTWEIGHT NATIVE PYTHON BACKGROUND HTTP PORT RECEIVER SERVER
# ----------------------------------------------------------------------
class LocalNoteReceiver(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        if self.path == '/receive_note':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            # SYSTEM PARSING FIX: Decode the incoming form-url data dictionary cleanly into Python keys
            parsed_params = parse_qs(post_data)
            
            # Extract first indexed values from the dictionary array lists safely
            compiled_payload = {
                "name": parsed_params.get("name", ["Babe"])[0],
                "email": parsed_params.get("email", ["Not Provided"])[0],
                "place": parsed_params.get("place", ["Not Provided"])[0],
                "note": parsed_params.get("note", [""])[0],
                "timestamp": parsed_params.get("timestamp", [None])[0]
            }
            
            st.session_state.received_data = compiled_payload
            
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()

def launch_receiver_background_node():
    server_address = ('', 5000)
    try:
        httpd = HTTPServer(server_address, LocalNoteReceiver)
        httpd.serve_forever()
    except Exception as e:
        pass

if "receiver_thread_active" not in st.session_state:
    st.session_state.receiver_thread_active = True
    background_thread = threading.Thread(target=launch_receiver_background_node, daemon=True)
    background_thread.start()

# ----------------------------------------------------------------------
# SYNCHRONIZED RE-RENDER IMAGE MATRIX DRAWING ENGINE
# ----------------------------------------------------------------------
if st.session_state.received_data:
    try:
        love_package = st.session_state.received_data
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
            
            if current_msg_time != st.session_state.last_processed_time:
                st.session_state.last_processed_time = current_msg_time
                st.balloons()

    except Exception as e:
        status_message.error(f"Error compiling canvas layers: {e}")
else:
    status_message.info("👋 Listening to local port 5000... Waiting for her to click Send Note! 💓")

time.sleep(1)
st.rerun()
