import streamlit as st
import pandas as pd
import math
from itertools import permutations
import plotly.graph_objects as go
import random

# ===== PAGE CONFIG (MUST BE FIRST) =====
st.set_page_config(page_title="ICSA Dimensions Calculation", layout="wide", page_icon="🚢")

# ===== CUSTOM CSS =====    
st.markdown("""
<style>
    .stApp { background-color: #f0f4f8; }

    input[type="number"], input[type="text"],
    .stNumberInput input, .stTextInput input {
        background-color: #ffffff !important; color: #000000 !important; font-size: 20px !important;
    }
    .stSelectbox > div > div { background-color: #ffffff !important; color: #000000 !important; font-size: 20px !important; }
    [data-baseweb="select"] *  { color: #000000 !important; font-size: 20px !important; }
    [data-baseweb="popover"] * { color: #000000 !important; background: #ffffff !important; font-size: 20px !important; }
    label, [data-testid="stWidgetLabel"] > div { color: #000000 !important; font-size: 20px !important; }
    .stCheckbox span { color: #000000 !important; font-size: 20px !important; }
    .stMarkdown p, .stMarkdown li, .stMarkdown strong, .stMarkdown span { color: #000000 !important; font-size: 20px !important; }
    [data-testid="stExpander"] summary span { color: #000000 !important; font-size: 20px !important; }
    button[data-baseweb="tab"] { color: #000000 !important; font-size: 20px !important; font-weight: 600 !important; }

    .header-card {
        background: linear-gradient(135deg, #1a3a5c 0%, #2e6da4 100%);
        border-radius: 14px; padding: 23px 33px; margin-bottom: 22px;
        display: flex; align-items: center; justify-content: space-between;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .header-title { color: white; font-size: 29px; font-weight: 700; margin: 0; text-align: center; }
    .header-sub   { color: #b8d4f0; font-size: 16px; text-align: center; }

    .metric-card {
        background: white; border-radius: 10px; padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-left: 4px solid #2e6da4; text-align: center;
    }
    .metric-val { font-size: 35px; font-weight: 700; }
    .metric-lbl { font-size: 18px; color: #555; text-transform: uppercase; letter-spacing: 1px; }

    .section-header {
        background: white; border-radius: 8px; padding: 12px 18px; margin: 18px 0 12px 0;
        border-left: 4px solid #2e6da4; font-weight: 700; font-size: 17px;
        color: #1a3a5c; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }
    .tbl-hdr { font-size: 15px; font-weight: 700; color: #1a3a5c; padding-bottom: 4px; }

    .pill-warn { background:#fff3cd; color:#856404; border-radius:20px; padding:3px 10px; font-size:18px; font-weight:600; display:inline-block; }
    .pill-ok   { background:#d1e7dd; color:#0f5132; border-radius:20px; padding:3px 10px; font-size:18px; font-weight:600; display:inline-block; }
    .pill-err  { background:#f8d7da; color:#842029; border-radius:20px; padding:3px 10px; font-size:18px; font-weight:600; display:inline-block; }
    .pill-info { background:#cfe2ff; color:#084298; border-radius:20px; padding:3px 10px; font-size:18px; font-weight:600; display:inline-block; }

    .vehicle-best  { background:linear-gradient(135deg,#e8f4fd,#ffffff); border:2px solid #2e6da4; border-radius:10px; padding:16px 20px; margin-bottom:12px; }
    .vehicle-other { background:white; border:1px solid #dee2e6; border-radius:8px; padding:12px 16px; margin-bottom:8px; }
    .vehicle-row   { background:#f8f9ff; border:1px solid #c5d5e8; border-radius:8px; padding:12px 16px; margin-bottom:8px; }
    .final-card    { background:white; border-radius:10px; padding:18px 22px; margin-bottom:12px; border-left:5px solid #198754; box-shadow:0 2px 8px rgba(0,0,0,0.08); }

    #MainMenu { visibility: hidden; }
    footer     { visibility: hidden; }
    header     { visibility: hidden; }

    .stButton > button { border-radius: 8px; font-weight: 600; font-size: 20px; transition: all 0.2s; }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }
    div[data-testid="stDataFrame
            Resizable"] { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ===== SESSION INIT =====
for key, default in [
    ("auth", False), ("user", ""), ("packages", []),
    ("vehicle_options", None), ("confirmed", None), ("plan_submitted", False)
]:
    if key not in st.session_state:
        st.session_state[key] = default

users = {
    "admin": "ICSA123", "manager": "ICSA456",
    "user1": "ICSA789", "client1": "CLIENT123", "viewer": "VIEW123"
}
#---
# ===== LOGIN =====
def login():
    st.markdown("""
    <div style="max-width:420px;margin:60px auto;background:white;padding:40px;
    border-radius:16px;box-shadow:0 8px 30px rgba(0,0,0,0.12);">
    <h2 style="text-align:center;color:#1a3a5c;">🔐 ICSA Dimensions Calculation</h2>
    <p style="text-align:center;color:#888;font-size:14px;">LogistICSA</p>
    </div>""", unsafe_allow_html=True)
    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown("### Sign In")
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        if st.button("Login →", use_container_width=True, type="primary"):
            if username in users and users[username] == password:
                st.session_state["auth"] = True
                st.session_state["user"] = username
                st.rerun()
            else:
                st.error("❌ Invalid credentials.")

if not st.session_state["auth"]:
    login()
    st.stop()
# =========================
# MASTER DATA
# =========================
package_types = [
    "Carton Box","Corrugated Box","Envelope","Poly Bag / Mailer",
    "Wooden Crate","Wooden Box","Metal Case","Pallet","Pallet Box",
    "Shrink-wrapped Pallet","Drum","Barrel","IBC (Intermediate Bulk Container)",
    "Sack / Bag","Insulated Box","Refrigerated Package (Reefer)",
    "Gel Pack Package","Cylindrical Package","Flat Pack","Hanging Garment Box",
    "Skid","Loose Cargo","Over-Dimensional Cargo (ODC)","UN Certified Hazardous Package",
    "Spill-proof Container","Bubble Wrap Package","Foam-Protected Package","Tamper-proof Bag"
]

PKG_VEHICLE_TYPE = {
    "Carton Box":"any","Corrugated Box":"any","Envelope":"closed","Poly Bag / Mailer":"closed",
    "Wooden Crate":"any","Wooden Box":"any","Metal Case":"any","Pallet":"any","Pallet Box":"any",
    "Shrink-wrapped Pallet":"any","Drum":"closed","Barrel":"closed",
    "IBC (Intermediate Bulk Container)":"closed","Sack / Bag":"closed","Insulated Box":"closed",
    "Refrigerated Package (Reefer)":"reefer","Gel Pack Package":"closed",
    "Cylindrical Package":"closed","Flat Pack":"any","Hanging Garment Box":"closed",
    "Skid":"open","Loose Cargo":"any","Over-Dimensional Cargo (ODC)":"open",
    "UN Certified Hazardous Package":"closed","Spill-proof Container":"closed",
    "Bubble Wrap Package":"any","Foam-Protected Package":"any","Tamper-proof Bag":"closed",
}

def vehicle_category(name):
    n = name.lower()
    if "container" in n: return "closed"
    if "platform" in n or "trailer" in n or "flatbed" in n: return "open"
    return "closed"

# name, L(ft), W(ft), H(ft), CBM capacity
vehicle_data = [
    ("TATA ACE",                  6,   4,   5,   6),
    ("TATA 407",                  9,   6,   5,   9),
    ("TATA - 12 Feet",           12,   6.4, 5,  11),
    ("Canter - 14 Feet",         14,   6.4, 5,  14),
    ("LPT - 17 Feet",            17,   6.8, 6,  17),
    ("1109 - 19 Feet",           19,   7,   7,  21),
    ("LP Truck - 18 Feet",       18,   6.9, 7,  20),
    ("Taurus - 22 Feet",         22,   7.2, 7,  28),
    ("Taurus - 24-25 Feet",      24,   7.3, 7,  30),
    ("Taurus - 25-26 Feet",      25,   7.3, 7,  34),
    ("20' Container",            20,   8,   8,  27),
    ("22' Container",            22,   8,   8,  29),
    ("24' Container",            24,   8,   8,  35),
    ("28' Container",            28,   8,   8,  40),
    ("32' Container S.AXL",      32,   8,   8,  50),
    ("32' Container M.AXL",      32,   8,   8,  50),
    ("32' Container HQ",         32,   9,  10,  55),
    ("34' Container",            34,   8,   8,  55),
    ("40' Container",            40,   8,   8,  60),
    ("Platform 20 Feet",         20,   8,   7,  30),
    ("Platform 22 Feet",         22,   8,   7,  33),
    ("Platform/Half Body 28 FT", 28,   8,   7,  42),
    ("40 Feet High Bed Trailer", 40,   8,   7,  60),
    ("50 Feet Semi Trailer",     50,   8,   7,  75),
    ("40 Feet Semi Trailer",     40,   8,   7,  60),
]

# =========================
# UTILS
# =========================
def to_feet(v, u):
    return {"mm":v/304.8,"cm":v/30.48,"m":v*3.28084,"inch":v/12}[u]

def calc_cbm(L, W, H, qty):
    return (L*W*H*qty)/35.315 if (L and W and H) else 0

def validate_dimensions(L, W, H, unit):
    warns=[]
    f={"mm":0.1,"cm":1,"m":100,"inch":2.54}[unit]
    lc,wc,hc=L*f,W*f,H*f
    if lc>2000 or wc>2000 or hc>2000: warns.append("⚠️ Dimensions look unrealistically large — check unit")
    if 0<lc<1 or 0<wc<1 or 0<hc<1:   warns.append("⚠️ Very small dimensions — check unit")
    return warns

def get_best_orientation(pL,pW,pH,vL,vW,vH,rot):
    orients=list(set(permutations([pL,pW,pH]))) if rot else [(pL,pW,pH)]
    best=None
    for (l,w,h) in orients:
        if l<=vL and w<=vW and h<=vH:
            if best is None or (vL-l+vW-w+vH-h)<(vL-best[0]+vW-best[1]+vH-best[2]):
                best=(l,w,h)
    return (True,*best) if best else (False,pL,pW,pH)

def boxes_per_vehicle(pL,pW,pH,vL,vW,vH,rot,s_on,s_un):
    orients=list(set(permutations([pL,pW,pH]))) if rot else [(pL,pW,pH)]
    best_count=0
    for (l,w,h) in orients:
        if not(l and w and h): continue
        aL=math.floor(vL/l) if l<=vL else 0
        aW=math.floor(vW/w) if w<=vW else 0
        if s_on and s_un:     sl=math.floor(vH/h) if h>0 else 1
        elif s_on or s_un:    sl=min(2,math.floor(vH/h)) if h>0 else 1
        else:                 sl=1 if h<=vH else 0
        c=aL*aW*sl
        if c>best_count: best_count=c
    return max(0,best_count)

def get_required_vehicle_type(packages):
    types={PKG_VEHICLE_TYPE.get(p.get("Box Name",""),"any") for p in packages}
    if "reefer" in types: return "reefer"
    if "open" in types and "closed" in types: return "closed"
    if "open" in types: return "open"
    if "closed" in types: return "closed"
    return "any"

def vehicle_matches_type(vname, req):
    if req=="any": return True,""
    vcat=vehicle_category(vname)
    if req=="reefer": return False,"⚠️ Reefer cargo needs refrigerated transport"
    if req=="closed" and vcat=="open": return False,"⚠️ Open vehicle — not suitable for enclosed cargo"
    return True,""

def suggest_vehicles(packages):
    valid=[p for p in packages if p["L"]>0 and p["W"]>0 and p["H"]>0 and p["Quantity"]>0]
    if not valid: return []
    req_type=get_required_vehicle_type(valid)
    total_qty=sum(p["Quantity"] for p in valid)
    results=[]

    for (name,vL,vW,vH,cap) in vehicle_data:
        type_ok,type_warn=vehicle_matches_type(name,req_type)
        fits_all=True
        eff_cbm=0.0
        row_details=[]

        for pkg in valid:
            rot=pkg.get("Rotation Allowed",False)
            s_on=pkg.get("Stacking On Top",False)
            s_un=pkg.get("Stacking Under",False)
            fits,bL,bW,bH=get_best_orientation(pkg["L"],pkg["W"],pkg["H"],vL,vW,vH,rot)
            if not fits: fits_all=False
            sf=0.6 if (s_on and s_un) else 0.8 if (s_on or s_un) else 1.0
            eff_cbm+=calc_cbm(bL,bW,bH,pkg["Quantity"])*sf
            bpv=boxes_per_vehicle(pkg["L"],pkg["W"],pkg["H"],vL,vW,vH,rot,s_on,s_un) if fits else 0
            row_details.append({"box_name":pkg["Box Name"],"qty":pkg["Quantity"],"bpv":bpv,"fits":fits})

        vehicles_needed=math.ceil(eff_cbm/cap) if eff_cbm>0 else 1
        total_cap=vehicles_needed*cap
        remaining_cbm=total_cap-eff_cbm
        utilization=round(eff_cbm/total_cap*100,1) if total_cap>0 else 0
        total_box_cap=sum(r["bpv"]*vehicles_needed for r in row_details)
        remaining_box=max(0,total_box_cap-total_qty)

        warns=[]
        if not type_ok:                            warns.append(type_warn)
        if not fits_all:                           warns.append("📦 Some packages exceed vehicle dimensions")
        if utilization<40 and vehicles_needed==1:  warns.append("📉 Low space use — consider smaller vehicle")
        if vehicles_needed>5:                      warns.append("🔢 Many vehicles needed")

        score=0
        if type_ok:  score+=3
        if fits_all: score+=3
        score+=min(utilization/20,3)
        score-=vehicles_needed*0.1

        results.append({
            "Vehicle":name,"Vehicle Size (ft)":f"{vL}×{vW}×{vH}","Cap (CBM)":cap,
            "Vehicles Needed":vehicles_needed,"Eff. CBM":round(eff_cbm,3),
            "Total Cap (CBM)":round(total_cap,2),"Remaining CBM":round(remaining_cbm,3),
            "Utilization %":utilization,"Total Box Capacity":total_box_cap,
            "Boxes Occupied":total_qty,"Boxes Remaining":remaining_box,
            "Fits Dims":fits_all,"Type OK":type_ok,"Req Vehicle Type":req_type,
            "_warnings":warns,"_row_details":row_details,"_score":score,
        })

    results.sort(key=lambda x:(-x["_score"],x["Vehicles Needed"],-x["Utilization %"]))
    return results

# =========================
#---SMART PACKING AI ENGINE
def generate_3d_container(packages, vL, vW, vH):
    

    fig = go.Figure()

    # ===== DRAW CONTAINER (STRONG BLACK FRAME) =====
    edges = [
        ([0, vL], [0, 0], [0, 0]), ([0, vL], [vW, vW], [0, 0]),
        ([0, vL], [0, 0], [vH, vH]), ([0, vL], [vW, vW], [vH, vH]),

        ([0, 0], [0, vW], [0, 0]), ([vL, vL], [0, vW], [0, 0]),
        ([0, 0], [0, vW], [vH, vH]), ([vL, vL], [0, vW], [vH, vH]),

        ([0, 0], [0, 0], [0, vH]), ([vL, vL], [0, 0], [0, vH]),
        ([0, 0], [vW, vW], [0, vH]), ([vL, vL], [vW, vW], [0, vH]),
    ]

    for e in edges:
        fig.add_trace(go.Scatter3d(
            x=e[0], y=e[1], z=e[2],
            mode='lines',
            line=dict(color='black', width=5),
            showlegend=False
        ))

    # ===== COLORS =====
    colors = ["red", "blue", "green", "orange", "purple", "cyan"]

    placed_boxes = []
    box_counter = 1

    # ===== SMART PACKING CORE =====
    cursor_x = cursor_y = cursor_z = 0
    max_row_height = 0
    max_layer_height = 0

    for idx, pkg in enumerate(packages):

        dims = sorted([pkg["L"], pkg["W"], pkg["H"]], reverse=True)
        l, w, h = dims # AUTO ROTATION

        qty = int(pkg["Quantity"])

        for _ in range(qty):

            # Move to next row
            if cursor_x + l > vL:
                cursor_x = 0
                cursor_y += max_row_height
                max_row_height = 0

            # Move to next layer
            if cursor_y + w > vW:
                cursor_y = 0
                cursor_z += max_layer_height
                max_layer_height = 0

            # Stop if container full
            if cursor_z + h > vH:
                break

            # Store box position
            placed_boxes.append((cursor_x, cursor_y, cursor_z, l, w, h, idx))

            # Update positions
            cursor_x += l
            max_row_height = max(max_row_height, w)
            max_layer_height = max(max_layer_height, h)

    # ===== DRAW BOXES =====
    for (x0, y0, z0, l, w, h, idx) in placed_boxes:

        color = colors[idx % len(colors)]

        fig.add_trace(go.Mesh3d(
            x=[x0, x0+l, x0+l, x0, x0, x0+l, x0+l, x0],
            y=[y0, y0, y0+w, y0+w, y0, y0, y0+w, y0+w],
            z=[z0, z0, z0, z0, z0+h, z0+h, z0+h, z0+h],
            color=color,
            opacity=1,
            flatshading=True,
            showscale=False
        ))

        # ===== BOX NUMBER LABEL =====
        fig.add_trace(go.Scatter3d(
            x=[x0 + l/2],
            y=[y0 + w/2],
            z=[z0 + h/2],
            text=[str(box_counter)],
            mode='text',
            textfont=dict(color='black', size=10),
            showlegend=False
        ))

        box_counter += 1

    # ===== EMPTY SPACE (TRANSPARENT GREY BLOCK) =====
    if placed_boxes:
        used_x = max([b[0] + b[3] for b in placed_boxes])
        used_y = max([b[1] + b[4] for b in placed_boxes])
        used_z = max([b[2] + b[5] for b in placed_boxes])

        fig.add_trace(go.Mesh3d(
            x=[used_x, vL, vL, used_x, used_x, vL, vL, used_x],
            y=[0, 0, vW, vW, 0, 0, vW, vW],
            z=[0, 0, 0, 0, vH, vH, vH, vH],
            color='lightgrey',
            opacity=0.2,
            showscale=False
        ))

    # ===== LAYOUT =====
    fig.update_layout(
        scene=dict(
            xaxis=dict(backgroundcolor="white", gridcolor="black"),
            yaxis=dict(backgroundcolor="white", gridcolor="black"),
            zaxis=dict(backgroundcolor="white", gridcolor="black"),
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=0, r=0, b=0, t=0)
    )

    return fig
# =========================
# HEADER
# =========================
st.markdown("""
<div class="header-card">
    <div><img src="https://icsagroup.com/wp-content/themes/icsa/images/logo.png"
         style="height:50px;" onerror="this.style.display='none'"/></div>
    <div>
        <p class="header-title">LogistICSA</p>
        <p class="header-sub">📦ICSA Dimensions Calculation</p>
    </div>
    <div style="text-align:right;"><img src="http://icsagroup.com/wp-content/uploads/2025/10/94-Years-Unit.png"
         style="height:40px;" onerror="this.style.display='none'"/></div>
</div>""", unsafe_allow_html=True)

c1,c2,c3,c4=st.columns([2,3,2,1])
with c1: job_id=st.text_input("🆔 Job ID",max_chars=15,placeholder="e.g. JOB-2025-001")
with c2: st.markdown(f"<div style='padding-top:28px;color:#000;font-size:15px;'>👤 Logged in as <strong>{st.session_state['user']}</strong></div>",unsafe_allow_html=True)
with c4:
    if st.button("🚪 Logout",use_container_width=True):
        st.session_state["auth"]=False; st.session_state["user"]=""; st.rerun()

st.markdown("---")

# =========================
# QUICK CALCULATOR
# =========================
st.markdown('<div class="section-header">📏 Quick Package Calculator</div>',unsafe_allow_html=True)
with st.container():
    cols=st.columns([1.2,1,1,1,1,1,1.5])
    unit  =cols[0].selectbox("Unit",["mm","cm","m","inch"],key="unit_sel")
    L_in  =cols[1].number_input("Length",         min_value=0.0,key="qL")
    W_in  =cols[2].number_input("Width",           min_value=0.0,key="qW")
    H_in  =cols[3].number_input("Height",          min_value=0.0,key="qH")
    qty_in=cols[4].number_input("Quantity",        min_value=1,  key="qQty")
    wt_in =cols[5].number_input("Weight/pc (kg)", min_value=0.0,key="qWt")

    if L_in>0 and W_in>0 and H_in>0:
        lf=to_feet(L_in,unit);wf=to_feet(W_in,unit);hf=to_feet(H_in,unit)
        prev_cbm=calc_cbm(lf,wf,hf,qty_in)
        cols[6].markdown(f"""<div style="margin-top:22px;background:#e8f4fd;border-radius:8px;
        padding:10px;text-align:center;font-size:15px;color:#000;">
            <strong>{round(prev_cbm,3)} CBM</strong><br>
            <span style="color:#444;">{round(lf,2)}×{round(wf,2)}×{round(hf,2)} ft</span>
        </div>""",unsafe_allow_html=True)

    for w in (validate_dimensions(L_in,W_in,H_in,unit) if L_in>0 and W_in>0 and H_in>0 else []):
        st.warning(w)

    if st.button("➕ Add Package",type="primary"):
        if not(L_in and W_in and H_in): st.error("⚠️ Enter all dimensions (L, W, H)")
        else:
            st.session_state.packages.append({
                "Box Name":package_types[0],
                "L":round(to_feet(L_in,unit),3),"W":round(to_feet(W_in,unit),3),"H":round(to_feet(H_in,unit),3),
                "Quantity":int(qty_in),"Weight Piece (KG)":float(wt_in),
                "Rotation Allowed":False,"Stacking On Top":False,"Stacking Under":False
            })
            st.rerun()

# =========================
# PACKAGE TABLE
# =========================
st.markdown('<div class="section-header">📦 Package Details (Dimensions in Feet)</div>',unsafe_allow_html=True)

ca,cb=st.columns([1,5])
with ca:
    if st.button("➕ Add Empty Row"):
        st.session_state.packages.append({
            "Box Name":package_types[0],"L":0.0,"W":0.0,"H":0.0,"Quantity":1,
            "Weight Piece (KG)":0.0,"Rotation Allowed":False,"Stacking On Top":False,"Stacking Under":False
        });st.rerun()
with cb:
    if st.button("🗑️ Clear All"):
        for k in ["packages","vehicle_options","confirmed"]: st.session_state[k]=None if k!="packages" else []
        st.session_state.plan_submitted=False;st.rerun()

hdr=st.columns([2,0.8,0.8,0.8,0.7,0.9,0.8,0.8,0.75,0.75,0.75,0.5])
for h,lbl in zip(hdr,["Box Name","L (ft)","W (ft)","H (ft)","Qty","Wt/pc (kg)","Total Wt","CBM","🔄 Rotate","⬆️ On Top","⬇️ Under","Del"]):
    h.markdown(f"<div class='tbl-hdr'>{lbl}</div>",unsafe_allow_html=True)

delete_index=None
total_cbm=total_weight=total_boxes=0.0
row_issues=[]

for i,pkg in enumerate(st.session_state.packages):
    cols=st.columns([2,0.8,0.8,0.8,0.7,0.9,0.8,0.8,0.75,0.75,0.75,0.5])
    pkg["Box Name"]         =cols[0].selectbox("",package_types,index=package_types.index(pkg["Box Name"]) if pkg["Box Name"] in package_types else 0,key=f"name{i}",label_visibility="collapsed")
    pkg["L"]                =cols[1].number_input("",value=float(pkg["L"]),min_value=0.0,key=f"L{i}",label_visibility="collapsed",format="%.3f")
    pkg["W"]                =cols[2].number_input("",value=float(pkg["W"]),min_value=0.0,key=f"W{i}",label_visibility="collapsed",format="%.3f")
    pkg["H"]                =cols[3].number_input("",value=float(pkg["H"]),min_value=0.0,key=f"H{i}",label_visibility="collapsed",format="%.3f")
    pkg["Quantity"]         =cols[4].number_input("",value=int(pkg["Quantity"]),min_value=1,key=f"Q{i}",label_visibility="collapsed")
    pkg["Weight Piece (KG)"]=cols[5].number_input("",value=float(pkg["Weight Piece (KG)"]),min_value=0.0,key=f"WT{i}",label_visibility="collapsed")

    tot_wt=pkg["Quantity"]*pkg["Weight Piece (KG)"]
    cbm=calc_cbm(pkg["L"],pkg["W"],pkg["H"],pkg["Quantity"])
    row_warn=[]
    if not(pkg["L"] and pkg["W"] and pkg["H"]): row_warn.append("missing dims")
    if not pkg["Weight Piece (KG)"]:            row_warn.append("no weight")

    cols[6].markdown(f"<div style='padding-top:8px;font-size:15px;color:#000;'>{round(tot_wt,2)}</div>",unsafe_allow_html=True)
    cols[7].markdown(f"<div style='padding-top:8px;font-size:15px;font-weight:700;color:{'#0a5c2e' if cbm>0 else '#842029'};'>{round(cbm,3)}</div>",unsafe_allow_html=True)

    pkg["Rotation Allowed"]=cols[8].checkbox("", value=pkg["Rotation Allowed"],key=f"R{i}",label_visibility="collapsed")
    pkg["Stacking On Top"] =cols[9].checkbox("", value=pkg["Stacking On Top"], key=f"T{i}",label_visibility="collapsed")
    pkg["Stacking Under"]  =cols[10].checkbox("",value=pkg["Stacking Under"],  key=f"U{i}",label_visibility="collapsed")
    if cols[11].button("🗑",key=f"del{i}"): delete_index=i

    if row_warn: row_issues.append((i+1,row_warn))
    total_cbm+=cbm; total_weight+=tot_wt; total_boxes+=pkg["Quantity"]

if delete_index is not None:
    st.session_state.packages.pop(delete_index);st.rerun()

if row_issues:
    with st.expander(f"⚠️ {len(row_issues)} row(s) have issues",expanded=False):
        for rn,issues in row_issues: st.markdown(f"**Row {rn}:** {', '.join(issues)}")

# =========================
# TOTALS
# =========================
st.markdown("---")
m1,m2,m3,m4=st.columns(4)
def metric_card(col,val,label,color="#2e6da4"):
    col.markdown(f"""<div class="metric-card" style="border-left-color:{color};">
        <div class="metric-val" style="color:{color};">{val}</div>
        <div class="metric-lbl">{label}</div></div>""",unsafe_allow_html=True)

metric_card(m1,round(total_cbm,3),   "Total CBM",        "#2e6da4")
metric_card(m2,round(total_weight,2),"Total Weight (kg)","#198754")
metric_card(m3,int(total_boxes),     "Total Boxes",       "#fd7e14")
metric_card(m4,len(st.session_state.packages),"Cargo Rows","#6f42c1")

# =========================
# SAVE & CALCULATE
# =========================
st.markdown("")
cc,_=st.columns([2,5])
with cc: calc_btn=st.button("🔍 Save & Calculate Vehicle Options",type="primary",use_container_width=True)

if calc_btn:
    if total_cbm==0:
        st.error("⚠️ No valid cargo data — enter dimensions for at least one package")
    else:
        valid_pkgs=[p for p in st.session_state.packages if p["L"]>0 and p["W"]>0 and p["H"]>0 and p["Quantity"]>0]
        skipped=len(st.session_state.packages)-len(valid_pkgs)
        if skipped: st.warning(f"⚠️ {skipped} row(s) with missing dimensions ignored")
        st.session_state.vehicle_options=suggest_vehicles(valid_pkgs)
        st.session_state.confirmed=None
        st.session_state.plan_submitted=False

# =========================
# VEHICLE SUGGESTIONS
# =========================
if st.session_state.vehicle_options:
    results     =st.session_state.vehicle_options
    best_results=[r for r in results if r["Type OK"] and r["Fits Dims"]]
    other_results=[r for r in results if not(r["Type OK"] and r["Fits Dims"])]
    req_type    =results[0]["Req Vehicle Type"] if results else "any"

    st.markdown('<div class="section-header">🚚 Vehicle Suggestions</div>',unsafe_allow_html=True)

    if req_type!="any":
        lbl={"closed":"🔒 Enclosed vehicles recommended (based on package type)",
             "open":  "🚛 Open / flatbed vehicles suitable (based on package type)",
             "reefer":"❄️ Refrigerated transport required (Reefer cargo detected)"}
        st.info(lbl.get(req_type,""))

    tab_best,tab_other,tab_row,tab_final=st.tabs(["⭐ Best Suggestions","🔽 Other Options","📊 Row-wise Plan","📋 Final Plan"])

    # ── helper ──
    def veh_card(r, card_key, btn_label, card_class="vehicle-best"):
        util=r["Utilization %"]
        uc="#198754" if util>=70 else "#fd7e14" if util>=40 else "#dc3545"
        warn_html=" ".join([f'<span class="pill-warn">{w}</span>' for w in r["_warnings"]])
        boc=r["Boxes Occupied"]; btc=r["Total Box Capacity"]; brc=r["Boxes Remaining"]
        box_pct=round(boc/btc*100,1) if btc>0 else 0
        st.markdown(f"""
        <div class="{card_class}">
            <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
                <div>
                    <span style="font-size:18px;font-weight:700;color:#1a3a5c;">🚛 {r['Vehicle']}</span>
                    <span style="margin-left:10px;color:#444;font-size:14px;">{r['Vehicle Size (ft)']} ft &nbsp;|&nbsp; {r['Cap (CBM)']} CBM cap</span>
                </div>
                <div style="text-align:right;">
                    <span style="font-size:26px;font-weight:700;color:#2e6da4;">{r['Vehicles Needed']}</span>
                    <span style="color:#444;font-size:14px;"> vehicle(s) needed</span>
                </div>
            </div>
            <div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:18px;font-size:15px;color:#000;">
                <span>📦 CBM Used: <strong>{r['Eff. CBM']}</strong> / {r['Total Cap (CBM)']}</span>
                <span>🟩 CBM Free: <strong>{r['Remaining CBM']}</strong></span>
                <span>📊 Space Used: <strong style="color:{uc};">{util}%</strong></span>
            </div>
            <div style="margin-top:6px;display:flex;flex-wrap:wrap;gap:18px;font-size:15px;color:#000;">
                <span>📫 Boxes Occupied: <strong>{boc}</strong></span>
                <span>📬 Total Box Capacity: <strong>{btc}</strong></span>
                <span>📭 Box Spaces Free: <strong>{brc}</strong></span>
                <span>🎯 Box Fill: <strong style="color:{uc};">{box_pct}%</strong></span>
            </div>
            <div style="margin-top:8px;">{warn_html}</div>
        </div>""",unsafe_allow_html=True)

        if st.button(btn_label, key=card_key):
            existing=st.session_state.confirmed or []
            if r["Vehicle"] not in [x["Vehicle"] for x in existing]:
                existing.append(r)
                st.session_state.confirmed=existing
            st.success(f"✅ {r['Vehicle']} added to Final Plan — go to 📋 Final Plan tab.")

    # ─── TAB 1: BEST ───
    with tab_best:
        show=best_results[:5] if best_results else results[:5]
        st.markdown(f"<div style='font-size:15px;color:#000;margin-bottom:12px;'>Top <strong>{len(show)}</strong> suitable vehicle(s) for your cargo:</div>",unsafe_allow_html=True)
        if not best_results:
            st.warning("⚠️ No fully matching vehicle found — showing closest options.")
        for idx,r in enumerate(show):
            veh_card(r, f"bsel_{idx}", f"✅ Select — {r['Vehicle']}", "vehicle-best")

    # ─── TAB 2: OTHER OPTIONS ───
    with tab_other:
        show_others=other_results if other_results else [r for r in results if r not in best_results[:5]]
        st.markdown(f"<div style='font-size:15px;color:#000;margin-bottom:12px;'><strong>{len(show_others)}</strong> other vehicle(s) (with warnings / partial fit):</div>",unsafe_allow_html=True)
        if not show_others:
            st.info("No other options — all suitable vehicles shown in Best Suggestions.")
        else:
            for idx,r in enumerate(show_others):
                veh_card(r, f"osel_{idx}", f"➕ Add to Plan — {r['Vehicle']}", "vehicle-other")

    # ─── TAB 3: ROW-WISE ───
    with tab_row:
        st.markdown(
        "<div style='font-size:15px;color:#000;margin-bottom:12px;'>"
        "<strong>Individual vehicle suggestion per row (pure dimension-based):</strong>"
        "</div>",
        unsafe_allow_html=True
        )

        valid_pkgs = [
        p for p in st.session_state.packages
        if p["L"] > 0 and p["W"] > 0 and p["H"] > 0 and p["Quantity"] > 0
         ]

        if not valid_pkgs:
            st.info("No packages with valid dimensions yet.")
        else:
            for i, pkg in enumerate(valid_pkgs):

            # 🔥 KEY CHANGE → evaluate ONLY THIS ROW
                single_pkg = [pkg]
                row_results = suggest_vehicles(single_pkg)

                if not row_results:
                    continue

                best = row_results[0]
                alternatives = row_results[1:3]

                row_cbm = calc_cbm(pkg["L"], pkg["W"], pkg["H"], pkg["Quantity"])

                pt_req = PKG_VEHICLE_TYPE.get(pkg["Box Name"], "any")
                tbadge = {
                "closed": "🔒 Closed",
                "open": "🚛 Open",
                "reefer": "❄️ Reefer",
                "any": "✅ Any"
                }.get(pt_req, "")

                rot_tag = "🔄 Rotation ON" if pkg.get("Rotation Allowed") else "🔒 No Rotation"

            # ===== ROW HEADER =====
            st.markdown(f"""
            <div class="vehicle-row">
                <span style="font-size:16px;font-weight:700;color:#1a3a5c;">
                    Row {i+1} — {pkg['Box Name']}
                </span>
                <span class="pill-info" style="margin-left:8px;">{tbadge}</span>
                <span class="pill-info" style="margin-left:4px;">{rot_tag}</span>

                <div style="margin-top:4px;font-size:14px;color:#000;">
                    {pkg['Quantity']} pcs |
                    {round(pkg['L'],2)} × {round(pkg['W'],2)} × {round(pkg['H'],2)} ft |
                    {round(row_cbm,3)} CBM
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ===== BEST VEHICLE =====
            util = best["Utilization %"]
            uc = "#198754" if util >= 70 else "#fd7e14" if util >= 40 else "#dc3545"

            st.markdown(f"""
            <div style="background:#f0fff4;border:2px solid #198754;border-radius:8px;
            padding:12px 16px;margin-bottom:6px;font-size:15px;color:#000;">
                <strong>⭐ Best Vehicle:</strong> 🚛 <strong>{best['Vehicle']}</strong>
                &nbsp; × &nbsp;<strong>{best['Vehicles Needed']}</strong>
                &nbsp; | &nbsp; Utilization:
                <strong style="color:{uc};">{util}%</strong>
            </div>
            """, unsafe_allow_html=True)

            # ===== ALTERNATIVES =====
            if alternatives:
                alt_list = []
                for alt in alternatives:
                    alt_list.append(
                        f"🚛 {alt['Vehicle']} ({alt['Utilization %']}%)"
                    )

                st.markdown(f"""
                <div style="background:#fff;border:1px solid #dee2e6;border-radius:6px;
                padding:8px 14px;margin-bottom:12px;font-size:14px;color:#444;">
                    <strong>Other options:</strong>
                    {' | '.join(alt_list)}
                </div>
                """, unsafe_allow_html=True)

            # ===== ADD BUTTON =====
            if st.button(f"✅ Add Row {i+1} Vehicle ({best['Vehicle']})", key=f"row_add_{i}"):
                existing = st.session_state.confirmed or []
                if best["Vehicle"] not in [x["Vehicle"] for x in existing]:
                    existing.append(best)
                    st.session_state.confirmed = existing
                st.success(f"Added {best['Vehicle']} to Final Plan")

    # ─── TAB 4: FINAL PLAN ───
    with tab_final:
        st.markdown('<div class="section-header">📋 Final Shipment Plan</div>',unsafe_allow_html=True)
        confirmed=st.session_state.confirmed or []

        if not confirmed:
            st.info("👆 Select vehicles from Best Suggestions, Other Options, or Row-wise Plan tabs — they will appear here.")
        else:
            if job_id:
                st.markdown(f"<div style='font-size:16px;color:#000;margin-bottom:12px;'><strong>Job ID:</strong> <code>{job_id}</code></div>",unsafe_allow_html=True)

            st.markdown(f"<div style='font-size:15px;color:#000;margin-bottom:10px;'><strong>{len(confirmed)}</strong> vehicle type(s) in your plan:</div>",unsafe_allow_html=True)

            for r in confirmed:
                util=r["Utilization %"]
                uc="#198754" if util>=70 else "#fd7e14" if util>=40 else "#dc3545"
                boc=r["Boxes Occupied"]; btc=r["Total Box Capacity"]; brc=r["Boxes Remaining"]
                st.markdown(f"""
                <div class="final-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
                        <div>
                            <span style="font-size:18px;font-weight:700;color:#000;">🚛 {r['Vehicle']}</span>
                            <span style="color:#555;font-size:14px;margin-left:10px;">{r['Vehicle Size (ft)']} ft</span>
                        </div>
                        <div><span style="font-size:28px;font-weight:700;color:#198754;">{r['Vehicles Needed']}</span>
                        <span style="color:#555;font-size:14px;"> vehicle(s)</span></div>
                    </div>
                    <div style="margin-top:10px;display:flex;flex-wrap:wrap;gap:20px;font-size:15px;color:#000;">
                        <span>📦 CBM Used: <strong>{r['Eff. CBM']}</strong></span>
                        <span>📊 Total CBM Cap: <strong>{r['Total Cap (CBM)']}</strong></span>
                        <span>🟩 CBM Free: <strong>{r['Remaining CBM']}</strong></span>
                        <span>🎯 Space: <strong style="color:{uc};">{util}%</strong></span>
                    </div>
                    <div style="margin-top:6px;display:flex;flex-wrap:wrap;gap:20px;font-size:15px;color:#000;">
                        <span>📫 Boxes Occupied: <strong>{boc}</strong></span>
                        <span>📬 Total Box Capacity: <strong>{btc}</strong></span>
                        <span>📭 Box Spaces Free: <strong>{brc}</strong></span>
                    </div>
                </div>""",unsafe_allow_html=True)

            # Remove option
            rc,_=st.columns([2,4])
            with rc:
                to_remove=st.selectbox("Remove a vehicle:",["— keep all —"]+[r["Vehicle"] for r in confirmed],key="remove_sel")
            if st.button("🗑️ Remove Selected Vehicle"):
                if to_remove!="— keep all —":
                    st.session_state.confirmed=[r for r in confirmed if r["Vehicle"]!=to_remove]; st.rerun()

            # Summary table
            st.markdown("<div style='font-size:15px;color:#000;margin:14px 0 6px 0;'><strong>Summary Table:</strong></div>",unsafe_allow_html=True)
            summary_df=pd.DataFrame([{
                "Vehicle":r["Vehicle"],"Size (ft)":r["Vehicle Size (ft)"],
                "Vehicles Needed":r["Vehicles Needed"],"CBM Used":r["Eff. CBM"],
                "Total CBM Cap":r["Total Cap (CBM)"],"CBM Free":r["Remaining CBM"],
                "Boxes Occupied":r["Boxes Occupied"],"Box Capacity":r["Total Box Capacity"],
                "Box Spaces Free":r["Boxes Remaining"],"Space Used %":r["Utilization %"],
            } for r in confirmed])
            st.dataframe(summary_df,use_container_width=True,hide_index=True)

            st.markdown(f"""
            <div style="background:#d1e7dd;border-radius:8px;padding:12px 16px;margin-top:10px;font-size:15px;color:#000;">
                <strong>📦 Total Cargo:</strong> {round(total_cbm,3)} CBM &nbsp;|&nbsp;
                {round(total_weight,2)} kg &nbsp;|&nbsp; {int(total_boxes)} boxes
            </div>""",unsafe_allow_html=True)

            st.markdown("")

            if not st.session_state.plan_submitted:
                s1,s2=st.columns([1,4])
                with s1:
                    if st.button("🚀 Save & Submit Plan",type="primary",use_container_width=True):
                        st.session_state.plan_submitted=True; st.rerun()
                with s2:
                    if st.button("🔄 Reset Everything"):
                        for k in ["packages","vehicle_options","confirmed"]:
                            st.session_state[k]=[] if k=="packages" else None
                        st.session_state.plan_submitted=False; st.rerun()
            else:
                st.markdown("""
                <div style="background:#d1fae5;border:2px solid #059669;border-radius:12px;
                padding:24px;text-align:center;margin-top:16px;">
                    <div style="font-size:42px;">✅</div>
                    <div style="font-size:22px;font-weight:700;color:#065f46;margin-top:8px;">
                        Shipment Plan Submitted Successfully!
                    </div>
                    <div style="font-size:16px;color:#047857;margin-top:6px;">
                        Your cargo plan has been saved and confirmed.
                    </div>
                </div>""",unsafe_allow_html=True)
                st.markdown("")
                if st.button("🔄 Start New Plan",type="primary"):
                    for k in ["packages","vehicle_options","confirmed"]:
                        st.session_state[k]=[] if k=="packages" else None
                    st.session_state.plan_submitted=False; st.rerun()
# =========================
# 3D VISUALIZATION SECTION
# =========================
st.markdown('<div class="section-header">📦 3D Container Loading View</div>', unsafe_allow_html=True)

if st.session_state.vehicle_options:

    selected_vehicle = st.selectbox(
        "Select Vehicle for 3D View",
        [v["Vehicle"] for v in st.session_state.vehicle_options]
    )

    vehicle_info = next(v for v in vehicle_data if v[0] == selected_vehicle)
    vL, vW, vH = vehicle_info[1], vehicle_info[2], vehicle_info[3]

    total_packages = sum(
    p["Quantity"]
    for p in st.session_state.packages
    if p["L"] > 0 and p["W"] > 0 and p["H"] > 0
    )

    st.info(
    f"Showing realistic loading inside: {selected_vehicle} "
    f"({vL}×{vW}×{vH} ft) | 📦 Total Packages: {total_packages}"
    )

    valid_pkgs = [
        p for p in st.session_state.packages
        if p["L"] > 0 and p["W"] > 0 and p["H"] > 0
    ]

    if valid_pkgs:
        fig = generate_3d_container(valid_pkgs, vL, vW, vH)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No valid packages to visualize.")
