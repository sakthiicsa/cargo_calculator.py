import streamlit as st
import math
import pandas as pd

# ===== PAGE CONFIG =====
st.set_page_config(layout="wide")

# =====CSS =====
st.markdown("""
<style>

/* ===== GLOBAL ===== */
.stApp {
    background-color: #F1F3F6;
    font-family: "Segoe UI", Arial, sans-serif;
}

/* FIX ALL TEXT VISIBILITY */
html, body, [class*="css"]  {
    color: #111111 !important;
}

/* ===== HEADER ===== */
.top-header {
    background-color: #1558A6;
    padding: 14px 20px;
    color: white !important;
    font-size: 20px;
    font-weight: 600;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #1F5AA6 !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] * {
    color: white !important;
    font-size: 14px;
}

/* ===== MAIN CONTENT ===== */
.main-container {
    background-color: white;
    padding: 25px;
    border-radius: 10px;
}

/* ===== HEADINGS ===== */
h1, h2, h3 {
    color: #0A2540 !important;
    font-weight: 600;
}

/* ===== LABELS ===== */
label {
    color: #333 !important;
    font-weight: 600;
}

/* ===== INPUT FIELDS ===== */
input, textarea {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #D0D5DD !important;
    border-radius: 6px;
}

/* Selectbox */
div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

/* ===== BUTTON ===== */
.stButton button {
    background-color: #1558A6 !important;
    color: white !important;
    border-radius: 6px;
    font-weight: 600;
}

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"] * {
    color: #000000 !important;
}

/* ===== ALERTS ===== */
div[data-testid="stAlert"] {
    background-color: #2A52A8 !important;
    border-left: 5px solid #1558A6 !important;
    color: #000000 !important;
}

/* REMOVE FADED EFFECT */
section.main > div {
    opacity: 1 !important;
}

</style>
""", unsafe_allow_html=True)

# ===== HEADER =====


# ===== SIDEBAR (STATIC LIKE IMAGE) =====
st.sidebar.markdown("""
<div>
<h3> st.image("Logo1.png", width=220) </h3>
<p> st.markdown('<div class="top-header">International Clearing And Shipping Agency</div>', unsafe_allow_html=True)
<br><hr>

<p>👤 Welcome User</p>

</div>
""", unsafe_allow_html=True)

# ===== MAIN CONTAINER =====
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.title("🚚 Vehicle Load Calculator")

left, right = st.columns([1, 1])

# ===== INPUT =====
with left:
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

# ===== FUNCTIONS =====
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

# ===== VEHICLES =====
vehicles = [
    {"name": "32 ft Truck", "L": 32, "W": 8, "H": 8},
    {"name": "40 ft Trailer", "L": 40, "W": 8, "H": 8.5},
    {"name": "40 ft High", "L": 40, "W": 8, "H": 10},
    {"name": "45 ft Trailer", "L": 45, "W": 8, "H": 8.5},
    {"name": "45 ft High", "L": 45, "W": 8, "H": 10},
    {"name": "Open Truck", "L": 40, "W": 8, "H": 6},
    {"name": "Flatbed", "L": 40, "W": 8, "H": None},
]

# ===== RESULTS =====
with right:
    st.subheader("📊 Results")

    if st.button("Calculate"):

        if L > 0 and W > 0 and H > 0:

            L_ft = to_feet(L, unit)
            W_ft = to_feet(W, unit)
            H_ft = to_feet(H, unit)

            L_m = to_meters(L, unit)
            W_m = to_meters(W, unit)
            H_m = to_meters(H, unit)

            CBM = round(L_m * W_m * H_m, 3)
            total_cbm = round(CBM * qty, 3)

            st.subheader("📦 Summary")
            st.write(f"CBM per package: {CBM}")
            st.write(f"Total CBM: {total_cbm}")
            st.write(f"Quantity: {qty}")

            st.subheader("📏 Dimensions")
            st.write(f"Feet: {round(L_ft,2)} × {round(W_ft,2)} × {round(H_ft,2)} ft")
            st.write(f"Meters: {round(L_m,2)} × {round(W_m,2)} × {round(H_m,2)} m")

            if H_ft > 10:
                st.error("🚨 ODC Cargo")
            elif CBM > 30:
                st.warning("⚠️ Heavy Cargo")
            else:
                st.success("✅ Standard Cargo")

            st.subheader("🚚 Vehicle Recommendation")

            results = []

            for v in vehicles:
                if v["H"] is None:
                    fit = int(v["L"] // L_ft) * int(v["W"] // W_ft)
                else:
                    fit = int(v["L"] // L_ft) * int(v["W"] // W_ft) * int(v["H"] // H_ft)

                if fit > 0:
                    results.append({
                        "Vehicle": v["name"],
                        "Fit": fit,
                        "Required": math.ceil(qty / fit)
                    })

            df = pd.DataFrame(results)
            st.dataframe(df, use_container_width=True)

        else:
            st.warning("⚠️ Please enter all values")

st.markdown('</div>', unsafe_allow_html=True)
