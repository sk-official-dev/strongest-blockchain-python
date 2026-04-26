import streamlit as st

# Page Configuration
st.set_page_config(page_title="Saksham Katkar Portfolio", page_icon="🚀")

# Title and Identity
st.title("🚀 Saksham Katkar")
st.subheader("Official Developer (sk-official-dev)")

# --- Contact & Links (इथे आता लिंक काम करेल) ---
st.header("Contact & Links")
col1, col2 = st.columns(2)

with col1:
    st.write("👤 **Name:** Saksham Katkar")
    st.write("📞 **Mobile:** +91 7498942946")
    st.write("🔗 **GitHub Profile:** [github.com/sk-official-dev](https://github.com/sk-official-dev)")

with col2:
    st.write("📧 **Email:** sakshamkatkar86@gmail.com")
    st.write("📂 **Main Project:** [Blockchain Land Registry](https://github.com/sk-official-dev/strongest-blockchain-python)")

st.write("---")

# About Me Section
st.header("About Me")
st.write("""
I am a 12th-grade student currently preparing for **CET & JEE 2026**.  
Beyond academics, I am deeply passionate about coding and software development. 
My goal is to build technology that solves real-world security and accessibility problems.
""")

# Projects Section
st.header("My Projects")

# Project 1 with Link
with st.expander("🔗 Project 1: Secure Land Registry Blockchain"):
    st.write("**Description:** A high-security blockchain architecture designed to keep land records safe and tamper-proof.")
    st.info("Status: My First Major Project - 50% Completed")
    st.write("**Direct Link:** [View Code on GitHub](https://github.com/sk-official-dev/strongest-blockchain-python)")

# Project 2
with st.expander("🤖 Project 2: Free AI Tool (Saksham AI)"):
    st.write("**Description:** An offline AI tool designed to run at zero cost (0 INR) for everyone.")
    st.success("Goal: Making AI accessible to all without subscriptions.")

# Future Goals
st.header("Future Goals")
st.write("I am constantly learning and building. More advanced projects are coming soon!")

# Footer
st.write("---")
st.caption("Made with ❤️ by Saksham Katkar")