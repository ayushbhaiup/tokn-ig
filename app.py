import streamlit as st
import requests
import time

st.set_page_config(
    page_title="YKTI — Instagram Token Extractor",
    page_icon="⚡",
    layout="centered"
)

# ── Custom CSS ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif !important; }

.stApp {
    background: radial-gradient(circle at top left, #0f0c1a, #0a0a12);
    color: #e8e8f0;
}

.main-header {
    text-align: center;
    padding: 30px 0 10px;
}
.badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(245,200,66,0.15), rgba(255,79,163,0.1));
    border: 1px solid rgba(245,200,66,0.3);
    border-radius: 100px;
    padding: 6px 20px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    color: #f5c842;
    margin-bottom: 16px;
}
.main-title {
    font-size: 42px;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -1px;
    margin-bottom: 8px;
}
.grad { 
    background: linear-gradient(135deg, #f5c842, #ff4fa3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle { font-size: 13px; color: rgba(232,232,240,0.5); margin-bottom: 30px; }

.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 20px;
}

.token-box {
    background: rgba(0,0,0,0.5);
    border: 1px solid rgba(0,255,224,0.2);
    border-radius: 12px;
    padding: 14px 16px;
    font-family: 'DM Mono', monospace;
    font-size: 13px;
    color: #00ffe0;
    word-break: break-all;
    margin-bottom: 8px;
}
.token-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: rgba(232,232,240,0.4);
    margin-bottom: 6px;
    margin-top: 14px;
}
.success-box {
    background: linear-gradient(135deg, rgba(57,255,154,0.08), rgba(0,255,224,0.05));
    border: 1px solid rgba(57,255,154,0.25);
    border-radius: 14px;
    padding: 20px;
    margin-top: 20px;
}
.error-box {
    background: rgba(255,79,106,0.08);
    border: 1px solid rgba(255,79,106,0.3);
    border-radius: 14px;
    padding: 16px 20px;
    color: #ff4f6a;
    margin-top: 20px;
    font-size: 14px;
}
.warn-box {
    background: rgba(245,200,66,0.05);
    border: 1px solid rgba(245,200,66,0.15);
    border-radius: 10px;
    padding: 12px 16px;
    font-size: 12px;
    color: rgba(245,200,66,0.7);
    margin-bottom: 20px;
}
.footer {
    text-align: center;
    padding: 20px 0;
    font-size: 11px;
    color: rgba(255,255,255,0.2);
    letter-spacing: 2px;
    text-transform: uppercase;
}
.footer span { color: #f5c842; }

/* Button styling */
.stButton > button {
    width: 100%;
    padding: 16px !important;
    background: linear-gradient(135deg, #f5c842, #e8a020) !important;
    color: #080600 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 800 !important;
    font-size: 14px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 12px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 40px rgba(245,200,66,0.4) !important;
}

/* Input styling */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #e8e8f0 !important;
    font-family: 'Syne', sans-serif !important;
    padding: 14px 16px !important;
}
.stTextInput > div > div > input:focus {
    border-color: rgba(245,200,66,0.45) !important;
    box-shadow: 0 0 0 3px rgba(245,200,66,0.07) !important;
}
label { color: rgba(232,232,240,0.5) !important; font-size: 10px !important; letter-spacing: 2px !important; text-transform: uppercase !important; }

div[data-testid="stDecoration"] { display: none; }
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="badge">⚡ YK TRICKS INDIA ⚡</div>
    <div class="main-title">Instagram<br><span class="grad">Token Extractor</span></div>
    <div class="subtitle">Session ID & User Token — Instant Extract</div>
</div>
""", unsafe_allow_html=True)

# ── Warning ──────────────────────────────────────────────────
st.markdown("""
<div class="warn-box">
⚠️ <strong style="color:#f5c842">Note:</strong> 
Data sirf Instagram ke official servers pe jaata hai. 
Koi credentials store nahi hote. Apna personal account use karo.
</div>
""", unsafe_allow_html=True)

# ── Form ─────────────────────────────────────────────────────
username = st.text_input("👤  Instagram Username", placeholder="your_username")
password = st.text_input("🔑  Password", placeholder="••••••••••••", type="password")

# ── Login Function ───────────────────────────────────────────
def login_instagram(username, password):
    login_url = "https://www.instagram.com/accounts/login/ajax/"
    session = requests.Session()

    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
    })

    try:
        r1 = session.get("https://www.instagram.com/accounts/login/", timeout=20)
        csrf_token = session.cookies.get("csrftoken", "")

        if not csrf_token:
            return {"success": False, "error": "CSRF token nahi mila. Internet check karo ya Instagram band hai."}

        time.sleep(1)

        session.headers.update({
            "X-CSRFToken": csrf_token,
            "X-Instagram-AJAX": "1",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.instagram.com/accounts/login/",
            "Origin": "https://www.instagram.com",
            "Content-Type": "application/x-www-form-urlencoded",
        })

        payload = {
            "username": username,
            "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}",
            "queryParams": "{}",
            "optIntoOneTap": "false",
        }

        r2 = session.post(login_url, data=payload, timeout=20)

        try:
            resp = r2.json()
        except Exception:
            return {"success": False, "error": f"Instagram response parse nahi hua: {r2.text[:200]}"}

        if resp.get("authenticated"):
            cookies = {c.name: c.value for c in session.cookies}
            return {
                "success": True,
                "sessionid": cookies.get("sessionid", ""),
                "ds_user_id": cookies.get("ds_user_id", ""),
                "username": username,
            }
        elif resp.get("two_factor_required"):
            return {"success": False, "error": "2FA ON hai. Instagram app mein 2FA band karo phir try karo."}
        elif resp.get("checkpoint_url"):
            return {"success": False, "error": "Instagram ne checkpoint diya. App mein verify karo phir retry karo."}
        elif resp.get("user") is False:
            return {"success": False, "error": "Username galat hai ya account nahi hai."}
        elif resp.get("authenticated") is False:
            return {"success": False, "error": "Password galat hai."}
        else:
            return {"success": False, "error": f"Login failed: {str(resp)[:200]}"}

    except requests.exceptions.Timeout:
        return {"success": False, "error": "Timeout. Internet check karo."}
    except Exception as e:
        return {"success": False, "error": str(e)}

# ── Button ───────────────────────────────────────────────────
if st.button("⚡  EXTRACT TOKEN"):
    if not username or not password:
        st.markdown('<div class="error-box">⚠️ Username aur Password dono daalo!</div>', unsafe_allow_html=True)
    else:
        with st.spinner("🔐 Instagram se connect ho raha hai..."):
            result = login_instagram(username, password)

        if result["success"]:
            st.markdown('<div class="success-box">', unsafe_allow_html=True)
            st.markdown("### ✅ Token Extracted Successfully!")

            st.markdown('<div class="token-label">Session ID (Token)</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="token-box">{result["sessionid"]}</div>', unsafe_allow_html=True)
            st.code(result["sessionid"], language=None)

            st.markdown('<div class="token-label">DS User ID</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="token-box">{result["ds_user_id"]}</div>', unsafe_allow_html=True)
            st.code(result["ds_user_id"], language=None)

            st.markdown('<div class="token-label">Username</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="token-box">{result["username"]}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.success("✅ Upar wale boxes se Copy kar lo!")
        else:
            st.markdown(f'<div class="error-box">❌ {result["error"]}</div>', unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────
st.markdown("""
<div class="footer">
Powered by <span>YKTI</span> — YK Tricks India<br>
<a href="https://wa.me/918115048433" style="color:rgba(255,79,163,0.6); text-decoration:none;">
📲 WhatsApp: +91 8115048433
</a>
</div>
""", unsafe_allow_html=True)
