import streamlit as st
import math


st.markdown("""
<style>

/* ===== BACKGROUND ===== */
.stApp {
    background-color: #F4F7FB;
}

/* ===== FORCE TEXT VISIBILITY ===== */
h1, h2, h3, h4, h5, h6 {
    color: #0A2540 !important;
}

p, label {
    color: #000000 !important;
    font-size: 16px !important;
}

/* Streamlit text elements */
.stMarkdown, .stText {
    color: #000000 !important;
}

/* ===== HEADER ===== */
.main-title {
    font-size: 44px;
    font-weight: 700;
    color: #0A2540;
}

/* ===== INPUT BOXES ===== */
.stNumberInput input {
    color: black !important;
    background-color: white !important;
}

/* ===== SELECT BOX FIX ===== */
div[data-baseweb="select"] > div {
    background-color: #2E8BC0;
}

div[data-baseweb="select"] span {
    color: white !important;
}

/* Dropdown options */
div[role="option"] {
    color: black !important;
}

/* ===== BUTTON ===== */
.stButton button {
    background-color: #2E8BC0;
    color: white;
}

/* ===== SUCCESS BOX FIX ===== */
.stAlert {
    color: black !important;
}

</style>
""", unsafe_allow_html=True)


# ===== HEADER =====
col1, col2 = st.columns([1, 5], vertical_alignment="center")

with col1:
    st.image("Logo1.png", width=220)

with col2:
    st.markdown(
        "<div class='main-title'>International Clearing And Shipping Agency</div>",
        unsafe_allow_html=True
    )

st.markdown("---")

st.header("📦 Cargo Volume & Vehicle Planner")

# ===== INPUT =====
unit = st.selectbox("Select Unit", ["mm", "cm", "m", "inch"])

L = st.number_input("Length", min_value=0.0)
W = st.number_input("Width", min_value=0.0)
H = st.number_input("Height", min_value=0.0)
qty = st.number_input("Number of Packages", min_value=1)

# ===== FUNCTIONS =====
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

# ===== VEHICLE DATA =====
vehicles = [
    {"name": "32 ft Truck", "L": 32, "W": 8, "H": 8},
    {"name": "40 ft Trailer", "L": 40, "W": 8, "H": 8.5},
    {"name": "40 ft High", "L": 40, "W": 8, "H": 10},
    {"name": "45 ft Trailer", "L": 45, "W": 8, "H": 8.5},
    {"name": "45 ft High", "L": 45, "W": 8, "H": 10},
    {"name": "Open Truck", "L": 40, "W": 8, "H": 6},
    {"name": "Flatbed", "L": 40, "W": 8, "H": None},
]

# ===== CALCULATE =====
if st.button("Calculate"):

    if L > 0 and W > 0 and H > 0:

        # Convert
        L_ft = to_feet(L, unit)
        W_ft = to_feet(W, unit)
        H_ft = to_feet(H, unit)

        L_m = to_meters(L, unit)
        W_m = to_meters(W, unit)
        H_m = to_meters(H, unit)

        CBM = round(L_m * W_m * H_m, 3)

        # ===== VALIDATION =====
        if CBM > 1000:
            st.warning("⚠️ CBM is very high. Please check if units are correct.")

        if L_ft > 100 or W_ft > 50 or H_ft > 50:
            st.warning("⚠️ Dimensions look unusually large. Please verify units.")

        # ===== OUTPUT =====
        st.subheader("📏 Dimensions")
        st.write(f"{round(L_ft,2)} × {round(W_ft,2)} × {round(H_ft,2)} ft")

        st.subheader("📦 Volume")
        st.success(f"CBM per package: {CBM}")

        # ===== VEHICLE ANALYSIS =====
        st.subheader("🚚 Vehicle Fit Analysis")

        best_option = None
        failed_vehicles = []

        for v in vehicles:

            st.markdown(f"**🚛 {v['name']}**")

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

                if best_option is None or vehicles_needed < best_option["count"]:
                    best_option = {
                        "name": v["name"],
                        "count": vehicles_needed
                    }
            else:
                st.write("❌ Package too big")
                failed_vehicles.append(v["name"])

            st.markdown("---")

        # ===== FINAL RESULT =====
        if best_option:
            st.success(f"✅ Best Option: {best_option['name']} ({best_option['count']} vehicles)")
        else:
            st.error("❌ No suitable vehicle found.")

        # ===== FAILED VEHICLES =====
        if failed_vehicles:
            st.warning("⚠️ Not Suitable Vehicles:")
            for v in failed_vehicles:
                st.write(f"- {v}")

    else:
        st.warning("⚠️ Please enter all dimensions")
