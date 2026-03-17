import streamlit as st
import pandas as pd
import math

# --- Company Header ---
col1, col2 = st.columns([1, 4])

with col1:
    st.image("Logo1.png", width=200)

with col2:
    st.title("International Clearing And Shipping Agency")

st.markdown("---")
st.title("📦 Cargo Volume & Vehicle Planner")

# --- Upload Vehicle File ---
uploaded_file = st.file_uploader("📁 Upload Vehicle Master File", type=["xlsx", "csv"])

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

# --- Read Vehicle File ---
vehicles = []
df = None

if uploaded_file is not None:

    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(Vehicle_Data)
    else:
        df = pd.read_csv(Vehicle_Data)

    # Show uploaded data
    st.subheader("📋 Vehicle Master Data")
    st.dataframe(df)

    # Convert to list
    for _, row in df.iterrows():
        vehicles.append({
            "name": row["Vehicle Type"],
            "L": row["Length (ft)"],
            "W": row["Width (ft)"],
            "H": None if pd.isna(row["Height (ft)"]) else row["Height (ft)"],
            "CBM": row["CBM"]
        })

# --- Button ---
if st.button("Calculate"):

    if uploaded_file is None:
        st.warning("⚠️ Please upload vehicle master file")

    elif L > 0 and W > 0 and H > 0:

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

            # Flatbed (no height)
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
