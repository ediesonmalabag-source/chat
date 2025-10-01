import streamlit as st
import time

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

    if user_message in ["hi", "hello", "hey", "haha"]:
        return "👋 Hi! I'm the TESDA BIT Chatbot. Ask about qualifications, enrolment, assessment, or contact us—just tap a button or type below."

    elif "qualifications" in user_message:
        return "🎓 TESDA BIT offers 13 qualifications. Type a specific one (e.g., 'Cookery') to learn more."

    elif any(keyword in user_message for keyword in ["cookery", "cook", "cookery nc2"]):
        return """👨‍🍳 Cookery NC II<br>
        Nominal Duration: 316 hours<br>  
        Description: This qualification consists of competencies that a person must achieve to clean kitchen areas, prepare hot, cold meals 
        and desserts for guests in various food and beverage service facilities."""

    elif any(keyword in user_message for keyword in ["computer", "css", "computer systems servicing"]):
        return """💻 Computer Systems Servicing NC II<br>
        Nominal Duration: 280 hours<br>  
        Description: This qualification consists of competencies that a person must possess to install and configure computer systems, set up networks and servers, and maintain and repair them."""

    elif any(keyword in user_message for keyword in ["enrollment", "enroll", "enrol"]):
        return """
        📋 **Enrolment Requirements**<br>
        To enrol at TESDA BIT, please prepare the following:<br><br>
        • PSA Birth Certificate (photocopy)<br>
        • Marriage Certificate, if married (photocopy)<br>
        • 2 pcs 1x1 ID picture<br>
        • Filled-up Registration Form – <a href='https://bit.ly/3IOR8g8'>Download here</a><br><br>
        📌 Submit all requirements personally at the TESDA BIT Admin Office, or email them to <a href='mailto:bit@tesda.gov.ph'>bit@tesda.gov.ph</a>.
        """

    elif "assessment" in user_message:
        return "📊 Assessment schedules and requirements vary by qualification. Please contact TESDA BIT for details."

    elif "contact" in user_message:
        return "📞 You may reach TESDA BIT via email at [bit@tesda.gov.ph](mailto:bit@tesda.gov.ph) or visit the Admin Office during working hours."

    else:
        return "❓ I didn’t catch that. Try typing qualifications, enrolment, assessment, or contact—or just use the buttons below."

# --------------------------
# Determine user input
# --------------------------
user_input = None

if st.session_state.last_action:
    user_input = st.session_state.last_action
    st.session_state.last_action = None

if user_input is None:
    chat_in = st.chat_input("Type your message here...")
    if chat_in:
        user_input = chat_in

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
        st.markdown(
            f"<div style='background-color:#E6E6FA; padding:10px; border-radius:15px; margin:5px; text-align:left;'>"
            f"🤖 <b>{role}:</b> {msg}</div>",
            unsafe_allow_html=True,
        )

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
