import streamlit as st
import pandas as pd
import math


# ===== SESSION INIT =====
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "user" not in st.session_state:
    st.session_state["user"] = ""

# ===== USER DATABASE =====
users = {
    "admin": "ICSA123",
    "manager": "ICSA456",
    "user1": "ICSA789",
    "client1": "CLIENT123",
    "viewer": "VIEW123"
}

# ===== LOGIN FUNCTION =====
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

# ===== MAIN APP =====
st.success(f"Welcome to Cargo Planner 🚚, {st.session_state['user']}")

# ===== LOGOUT =====
if st.button("Logout"):
    st.session_state["auth"] = False
    st.session_state["user"] = ""
    st.rerun()

st.set_page_config(page_title="ICSA Cargo Planner PRO", layout="wide")

# =========================
# SESSION INIT
# =========================
if "packages" not in st.session_state:
    st.session_state.packages = []

if "vehicle_options" not in st.session_state:
    st.session_state.vehicle_options = None

if "confirmed" not in st.session_state:
    st.session_state.confirmed = None

# =========================
# HEADER
# =========================
c1, c2, c3 = st.columns([1,4,1])

with c1:
    st.image("https://icsagroup.com/wp-content/themes/icsa/images/logo.png", width=120)

with c2:
    st.markdown(
        "<h3 style='text-align:center;'>International Clearing & Shipping Agency Pvt Ltd</h3>",
        unsafe_allow_html=True
    )

with c3:
    st.image("http://icsagroup.com/wp-content/uploads/2025/10/94-Years-Unit.png", width=80)

st.header("📦 Cargo Volume & Vehicle Planner")
st.markdown("---")

# =========================
# JOB ID
# =========================
col1, col2 = st.columns([1,5])
with col1:
    job_id = st.text_input("Job ID", max_chars=15)

# =========================
# MASTER DATA
# =========================
package_types = [
"Carton Box","Corrugated Box","Envelope","Poly Bag / Mailer",
"Wooden Crate","Wooden Box","Metal Case","Pallet","Pallet Box",
"Shrink-wrapped Pallet","Drum","Barrel","IBC (Intermediate Bulk Container)",
"Sack / Bag","Insulated Box","Refrigerated Package (Reefer)",
"Gel Pack Package","Cylindrical Package","Flat Pack",
"Hanging Garment Box","Skid","Loose Cargo",
"Over-Dimensional Cargo (ODC)","UN Certified Hazardous Package",
"Spill-proof Container","Bubble Wrap Package",
"Foam-Protected Package","Tamper-proof Bag"
]

vehicle_data = [
("TATA ACE","6 * 4 * 5","6"),
("TATA 407","9 * 6 * 5","8,9"),
("TATA - 12 Feet","12 * 6.4 * 5","11"),
("Canter - 14 Feet","14 * 6.4 * 5","14"),
("LPT - 17 Feet","17 * 6.8 * 6","17"),
("1109 - 19 Feet","19 * 7 * 7","21"),
("LP Truck - 18 Feet","18 * 6.9 * 7","20"),
("Taurus - 22 Feet / 15 MT","22 * 7.2 * 7","28"),
("Taurus - 24-25 Feet / 20 MT","24 * 7.3 * 7","30"),
("Taurus - 25-26 Feet / 25 M.T.","25 * 7.3 * 7","34"),
("20' Container","20 * 8 * 8","27"),
("22' Container","22 * 8 * 8","29"),
("24' Container","24 * 8 * 8","35"),
("28' Container","28 * 8 * 8","40"),
("32' Container S. AXL","32 * 8 * 8","50"),
("32' Container M.AXL","32 * 8 * 8","50"),
("32' Container HQ","32 * 9 * 10","55"),
("34' Container","34 * 8 * 8","55"),
("40' Container","40 * 8 * 8","55-60"),
("Platform Truck 20 Feet","20 * 8 * 7","30"),
("Platform Truck 22 Feet","22 * 8 * 7","33"),
("Platform / Half Body JCB Truck 28 FT","28 * 8 * 7","42"),
("40 Feet High Bed Trailer","40 * 8 * 7","60"),
("50 Feet Trailer / Semi Trailer","50 * 8 * 7","75"),
("40 Feet Semi Trailer","40 * 8 * 7","60"),
]

vehicle_df = pd.DataFrame(vehicle_data, columns=["Vehicle","Size","CBM"])

# =========================
# UTILS
# =========================
def to_feet(v,u):
    return {"mm":v/304.8,"cm":v/30.48,"m":v*3.28084,"inch":v/12}[u]

def calc_cbm(L,W,H,qty):
    return (L*W*H*qty)/35.315 if L and W and H else 0

def get_max_cbm(cbm):
    s=str(cbm)
    if "-" in s:
        return float(s.split("-")[-1])
    if "," in s:
        return float(s.split(",")[-1])
    return float(s)

# =========================
# INPUT
# =========================
st.subheader("📏 Package Dimension Calculator")

cols = st.columns(5)
unit = cols[0].selectbox("Unit", ["mm","cm","m","inch"])
L = cols[1].number_input("Length", min_value=0.0)
W = cols[2].number_input("Width", min_value=0.0)
H = cols[3].number_input("Height", min_value=0.0)
qty = cols[4].number_input("Quantity", min_value=1)

