import streamlit as st
import time
import re

# --------------------------
# Page config (must be first)
# --------------------------
st.set_page_config(page_title="Simple Chatbot", page_icon="🤖", layout="wide")

# --------------------------
# Session state setup
# --------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [("Bot", "👋 Hi! I'm the TESDA BIT Chatbot. Ask about qualifications, enrolment, assessment, or contact us—just tap a button or type below.")]
if "last_action" not in st.session_state:
    st.session_state.last_action = None

# --------------------------
# Banner and Title
# --------------------------
st.image("https://raw.githubusercontent.com/ediesonmalabag-source/chat/main/bit_banner.png", use_container_width=True)
st.markdown("""
    <div style='text-align: center;'>
        <h3 style='color: #003366;'>🤖 TESDA BIT Chatbot</h3>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------
# DEFINING QUALIFICATION RESPONSES
# -------------------------------------
cookery_response = """<h4 style='color:#003366; font-weight:bold;'>🍳Cookery NC II</h4>
        ⏱️ <b>Nominal Duration:</b> 316 hours (approx. 40 days)<br><br>
        📚 <b>Qualification Description:</b><br>
        This qualification consists of competencies that a person must achieve to clean kitchen areas, prepare hot, cold meals 
        and desserts for guests in various food and beverage service facilities.<br><br>
        🧰 <b>Cluster of Core Units of Competencies:</b><br>
        • Prepare and Cook Hot Meals<br>
        • Prepare Cold Meals<br>
        • Prepare Sweets<br><br>
        📌 <b>Entry Requirements:</b><br>
        • can communicate both in oral and written<br> 
        • physically and mentally fit<br> 
        • with good moral character<br> 
        • can perform basic mathematical computation<br><br>
       📊 <b>Assessment Information:</b><br
       • Held at the TESDA-BIT Assessment Center<br>
       • Covers practical cooking tasks, food safety, and presentation<br>
       • <b>Assessment fee: ₱978</b> — <b>Free for TESDA scholars</b> (present scholarship ID or enrolment proof)<br>
       • <a href='https://yourdomain.com/forms/self-assessment-guide-cookery.pdf' target='_blank'>📥 Download Self-Assessment Guide (PDF)</a> or request a printed copy<br>
       <b>Eligibility:</b> Assessment is open to:<br>
       • Trainees who have successfully completed Cookery NC II training<br>
       • Industry workers with relevant experience and a valid Certificate of Employment<br>
       <b>Certification:</b> Passers receive a TESDA National Certificate (NC II), valid for 5 years and recognized both nationwide and internationally.<br><br>
        🏨 <b>Career Opportunities:</b><br>
        • Cook or Commis<br>
        • Assistant Cook<br><br>
        ✅ <i>Want to enrol?</i> Tap the 📝 <b>Enrolment</b> button below
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
    if st.button("🔄 Reset Chat"):
        st.session_state.messages = [("Bot", "👋 Hi! I'm the TESDA BIT Chatbot. Ask about qualifications, enrolment, assessment, or contact us—just tap a button or type below.")]
        st.session_state.last_action = None
        st.rerun()

# --------------------------
# Chatbot response function
# --------------------------
def chatbot_response(user_message: str) -> str:
    user_message = user_message.lower().strip()
    user_message = re.sub(r'[^\w\s]', '', user_message)  # ✅ Removes punctuation like ? . ! etc.
 
    # 🔍 Match specific qualifications first
    for keyword, response in qualification_responses.items():
        if keyword in user_message:
            return response
    
    # 👋 Greetings
    if user_message in ["hi", "hello", "hey", "haha"]:
        return "👋 Hi! I'm the TESDA BIT Chatbot. Ask about qualifications, enrolment, assessment, or contact us—just tap a button or type below."

    # ------------
    # ENROLMENT
    # ------------
    elif any(kw in user_message.lower() for kw in ["enrollment", "enrolment", "enroll", "enrol", "enroling", "enrolling"]):
        return """<h4 style='color:#003366; font-weight:bold;'>📋 Enrolment Procedures</h4>        
        📥 <b>Download the Fillable PDF Registration Form</b> – <a href='https://github.com/ediesonmalabag-source/chat/raw/main/BIT_Registration_Form_Fillable_v1.pdf' target='_blank' style='color:#003366; font-weight:bold;'>Click here to download</a><br>
        🖥️ Open the form using any PDF reader (e.g., Adobe Acrobat, browser, Foxit)<br>
        ✍️ Fill in your personal details digitally using the fillable fields<br>
        🖨️ Print the completed form<br>
        ✒️ Write your <b>full name and signature</b> in the spaces provided<br>
        🖼️ Attach <b>two (2) recent 1x1 ID photos</b> taken within the last 6 months in the designated boxes on the form<br><br>
        <b>📋 Additional Enrolment Requirements:</b><br>
        • <b>Photocopy of PSA Birth Certificate</b><br>
        • <b>Photocopy of Marriage Certificate</b>, if married<br><br>
        📌 <b>Submit all documents</b> personally at the TESDA BIT Admin Office, or email them to <a href='mailto:bit@tesda.gov.ph'>bit@tesda.gov.ph</a><br><br>
        📅 <i>Note: Enrolment is open year-round, but slots are limited. Submit early to secure your schedule.</i><br><br>
        ✅ <b>Need help?</b> Tap the <b>📞 Contact</b> button below for assistance.
        """
    
    # ------------
    # CONTACT
    # -------------

    elif any(kw in user_message.lower() for kw in ["contact", "help", "assist", "support", "reach out", "call", "email"]):
        return """<h4 style='color:#003366; font-weight:bold;'>📞 TESDA-BIT Contact Information</h4>
        🌐 <b>Facebook Page:</b> <a href='https://www.facebook.com/profile.php?id=61561653118631' target='_blank' style='color:#003366; font-weight:italic;'>Bangui Institute of Technology TESDA</a><br>
        💬 <b>Messenger Chat:</b> <a href='https://www.facebook.com/messages/t/61561653118631' target='_blank'>Send a message via Messenger</a><br>
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
        return """<h4 style='color:#003366; font-weight:bold;'>🧰 TESDA-BIT Qualifications Offered</h4>
        🎓 <b>National Certificate Programs:</b><br>
        •🧁Bread and Pastry Production NC II<br>
        •💻Computer Systems Servicing NC II<br>
        •🍳Cookery NC II<br>
        •🚗Driving NC II<br>
        •🍽️Food and Beverage Services NC II<br>
        •🏭Food Processing NC II<br>
        •🧹Housekeeping NC II<br>
        •🧱Masonry NC II<br>
        •🔧Motorcycle/Small Engine Servicing NC II<br>
        •🌱Organic Agriculture Production NC II<br>
        •🔩Shielded Metal Arc Welding (SMAW) NC I<br>
        •🔩Shielded Metal Arc Welding (SMAW) NC II<br><br>
         🧑‍🏫 <b>Trainer Qualification:</b><br>
        •🏘️Community-Based Trainers Methodology Course<br>
        •📋Trainer's Methodology Level I (for aspiring trainers and assessors)<br><br>
        ⏱️<b>Training Duration:</b><br>
        • Varies per qualification<br>
        • Includes classroom instruction, hands-on activities, and competency assessment<br><br>
        📜 <b>Certification:</b><br>
        • Trainees who pass the national assessment will receive a TESDA National Certificate (NC I or NC II)<br>
        • TM Level I passers are qualified to deliver and assess Competency-Based Training programs<br>
        • CBTMC passers are qualified to deliver community-based trainings<br>
        • Certificates are recognized nationwide and valued globally, especially in hospitality and technical fields.<br><br>
        📅 <i>Note: All qualifications follow TESDA’s Competency-Based Training (CBT) format and are aligned with industry standards.</i><br><br>
        💡 <b>Want to explore a course?</b><br>
        Just type the name of a qualification (e.g., <i>cookery</i>, <i>css</i>, or <i>bread and pastry</i>) to view full details — including duration, core competencies, and career opportunities.<br><br>
        📞 <b>Need help deciding?</b> Tap the <b>Contact</b> button below to reach us directly.<br>
        📝 <b>Ready to enrol?</b> Tap the <b>Enrolment</b> button to begin your registration.
        """

    elif "assessment" in user_message:
        return "📊 Assessment schedules and requirements vary by qualification. Please contact TESDA BIT for details."

    

    else:
        return "❓ I didn’t catch that. Try typing qualifications, enrolment, assessment, or contact—or just use the buttons below."

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
    else:
        st.markdown(msg, unsafe_allow_html=True)


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


#AVOID COVERING MESSAGE BOX ON MOBILE




