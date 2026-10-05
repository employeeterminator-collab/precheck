import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Shisa Kanko Examination - System Readiness Check",
    page_icon="🛠️",
    layout="centered"
)

# Hide anchor link icons next to headers
st.markdown(
    """
    <style>
    [data-testid="stHeaderActionElements"], a.header-anchor {
        display: none !important;
    }
    .status-box-pass {
        padding: 15px; border-radius: 8px; background-color: #d1e7dd; 
        color: #0f5132; border: 1px solid #badbcc; margin-bottom: 15px;
    }
    .status-box-fail {
        padding: 15px; border-radius: 8px; background-color: #f8d7da; 
        color: #842029; border: 1px solid #f5c2c7; margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛠️ Pre-Exam System Readiness Check")
st.write("Please complete all system diagnostics on the desktop or laptop computer and network you intend to use for the examination.")

# Track camera test in session state
if "camera_verified" not in st.session_state:
    st.session_state.camera_verified = False

# Step 1: Client-Side JS Device & Storage Reachability Diagnostic
st.subheader("1. Device & Network Route Check")

components.html(
    """
    <div id="diag-container">🔍 Running device & network diagnostics...</div>

    <script>
    async function runCheck() {
        const results = {
            isMobile: false,
            storageAccessible: false,
            overallPass: false,
            reasons: []
        };

        // 1. Mobile & Tablet Detection
        const ua = navigator.userAgent;
        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(ua) || (navigator.maxTouchPoints && navigator.maxTouchPoints > 2 && /Macintosh/.test(ua))) {
            results.isMobile = true;
            results.reasons.push("Mobile or tablet device detected. Examinations must be taken on a desktop or laptop computer.");
        }

        // 2. Image Storage Server Reachability Check
        try {
            const res = await fetch("https://api.imgbb.com/1/upload", { method: "OPTIONS" });
            results.storageAccessible = true;
        } catch (err) {
            results.storageAccessible = false;
            results.reasons.push("Unable to reach our image storage server. Please verify your internet connection or disable firewalls/VPNs.");
        }

        results.overallPass = !results.isMobile && results.storageAccessible;

        const container = document.getElementById("diag-container");
        if (results.overallPass) {
            container.innerHTML = `
                <div style="padding:12px; background:#d1e7dd; color:#0f5132; border-radius:6px; font-family:sans-serif;">
                    <b>✅ Device & Network Route Passed</b>
                </div>`;
        } else {
            let html = `<div style="padding:12px; background:#f8d7da; color:#842029; border-radius:6px; font-family:sans-serif;">
                <b>❌ System Readiness Failed</b><ul style="margin-top:5px; margin-bottom:0;">`;
            results.reasons.forEach(r => { html += `<li>${r}</li>`; });
            html += `</ul></div>`;
            container.innerHTML = html;
        }
    }
    runCheck();
    </script>
    """,
    height=130
)

# Step 2: Native Streamlit Camera Verification
st.subheader("2. Camera Hardware Verification")
st.caption("Please take a test snapshot below to grant and verify browser camera permissions.")

test_photo = st.camera_input("Take Test Snapshot")

if test_photo:
    st.success("✅ Camera hardware and permissions verified!")
    st.session_state.camera_verified = True

st.divider()

# Diagnostic Criteria Overview
st.subheader("Diagnostic Criteria Breakdown")
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🖥️ Device & Browser")
    st.markdown("- **Approved:** Desktop / Laptop (Mac or Windows PC)")
    st.markdown("- **Prohibited:** Mobile Phones & Tablets")
    st.markdown("- **Recommended Browser:** Google Chrome or Microsoft Edge")

with col2:
    st.markdown("### 🌐 Network & Hardware")
    st.markdown("- **Webcam:** Functional & Permission Granted")
    st.markdown("- **API Route:** Unblocked access to our image storage server")
    st.markdown("- **VPN / Proxy:** Must be turned OFF")

st.divider()

# Initialize pass status in session state
if "passed_precheck" not in st.session_state:
    st.session_state.passed_precheck = False

# Step 3: Candidate Verification & Access Gate
st.subheader("3. Final Verification & Launch")

c1 = st.checkbox("I am using a private home network (Not Hotel / Public / Corporate Wi-Fi)")
c2 = st.checkbox("I have disabled all active VPNs and proxy browser extensions")
c3 = st.checkbox("I am using a desktop or laptop computer with Google Chrome or Microsoft Edge")

# Verification Trigger
if st.button("Verify System Requirements", type="primary"):
    if not st.session_state.get("camera_verified", False):
        st.error("❌ System Readiness Failed: You must take a test snapshot above to verify your camera before proceeding.")
        st.session_state.passed_precheck = False
    elif not (c1 and c2 and c3):
        st.error("❌ Please confirm all self-verification checkboxes before attempting the exam.")
        st.session_state.passed_precheck = False
    else:
        st.success("✅ System Verification Passed! Click below to enter the examination.")
        st.session_state.passed_precheck = True

# Native Streamlit Link Button (Bypasses iframe security blocks)
if st.session_state.passed_precheck:
    st.divider()
    st.link_button(
        "🚀 Proceed to Official Examination Portal ➡️",
        "https://exam2.shisakanko.org/",
        type="primary",
        use_container_width=True
    )

st.divider()
