import streamlit as st
import google.generativeai as genai
from datetime import datetime

st.set_page_config(page_title="AI Chat Support Bot", page_icon="🤖", layout="wide")

# ====================== YOUR GEMINI KEY ======================
genai.configure(api_key="AIzaSyANtAmTxY-RX-4DnDZNvkrZsUymoB2QXgE")

model = genai.GenerativeModel('gemini-2.5-flash')

st.title("🤖 AI Chat Support Bot - TechMart")
st.caption("Built by Muhammad Talha | Virtual Assistant & Customer Support Specialist")

# ====================== SIDEBAR (Professional Look) ======================
with st.sidebar:
    st.header("🚀 About this Project")
    st.write("**Skills demonstrated:**")
    st.write("• Live Chat Support")
    st.write("• Ticket Management (Zendesk style)")
    st.write("• Order Data Lookup")
    st.write("• AI Automation")
    st.divider()
    st.write("**Tech:** Python • Streamlit • Google Gemini API")
    st.write(f"**Session started:** {datetime.now().strftime('%H:%M:%S')}")

    # Show created tickets in sidebar
    if "tickets" not in st.session_state:
        st.session_state.tickets = []
    if st.session_state.tickets:
        st.subheader("📋 Your Tickets")
        for t in st.session_state.tickets:
            st.write(f"**#{t['id']}** - {t['status']}")

# ====================== FAKE ORDER DATABASE ======================
fake_orders = {
    "TM-1001": {"status": "Shipped", "date": "2026-04-05", "items": "iPhone 13 + Charger", "tracking": "TRK987654"},
    "TM-1002": {"status": "Delivered", "date": "2026-04-03", "items": "Samsung Galaxy Buds", "tracking": "TRK123456"},
    "TM-1003": {"status": "Processing", "date": "2026-04-07", "items": "Laptop Stand + Mouse", "tracking": "Not available yet"}
}

# ====================== SYSTEM PROMPT (Brain of the AI) ======================
SYSTEM_PROMPT = """
You are a friendly, professional AI Customer Support Agent for TechMart (e-commerce store).
Answer ONLY using the knowledge below. Be polite and helpful.
If the question is not covered, offer to escalate or create a ticket.

FAQ:
- Track order → Use Order Lookup tool or check "My Orders".
- Return policy → 30 days, unused with packaging.
- Shipping time → Standard: 5-7 days | Express: 2-3 days.
- Payment → Cards, PayPal, JazzCash, EasyPaisa.
- Cancel order → Within 24 hours.
- Human support → Click "Escalate to Human" or create ticket.
"""

# ====================== INITIALIZE SESSION STATE ======================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! 👋 Welcome to TechMart AI Support. How can I help you today?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ====================== QUICK ACTION BUTTONS ======================
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("🔍 Track My Order", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Track my order"})
        st.rerun()
with col2:
    if st.button("📦 Return Policy", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "What is your return policy?"})
        st.rerun()
with col3:
    if st.button("🧾 Create Ticket", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "I want to create a support ticket"})
        st.rerun()
with col4:
    if st.button("📧 Export Chat", use_container_width=True):
        st.session_state.messages.append({"role": "user", "content": "Export this chat as email"})
        st.rerun()

# ====================== MAIN CHAT LOGIC ======================
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            full_prompt = SYSTEM_PROMPT + "\n\nConversation history:\n"
            for m in st.session_state.messages:
                if m["role"] == "user":
                    full_prompt += f"User: {m['content']}\n"
                elif m["role"] == "assistant":
                    full_prompt += f"Assistant: {m['content']}\n"

            response = model.generate_content(full_prompt)
            answer = response.text
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

# ====================== SPECIAL FEATURES (Order Lookup + Ticket + Export) ======================
# These run after every rerun

# 1. Order Lookup
if len(st.session_state.messages) > 0 and "track my order" in st.session_state.messages[-1]["content"].lower():
    order_id = st.text_input("Enter your Order ID (e.g. TM-1001):", key="order_input")
    if st.button("🔍 Lookup Order"):
        if order_id in fake_orders:
            order = fake_orders[order_id]
            st.success(f"✅ Order {order_id} found!")
            st.write(f"**Status:** {order['status']}")
            st.write(f"**Date:** {order['date']}")
            st.write(f"**Items:** {order['items']}")
            st.write(f"**Tracking:** {order['tracking']}")
        else:
            st.error("Order ID not found. Please check and try again.")

# 2. Create Ticket
if len(st.session_state.messages) > 0 and "create a support ticket" in st.session_state.messages[-1]["content"].lower():
    with st.form("ticket_form"):
        subject = st.text_input("Subject")
        issue = st.text_area("Describe your issue")
        if st.form_submit_button("Submit Ticket"):
            ticket_id = f"TK-{len(st.session_state.tickets) + 1000}"
            st.session_state.tickets.append({
                "id": ticket_id,
                "subject": subject,
                "issue": issue,
                "status": "Open"
            })
            st.success(f"✅ Ticket #{ticket_id} created successfully!")

# 3. Export Chat as Email
if len(st.session_state.messages) > 0 and "export this chat" in st.session_state.messages[-1]["content"].lower():
    st.subheader("📧 Chat Transcript")
    transcript = "\n\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state.messages])
    st.code(transcript, language=None)
    st.download_button("Download as .txt", transcript, file_name="chat_transcript.txt")