import streamlit as st
import math
import pandas as pd

# ===== PAGE CONFIG =====
st.set_page_config(layout="wide")

# ===== PORTAL CSS =====
st.markdown("""
<style>

/* ===== GLOBAL ===== */
.stApp {
    background-color: #F1F3F6;
    font-family: "Segoe UI", Arial, sans-serif;
}

/* ===== TOP HEADER ===== */
.top-header {
    background-color: #1558A6;
    padding: 14px 20px;
    color: white;
    font-size: 20px;
    font-weight: 600;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #1558A6 !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ===== MAIN CONTENT ===== */
.main-container {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
}

/* ===== TEXT ===== */
h1, h2, h3 {
    color: #0A2540;
    font-weight: 600;
}

label {
    font-size: 14px;
    font-weight: 600;
    color: #333;
}

/* ===== INPUTS ===== */
input, textarea, div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    border: 1px solid #D0D5DD !important;
    border-radius: 6px;
    font-size: 14px;
}

/* ===== BUTTON ===== */
.stButton button {
    background-color: #1558A6;
    color: white;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 600;
}

/* ===== TABLE ===== */
[data-testid="stDataFrame"] {
    background-color: white;
    border-radius: 6px;
}

/* ===== ALERTS ===== */
div[data-testid="stAlert"] {
    border-left: 5px solid #1558A6;
}

/* ===== SMALL TEXT ===== */
p {
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
st.markdown('<div class="top-header">LogistiCSA Portal</div>', unsafe_allow_html=True)

# ===== SIDEBAR =====
st.sidebar.markdown("### 📂 Operations")
menu = st.sidebar.radio(
    "",
    ["Import", "Export", "CFS Yard Mapping", "Finance", "Human Resource"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("👤 Welcome User")

# ===== MAIN CONTAINER START =====
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# ===== PAGE TITLE =====
st.title("🚚 Vehicle Load Calculator")

# ===== LAYOUT =====
left, right = st.columns([1, 1])

# ================= LEFT SIDE =================
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

# ================= RIGHT SIDE =================
with right:
    st.subheader("📊 Results")

    if st.button("Calculate"):

        if L > 0 and W > 0 and H > 0:

            # ===== CONVERSIONS =====
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

            # ===== DIMENSIONS =====
            st.subheader("📏 Dimensions")
            st.write(f"Feet: {round(L_ft,2)} × {round(W_ft,2)} × {round(H_ft,2)} ft")
            st.write(f"Meters: {round(L_m,2)} × {round(W_m,2)} × {round(H_m,2)} m")

            # ===== CARGO TYPE =====
            if H_ft > 10:
                cargo_type = "Over Dimensional Cargo (ODC)"
                st.error("🚨 ODC Cargo (Height exceeds limit)")
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
            else:
                st.error("❌ No suitable vehicle found")

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
            st.warning("⚠️ Please enter all dimensions")

# ===== MAIN CONTAINER END =====
st.markdown('</div>', unsafe_allow_html=True)
