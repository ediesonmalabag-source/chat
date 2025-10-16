import streamlit as st
import time
import re
from streamlit_javascript import st_javascript
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from pdfrw.buildxobj import pagexobj
from pdfrw.toreportlab import makerl

from datetime import date

import urllib.request
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os  # ✅ Needed for checking file existence

# ✅ Download font from GitHub if not already present
font_url = "https://raw.githubusercontent.com/ediesonmalabag-source/chat/main/DejaVuSans.ttf"
font_path = "DejaVuSans.ttf"

try:
    if not os.path.exists(font_path):
        urllib.request.urlretrieve(font_url, font_path)
    pdfmetrics.registerFont(TTFont("DejaVuSans", font_path))
except Exception as e:
    st.error(f"Font loading failed: {e}")

# ---------------------------------------
# 🔧 PDF FILLING FUNCTION (top of file)
# ---------------------------------------

def fill_pdf(input_pdf_path, output_pdf_path, data_dict):
    try:
        template_pdf = PdfReader(input_pdf_path)

        for page_index, page in enumerate(template_pdf.pages):
            # Create overlay canvas for this page
            packet = BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)

            annots = page.get(PdfName("Annots"))
            if annots:
                for a in annots:
                    if a.get(PdfName("Subtype")) == PdfName("Widget"):
                        t = a.get(PdfName("T"))
                        rect = a.get(PdfName("Rect"))
                        if t and rect:
                            key = t.to_unicode().strip("()") if hasattr(t, "to_unicode") else t[1:-1]
                            if key in data_dict:
                                x, y = float(rect[0]), float(rect[1])
                                can.setFont("DejaVuSans", 10)
                                can.drawString(x + 2, y + 2, str(data_dict[key]))
            
            # ✅ Draw circle-based SEX SELECTION: MALE OR FEMALE
            can.setStrokeColorRGB(0, 0, 0)  # Black outline
            can.setFillColorRGB(0, 0, 0)    # Black fill for selected

            # Draw empty circles
            can.circle(40, 350, 4, stroke=1, fill=0)  # Male
            can.circle(40, 333, 4, stroke=1, fill=0)  # Female

            # Fill selected circle
            if data_dict.get("Sex") == "Male":
                can.circle(40, 350, 3, stroke=0, fill=1)
            elif data_dict.get("Sex") == "Female":
                can.circle(40, 333, 3, stroke=0, fill=1)

            can.save()
            packet.seek(0)

            # Read overlay and merge with current page
            overlay_pdf = PdfReader(packet)
            if overlay_pdf.pages:
                overlay_page = overlay_pdf.pages[0]
                if overlay_page.Contents:
                    from pdfrw import PdfArray
                    if page.Contents:
                        page.Contents = PdfArray([page.Contents, overlay_page.Contents])
                    else:
                        page.Contents = overlay_page.Contents

            # Remove form fields
            if PdfName("Annots") in page:
                del page[PdfName("Annots")]

        PdfWriter().write(output_pdf_path, template_pdf)
        return True, None

    except Exception as e:
        return False, f"Failed to generate visible PDF: {e}"
        
# --------------------------
# Page config (must be first)
# --------------------------
st.set_page_config(page_title="Simple Chatbot", page_icon="🤖", layout="wide")