if st.button("📐 Calculate & Add"):
    if L == 0 or W == 0 or H == 0:
        st.warning("⚠️ Enter all dimensions")
    else:
        st.session_state.packages.append({
            "Box Name":package_types[0],
            "L":round(to_feet(L,unit),2),
            "W":round(to_feet(W,unit),2),
            "H":round(to_feet(H,unit),2),
            "Quantity":qty,
            "Weight Piece (KG)":0.0,
            "Rotation Allowed":False,
            "Stacking On Top":False,
            "Stacking Under":False
        })

# =========================
# TABLE HEADER + ADD ROW
# =========================
st.subheader("📦 Package Details (Feet)")

if st.button("➕ Add Cargo Row"):
    st.session_state.packages.append({
        "Box Name":package_types[0],
        "L":0.0,"W":0.0,"H":0.0,
        "Quantity":1,
        "Weight Piece (KG)":0.0,
        "Rotation Allowed":False,
        "Stacking On Top":False,
        "Stacking Under":False
    })

header = st.columns([2,1,1,1,1,1,1,1,1,1,1,1])
titles = ["Box Name","L","W","H","Qty","Weight","Total Wt","CBM","Rotation","On Top","Under","Delete"]

for col, t in zip(header, titles):
    col.markdown(f"**{t}**")

# =========================
# TABLE ROWS
# =========================
delete_index=None
total_cbm=0
total_weight=0
total_boxes=0

for i,pkg in enumerate(st.session_state.packages):

    cols = st.columns([2,1,1,1,1,1,1,1,1,1,1,1])

    pkg["Box Name"]=cols[0].selectbox("",package_types,key=f"name{i}")
    pkg["L"]=cols[1].number_input("",value=float(pkg["L"]),key=f"L{i}")
    pkg["W"]=cols[2].number_input("",value=float(pkg["W"]),key=f"W{i}")
    pkg["H"]=cols[3].number_input("",value=float(pkg["H"]),key=f"H{i}")
    pkg["Quantity"]=cols[4].number_input("",value=int(pkg["Quantity"]),key=f"Q{i}")
    pkg["Weight Piece (KG)"]=cols[5].number_input("",value=float(pkg["Weight Piece (KG)"]),key=f"WT{i}")

    tot_wt=pkg["Quantity"]*pkg["Weight Piece (KG)"]
    cbm=calc_cbm(pkg["L"],pkg["W"],pkg["H"],pkg["Quantity"])

    cols[6].write(round(tot_wt,2))
    cols[7].write(round(cbm,2))

    pkg["Rotation Allowed"]=cols[8].checkbox("",value=pkg["Rotation Allowed"],key=f"R{i}")
    pkg["Stacking On Top"]=cols[9].checkbox("",value=pkg["Stacking On Top"],key=f"T{i}")
    pkg["Stacking Under"]=cols[10].checkbox("",value=pkg["Stacking Under"],key=f"U{i}")

    if cols[11].button("🗑",key=f"del{i}"):
        delete_index=i

    total_cbm+=cbm
    total_weight+=tot_wt
    total_boxes+=pkg["Quantity"]

if delete_index is not None:
    st.session_state.packages.pop(delete_index)
    st.rerun()

# =========================
# TOTALS
# =========================
st.markdown("---")
c1,c2,c3=st.columns(3)
c1.metric("Total CBM",round(total_cbm,2))
c2.metric("Total Weight (kg)",round(total_weight,2))
c3.metric("Total Boxes",int(total_boxes))

# =========================
# SAVE & CALCULATE
# =========================
if st.button("💾 Save & Calculate"):

    if total_cbm==0:
        st.warning("⚠️ No valid cargo data")
    else:
        results=[]

        for _,v in vehicle_df.iterrows():
            cap=get_max_cbm(v["CBM"])
            vehicles=math.ceil(total_cbm/cap)

            occupied=total_cbm
            total_capacity=vehicles*cap
            remaining=total_capacity-occupied

            results.append({
                "Select":False,
                "Vehicle":v["Vehicle"],
                "Size":v["Size"],
                "Capacity (CBM)":cap,
                "Total Capacity":round(total_capacity,2),
                "Occupied":round(occupied,2),
                "Remaining":round(remaining,2),
                "Vehicles Needed":vehicles
            })

        df=pd.DataFrame(results).sort_values("Vehicles Needed")

        st.session_state.vehicle_options={
            "best":df.head(3),
            "other":df
        }

# =========================
# VEHICLE DISPLAY
# =========================
if st.session_state.vehicle_options:

    st.subheader("🚚 Best Options")
    best_df=st.data_editor(st.session_state.vehicle_options["best"],use_container_width=True)

    st.subheader("🔽 Other Options")
    other_df=st.data_editor(st.session_state.vehicle_options["other"],use_container_width=True)

    selected=pd.concat([
        best_df[best_df["Select"]==True],
        other_df[other_df["Select"]==True]
    ])

    if st.button("✅ Confirm Selection"):
        if selected.empty:
            st.warning("⚠️ Select at least one vehicle")
        else:
            st.session_state.confirmed=selected

# =========================
# FINAL
# =========================
if st.session_state.confirmed is not None:
    st.subheader("📦 Final Plan")
    st.dataframe(st.session_state.confirmed,use_container_width=True)

    if st.button("💾 Submit Plan"):
        st.toast("Shipment Planned Successfully", icon="✅")
