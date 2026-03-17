import streamlit as st
import math
st.markdown("""
    <style>

    /* ===== BACKGROUND ===== */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa, #e4ecf7);
        font-family: 'Segoe UI', sans-serif;
    }

    /* ===== HEADINGS ===== */
    h1 {
        color: #0A2540 !important;
        font-weight: 700;
        letter-spacing: 0.5px;
    }

    h2, h3 {
        color: #1B4F72 !important;
        font-weight: 600;
    }

    /* ===== NORMAL TEXT ===== */
    p, div, span, label {
        color: #2C3E50 !important;
        font-size: 15px;
    }

    /* ===== INPUT BOXES ===== */
    .stNumberInput input {
        background-color: white !important;
        border: 1px solid #d0d7e2;
        border-radius: 8px;
        color: #2C3E50 !important;
        padding: 6px;
    }

    /* ===== SELECT BOX ===== */
    div[data-baseweb="select"] > div {
        background-color: #2E8BC0 !important;  /* sea blue */
        border-radius: 8px;
        border: none;
    }

    div[data-baseweb="select"] span {
        color: white !important;
        font-weight: 500;
    }

    div[data-baseweb="select"] svg {
        fill: white !important;
    }

    /* ===== DROPDOWN ===== */
    div[role="listbox"] {
        background-color: white !important;
        border-radius: 8px;
        border: 1px solid #d0d7e2;
    }

    div[role="option"] {
        color: #2C3E50 !important;
        padding: 8px;
    }

    div[role="option"]:hover {
        background-color: #EAF3FB !important;
    }

    /* ===== BUTTON ===== */
    .stButton button {
        background: linear-gradient(90deg, #2E8BC0, #1B4F72);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 8px 20px;
        font-weight: 600;
        transition: 0.3s;
    }

    .stButton button:hover {
        background: linear-gradient(90deg, #1B4F72, #163A5F);
        transform: scale(1.03);
    }

    /* ===== CARDS (SECTIONS) ===== */
    .block-container {
        padding-top: 2rem;
    }

    /* ===== SUCCESS BOX ===== */
    .stAlert {
        border-radius: 10px;
    }

    </style>
""", unsafe_allow_html=True)

# --- Company Header ---
col1, col2 = st.columns([1, 4])

with col1:
    st.image("Logo1.png", width=200)

with col2:
    st.title("International Clearing And Shipping Agency")

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
