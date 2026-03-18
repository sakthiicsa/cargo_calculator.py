import streamlit as st
import math
import pandas as pd

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Dimensions Calculation", layout="wide")

# ===== STYLE =====
st.markdown("""
<style>
.stApp {background-color: #F4F7FB;}

h1, h2, h3 {
    color: #0A2540 !important;
}

/* Input Fields Light Theme */
.stNumberInput input, .stSelectbox div {
    background-color: #E8F1FB !important;
    color: black !important;
}

/* Card */
.card {
    padding: 15px;
    border-radius: 12px;
    background: white;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    margin-bottom: 10px;
}

/* Button */
.stButton button {
    background-color: #2E8BC0;
    color: white;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
col1, col2 = st.columns([1, 6])
with col1:
    st.image("Logo1.png", width=160)

with col2:
    st.markdown("<h1>International Clearing And Shipping Agency</h1>", unsafe_allow_html=True)

st.markdown("---")

# ===== FUNCTIONS =====
def to_feet(v, u):
    return {
        "mm": v / 304.8,
        "cm": v / 30.48,
        "m": v * 3.28084,
        "inch": v / 12
    }[u]

def to_meters(v, u):
    return {
        "mm": v / 1000,
        "cm": v / 100,
        "m": v,
        "inch": v * 0.0254
    }[u]

# ===== VEHICLES =====
vehicles = [
    {"Vehicle": "32 ft Truck", "L": 32, "W": 8, "H": 8},
    {"Vehicle": "40 ft Trailer", "L": 40, "W": 8, "H": 8.5},
    {"Vehicle": "40 ft High", "L": 40, "W": 8, "H": 10},
    {"Vehicle": "45 ft Trailer", "L": 45, "W": 8, "H": 8.5},
    {"Vehicle": "45 ft High", "L": 45, "W": 8, "H": 10},
    {"Vehicle": "Open Truck", "L": 40, "W": 8, "H": 6},
    {"Vehicle": "Flatbed", "L": 40, "W": 8, "H": None},
]

# ===== LAYOUT =====
left, right = st.columns([1, 1.2], gap="large")

# ================= LEFT SIDE =================
with left:
    st.markdown("##📦 Cargo Volume & Vehicle Planner")

    unit = st.selectbox("Select Unit", ["mm", "cm", "m", "inch"])

    c1, c2, c3 = st.columns(3)
    with c1:
        L = st.number_input("Length", min_value=0.0, step=0.1)
    with c2:
        W = st.number_input("Width", min_value=0.0, step=0.1)
    with c3:
        H = st.number_input("Height", min_value=0.0, step=0.1)

    qty = st.number_input("Number of Packages", min_value=1, step=1)

    calculate = st.button("Calculate", use_container_width=True)

# ================= RIGHT SIDE =================
with right:
    st.markdown("## Results")

    if calculate:

        if L <= 0 or W <= 0 or H <= 0:
            st.warning("⚠️ Please enter valid dimensions")

        else:
            # ===== CONVERT =====
            L_ft, W_ft, H_ft = to_feet(L, unit), to_feet(W, unit), to_feet(H, unit)
            L_m, W_m, H_m = to_meters(L, unit), to_meters(W, unit), to_meters(H, unit)

            CBM = round(L_m * W_m * H_m, 3)
            total_cbm = round(CBM * qty, 3)

            # ===== SUMMARY =====
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(f"<div class='card'><b>📏 Dimensions</b><br>{L_ft:.2f} × {W_ft:.2f} × {H_ft:.2f} ft</div>", unsafe_allow_html=True)

            with c2:
                st.markdown(f"<div class='card'><b>📦 CBM / Package</b><br>{CBM}</div>", unsafe_allow_html=True)

            with c3:
                st.markdown(f"<div class='card'><b>📊 Total CBM</b><br>{total_cbm}</div>", unsafe_allow_html=True)

            # ===== VEHICLE TABLE =====
            st.markdown("### 🚚 Vehicle Optimization Table")

            table_data = []
            best_option = None

            for v in vehicles:

                if v["H"] is None:
                    total_fit = int(v["L"] // L_ft) * int(v["W"] // W_ft)
                else:
                    total_fit = (
                        int(v["L"] // L_ft)
                        * int(v["W"] // W_ft)
                        * int(v["H"] // H_ft)
                    )

                if total_fit > 0:
                    vehicles_needed = math.ceil(qty / total_fit)
                else:
                    vehicles_needed = "Not Fit"

                table_data.append({
                    "Vehicle": v["Vehicle"],
                    "Packages / Vehicle": total_fit,
                    "Vehicles Required": vehicles_needed
                })

                if isinstance(vehicles_needed, int):
                    if best_option is None or vehicles_needed < best_option["count"]:
                        best_option = {
                            "name": v["Vehicle"],
                            "count": vehicles_needed
                        }

            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True)

            # ===== BEST OPTION =====
            st.markdown("## ✅ Best Recommendation")

            if best_option:
                st.success(f"{best_option['name']} → {best_option['count']} vehicle(s)")
            else:
                st.error("❌ No suitable vehicle found")

            # ===== DOWNLOAD =====
            report = f"""
CARGO REPORT
-----------------------
Dimensions (ft): {L_ft:.2f} x {W_ft:.2f} x {H_ft:.2f}
CBM per package: {CBM}
Total Packages: {int(qty)}
Total CBM: {total_cbm}

Best Vehicle: {best_option['name'] if best_option else 'N/A'}
Vehicles Required: {best_option['count'] if best_option else 'N/A'}
"""

            st.download_button("📥 Download Report", report, "cargo_report.txt")

    else:
        st.info("👉 Enter inputs on the left and click Calculate")
