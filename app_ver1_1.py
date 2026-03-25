import streamlit as st
import pandas as pd
import math

# MUST BE FIRST
st.set_page_config(page_title="ICSA Cargo Planner PRO", layout="wide")

# ===== SESSION INIT =====
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "user" not in st.session_state:
    st.session_state["user"] = ""

if "packages" not in st.session_state:
    st.session_state["packages"] = []

if "vehicle_options" not in st.session_state:
    st.session_state["vehicle_options"] = None

if "confirmed" not in st.session_state:
    st.session_state["confirmed"] = None


# ===== USER DATABASE =====
users = {
    "admin": "ICSA123",
    "manager": "ICSA456",
    "user1": "ICSA789",
    "client1": "CLIENT123",
    "viewer": "VIEW123"
}


# ===== LOGIN =====
def login():
    st.title("🔐 Secure Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and users[username] == password:
            st.session_state["auth"] = True
            st.session_state["user"] = username
            st.success(f"Welcome {username} ✅")
            st.rerun()
        else:
            st.error("Invalid credentials ❌")


# ===== AUTH CHECK =====
if not st.session_state["auth"]:
    login()
    st.stop()


# ===== HEADER =====
c1, c2, c3 = st.columns([1, 4, 1])

with c1:
    st.image("https://icsagroup.com/wp-content/themes/icsa/images/logo.png", width=120)

with c2:
    st.markdown(
        "<h3 style='text-align:center;'>International Clearing & Shipping Agency Pvt Ltd</h3>",
        unsafe_allow_html=True
    )

with c3:
    st.image("http://icsagroup.com/wp-content/uploads/2025/10/94-Years-Unit.png", width=80)

st.success(f"Welcome to Cargo Planner 🚚, {st.session_state['user']}")

# ===== LOGOUT =====
if st.button("Logout"):
    st.session_state["auth"] = False
    st.session_state["user"] = ""
    st.rerun()

st.header("📦 Cargo Volume & Vehicle Planner")
st.markdown("---")


# ===== JOB ID =====
col1, col2 = st.columns([1, 5])
with col1:
    job_id = st.text_input("Job ID", max_chars=15)


# ===== MASTER DATA =====
package_types = ["Carton Box","Corrugated Box","Envelope","Poly Bag / Mailer"]

vehicle_data = [
("TATA ACE","6 * 4 * 5","6"),
("TATA 407","9 * 6 * 5","9"),
("TATA - 12 Feet","12 * 6.4 * 5","11"),
("Canter - 14 Feet","14 * 6.4 * 5","14"),
("20' Container","20 * 8 * 8","27"),
("32' Container HQ","32 * 9 * 10","55"),
("40' Container","40 * 8 * 8","60"),
]

vehicle_df = pd.DataFrame(vehicle_data, columns=["Vehicle","Size","CBM"])


# ===== UTILS =====
def to_feet(v, u):
    return {"mm": v/304.8, "cm": v/30.48, "m": v*3.28084, "inch": v/12}[u]

def calc_cbm(L, W, H, qty):
    return (L * W * H * qty) / 35.315 if L and W and H else 0

def get_max_cbm(cbm):
    return float(str(cbm).split("-")[-1])


# ===== INPUT =====
st.subheader("📏 Package Dimension Calculator")

cols = st.columns(5)
unit = cols[0].selectbox("Unit", ["mm","cm","m","inch"])
L = cols[1].number_input("Length", min_value=0.0, step=0.1)
W = cols[2].number_input("Width", min_value=0.0, step=0.1)
H = cols[3].number_input("Height", min_value=0.0, step=0.1)
qty = cols[4].number_input("Quantity", min_value=1)

if st.button("📐 Calculate & Add"):
    if L == 0 or W == 0 or H == 0:
        st.warning("⚠️ Enter all dimensions")
    else:
        st.session_state["packages"].append({
            "Box Name": package_types[0],
            "L": round(to_feet(L, unit), 2),
            "W": round(to_feet(W, unit), 2),
            "H": round(to_feet(H, unit), 2),
            "Quantity": qty,
            "Weight Piece (KG)": 0.0,
            "Rotation Allowed": False,
            "Stacking On Top": False,
            "Stacking Under": False
        })


# ===== TABLE =====
st.subheader("📦 Package Details (Feet)")

if st.button("➕ Add Cargo Row"):
    st.session_state["packages"].append({
        "Box Name": package_types[0],
        "L": 0.0, "W": 0.0, "H": 0.0,
        "Quantity": 1,
        "Weight Piece (KG)": 0.0,
        "Rotation Allowed": False,
        "Stacking On Top": False,
        "Stacking Under": False
    })

total_cbm = 0
total_weight = 0
total_boxes = 0
delete_index = None

for i, pkg in enumerate(st.session_state["packages"]):

    cols = st.columns(12)

    pkg["Box Name"] = cols[0].selectbox("", package_types, key=f"name{i}")
    pkg["L"] = cols[1].number_input("", value=float(pkg["L"]), key=f"L{i}")
    pkg["W"] = cols[2].number_input("", value=float(pkg["W"]), key=f"W{i}")
    pkg["H"] = cols[3].number_input("", value=float(pkg["H"]), key=f"H{i}")
    pkg["Quantity"] = cols[4].number_input("", value=int(pkg["Quantity"]), key=f"Q{i}")
    pkg["Weight Piece (KG)"] = cols[5].number_input("", value=float(pkg["Weight Piece (KG)"]), key=f"WT{i}")

    tot_wt = pkg["Quantity"] * pkg["Weight Piece (KG)"]
    cbm = calc_cbm(pkg["L"], pkg["W"], pkg["H"], pkg["Quantity"])

    cols[6].write(round(tot_wt, 2))
    cols[7].write(round(cbm, 2))

    pkg["Rotation Allowed"] = cols[8].checkbox("", value=pkg["Rotation Allowed"], key=f"R{i}")
    pkg["Stacking On Top"] = cols[9].checkbox("", value=pkg["Stacking On Top"], key=f"T{i}")
    pkg["Stacking Under"] = cols[10].checkbox("", value=pkg["Stacking Under"], key=f"U{i}")

    if cols[11].button("🗑", key=f"del{i}"):
        delete_index = i

    total_cbm += cbm
    total_weight += tot_wt
    total_boxes += pkg["Quantity"]

if delete_index is not None:
    st.session_state["packages"].pop(delete_index)
    st.rerun()


# ===== TOTALS =====
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Total CBM", round(total_cbm, 2))
c2.metric("Total Weight (kg)", round(total_weight, 2))
c3.metric("Total Boxes", int(total_boxes))


# ===== CALCULATION =====
if st.button("💾 Save & Calculate"):

    if total_cbm == 0:
        st.warning("⚠️ No valid cargo data")
    else:
        results = []

        for _, v in vehicle_df.iterrows():
            cap = get_max_cbm(v["CBM"])
            vehicles = math.ceil(total_cbm / cap)

            total_capacity = vehicles * cap
            remaining = total_capacity - total_cbm

            results.append({
                "Select": False,
                "Vehicle": v["Vehicle"],
                "Capacity": cap,
                "Total Capacity": total_capacity,
                "Occupied": total_cbm,
                "Remaining": remaining,
                "Vehicles Needed": vehicles
            })

        df = pd.DataFrame(results).sort_values("Vehicles Needed")

        st.session_state["vehicle_options"] = {
            "best": df.head(3),
            "other": df
        }


# ===== VEHICLE DISPLAY =====
if st.session_state["vehicle_options"]:

    st.subheader("🚚 Best Options")
    best_df = st.data_editor(st.session_state["vehicle_options"]["best"], use_container_width=True)

    st.subheader("🔽 Other Options")
    other_df = st.data_editor(st.session_state["vehicle_options"]["other"], use_container_width=True)

    selected = pd.concat([
        best_df[best_df["Select"] == True],
        other_df[other_df["Select"] == True]
    ])

    if st.button("✅ Confirm Selection"):
        if selected.empty:
            st.warning("⚠️ Select at least one vehicle")
        else:
            st.session_state["confirmed"] = selected


# ===== FINAL =====
if st.session_state["confirmed"] is not None:
    st.subheader("📦 Final Plan")
    st.dataframe(st.session_state["confirmed"], use_container_width=True)

    if st.button("💾 Submit Plan"):
        st.success("Shipment Planned Successfully ✅")
