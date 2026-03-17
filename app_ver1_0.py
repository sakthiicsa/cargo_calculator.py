import streamlit as st
import math
import pandas as pd

# ===== PAGE STYLE =====
st.set_page_config(layout="wide")

st.markdown("""
<style>

/* ===== APP BACKGROUND ===== */
.stApp {
    background-color: #F4F7FB;
}

/* ===== TEXT VISIBILITY FIX ===== */
body, p, span, div, label {
    color: #000000 !important;
    opacity: 1 !important;
}

/* HEADINGS */
h1, h2, h3 {
    color: #0A2540 !important;
    font-weight: 600 !important;
}

/* ===== INPUTS ===== */
input, textarea {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border-radius: 6px !important;
}

/* Number input */
.stNumberInput input {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

/* ===== SELECT BOX ===== */
div[data-baseweb="select"] > div {
    background-color: #2E8BC0 !important;
    border-radius: 6px !important;
}

/* Selected text */
div[data-baseweb="select"] span {
    color: #FFFFFF !important;
    font-weight: 500;
}

/* Dropdown */
div[role="listbox"] {
    background-color: #FFFFFF !important;
}

/* Options */
div[role="option"] {
    color: #000000 !important;
}

/* ===== BUTTON ===== */
.stButton button {
    background-color: #2E8BC0 !important;
    color: #FFFFFF !important;
    border-radius: 6px;
}

/* ===== DATAFRAME FIX ===== */
.stDataFrame {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

/* ===== ALERT BOXES (VERY IMPORTANT) ===== */
.stAlert {
    background-color: #EAF3FB !important;
    color: #000000 !important;
    border-radius: 8px;
}

/* ===== REMOVE FADED LOOK ===== */
[data-testid="stMarkdownContainer"] {
    opacity: 1 !important;
}

/* ===== HEADERS SPACING ===== */
.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
col1, col2 = st.columns([1,5])
with col1:
    st.image("Logo1.png", width=200)
with col2:
    st.markdown("<div class='main-title'>International Clearing And Shipping Agency</div>", unsafe_allow_html=True)

st.markdown("---")

# ===== LAYOUT =====
left, right = st.columns([1,1])

# ================= LEFT SIDE (INPUTS) =================
with left:
    st.header("📥 Input Details")

    unit = st.selectbox("Select Unit", ["mm", "cm", "m", "inch"])

    L = st.number_input("Length", min_value=0.0)
    W = st.number_input("Width", min_value=0.0)
    H = st.number_input("Height", min_value=0.0)

    qty = st.number_input("Number of Packages", min_value=1)

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

# ================= RIGHT SIDE (RESULTS) =================
with right:
    st.header("📊 Results")

    if st.button("Calculate"):

        if L > 0 and W > 0 and H > 0:

            # ===== CONVERSION =====
            L_ft = to_feet(L, unit)
            W_ft = to_feet(W, unit)
            H_ft = to_feet(H, unit)

            L_m = to_meters(L, unit)
            W_m = to_meters(W, unit)
            H_m = to_meters(H, unit)

            CBM = round(L_m * W_m * H_m, 3)
            total_cbm = round(CBM * qty, 3)

            # ===== SUMMARY =====
            st.subheader("📦 Summary")
            st.write(f"CBM per package: {CBM}")
            st.write(f"Total CBM: {total_cbm}")
            st.write(f"Quantity: {qty}")

            # ===== CARGO TYPE =====
            if H_ft > 10:
                cargo_type = "Over Dimensional Cargo (ODC)"
                st.error("🚨 ODC Cargo (Height exceeds standard limit)")
            elif CBM > 30:
                cargo_type = "Heavy Industrial Cargo"
                st.warning("⚠️ Heavy Cargo")
            else:
                cargo_type = "Standard Cargo"
                st.success("✅ Standard Cargo")

            st.write(f"Cargo Type: {cargo_type}")

            # ===== VEHICLE ANALYSIS =====
            st.subheader("🚚 Vehicle Recommendation")

            best_option = None
            results = []
            failed = []

            for v in vehicles:

                if v["H"] is None:
                    fit = int(v["L"] // L_ft) * int(v["W"] // W_ft)
                else:
                    fit = int(v["L"] // L_ft) * int(v["W"] // W_ft) * int(v["H"] // H_ft)

                if fit > 0:
                    needed = math.ceil(qty / fit)

                    results.append({
                        "Vehicle": v["name"],
                        "Fit per Vehicle": fit,
                        "Vehicles Required": needed
                    })

                    if best_option is None or needed < best_option["count"]:
                        best_option = {"name": v["name"], "count": needed}
                else:
                    failed.append(v["name"])

            df = pd.DataFrame(results)

            st.dataframe(df, use_container_width=True)

            # ===== BEST OPTION =====
            if best_option:
                st.success(f"🏆 Best Vehicle: {best_option['name']} ({best_option['count']} required)")

            # ===== FAILED =====
            if failed:
                st.warning("Not Suitable Vehicles:")
                st.write(", ".join(failed))

            # ===== EXPORT =====
            st.download_button(
                "📥 Download Report",
                df.to_csv(index=False),
                file_name="vehicle_plan.csv",
                mime="text/csv"
            )

        else:
            st.warning("⚠️ Enter valid dimensions")
