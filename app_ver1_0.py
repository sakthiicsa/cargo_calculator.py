import streamlit as st
import math
import pandas as pd

# ===== PAGE CONFIG =====
st.set_page_config(layout="wide")

# ===== CLEAN LIGHT + READABLE UI =====
st.markdown("""
<style>

/* App background */
.stApp {
    background-color: #F4F7FB;
}

/* Strong readable text everywhere */
html, body, [class*="css"] {
    color: #111111 !important;
    font-size: 15px;
}

/* Headings */
h1, h2, h3 {
    color: #0A2540 !important;
    font-weight: 700;
}

/* Labels */
label {
    color: #111111 !important;
    font-weight: 600;
}

/* Inputs */
input, textarea {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #CCCCCC !important;
    border-radius: 6px;
}

/* Selectbox */
div[data-baseweb="select"] {
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

/* Containers (remove dark boxes) */
div[data-testid="stDataFrame"],
div[data-testid="stTable"],
div[data-testid="stAlert"],
div[data-testid="stMarkdownContainer"],
div[data-testid="stDownloadButton"],
div[data-testid="stButton"] {
    background-color: #FFFFFF !important;
    border-radius: 10px;
    padding: 10px;
}

/* Dataframe text */
[data-testid="stDataFrame"] * {
    color: #000000 !important;
}

/* Button */
.stButton button {
    background-color: #2E8BC0 !important;
    color: #FFFFFF !important;
    font-weight: 600;
    border-radius: 8px;
}

/* Alerts */
div[data-testid="stAlert"] {
    background-color: #FFFFFF !important;
    border-left: 5px solid #2E8BC0 !important;
}

/* Remove dark overlay */
section.main > div {
    background-color: transparent !important;
}

/* Title */
.company-title {
    font-size: 36px;
    font-weight: 700;
    color: #0A2540 !important;
}

/* Table text */
table {
    color: #000000 !important;
}

</style>
""", unsafe_allow_html=True)

# ===== HEADER =====
col1, col2 = st.columns([1,5])

with col1:
    st.image("Logo1.png", width=180)

with col2:
    st.markdown(
        "<div class='company-title'>International Clearing And Shipping Agency</div>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ===== MAIN LAYOUT =====
left, right = st.columns([1,1])

# ================= LEFT =================
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

# ================= RIGHT =================
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
                st.error("🚨 ODC Cargo (Height exceeds limit)")
                cargo_type = "ODC"
            elif CBM > 30:
                st.warning("⚠️ Heavy Cargo")
                cargo_type = "Heavy"
            else:
                st.success("✅ Standard Cargo")
                cargo_type = "Standard"

            st.write(f"Cargo Type: {cargo_type}")

            # ===== VEHICLE =====
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

            st.table(df)  # cleaner than dataframe

            if best_option:
                st.success(f"🏆 Best Vehicle: {best_option['name']} ({best_option['count']} required)")
            else:
                st.error("❌ No suitable vehicle found")

            if failed:
                st.warning("Not Suitable Vehicles:")
                st.write(", ".join(failed))

            # ===== DOWNLOAD =====
            st.download_button(
                "📥 Download Report",
                df.to_csv(index=False),
                file_name="vehicle_plan.csv",
                mime="text/csv"
            )

        else:
            st.warning("⚠️ Please enter all dimensions")
