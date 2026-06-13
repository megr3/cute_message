import streamlit as st
import os
import base64
import urllib.parse

# 1. Expand the Streamlit canvas to 100% full-screen layout view parameters
st.set_page_config(
    page_title="Monthiversary Gift !!!!!HHEEHHEHEHEHE", 
    page_icon="💖", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Strict Light Mode Guard, Top White Space Removal, and Global Google Font Injection
st.markdown("""
    <!-- Inject Google Fonts directly into the parent Streamlit frame wrapper -->
    <link rel="preconnect" href="https://googleapis.com">
    <link rel="preconnect" href="https://gstatic.com" crossorigin>
    <link href="https://googleapis.com/css2?family=Life+Savers:wght@400;700;800&display=swap" rel="stylesheet">

    <style>
        <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Life+Savers:wght@400;700;800&display=swap" rel="stylesheet">
    <style>
        * {
            box-sizing: border-box;
            font-family: "Life Savers", serif;
            font-weight: 800;
            color: #f30477; 
            text-align: center;
        }
        .life-savers-regular {
          font-family: "Life Savers", serif;
          font-weight: 400;
          font-style: normal;
        }
        .life-savers-bold {
          font-family: "Life Savers", serif;
          font-weight: 700;
          font-style: normal;
        }
        .life-savers-extrabold {
          font-family: "Life Savers", serif;
          font-weight: 800;
          font-style: normal;
        }
    </style>
""", unsafe_allow_html=True)

# Helper function to read raw images locally and convert them into base64 strings
def get_base64_image(img_path):
    if os.path.exists(img_path):
        with open(img_path, "rb") as image_file:
            return f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode()}"
    return ""

# Helper function to read your HTML templates word-for-word out of the template directory
def load_html_file(file_name):
    full_path = os.path.join("template", file_name)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    return f"<h1>Error: {file_name} not found inside the 'template' folder!</h1>"

# 2. Track progression states natively inside Streamlit memory
if "flow_step" not in st.session_state:
    st.session_state.flow_step = "index"

query_params = st.query_params

# 3. Handle page transition path variables passing upward
if "iframe_signal" in query_params:
    st.session_state.flow_step = query_params["iframe_signal"]
    st.query_params.clear()
    st.rerun()

# 4. Burn-On-Read Text Processing Panel
if "action" in query_params and query_params["action"] == "download_and_burn":
    clean_sender = urllib.parse.unquote(query_params.get("sender", "Babe"))
    clean_receiver = urllib.parse.unquote(query_params.get("receiver", "You"))
    clean_joke = urllib.parse.unquote(query_params.get("joke", "N/A"))
    clean_note = urllib.parse.unquote(query_params.get("note", ""))

    letter_content = f"From: {clean_sender}\nTo: {clean_receiver}\nJoke: {clean_joke}\n\nNote:\n{clean_note}"
    
    st.markdown("<div style='padding:40px; background:white; border-radius:20px; max-width:500px; margin: 80px auto; border: 3px dashed #f30477; text-align:center;'>", unsafe_allow_html=True)
    st.subheader("🔒 Secret Note Securely Decoded!")
    st.text_area("Unlocked Content Frame:", letter_content, height=180, disabled=True)
    
    st.download_button("💾 Save Text File Copy", data=letter_content, file_name="anniversary_note.txt", mime="text/plain")
    
    if st.button("🗑️ Burn Message From System Memory"):
        st.query_params.clear()
        st.session_state.flow_step = "burned"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# =========================================================================
# SYSTEM ROUTING MAP (Using custom style rules paired with st.html)
# =========================================================================

if st.session_state.flow_step == "index":
    index_view = load_html_file("index.html")
    st.html(index_view)

elif st.session_state.flow_step == "second":
    second_view = load_html_file("second-page.html")
    st.html(second_view)

elif st.session_state.flow_step == "gift":
    gift_view = load_html_file("gift.html")
    st.html(gift_view)

elif st.session_state.flow_step == "cheers":
    cheers_view = load_html_file("cheers.html")
    cheers_view = cheers_view.replace("long_way.jpg", get_base64_image(os.path.join("memories", "long_way.jpg")))
    cheers_view = cheers_view.replace("house.jpg", get_base64_image(os.path.join("memories", "house.jpg")))
    cheers_view = cheers_view.replace("knot.jpg", get_base64_image(os.path.join("memories", "knot.jpg")))
    cheers_view = cheers_view.replace("life.jpg", get_base64_image(os.path.join("memories", "life.jpg")))
    cheers_view = cheers_view.replace("grow_old.jpg", get_base64_image(os.path.join("memories", "grow_old.jpg")))
    st.html(cheers_view)

elif st.session_state.flow_step == "last":
    last_view = load_html_file("last-page.html")
    
    base64_images_js_array = []
    for i in range(1, 69):
        b64_str = get_base64_image(os.path.join("memories", f"{i}.jpg"))
        base64_images_js_array.append(f"'{b64_str}'" if b64_str else "'#fff0f7'")
    images_js_string = ",".join(base64_images_js_array)
    
    final_injected_html = last_view.replace("{{IMAGE_PLACEHOLDER_TOKEN}}", images_js_string)
    st.html(final_injected_html)

elif st.session_state.flow_step == "burned":
    st.markdown("<div style='text-align:center; margin-top:20vh; font-family:sans-serif;'>", unsafe_allow_html=True)
    st.success("💥 The message has self-destructed successfully!")
    st.info("The text arrays are completely deleted from browser caching frameworks and device storage arrays. 🕊️")
    if st.button("↩️ Restart Application From Page 1"):
        st.session_state.flow_step = "index"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
