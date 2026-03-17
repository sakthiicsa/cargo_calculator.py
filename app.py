import streamlit as st
import math
st.markdown("""
<style>

/* ===== GLOBAL CLEAN ===== */
.stApp {
    background: #F4F7FB;
    font-family: 'Segoe UI', sans-serif;
}

/* ===== HEADER ===== */
.main-title {
    font-size: 52px;
    font-weight: 800;
    color: #0A2540;
    margin-top: 10px;
}

/* Section title */
h2 {
    font-size: 30px;
    color: #1B4F72;
}

/* Labels */
label {
    font-size: 18px !important;
    color: #2C3E50 !important;
}

/* ===== INPUT BOXES ===== */
.stNumberInput input {
    font-size: 16px !important;
    padding: 10px;
    border-radius: 8px;
}

/* ===== SELECT BOX (SAFE FIX) ===== */
div[data-baseweb="select"] > div {
    background-color: #2E8BC0;
    border-radius: 8px;
}

/* ONLY selected value */
div[data-baseweb="select"] span {
    color: white !important;
    font-size: 16px;
}

/* Arrow */
div[data-baseweb="select"] svg {
    fill: white;
}

/* Dropdown menu */
div[role="listbox"] {
    background-color: white;
}

/* Options */
div[role="option"] {
    color: black;
    font-size: 16px;
}

/* Hover */
div[role="option"]:hover {
    background-color: #EAF3FB;
}

/* ===== BUTTON ===== */
.stButton button {
    background-color: #2E8BC0;
    color: white;
    font-size: 18px;
    border-radius: 8px;
    padding: 10px 20px;
}

/* ===== SPACING FIX ===== */
hr {
    margin: 5px 0;
}

</style>
""", unsafe_allow_html=True)

# --- Company Header ---

col1, col2 = st.columns([1, 8], vertical_alignment="center")

with col1:
    st.image("Logo1.png", width=180)

with col2:
    st.markdown(
        "<div class='main-title'>International Clearing And Shipping Agency</div>",
        unsafe_allow_html=True
    )

st.markdown("---")
st.title("📦 Cargo Volume & Vehicle Planner")

# --- Unit Selection ---
unit = st.selectbox("Select Unit", ["mm", "cm", "m", "inch"])

# --- Inputs ---
L = st.number_input("Length", min_value=0.0)
W = st.number_input("Width", min_value=0.0)
H = st.number_input("Height", min_value=0.0)
qty = st.number_input("Number of Packages", min_value=1)

# --- Conversion Functions ---
def to_feet(value, unit):
    if unit == "mm":
        return value / 304.8
    elif unit == "cm":
        return value / 30.48
    elif unit == "m":
        return value * 3.28084
    elif unit == "inch":
        return value / 12

def to_meters(value, unit):
    if unit == "mm":
        return value / 1000
    elif unit == "cm":
        return value / 100
    elif unit == "m":
        return value
    elif unit == "inch":
        return value * 0.0254

# --- Vehicle Master Data ---
vehicles = [
    {"name": "32 ft Truck", "L": 32, "W": 8, "H": 8, "CBM": 58},
    {"name": "40 ft Trailer", "L": 40, "W": 8, "H": 8.5, "CBM": 77},
    {"name": "40 ft High", "L": 40, "W": 8, "H": 10, "CBM": 90},
    {"name": "45 ft Trailer", "L": 45, "W": 8, "H": 8.5, "CBM": 87},
    {"name": "45 ft High", "L": 45, "W": 8, "H": 10, "CBM": 102},
    {"name": "Open Truck", "L": 40, "W": 8, "H": 6, "CBM": 54},
    {"name": "Flatbed", "L": 40, "W": 8, "H": None, "CBM": None},
]

# --- Button ---
if st.button("Calculate"):

    if L > 0 and W > 0 and H > 0:

        # --- Convert ---
        L_ft = to_feet(L, unit)
        W_ft = to_feet(W, unit)
        H_ft = to_feet(H, unit)

        L_m = to_meters(L, unit)
        W_m = to_meters(W, unit)
        H_m = to_meters(H, unit)

        CBM = round(L_m * W_m * H_m, 3)

        # --- Output Dimensions ---
        st.subheader("📏 Dimensions")
        st.write(f"{round(L_ft,2)} ft × {round(W_ft,2)} ft × {round(H_ft,2)} ft")

        st.subheader("📦 Volume")
        st.success(f"CBM per package: {CBM}")

        # --- Vehicle Analysis ---
        st.subheader("🚚 Vehicle Fit Analysis")

        best_option = None

        for v in vehicles:

            st.write(f"### 🚛 {v['name']}")

            # Flatbed logic
            if v["H"] is None:

                fit_L = int(v["L"] // L_ft)
                fit_W = int(v["W"] // W_ft)
                total_fit = fit_L * fit_W

            else:
                fit_L = int(v["L"] // L_ft)
                fit_W = int(v["W"] // W_ft)
                fit_H = int(v["H"] // H_ft)
                total_fit = fit_L * fit_W * fit_H

            if total_fit > 0:
                vehicles_needed = math.ceil(qty / total_fit)

                st.write(f"Packages per vehicle: {total_fit}")
                st.write(f"Vehicles required: {vehicles_needed}")

                # Best option logic
                if best_option is None or vehicles_needed < best_option["count"]:
                    best_option = {
                        "name": v["name"],
                        "count": vehicles_needed
                    }

            else:
                st.write("❌ Package too big")

            st.markdown("---")

        # --- Best Vehicle ---
        if best_option:
            st.success(f"✅ Best Option: {best_option['name']} ({best_option['count']} vehicles)")

    else:
        st.warning("⚠️ Please enter all dimensions")
