import streamlit as st

st.title("📦 Cargo Volume Calculator")

# Dropdown for unit
unit = st.selectbox("Select Unit", ["mm", "cm", "m", "inch"])

# Inputs
L = st.number_input("Length", min_value=0.0)
W = st.number_input("Width", min_value=0.0)
H = st.number_input("Height", min_value=0.0)

# --- Accurate Conversion functions ---
def to_feet(value, unit):
    if unit == "mm":
        return value / 304.8          # ✅ accurate
    elif unit == "cm":
        return value / 30.48          # ✅ accurate
    elif unit == "m":
        return value * 3.28084        # ✅ accurate
    elif unit == "inch":
        return value / 12             # ✅ accurate

def to_meters(value, unit):
    if unit == "mm":
        return value / 1000
    elif unit == "cm":
        return value / 100
    elif unit == "m":
        return value
    elif unit == "inch":
        return value * 0.0254

# --- Calculation ---
if L > 0 and W > 0 and H > 0:

    # Feet (accurate)
    L_ft = round(to_feet(L, unit), 2)
    W_ft = round(to_feet(W, unit), 2)
    H_ft = round(to_feet(H, unit), 2)

    # CBM (always accurate because meters used)
    L_m = to_meters(L, unit)
    W_m = to_meters(W, unit)
    H_m = to_meters(H, unit)

    CBM = round(L_m * W_m * H_m, 3)

    # Output
    st.subheader("📏 Dimensions in Feet (Accurate)")
    st.write(f"L: {L_ft} ft | W: {W_ft} ft | H: {H_ft} ft")

    st.subheader("📦 Volume")
    st.success(f"CBM: {CBM}")
