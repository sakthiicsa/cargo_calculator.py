import streamlit as st
import math
import pandas as pd

st.set_page_config(layout="wide")

# ===== PREMIUM UI CSS =====
st.markdown("""
<style>

/* ===== GLOBAL ===== */
.stApp {
    background: #F4F7FB;
    font-family: 'Segoe UI', sans-serif;
}

/* Remove default padding */
.block-container {
    padding-top: 2rem;
}

/* ===== HEADER ===== */
.header-box {
    background: white;
    padding: 15px 25px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    display: flex;
    align-items: center;
}

.company-title {
    font-size: 28px;
    font-weight: 700;
    color: #0A2540;
}

/* ===== CARDS ===== */
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
    margin-bottom: 20px;
}

/* ===== INPUTS ===== */
input, textarea {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border-radius: 6px !important;
}

/* ===== BUTTON ===== */
.stButton button {
    background: linear-gradient(135deg, #2E8BC0, #1B6CA8);
    color: white;
    font-weight: 600;
    border-radius: 8px;
    height: 45px;
    width: 100%;
}

/* ===== TABLE ===== */
table {
    color: black !important;
}

/* ===== ALERT CLEAN ===== */
div[data-testid="stAlert"] {
    background-color: #FFFFFF !important;
    border-left: 5px solid #2E8BC0 !important;
    border-radius: 8px;
}

/* ===== SUBHEADERS ===== */
h2 {
    color: #0A2540;
}

</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
col1, col2 = st.columns([1,5])

with col1:
    st.image("Logo1.png", width=120)

with col2:
    st.markdown("<div class='company-title'>International Clearing And Shipping Agency</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== MAIN LAYOUT =====
left, right = st.columns([1,1])

# ================= LEFT CARD =================
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📥 Input Details")

    unit = st.selectbox("Select Unit", ["mm", "cm", "m", "inch"])

    col1, col2, col3 = st.columns(3)

    with col1:
        L = st.number_input("Length", min_value=0.0)

    with col2:
        W = st.number_input("Width", min_value=0.0)

    with col3:
        H = st.number_input("Height", min_value=0.0)

    qty = st.number_input("Number of Packages", min_value=1)

    calculate = st.button("🚀 Calculate")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= FUNCTIONS =================
def to_feet(value, unit):
    return {
        "mm": value / 304.8,
        "cm": value / 30.48,
        "m": value * 3.28084,
        "inch": value / 12
    }[unit]

def to_meters(value, unit):
    return {
        "mm": value / 1000,
        "cm": value / 100,
        "m": value,
        "inch": value * 0.0254
    }[unit]

vehicles = [
    {"name": "32 ft Truck", "L": 32, "W": 8, "H": 8},
    {"name": "40 ft Trailer", "L": 40, "W": 8, "H": 8.5},
    {"name": "40 ft High", "L": 40, "W": 8, "H": 10},
    {"name": "45 ft Trailer", "L": 45, "W": 8, "H": 8.5},
    {"name": "45 ft High", "L": 45, "W": 8, "H": 10},
    {"name": "Open Truck", "L": 40, "W": 8, "H": 6},
    {"name": "Flatbed", "L": 40, "W": 8, "H": None},
]

# ================= RIGHT CARD =================
with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    st.subheader("📊 Results")

    if calculate:

        if L > 0 and W > 0 and H > 0:

            L_ft = to_feet(L, unit)
            W_ft = to_feet(W, unit)
            H_ft = to_feet(H, unit)

            L_m = to_meters(L, unit)
            W_m = to_meters(W, unit)
            H_m = to_meters(H, unit)

            CBM = round(L_m * W_m * H_m, 3)
            total_cbm = round(CBM * qty, 3)

            st.markdown("### 📦 Summary")
            st.write(f"CBM per package: **{CBM}**")
            st.write(f"Total CBM: **{total_cbm}**")

            if H_ft > 10:
                st.error("ODC Cargo")
            elif CBM > 30:
                st.warning("Heavy Cargo")
            else:
                st.success("Standard Cargo")

            # ===== VEHICLE =====
            results = []

            for v in vehicles:
                if v["H"] is None:
                    fit = int(v["L"] // L_ft) * int(v["W"] // W_ft)
                else:
                    fit = int(v["L"] // L_ft) * int(v["W"] // W_ft) * int(v["H"] // H_ft)

                if fit > 0:
                    needed = math.ceil(qty / fit)
                    results.append([v["name"], fit, needed])

            df = pd.DataFrame(results, columns=["Vehicle", "Fit", "Required"])

            st.markdown("### 🚚 Vehicle Plan")
            st.table(df)

        else:
            st.warning("Enter all dimensions")

    st.markdown("</div>", unsafe_allow_html=True)