st.markdown("""
<style>
html {
  scroll-behavior: smooth;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------
# QUERY PARAM TRIGGER FOR PDF FORM on Page Config
# ---------------------------------
if st.query_params.get("form") == "1" and st.session_state.get("show_enrolment_form") != "form":
    st.session_state.show_enrolment_form = "form"
    st.query_params.clear()

# --------------------------
# Compact layout CSS (place here)
# --------------------------
st.markdown("""
<style>
/* remove bottom margin below Streamlit image and header spacing */
img[alt="image"] { display:block; margin-bottom: 0 !important; }
h3 { margin-top: 0 !important; margin-bottom: 0 !important; }
</style>
""", unsafe_allow_html=True)

# --------------------------
# Session state initialization (must run before any .append calls)
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "welcome_sent" not in st.session_state:
    st.session_state.welcome_sent = False
if "last_action" not in st.session_state:
    st.session_state.last_action = None
    
# DETECT MOBILE MESSENGER BROWSER 
screen_width = st_javascript("window.innerWidth") or 768

if "show_mobile_warning" not in st.session_state:
    st.session_state.show_mobile_warning = False

if screen_width < 768 and "show_mobile_warning_evaluated" not in st.session_state:
    st.session_state.show_mobile_warning = True
    st.session_state.show_mobile_warning_evaluated = True
    
# --------------------------
# Force white background (even on mobile dark mode)
# --------------------------
st.markdown("""
    <style>
        /* White background */
        body, .main, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {
            background-color: white !important;
            color: #222 !important;
        }

        /* General text */
        html, body, p, div, span {
            color: #222 !important;
        }

        /* Emphasized button styling */
        button, [data-testid="baseButton-secondary"], [data-testid="baseButton-primary"] {
            background-color: #4A90E2 !important;  /* Soft Sky Blue */
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.75em 1.25em !important;
            font-weight: 700 !important;
            font-size: 18px !important;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15) !important;
            transition: all 0.2s ease-in-out;
        }

        /* Ensure label text is white */
        button * {
            color: white !important;
        }

        /* Hover effect */
        button:hover {
            background-color: #357ABD !important;
            transform: scale(1.03);
        }

        /* Active (pressed) effect */
        button:active {
            background-color: #2C5FA0 !important;
            transform: scale(0.98);
        }
        /* ✅ Disabled button style */
        button:disabled {
            background-color: #a0c4e2 !important;
            color: #eee !important;
            cursor: not-allowed !important;
        }
        /* ✅ Expander header text fix */
        [data-testid="stExpander"] > details > summary {
            color: #222 !important;
            background-color: #fff3cd !important;
            font-weight: 600 !important;
            padding: 8px !important;
            border-radius: 5px !important;
        }
        /* ✅ Input box styling */
        textarea {
            background-color: #f0f8ff !important;  /* Alice Blue */
            color: #222 !important;
            border: 1px solid #4A90E2 !important;
            border-radius: 8px !important;
            padding: 10px !important;
            font-size: 16px !important;
            font-family: 'Segoe UI', sans-serif !important;
        }
        /* ✅ Input box focus effect */
        textarea:focus {
            outline: none !important;
            box-shadow: 0 0 5px #4A90E2 !important;
        }
        /* ✅ Force light styling on all input boxes */
        input[type="text"], input[type="email"], input[type="tel"] {
        background-color: #f0f8ff !important;
        color: #222 !important;
        border: 1px solid #4A90E2 !important
        border-radius: 8px !important;
        padding: 10px !important;
        font-size: 16px !important;
        font-family: 'Segoe UI', sans-serif !important;
        }

        /* ✅ Focus effect */
        input[type="text"]:focus, input[type="email"]:focus, input[type="tel"]:focus {
        outline: none !important;
        box-shadow: 0 0 5px #4A90E2 !important;
        }
        
        /* ✅ Force light styling on selectbox */
        [data-testid="stSelectbox"] label,
        [data-testid="stSelectbox"] div[role="combobox"] {
            color: #222 !important;           /* Dark text */
            background-color: #f0f8ff !important;  /* Light background */
            border: 1px solid #4A90E2 !important;
            border-radius: 8px !important;
            padding: 6px !important;
            font-size: 16px !important;
            font-family: 'Segoe UI', sans-serif !important;
        }

        /* ✅ Dropdown options */
        [data-testid="stSelectbox"] ul {
            background-color: #ffffff !important;
            color: #222 !important;
    
    </style>
""", unsafe_allow_html=True)


# --------------------------
# Banner and Title
# --------------------------
# st.image("https://raw.githubusercontent.com/ediesonmalabag-source/chat/main/bit_banner.png", use_container_width=True)
# st.markdown("""
#  <div style='text-align:center; margin:0; padding:0;'>
#    <h3 style='color:#003366; margin:0; padding:0;'>🤖 TESDA BIT Chatbot</h3>
#  </div>
# """, unsafe_allow_html=True)

st.image("https://raw.githubusercontent.com/ediesonmalabag-source/chat/main/bit_banner.png", use_container_width=True)

# Add welcome message only once (immediately after banner)
if "welcome_sent" not in st.session_state:
    st.session_state.welcome_sent = False

if not st.session_state.welcome_sent:
    st.session_state.messages.append((
        "Bot",
        "👋 Hi there! I'm the TESDA BIT Chatbot. Whether you're on mobile or desktop, I can help you with qualifications, enrolment, assessment, or reaching TESDA BIT. Tap a button or send a message to get started."
    ))
    st.session_state.welcome_sent = True
    
# ----------------------------
# INITIALIZE SESSION STATE
# ----------------------------


# ensure flag exists for showing the enrolment form
if "show_enrolment_form" not in st.session_state:
    st.session_state.show_enrolment_form = "idle"


# ------------------------------------
# DEFINING QUALIFICATION RESPONSES
# -------------------------------------
cookery_response = """<h4 style='color:#003366; font-weight:bold;'>🍳Cookery NC II</h4>
        ⏱️ <b>Nominal Duration:</b> 316 hours (40 days)<br><br>
        <h5 style='color:#003366;'>📚 Qualification Description:</h5>
        This qualification consists of competencies that a person must achieve to clean kitchen areas, prepare hot, cold meals 
        and desserts for guests in various food and beverage service facilities.<br><br>
        <h5 style='color:#003366;'>🧰 Cluster of Core Units of Competencies:</h5>
        • Prepare and Cook Hot Meals<br>
        • Prepare Cold Meals<br>
        • Prepare Sweets<br><br>
        <h5 style='color:#003366;'>📌 Entry Requirements:</h5>
        • Can communicate both in oral and written<br> 
        • Physically and mentally fit<br> 
        • With good moral character<br> 
        • Can perform basic mathematical computation<br><br>
       <h5 style='color:#003366;'>📊 Assessment Information:</h5>
       • Held at the TESDA-BIT Assessment Center<br>
       • Covers hands-on cooking tasks, food safety, portioning, plating techniques, and kitchen sanitation based on TESDA standards.<br>
       • <b>Assessment fee: ₱978</b> — <b>Free for TESDA scholars</b> (just present your scholarship ID or enrolment proof)<br>
       • <a href='https://drive.google.com/file/d/1Z5vTvtxIRkiLTrGQPfy7g064scP7X_DG/view?usp=sharing' target='_blank'>📥 Download Self-Assessment Guide (PDF)</a> or request a printed copy<br><br>
       <h5 style='color:#003366;'>Eligibility:</h5>
       • Trainees who have successfully completed Cookery NC II training<br>
       • Industry workers with relevant experience and a valid Certificate of Employment<br><br>
       <h5 style='color:#003366;'>Certification:</h5> 
       Passers receive a TESDA National Certificate (NC II), valid for 5 years and recognized both nationwide and internationally.<br><br>
       <h5 style='color:#003366;'>🏨 Career Opportunities:</h5>
        • Cook or Commis - in hotels, restaurants or catering services<br>
        • Assistant Cook - in institutional or commercial kitchens<br><br>
        📝 <i>Want to enrol?</i> Tap the <b>Enrolment</b> button below<br>
        📊 <i>Ready for assessment?</i> Tap the <b>Assessment</b> button below<br>
        📞 <i>Need help or have questions?</i> Tap the <b>Contact</b> button below<br>
        🎓 <i>Want to explore other courses?</i> Type <b>css</b>, <b>baking</b> or <b>welding</b> to view more qualifications
        """

css_response = """<h4 style='color:#003366; font-weight:bold;'>💻Computer Systems Servicing NC II</h4>
... (your full HTML block here)
"""

bread_pastry_response = """<h4 style='color:#003366; font-weight:bold;'>🧁Bread and Pastry Production NC II</h4>
... (your full HTML block here)
"""
# ------------------------------------
# CREATE KEYWORD RESPONSE DICTIONARY
# -------------------------------------

qualification_responses = {
    "cookery nc ii": cookery_response,
    "cookery": cookery_response,
    "cook": cookery_response,
    "computer": css_response,
    "css": css_response,
    "computer servicing": css_response,
    "bread": bread_pastry_response,
    "pastry": bread_pastry_response,
    "baking": bread_pastry_response,
    "bread and pastry": bread_pastry_response,
}

# --------------------------
# Sidebar Info + Reset
# --------------------------
with st.sidebar:
    st.title("ℹ️ About this Chatbot")
    st.write("This is a simple rule-based chatbot built with Streamlit to help users explore TESDA-BIT qualifications, check enrolment and assessment info, or contact TESDA BIT directly.")
    st.markdown("""
    - 🎓 Explore TESDA qualifications  
    - 📝 Check enrolment requirements  
    - 📊 View assessment info and schedules  
    - 📞 Contact TESDA BIT for assistance  
    """)
    # Reset button
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = []
        st.session_state.welcome_sent = False
        st.session_state.last_action = None
        st.session_state.show_enrolment_form = "idle"
        st.rerun()
        
        
# --------------------------
# Chatbot response function
# --------------------------
def chatbot_response(user_message: str) -> str:
    user_message = user_message.lower().strip()
    user_message = re.sub(r'[^\w\s]', '', user_message)
    matched = False
    response_html = ""

    # Match specific qualifications first (these already contain HTML)
    for keyword, response in qualification_responses.items():
        if keyword in user_message:
            return response
            
# 👋 Greetings
    if user_message in ["hi", "hello", "hey", "haha"]:
        matched = True
        response_html = "👋 Hi! I'm the TESDA BIT Chatbot. Ask about qualifications, enrolment, assessment, or contact us—just tap a button or type below."
   
    # ------------
    # ENROLMENT
    # ------------
    elif any(kw in user_message for kw in ["enrollment", "enrolment", "enroll", "enrol", "enroling", "enrolling"]):
        matched = True
        response_html = """<h4 style='color:#003366; font-weight:bold;'>📋 TESDA Enrolment Form</h4>
        You can now fill out your TESDA registration form directly inside this app.<br><br>
        👉 <a href='?form=1' target='_self' style='font-weight:bold; color:#2C5FA0;'>Click here to fill up the form</a>
        Once submitted, you'll be able to download your completed PDF instantly.<br><br>
        ✅ <i>No need to print or scan — it's all digital.</i>
        """
       

    # ------------
    # CONTACT
    # -------------

    elif any(kw in user_message.lower() for kw in ["contact", "help", "assist", "support", "reach out", "call", "email"]):
        match =True
        response_html = """<h4 style='color:#003366; font-weight:bold;'>📞 TESDA-BIT Contact Information</h4>
        🌐 <b>Facebook Page:</b> <a href='https://www.facebook.com/profile.php?id=61561653118631' target='_blank' style='color:#003366; font-weight:italic;'>Bangui Institute of Technology TESDA</a><br>
        💬 <b>Messenger Chat:</b> <a href='https://m.me/bit.tesda' target='_blank'>Send a message via Messenger</a><br>
        📱 <b>Cellphone No.:</b> <a href="tel:09088600955" style="color:#003366; font-weight:italic;">0908-860-0955</a><br>
        📧 <b>Email:</b> <a href='mailto:bit@tesda.gov.ph'>bit@tesda.gov.ph</a><br>
        📍 <b>Office Address:</b> TESDA-Bangui Institute of Technology, Brgy. Manayon, Bangui, Ilocos Norte<br><br>
        🕒 <b>Office Hours:</b> Monday to Friday, 8:00 AM – 5:00 PM<br>
        📅 <b>Walk-in Inquiries:</b> No appointment needed during office hours<br><br>
        ✅ <i>For enrolment assistance, document submission, or qualification inquiries, feel free to reach out anytime.</i>
        """
 # ------------
 # QUALIFICATION
 # -------------
    elif any(kw in user_message.lower() for kw in ["qualification", "course", "program", "training", "offered", "available courses"]):
        match = True
        response_html = """<h4 style='color:#003366; font-weight:bold;'>🎓 TESDA-BIT Qualifications Offered</h4>
        <h5 style='color:#003366;'>🧰 National Certificate Programs:</h5>
        •🧁<b>Bread and Pastry Production NC II</b><br>
        •💻<b>Computer Systems Servicing NC II</b><br>
        •🍳<b>Cookery NC II</b><br>
        •🚗<b>Driving NC II</b><br>
        •🍽️<b>Food and Beverage Services NC II</b><br>
        •🏭<b>Food Processing NC II</b><br>
        •🧹<b>Housekeeping NC II</b><br>
        •🧱<b>Masonry NC II</b><br>
        •🔧<b>Motorcycle Small Engine Servicing NC II</b><br>
        •🌱<b>Organic Agriculture Production NC II</b><br>
        •🔩<b>Shielded Metal Arc Welding (SMAW) NC I</b><br>
        •🔩<b>Shielded Metal Arc Welding (SMAW) NC II</b><br><br>
         <h5 style='color:#003366;'>🧑‍🏫 Trainer Qualification:</h5>
        •🏘️<b>Community-Based Trainers Methodology Course</b><br>
        •📋<b>Trainers Methodology Level I</b> (for aspiring trainers and assessors)<br><br>
        <h5 style='color:#003366;'>⏱️ Training Duration:</h5>
        • Varies per qualification<br>
        • Includes classroom instruction, hands-on activities, and competency assessment<br><br>
        <h5 style='color:#003366;'>📜 Certification:</h5>
        • Trainees who pass the national assessment will receive a <b>TESDA National Certificate (NC I or NC II)</b><br>
        • <b>Trainer’s Methodology Level I</b> passers are qualified to deliver and assess Competency-Based Training programs<br>
        • CBTMC passers are qualified to deliver community-based trainings<br>
        • Certificates are recognized nationwide and valued globally, especially in hospitality and technical fields.<br><br>
        📅 <i>Note: All qualifications follow TESDA’s Competency-Based Training (CBT) format and are aligned with industry standards.</i><br><br>
        💡 <b>Want to explore a course?</b><br>
        Just type the name of a qualification (e.g., <i>cookery</i>, <i>css</i>, or <i>bread and pastry</i>) to view full details — including duration, core competencies, and career opportunities.<br><br>
        📞 <b>Need help deciding?</b> Tap the <b>Contact</b> button below to reach us directly.<br>
        📝 <b>Ready to enrol?</b> Tap the <b>Enrolment</b> button to begin your registration.
        """

    elif "assessment" in user_message:
        match = True
        response_html = "📊 Assessment schedules and requirements vary by qualification. Please contact TESDA BIT for details."


    # ❓ Fallback MESSAGE, if no match found
    if not matched and response_html == "":
        response_html = """❓ <b>I couldn’t match your message to a specific qualification, enrolment steps, or assessment details.</b><br><br>
        Here are a few examples of what you can ask about:<br>
        • 🍳 Cookery NC II<br>
        • 💻 Computer Systems Servicing NC II<br>
        • 🧁 Bread and Pastry Production NC II<br>
        (…and many more!)<br><br>
        Type <b>qualification</b> to see the full list.<br><br>
        You can also ask about:<br>
        • 📝 Enrolment<br>
        • 📊 Assessment<br>
        • 📞 Contact<br><br>
        Or just tap the buttons below!
        """
    return response_html
    


# --------------------------
# Determine user input
# --------------------------
user_input = None  # ✅ Initialize first

chat_in = st.chat_input("Type your message here...")
if chat_in:
    user_input = chat_in

if st.session_state.last_action:
    user_input = st.session_state.last_action
    st.session_state.last_action = None

# --------------------------
# Process user input
# --------------------------
if user_input:
    st.session_state.messages.append(("You", user_input))
    with st.spinner("Bot is typing..."):
        time.sleep(0.9)

    try:
        bot_reply = chatbot_response(user_input)
    except Exception as e:
        bot_reply = f"⚠️ An internal error occurred while generating a reply: {e}"

    st.session_state.messages.append(("Bot", bot_reply))
    st.markdown(bot_reply, unsafe_allow_html=True)




 
# --------------------------
# Display chat history
# --------------------------
for role, msg in st.session_state.messages:
    if role == "You":
        st.markdown(
            f"<div style='background-color:#DCF8C6; padding:10px; border-radius:15px; margin:5px; text-align:right;'>"
            f"🧑 <b>{role}:</b> {msg}</div>",
            unsafe_allow_html=True,
        )
    else: st.markdown( f"<div style='background-color:#e6f2ff; padding:10px 15px; border-radius:10px; margin-top:-6px; margin-bottom:10px; color:#003366;'>" f"{msg}" f"</div>", unsafe_allow_html=True, )

# --------------------------
# Mobile tip (moved after chat history so it appears in-view on mobile)
# --------------------------


if st.session_state.show_mobile_warning:
    with st.expander("📱 Mobile Tip", expanded=True):
        st.markdown(
            """
            <div style='background-color:#fff3cd; padding:10px; border-radius:6px; border:1px solid #ffeeba;'>
            If you're viewing this inside Messenger or another in-app browser, some features may not work properly.<br>
            Tap the <b style="color:#d6336c;">⋮ three-dot menu <u>in the top-right corner</u></b> and choose <b>'Open in Chrome'</b> or <b>'Open in Browser'</b> for full access.
            </div>
            """,
            unsafe_allow_html=True,
        )

        image_url = "https://raw.githubusercontent.com/ediesonmalabag-source/chat/main/openinchrome.png"
        st.markdown(
            f'''
            <figure style="margin:0;">
              <img src="{image_url}" alt="open in browser guide" style="max-width:100%; width:auto; height:auto; border-radius:6px;">
            </figure>
            ''',
            unsafe_allow_html=True,
        )

        st.markdown(
            "✅ If you're already in Chrome, Edge, Firefox, or another mobile browser, you can dismiss this message.",
            unsafe_allow_html=True,
        )

        if st.button("Dismiss this message", key="dismiss_mobile_tip"):
            st.session_state.show_mobile_warning = False
            
# --------------------------
# Bottom-aligned buttons
# --------------------------
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🎓 Qualifications"):
        st.session_state.last_action = "qualifications"
with col2:
    if st.button("📝 Enrolment"):
        st.session_state.last_action = "enrolment"
        
with col3:
    if st.button("📊 Assessment"):
        st.session_state.last_action = "assessment"
with col4:
    if st.button("📞 Contact"):
        st.session_state.last_action = "contact"


#------------------------
# FORM FILL UP BELOW INPUT CHAT BOX AND BUTTONS
# --------------------------
if st.session_state.get("show_enrolment_form") == "form":
    st.markdown("<div id='fillform'></div>", unsafe_allow_html=True)
    st.subheader("🧠 Fill the TESDA registration form")

    with st.form("tesda_form"):
        entry_date = st.date_input("Entry Date (MM/DD/YY)", value=date.today())
        last_name = st.text_input("Last Name", value="")
        first_name = st.text_input("First Name", value="")
        middle_name = st.text_input("Middle Name", value="")
        sex = st.selectbox("Sex", ["Male", "Female"])
        

            
        submitted = st.form_submit_button("Generate PDF")

    # ✅ Only run this block if form is submitted
    if submitted:
        if not last_name.strip() or not first_name.strip():
            st.error("Please provide at least your first and last name.")
        else:
            data = {
                "EntryDate": entry_date.strftime("%m/%d/%y"),
                "LastName": last_name.strip(),
                "FirstName": first_name.strip(),
                "MidName": middle_name.strip(),
                "Sex": sex,
                
            }

            import tempfile, os
            try:
                with st.spinner("Filling PDF..."):
                    tmp_out = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
                    tmp_out_path = tmp_out.name
                    tmp_out.close()

                    template_path = "tesdabit_regform.pdf"
                    ok_err = fill_pdf(template_path, tmp_out_path, data)

                    if isinstance(ok_err, tuple):
                        ok, err = ok_err
                    else:
                        ok, err = True, None

                if not ok:
                    st.error(f"PDF generation failed: {err}")
                else:
                    # ✅ Flatten the PDF to make it non-editable
                    from pdfrw import PdfName
                    flattened_pdf = PdfReader(tmp_out_path)
                    for page in flattened_pdf.pages:
                        if PdfName("Annots") in page:
                            del page[PdfName("Annots")]
                    PdfWriter().write(tmp_out_path, flattened_pdf)

                    # ✅ Serve the file for download
                    with open(tmp_out_path, "rb") as f:
                        st.success("✅ Your TESDA form has been filled and flattened.")
                        st.download_button(
                            "📥 Download Your Filled Form",
                            f,
                            file_name="TESDA_Registration.pdf",
                            mime="application/pdf",
                            )

                    
            except FileNotFoundError:
                st.error("Template PDF not found. Place tesdabit_regform.pdf in the app folder.")
            except Exception as e:
                st.error(f"Failed to generate PDF: {e}")
            finally:
                try:
                    os.remove(tmp_out_path)
                except Exception:
                    pass
