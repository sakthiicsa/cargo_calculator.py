import streamlit as st
import math

# ===== STYLE =====
st.markdown("""
<style>
.stApp {background-color: #F4F7FB;}

h1, h2, h3, h4 {color: #0A2540 !important;}

p, label {color: black !important;}

.stNumberInput input {
    background-color: white !important;
    color: black !important;
}

.stButton button {
    background-color: #2E8BC0;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
col1, col2 = st.columns([1, 5], vertical_alignment="center")

with col1:
    st.image("Logo1.png", width=200)

with col2:
    st.markdown(
        "<h1>International Clearing And Shipping Agency</h1>",
        unsafe_allow_html=True
    )

st.markdown("---")
st.header("📦 Cargo Volume & Vehicle Planner")

# ===== INPUT =====
unit = st.selectbox("Select Unit", ["mm", "cm", "m", "inch"])

col1, col2, col3 = st.columns(3)

with col1:
    L = st.number_input("Length", min_value=0.0, step=0.1)

with col2:
    W = st.number_input("Width", min_value=0.0, step=0.1)

with col3:
    H = st.number_input("Height", min_value=0.0, step=0.1)

qty = st.number_input("Number of Packages", min_value=1, step=1)

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

# ===== CALCULATE =====
if st.button("Calculate"):

    if L <= 0 or W <= 0 or H <= 0:
        st.warning("⚠️ Please enter valid dimensions")
        st.stop()

    # Convert
    L_ft, W_ft, H_ft = to_feet(L, unit), to_feet(W, unit), to_feet(H, unit)
    L_m, W_m, H_m = to_meters(L, unit), to_meters(W, unit), to_meters(H, unit)

    CBM = round(L_m * W_m * H_m, 3)

    # ===== OUTPUT =====
    st.subheader("📏 Dimensions (ft)")
    st.write(f"{L_ft:.2f} × {W_ft:.2f} × {H_ft:.2f}")

    st.subheader("📦 Volume")
    st.success(f"CBM per package: {CBM}")

    # ===== VEHICLE ANALYSIS =====
    st.subheader("🚚 Vehicle Fit Analysis")

    best_option = None
    failed_vehicles = []

    for v in vehicles:

        st.markdown(f"**🚛 {v['name']}**")

        fit_L = int(v["L"] // L_ft)
        fit_W = int(v["W"] // W_ft)

        if v["H"] is None:
            total_fit = fit_L * fit_W
        else:
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

    # ===== FINAL REPORT =====
    st.markdown("## 📊 Final Report")

    st.markdown("### 📦 Cargo Summary")
    st.write(f"**Dimensions (ft):** {L_ft:.2f} × {W_ft:.2f} × {H_ft:.2f}")
    st.write(f"**CBM per Package:** {CBM}")
    st.write(f"**Total Packages:** {int(qty)}")
    st.write(f"**Total Volume:** {round(CBM * qty, 3)} CBM")

    st.markdown("---")

    if best_option:
        st.markdown("### 🚚 Recommended Plan")
        st.success(
            f"Best Vehicle: {best_option['name']}  \n"
            f"Vehicles Required: {best_option['count']}"
        )
    else:
        st.error("No suitable vehicle found")

    if failed_vehicles:
        st.markdown("### ⚠️ Not Suitable Vehicles")
        for v in failed_vehicles:
            st.write(f"- {v}")

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
