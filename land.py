import streamlit as st
import hashlib
import json
import os
import cv2
import numpy as np
import base64
import qrcode
from time import time, ctime
from fpdf import FPDF
from io import BytesIO
from PIL import Image

# --- १. USER SECURITY (Admin & User Roles) ---
USER_DB = {
    "admin": "sk123",    # ऑफिसरसाठी - सर्व अधिकार
    "user": "land789"    # नागरिक - फक्त पाहण्यासाठी
}

# --- २. AI IMAGE GUARD (कागदपत्र तपासणी) ---
def is_valid_document(image_file):
    try:
        file_bytes = np.asarray(bytearray(image_file.read()), dtype=np.uint8)
        img = cv2.imdecode(file_bytes, 1)
        if img is None:
            return False, "फाईल वाचता आली नाही."
        
        # Blur Detection (अंधूकपणा तपासणे)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # जर फोटो खूप अंधूक असेल तर (Threshold: 50)
        if laplacian_var < 50:
            return False, f"AI ने रिजेक्ट केले: फोटो खूप अंधूक (Blur) आहे. (Score: {int(laplacian_var)})"
        
        return True, "Success"
    except Exception as e:
        return False, f"एरर: {str(e)}"

# --- ३. BLOCKCHAIN ENGINE ---
class Blockchain:
    def __init__(self):
        self.file_name = 'land_data.json'
        self.chain = []
        self.load_data()

    def hash(self, block):
        block_copy = block.copy()
        block_copy.pop('hash', None)
        encoded_block = json.dumps(block_copy, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def create_block(self, owner, location, area, image_data=None):
        prev_hash = self.chain[-1]['hash'] if self.chain else '0'
        block = {
            'index': len(self.chain) + 1,
            'timestamp': ctime(time()),
            'owner': owner,
            'location': location,
            'area': area,
            'image': image_data,
            'previous_hash': prev_hash,
        }
        block['hash'] = self.hash(block)
        self.chain.append(block)
        self.save_data()

    def save_data(self):
        with open(self.file_name, 'w') as f:
            json.dump(self.chain, f, indent=4)

    def load_data(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as f:
                self.chain = json.load(f)
        else:
            self.create_block("Government Authority", "Root System", "0", None)

# --- ४. UTILITY FUNCTIONS (QR & PDF) ---
def generate_qr(data):
    qr = qrcode.make(data)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    return buf.getvalue()

def generate_pdf(block, qr_bytes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 20)
    pdf.cell(200, 10, "SK SECURE BLOCKCHAIN REGISTRY", ln=True, align='C')
    pdf.ln(10)
    
    # QR Code on PDF
    qr_filename = f"temp_qr_{block['index']}.png"
    with open(qr_filename, "wb") as f:
        f.write(qr_bytes)
    pdf.image(qr_filename, x=165, y=10, w=30)
    os.remove(qr_filename)

    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Block Index: {block['index']}", ln=True)
    pdf.cell(200, 10, f"Owner: {block['owner']}", ln=True)
    pdf.cell(200, 10, f"Location: {block['location']}", ln=True)
    pdf.cell(200, 10, f"Area: {block['area']}", ln=True)
    pdf.cell(200, 10, f"Time: {block['timestamp']}", ln=True)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Hash: {block['hash']}")
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 10, "Digitally Signed and Verified by SK-Blockchain", ln=True, align='R')
    return pdf.output(dest='S').encode('latin-1')

# --- ५. WEB INTERFACE (STREAMLIT) ---
st.set_page_config(page_title="SK Pro Blockchain", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔒 Enterprise Security Login")
    user = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if user in USER_DB and USER_DB[user] == password:
            st.session_state.logged_in = True
            st.session_state.user_role = user
            st.rerun()
        else:
            st.error("Access Denied: Invalid Credentials")
else:
    bc = Blockchain()
    st.sidebar.success(f"Welcome, {st.session_state.user_role.upper()}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🏛️ Decentralized Land Registry System")

    # ADMIN SECTION: नवीन नोंदणी
    if st.session_state.user_role == "admin":
        with st.expander("➕ Register New Land Record (AI & Blockchain Secured)"):
            c1, c2 = st.columns(2)
            with c1:
                owner = st.text_input("Owner Full Name")
                loc = st.text_input("Land Location/Address")
            with c2:
                area = st.text_input("Total Area (Sq. Ft/Acres)")
                up = st.file_uploader("Upload Land Document (7/12 Extract)", type=['jpg', 'png', 'jpeg'])
            
            if st.button("Verify & Secure"):
                if owner and loc and area and up:
                    # AI Verification
                    is_ok, msg = is_valid_document(up)
                    if is_ok:
                        up.seek(0)
                        img_b64 = base64.b64encode(up.read()).decode()
                        bc.create_block(owner, loc, area, img_b64)
                        st.balloons()
                        st.success("AI Verified & Blockchain Secured!")
                    else:
                        st.error(msg)
                else:
                    st.warning("कृपया सर्व माहिती भरा.")

    # USER & ADMIN: रेकॉर्ड पाहणे
    st.divider()
    st.subheader("📜 Verified Digital Records")
    
    for b in reversed(bc.chain):
        with st.container():
            col_img, col_txt, col_qr, col_btn = st.columns([1, 2, 1, 1])
            with col_img:
                if b.get('image'):
                    st.image(base64.b64decode(b['image']), width=130)
                else:
                    st.info("No Image")
            with col_txt:
                st.markdown(f"### Block #{b['index']}")
                st.write(f"**Owner:** {b['owner']}")
                st.write(f"**Location:** {b['location']}")
                st.write(f"**Hash:** `{b['hash'][:20]}...`")
            
            qr_data = f"Owner: {b['owner']}, Hash: {b['hash']}"
            qr_bytes = generate_qr(qr_data)
            with col_qr:
                st.image(qr_bytes, width=100)
                st.caption("Scan to Verify")
            
            with col_btn:
                pdf_data = generate_pdf(b, qr_bytes)
                st.download_button(f"📥 Certificate", data=pdf_data, file_name=f"Record_{b['index']}.pdf")
            st.divider()