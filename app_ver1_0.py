import streamlit as st
import math
import pandas as pd

# ===== PAGE CONFIG =====
st.set_page_config(layout="wide")

# ===== CSS FIX =====
st.markdown("""
<style>

/* GLOBAL */
.stApp {
    background-color: #F1F3F6;
    font-family: "Segoe UI", Arial;
}

/* FIX TEXT VISIBILITY */
html, body, p, div, span, label {
    color: #111111 !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #1F5AA6 !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* MAIN BOX */
.main-container {
    background-color: white;
    padding: 25px;
    border-radius: 10px;
}

/* INPUTS */
input, textarea {
    background-color: white !important;
    color: black !important;
}

/* SELECT */
div[data-baseweb="select"] {
    background-color: white !important;
    color: black !important;
}

/* BUTTON */
.stButton button {
    background-color: #1558A6;
    color: white;
}

/* TABLE */
[data-testid="stDataFrame"] * {
    color: black !important;
}

/* ALERT FIX */
div[data-testid="stAlert"] {
    background-color: #FFFFFF !important;
    color: black !important;
    border-left: 5px solid #1558A6;
}

</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
st.sidebar.image("Logo1.png", width=180)
st.sidebar.markdown("### International Clearing And Shipping Agency")

st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Menu",
    ["Vehicle Calculator", "Vehicle Master Data", "Cargo Types Master Data"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("👤 Welcome User")

# ===== MASTER DATA =====
vehicle_master = pd.DataFrame([
    ["32 ft Truck", 32, 8, 8],
    ["40 ft Trailer", 40, 8, 8.5],
    ["40 ft High", 40, 8, 10],
], columns=["Vehicle", "Length(ft)", "Width(ft)", "Height(ft)"])

cargo_master = pd.DataFrame([
    ["Standard Cargo", "Normal shipment"],
    ["Heavy Cargo", "CBM > 30"],
    ["ODC", "Height > limit"]
], columns=["Cargo Type", "Description"])

# ===== MAIN =====
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ===== MENU LOGIC =====

# ================= VEHICLE MASTER =================
if menu == "Vehicle Master Data":
    st.title("🚚 Vehicle Master Data")
    st.dataframe(vehicle_master, use_container_width=True)

# ================= CARGO MASTER =================
elif menu == "Cargo Types Master Data":
    st.title("📦 Cargo Types Master Data")
    st.dataframe(cargo_master, use_container_width=True)

# ================= MAIN CALCULATOR =================
else:
    st.title("🚚 Vehicle Load Calculator")

    left, right = st.columns([1, 1])

    # INPUT
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

    # FUNCTIONS
    def to_feet(value, unit):
        return {"mm": value/304.8, "cm": value/30.48, "m": value*3.28, "inch": value/12}[unit]

    def to_meters(value, unit):
        return {"mm": value/1000, "cm": value/100, "m": value, "inch": value*0.0254}[unit]

    # RESULTS
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
                total_cbm = CBM * qty

                st.subheader("📦 Summary")
                st.write("CBM per package:", CBM)
                st.write("Total CBM:", total_cbm)

                st.subheader("📏 Dimensions")
                st.write("Feet:", round(L_ft,2), "x", round(W_ft,2), "x", round(H_ft,2))
                st.write("Meters:", round(L_m,2), "x", round(W_m,2), "x", round(H_m,2))

                if H_ft > 10:
                    st.error("ODC Cargo")
                elif CBM > 30:
                    st.warning("Heavy Cargo")
                else:
                    st.success("Standard Cargo")

            else:
                st.warning("Enter all values")

st.markdown('</div>', unsafe_allow_html=True)
