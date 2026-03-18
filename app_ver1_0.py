import streamlit as st
import math

# ===== PAGE CONFIG =====
st.set_page_config(page_title="Cargo Planner", layout="wide")

# ===== STYLE =====
st.markdown("""
<style>
.stApp {background-color: #F4F7FB;}

h1, h2, h3 {
    color: #0A2540 !important;
}

/* Card Style */
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
    st.image("Logo1.png", width=180)

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
    {"name": "32 ft Truck", "L": 32, "W": 8, "H": 8},
    {"name": "40 ft Trailer", "L": 40, "W": 8, "H": 8.5},
    {"name": "40 ft High", "L": 40, "W": 8, "H": 10},
    {"name": "45 ft Trailer", "L": 45, "W": 8, "H": 8.5},
    {"name": "45 ft High", "L": 45, "W": 8, "H": 10},
    {"name": "Open Truck", "L": 40, "W": 8, "H": 6},
    {"name": "Flatbed", "L": 40, "W": 8, "H": None},
]

# ===== LAYOUT =====
left, right = st.columns([1, 1.2], gap="large")

# ================= LEFT (INPUT) =================
with left:
    st.markdown("## 📥 Input Panel")

    st.markdown("<div class='card'>", unsafe_allow_html=True)

    unit = st.selectbox("Select Unit", ["mm", "cm", "m", "inch"])

    col1, col2, col3 = st.columns(3)
    with col1:
        L = st.number_input("Length", min_value=0.0, step=0.1)
    with col2:
        W = st.number_input("Width", min_value=0.0, step=0.1)
    with col3:
        H = st.number_input("Height", min_value=0.0, step=0.1)

    qty = st.number_input("Number of Packages", min_value=1, step=1)

    calculate = st.button("🚀 Calculate", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ================= RIGHT (OUTPUT) =================
with right:
    st.markdown("## 📊 Results Dashboard")

    if calculate:

        if L <= 0 or W <= 0 or H <= 0:
            st.warning("⚠️ Please enter valid dimensions")

        else:
            # ===== CONVERT =====
            L_ft, W_ft, H_ft = to_feet(L, unit), to_feet(W, unit), to_feet(H, unit)
            L_m, W_m, H_m = to_meters(L, unit), to_meters(W, unit), to_meters(H, unit)

            CBM = round(L_m * W_m * H_m, 3)

            # ===== SUMMARY CARDS =====
            c1, c2, c3 = st.columns(3)

            with c1:
                st.markdown(f"<div class='card'><b>📏 Dimensions</b><br>{L_ft:.2f} × {W_ft:.2f} × {H_ft:.2f} ft</div>", unsafe_allow_html=True)

            with c2:
                st.markdown(f"<div class='card'><b>📦 CBM / Package</b><br>{CBM}</div>", unsafe_allow_html=True)

            with c3:
                st.markdown(f"<div class='card'><b>📊 Total CBM</b><br>{round(CBM * qty, 3)}</div>", unsafe_allow_html=True)

            st.markdown("### 🚚 Vehicle Optimization")

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

                    st.markdown(
                        f"<div class='card'>🚛 <b>{v['name']}</b><br>"
                        f"Packages/Vehicle: {total_fit}<br>"
                        f"Vehicles Needed: {vehicles_needed}</div>",
                        unsafe_allow_html=True
                    )

                    if best_option is None or vehicles_needed < best_option["count"]:
                        best_option = {
                            "name": v["name"],
                            "count": vehicles_needed
                        }

            # ===== FINAL RESULT =====
            st.markdown("## ✅ Best Recommendation")

            if best_option:
                st.success(
                    f"{best_option['name']} → {best_option['count']} vehicle(s) required"
                )
            else:
                st.error("❌ No suitable vehicle found")

            # ===== DOWNLOAD =====
            report = f"""
CARGO REPORT
-----------------------
Dimensions (ft): {L_ft:.2f} x {W_ft:.2f} x {H_ft:.2f}
CBM per package: {CBM}
Total Packages: {int(qty)}
Total CBM: {round(CBM * qty, 3)}

Best Vehicle: {best_option['name'] if best_option else 'N/A'}
Vehicles Required: {best_option['count'] if best_option else 'N/A'}
"""

            st.download_button("📥 Download Report", report, "cargo_report.txt")

    else:
        st.info("👉 Enter details on the left and click Calculate")
