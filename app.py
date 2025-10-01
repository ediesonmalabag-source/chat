import streamlit as st
import time
# --------------------------
# Top title
# --------------------------
# Display banner image
st.image("https://raw.githubusercontent.com/ediesonmalabag-source/chat/main/bit_banner.png", use_container_width=True)

# Title with TESDA branding and subtitle
st.markdown("""
    <div style='text-align: center;'>
        <h3 style='color: #003366;'>🤖 TESDA BIT Chatbot</h3>
    </div>
""", unsafe_allow_html=True)





# --------------------------
# Simple rule-based chatbot function
# --------------------------



def chatbot_response(user_message: str) -> str:
    user_message = user_message.lower().strip()

    if user_message in ["hi", "hello", "hey", "haha"]:
        return "👋 Hi! I'm the TESDA BIT Chatbot. Ask about qualifications, enrolment, assessment, or contact us—just tap a button or type below."

    # Qualification Offerings ---
    
    elif "qualifications" in user_message:
        return "TESDA BIT offers 13 qualifications. Type a specific one (e.g., 'Cookery') to learn more."
    
    elif any(keyword in user_message for keyword in ["cookery", "cook", "cookery nc2"]):
        return """👨‍🍳 Cookery NC II<br>
        Nominal Duration: 316 hours<br>  
       Description: This qualification consists of competencies that a person must achieve to clean kitchen areas, prepare hot, cold meals 
       and desserts for guests in various food and beverage service facilities ."""
    
    elif any(keyword in user_message for keyword in ["computer", "css", "computer systems servicing"]):
        return """💻 **Computer Systems Servicing NC II**<br>
        Nominal Duration: 280 hours<br>  
        Description: This qualification consists of competencies that a person  must possess to enable to install and configure computers systems, set-up computer 
        networks and servers and to maintain and repair computer systems and networks."""

# Add more elif blocks for other qualifications...

   
   
                    


    elif  any(keyword in user_message for keyword in ["enrollment", "enroll", "enrol"]):
        return """
        📋 **Enrolment Requirements**<br>
        To enrol at TESDA BIT, please prepare the following:<br><br>
        • PSA Birth Certificate (photocopy)<br>
        • Marriage Certificate, if married (photocopy)<br>
        • 2 pcs 1x1 ID picture<br>
        • Filled-up Registration Form - <a href='https://bit.ly/3IOR8g8'>https://bit.ly/3IOR8g8</a><br><br>
        📌 Submit all requirements personally at the TESDA BIT Admin Office, or email them to <a href='mailto:bit@tesda.gov.ph'>bit@tesda.gov.ph</a>.
        """        


    else:
        return "❓ I didn’t catch that. Try typing qualifications, enrolment, assessment, or contact—or just use the buttons above."
        
# --------------------------
# Page config and session
# --------------------------
st.set_page_config(page_title="Simple Chatbot", page_icon="🤖", layout="wide")

if "messages" not in st.session_state:
    # messages is a list of tuples: (role, text)
    st.session_state.messages = [("Bot", " 👋 Hi! I'm the TESDA BIT Chatbot. Ask about qualifications, enrolment, assessment, or contact us—just tap a button or type below.")]

# last_action will hold a quick-action command when a button is clicked
if "last_action" not in st.session_state:
    st.session_state.last_action = None

# --------------------------
# Sidebar info + reset
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
# Determine user_input:
# - priority: last_action (button) -> chat_input (if available) -> text_input fallback
# --------------------------
user_input = None

# If a button was clicked (last_action set), consume it exactly once
if st.session_state.last_action:
    user_input = st.session_state.last_action
    # clear it immediately so it won't repeat on next run
    st.session_state.last_action = None

# Try to use chat_input (Streamlit >= 1.25). If not available, fall back to text_input.
try:
    # chat_input returns a value only when user submits
    if user_input is None:
        chat_in = st.chat_input("Type your message here...")
        if chat_in:
            user_input = chat_in
except Exception:
    # fallback to text_input with a session_state key so we can clear it after processing
    if user_input is None:
        # use a session key so we can reset it safely
        if "typed_value" not in st.session_state:
            st.session_state.typed_value = ""
        typed = st.text_input("Type your message here:", value=st.session_state.typed_value, key="typed_value")
        # Only process if not empty and not same as last processed (to avoid reprocessing)
        if typed and (len(st.session_state.messages) == 0 or st.session_state.messages[-1] != ("You", typed)):
            user_input = typed

# --------------------------
# Process a single user_input (if any)
# --------------------------
if user_input:
    # Append user message
    st.session_state.messages.append(("You", user_input))

    # Simulate typing effect (non-blocking visual)
    with st.spinner("Bot is typing..."):
        time.sleep(0.9)

    # Get bot reply
    try:
        bot_reply = chatbot_response(user_input)
    except Exception as e:
        bot_reply = f"⚠️ An internal error occurred while generating a reply: {e}"

    st.session_state.messages.append(("Bot", bot_reply))

    # If using the text_input fallback, clear stored value after processing
    if "typed_value" in st.session_state:
        st.session_state.typed_value = ""

# --------------------------
# Display conversation safely
# --------------------------
for entry in st.session_state.messages:
    # defensive check to avoid unpacking errors
    if not (isinstance(entry, (list, tuple)) and len(entry) == 2):
        # skip malformed entries
        continue
    role, msg = entry
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
# Fixed bottom button bar
# --------------------------
st.markdown("""
    <style>
    .fixed-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f9f9f9;
        padding: 10px 20px;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
        z-index: 9999;
    }
    .button-row {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
    }
    .button-row > div {
        flex: 1;
        margin: 5px;
    }
    </style>
    <div class="fixed-bottom">
        <div class="button-row">
            <div><button onclick="streamlitSend('qualifications')">🎓 Qualifications Offered</button></div>
            <div><button onclick="streamlitSend('enrolment')">📝 Enrolment</button></div>
            <div><button onclick="streamlitSend('assessment')">📊 Assessment</button></div>
            <div><button onclick="streamlitSend('contact')">📞 Contact Us</button></div>
        </div>
    </div>
    <script>
    function streamlitSend(action) {
        const input = window.parent.document.querySelector('input[type="text"]');
        if (input) {
            input.value = action;
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.form.dispatchEvent(new Event('submit'));
        }
    }
    </script>
""", unsafe_allow_html=True)

