import streamlit as st
import math
import pandas as pd

# ===== PAGE CONFIG =====
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# ===== CLEAN CSS =====
st.markdown("""
<style>

/* GLOBAL */
.stApp {
    background-color: #F1F3F6;
    font-family: "Segoe UI", Arial;
}

/* TEXT FIX */
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

/* MAIN */
.main-container {
    background-color: white;
    padding: 25px;
    border-radius: 10px;
}

/* INPUT */
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
    border-radius: 6px;
    font-weight: 600;
}

/* TABLE FIX */
[data-testid="stDataFrame"] {
    background-color: Seafoam Green !important;
}
[data-testid="stDataFrame"] * {
    color: black !important;
}

/* ALERT */
div[data-testid="stAlert"] {
    background-color: Seafoam Green !important;
    color: black !important;
    border-left: 5px solid #1558A6;
}

</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR =====
st.sidebar.image("Logo1.png", width=160)
st.sidebar.markdown("### International Clearing And Shipping Agency")
st.sidebar.markdown("---")

# PROFESSIONAL MENU
menu = st.sidebar.selectbox(
    "Navigation",
    ["Vehicle Calculator", "Vehicle Master Data", "Cargo Types"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("👤 Welcome User")

# ===== MASTER DATA =====
vehicle_master = pd.DataFrame([
    ["32 ft Truck", 32, 8, 8],
    ["40 ft Trailer", 40, 8, 8.5],
    ["40 ft High", 40, 8, 10],
    ["45 ft Trailer", 45, 8, 8.5],
], columns=["Vehicle", "Length(ft)", "Width(ft)", "Height(ft)"])

cargo_master = pd.DataFrame([
    ["Standard Cargo", "Normal shipment"],
    ["Heavy Cargo", "CBM > 30"],
    ["ODC", "Height > 10 ft"]
], columns=["Cargo Type", "Description"])

# ===== MAIN =====
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ================= VEHICLE MASTER =================
if menu == "Vehicle Master Data":
    st.title("🚚 Vehicle Master Data")
    st.dataframe(vehicle_master, use_container_width=True)

# ================= CARGO MASTER =================
elif menu == "Cargo Types":
    st.title("📦 Cargo Types")
    st.dataframe(cargo_master, use_container_width=True)

# ================= CALCULATOR =================
else:
    st.title("🚚 Vehicle Load Calculator")

    left, right = st.columns([1, 1])

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

    def to_feet(value, unit):
        return {
            "mm": value / 304.8,
            "cm": value / 30.48,
            "m": value * 3.28,
            "inch": value / 12
        }[unit]

    vehicles = [
        {"name": "32 ft Truck", "L": 32, "W": 8, "H": 8},
        {"name": "40 ft Trailer", "L": 40, "W": 8, "H": 8.5},
        {"name": "40 ft High", "L": 40, "W": 8, "H": 10},
        {"name": "45 ft Trailer", "L": 45, "W": 8, "H": 8.5},
    ]

    with right:
        st.subheader("📊 Results")

        if st.button("Calculate"):

            if L > 0 and W > 0 and H > 0:

                L_ft = to_feet(L, unit)
                W_ft = to_feet(W, unit)
                H_ft = to_feet(H, unit)

                # CBM
                CBM = round((L_ft * W_ft * H_ft) / 35.315, 3)

                st.subheader("📦 Summary")
                st.write("CBM per package:", CBM)
                st.write("Total CBM:", CBM * qty)

                # CARGO TYPE
                if H_ft > 10:
                    cargo = "ODC"
                    st.error("🚨 Over Dimensional Cargo")
                elif CBM > 30:
                    cargo = "Heavy Cargo"
                    st.warning("⚠️ Heavy Cargo")
                else:
                    cargo = "Standard Cargo"
                    st.success("✅ Standard Cargo")

                st.write("Cargo Type:", cargo)

                # VEHICLE ANALYSIS
                st.subheader("🚚 Vehicle Recommendation")

                results = []
                best = None

                for v in vehicles:
                    fit = int(v["L"] // L_ft) * int(v["W"] // W_ft) * int(v["H"] // H_ft)

                    if fit > 0:
                        needed = math.ceil(qty / fit)

                        results.append({
                            "Vehicle": v["name"],
                            "Capacity (units)": fit,
                            "Vehicles Required": needed
                        })

                        if best is None or needed < best["needed"]:
                            best = {"name": v["name"], "needed": needed}

                df = pd.DataFrame(results)
                st.dataframe(df, use_container_width=True)

                if best:
                    st.success(f"Best Option: {best['name']} ({best['needed']} vehicles)")

            else:
                st.warning("Please enter all values")

st.markdown('</div>', unsafe_allow_html=True)
