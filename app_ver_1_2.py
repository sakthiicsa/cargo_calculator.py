import streamlit as st
import pandas as pd
import math
from itertools import permutations

# ===== PAGE CONFIG (MUST BE FIRST) =====
st.set_page_config(page_title="ICSA Cargo Planner PRO", layout="wide", page_icon="🚢")

# ===== CUSTOM CSS =====
st.markdown("""
<style>
    /* ── App background ── */
    .stApp { background-color: #f0f4f8; }

    /* ── BLACK TEXT on white-background inputs & labels ── */
    input[type="number"], input[type="text"],
    .stNumberInput input, .stTextInput input {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    [data-baseweb="select"] * { color: #000000 !important; }
    [data-baseweb="popover"] * { color: #000000 !important; background: #ffffff !important; }
    label,
    [data-testid="stWidgetLabel"] > div {
        color: #000000 !important;
    }
    .stCheckbox span { color: #000000 !important; }
    .stMarkdown p, .stMarkdown li, .stMarkdown strong,
    .stMarkdown span { color: #000000 !important; }
    [data-testid="stExpander"] summary span { color: #000000 !important; }
    button[data-baseweb="tab"] { color: #000000 !important; }

    /* ── Header card (keep white text on dark bg) ── */
    .header-card {
        background: linear-gradient(135deg, #1a3a5c 0%, #2e6da4 100%);
        border-radius: 12px;
        padding: 20px 30px;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .header-title { color: white; font-size: 22px; font-weight: 700; margin: 0; text-align: center; }
    .header-sub   { color: #b8d4f0; font-size: 12px; text-align: center; }

    /* ── Metric cards ── */
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border-left: 4px solid #2e6da4;
        text-align: center;
    }
    .metric-val { font-size: 28px; font-weight: 700; }
    .metric-lbl { font-size: 12px; color: #555; text-transform: uppercase; letter-spacing: 1px; }

    /* ── Section headers ── */
    .section-header {
        background: white;
        border-radius: 8px;
        padding: 10px 16px;
        margin: 16px 0 10px 0;
        border-left: 4px solid #2e6da4;
        font-weight: 700;
        font-size: 15px;
        color: #1a3a5c;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    }

    /* ── Pills ── */
    .pill-warn { background: #fff3cd; color: #856404; border-radius: 20px; padding: 3px 10px; font-size: 12px; font-weight: 600; display: inline-block; }
    .pill-ok   { background: #d1e7dd; color: #0f5132; border-radius: 20px; padding: 3px 10px; font-size: 12px; font-weight: 600; display: inline-block; }
    .pill-err  { background: #f8d7da; color: #842029; border-radius: 20px; padding: 3px 10px; font-size: 12px; font-weight: 600; display: inline-block; }

    /* ── Vehicle cards ── */
    .vehicle-best  { background: linear-gradient(135deg, #e8f4fd, #ffffff); border: 2px solid #2e6da4; border-radius: 10px; padding: 14px 18px; margin-bottom: 10px; }
    .vehicle-other { background: white; border: 1px solid #dee2e6; border-radius: 8px; padding: 10px 14px; margin-bottom: 6px; }

    /* ── Hide Streamlit chrome ── */
    #MainMenu { visibility: hidden; }
    footer     { visibility: hidden; }
    header     { visibility: hidden; }

    /* ── Buttons ── */
    .stButton > button { border-radius: 8px; font-weight: 600; transition: all 0.2s; }
    .stButton > button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); }

    div[data-testid="stDataFrameResizable"] { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ===== SESSION INIT =====
for key, default in [
    ("auth", False), ("user", ""), ("packages", []),
    ("vehicle_options", None), ("confirmed", None)
]:
    if key not in st.session_state:
        st.session_state[key] = default

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
    st.markdown("""
    <div style="max-width:420px;margin:60px auto;background:white;padding:40px;
    border-radius:16px;box-shadow:0 8px 30px rgba(0,0,0,0.12);">
    <h2 style="text-align:center;color:#1a3a5c;margin-bottom:4px;">🔐 ICSA Cargo Planner</h2>
    <p style="text-align:center;color:#888;margin-bottom:24px;font-size:13px;">
    International Clearing &amp; Shipping Agency</p>
    </div>
    """, unsafe_allow_html=True)

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
                st.error("❌ Invalid credentials. Please try again.")

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
    "Gel Pack Package","Cylindrical Package","Flat Pack",
    "Hanging Garment Box","Skid","Loose Cargo",
    "Over-Dimensional Cargo (ODC)","UN Certified Hazardous Package",
    "Spill-proof Container","Bubble Wrap Package",
    "Foam-Protected Package","Tamper-proof Bag"
]

vehicle_data = [
    ("TATA ACE",              6,  4,  5,  6),
    ("TATA 407",              9,  6,  5,  9),
    ("TATA - 12 Feet",       12,  6.4, 5, 11),
    ("Canter - 14 Feet",     14,  6.4, 5, 14),
    ("LPT - 17 Feet",        17,  6.8, 6, 17),
    ("1109 - 19 Feet",       19,  7,   7, 21),
    ("LP Truck - 18 Feet",   18,  6.9, 7, 20),
    ("Taurus - 22 Feet",     22,  7.2, 7, 28),
    ("Taurus - 24-25 Feet",  24,  7.3, 7, 30),
    ("Taurus - 25-26 Feet",  25,  7.3, 7, 34),
    ("20' Container",        20,  8,   8, 27),
    ("22' Container",        22,  8,   8, 29),
    ("24' Container",        24,  8,   8, 35),
    ("28' Container",        28,  8,   8, 40),
    ("32' Container S.AXL",  32,  8,   8, 50),
    ("32' Container M.AXL",  32,  8,   8, 50),
    ("32' Container HQ",     32,  9,  10, 55),
    ("34' Container",        34,  8,   8, 55),
    ("40' Container",        40,  8,   8, 60),
    ("Platform 20 Feet",     20,  8,   7, 30),
    ("Platform 22 Feet",     22,  8,   7, 33),
    ("Platform/Half Body 28 FT", 28, 8, 7, 42),
    ("40 Feet High Bed Trailer", 40, 8, 7, 60),
    ("50 Feet Semi Trailer",     50, 8, 7, 75),
    ("40 Feet Semi Trailer",     40, 8, 7, 60),
]
# columns: name, vL, vW, vH (all in feet), cbm_capacity

# =========================
# UTILS
# =========================
def to_feet(v, u):
    return {"mm": v/304.8, "cm": v/30.48, "m": v*3.28084, "inch": v/12}[u]

def calc_cbm(L, W, H, qty):
    return (L * W * H * qty) / 35.315 if L and W and H else 0

def validate_dimensions(L, W, H, unit):
    """Returns list of warning strings."""
    warnings = []
    # Convert to cm for sanity checks
    to_cm = {"mm": 0.1, "cm": 1, "m": 100, "inch": 2.54}
    f = to_cm[unit]
    lc, wc, hc = L*f, W*f, H*f
    if lc > 2000 or wc > 2000 or hc > 2000:
        warnings.append("⚠️ Dimensions look unrealistically large — check unit selection")
    if lc < 1 or wc < 1 or hc < 1:
        warnings.append("⚠️ Very small dimensions detected — check unit selection")
    return warnings

def get_best_orientation(pkg_L, pkg_W, pkg_H, veh_L, veh_W, veh_H, rotation_allowed):
    """Return (fits, best_L, best_W, best_H) using rotation if allowed."""
    orientations = [(pkg_L, pkg_W, pkg_H)]
    if rotation_allowed:
        orientations = list(set(permutations([pkg_L, pkg_W, pkg_H])))

    best = None
    for (l, w, h) in orientations:
        if l <= veh_L and w <= veh_W and h <= veh_H:
            if best is None:
                best = (l, w, h)
            # prefer orientation that wastes least volume
            elif (veh_L - l) + (veh_W - w) + (veh_H - h) < (veh_L - best[0]) + (veh_W - best[1]) + (veh_H - best[2]):
                best = (l, w, h)
    if best:
        return True, best[0], best[1], best[2]
    return False, pkg_L, pkg_W, pkg_H

def suggest_vehicles_for_cbm(total_cbm, total_weight=0, packages=None):
    """
    Returns list of dicts with vehicle suggestion data.
    Uses rotation/stacking from packages list if provided.
    """
    results = []
    for (name, vL, vW, vH, cap) in vehicle_data:
        # --- Dimension-based fit check (per package) ---
        fits_all = True
        effective_cbm = total_cbm  # start with raw CBM

        if packages:
            for pkg in packages:
                if pkg["L"] == 0 or pkg["W"] == 0 or pkg["H"] == 0:
                    continue

                rot = pkg.get("Rotation Allowed", False)
                stacking_on = pkg.get("Stacking On Top", False)
                stacking_under = pkg.get("Stacking Under", False)

                fits, bL, bW, bH = get_best_orientation(
                    pkg["L"], pkg["W"], pkg["H"], vL, vW, vH, rot
                )
                if not fits:
                    fits_all = False
                    break

                # Stacking bonus: if stacking allowed, effective height per unit is halved
                if stacking_on and stacking_under:
                    stacking_factor = 0.6
                elif stacking_on or stacking_under:
                    stacking_factor = 0.8
                else:
                    stacking_factor = 1.0

                # Recalculate CBM with stacking factor for this package
                pkg_cbm = calc_cbm(bL, bW, bH, pkg["Quantity"]) * stacking_factor
                # We'll accumulate effective CBM below
            # Recalculate total effective CBM with all packages
            eff_cbm = 0
            for pkg in packages:
                if pkg["L"] == 0 or pkg["W"] == 0 or pkg["H"] == 0:
                    continue
                rot = pkg.get("Rotation Allowed", False)
                stacking_on = pkg.get("Stacking On Top", False)
                stacking_under = pkg.get("Stacking Under", False)
                fits, bL, bW, bH = get_best_orientation(
                    pkg["L"], pkg["W"], pkg["H"], vL, vW, vH, rot
                )
                if stacking_on and stacking_under:
                    sf = 0.6
                elif stacking_on or stacking_under:
                    sf = 0.8
                else:
                    sf = 1.0
                eff_cbm += calc_cbm(bL, bW, bH, pkg["Quantity"]) * sf
            effective_cbm = eff_cbm

        vehicles_needed = math.ceil(effective_cbm / cap) if effective_cbm > 0 else 1
        total_capacity = vehicles_needed * cap
        occupied = effective_cbm
        remaining = total_capacity - occupied
        utilization = (occupied / total_capacity * 100) if total_capacity > 0 else 0

        # Warnings
        w = []
        if not fits_all:
            w.append("📦 Package exceeds vehicle dimensions")
        if utilization < 40 and vehicles_needed == 1:
            w.append("📉 Low utilization — consider smaller vehicle")
        if vehicles_needed > 5:
            w.append("🔢 Many vehicles needed — optimize packaging")

        results.append({
            "Vehicle": name,
            "Vehicle Size (ft)": f"{vL}×{vW}×{vH}",
            "Cap (CBM)": cap,
            "Eff. CBM": round(effective_cbm, 2),
            "Vehicles Needed": vehicles_needed,
            "Total Capacity": round(total_capacity, 2),
            "Occupied": round(occupied, 2),
            "Remaining": round(remaining, 2),
            "Utilization %": round(utilization, 1),
            "Fits Dims": fits_all,
            "_warnings": w,
        })

    results.sort(key=lambda x: (x["Vehicles Needed"], -x["Utilization %"]))
    return results

# =========================
# HEADER
# =========================
st.markdown("""
<div class="header-card">
    <div>
        <img src="https://icsagroup.com/wp-content/themes/icsa/images/logo.png"
             style="height:50px;" onerror="this.style.display='none'"/>
    </div>
    <div>
        <p class="header-title">📦 ICSA Cargo Planner PRO</p>
        <p class="header-sub">International Clearing &amp; Shipping Agency Pvt Ltd</p>
    </div>
    <div style="text-align:right;">
        <img src="http://icsagroup.com/wp-content/uploads/2025/10/94-Years-Unit.png"
             style="height:40px;" onerror="this.style.display='none'"/>
    </div>
</div>
""", unsafe_allow_html=True)

# Top bar: Job ID + user info + logout
c1, c2, c3, c4 = st.columns([2, 3, 2, 1])
with c1:
    job_id = st.text_input("🆔 Job ID", max_chars=15, placeholder="e.g. JOB-2025-001")
with c2:
    st.markdown(f"""
    <div style="padding-top:28px;color:#555;font-size:13px;">
        👤 Logged in as <strong>{st.session_state['user']}</strong>
    </div>""", unsafe_allow_html=True)
with c4:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state["auth"] = False
        st.session_state["user"] = ""
        st.rerun()

st.markdown("---")

# =========================
# DIMENSION CALCULATOR
# =========================
st.markdown('<div class="section-header">📏 Quick Package Calculator</div>', unsafe_allow_html=True)

with st.container():
    cols = st.columns([1.2, 1, 1, 1, 1, 1, 1.5])
    unit  = cols[0].selectbox("Unit", ["mm","cm","m","inch"], key="unit_sel")
    L_in  = cols[1].number_input("Length", min_value=0.0, key="qL")
    W_in  = cols[2].number_input("Width",  min_value=0.0, key="qW")
    H_in  = cols[3].number_input("Height", min_value=0.0, key="qH")
    qty_in= cols[4].number_input("Quantity", min_value=1,  key="qQty")
    wt_in = cols[5].number_input("Weight/pc (kg)", min_value=0.0, key="qWt")

    # Live preview
    if L_in > 0 and W_in > 0 and H_in > 0:
        lf = to_feet(L_in, unit)
        wf = to_feet(W_in, unit)
        hf = to_feet(H_in, unit)
        prev_cbm = calc_cbm(lf, wf, hf, qty_in)
        cols[6].markdown(f"""
        <div style="padding-top:22px;background:#e8f4fd;border-radius:8px;
        padding:10px;text-align:center;font-size:13px;">
            <strong>{round(prev_cbm,3)} CBM</strong><br>
            <span style="color:#666;">{round(lf,2)}×{round(wf,2)}×{round(hf,2)} ft</span>
        </div>""", unsafe_allow_html=True)

    dim_warns = validate_dimensions(L_in, W_in, H_in, unit) if L_in > 0 and W_in > 0 and H_in > 0 else []
    for w in dim_warns:
        st.warning(w)

    if st.button("➕ Add Package", type="primary"):
        if L_in == 0 or W_in == 0 or H_in == 0:
            st.error("⚠️ Enter all dimensions (L, W, H)")
        else:
            st.session_state.packages.append({
                "Box Name": package_types[0],
                "L": round(to_feet(L_in, unit), 3),
                "W": round(to_feet(W_in, unit), 3),
                "H": round(to_feet(H_in, unit), 3),
                "Quantity": int(qty_in),
                "Weight Piece (KG)": float(wt_in),
                "Rotation Allowed": False,
                "Stacking On Top": False,
                "Stacking Under": False
            })
            st.rerun()

# =========================
# PACKAGE TABLE
# =========================
st.markdown('<div class="section-header">📦 Package Details (Dimensions in Feet)</div>', unsafe_allow_html=True)

col_add, col_clear = st.columns([1, 5])
with col_add:
    if st.button("➕ Add Empty Row"):
        st.session_state.packages.append({
            "Box Name": package_types[0],
            "L": 0.0, "W": 0.0, "H": 0.0,
            "Quantity": 1,
            "Weight Piece (KG)": 0.0,
            "Rotation Allowed": False,
            "Stacking On Top": False,
            "Stacking Under": False
        })
        st.rerun()
with col_clear:
    if st.button("🗑️ Clear All"):
        st.session_state.packages = []
        st.session_state.vehicle_options = None
        st.session_state.confirmed = None
        st.rerun()

# Table header
hdr = st.columns([2, 0.8, 0.8, 0.8, 0.7, 0.9, 0.8, 0.8, 0.75, 0.75, 0.75, 0.5])
hdr_labels = ["Box Name","L (ft)","W (ft)","H (ft)","Qty","Wt/pc (kg)","Total Wt","CBM","🔄 Rotate","⬆️ On Top","⬇️ Under","Del"]
for h, lbl in zip(hdr, hdr_labels):
    h.markdown(f"<div style='font-size:11px;font-weight:700;color:#1a3a5c;'>{lbl}</div>", unsafe_allow_html=True)

delete_index = None
total_cbm = 0.0
total_weight = 0.0
total_boxes = 0
row_issues = []

for i, pkg in enumerate(st.session_state.packages):
    cols = st.columns([2, 0.8, 0.8, 0.8, 0.7, 0.9, 0.8, 0.8, 0.75, 0.75, 0.75, 0.5])

    bg = "#f8f9fa" if i % 2 == 0 else "#ffffff"
    pkg["Box Name"]         = cols[0].selectbox("", package_types, index=package_types.index(pkg["Box Name"]) if pkg["Box Name"] in package_types else 0, key=f"name{i}", label_visibility="collapsed")
    pkg["L"]                = cols[1].number_input("", value=float(pkg["L"]), min_value=0.0, key=f"L{i}", label_visibility="collapsed", format="%.3f")
    pkg["W"]                = cols[2].number_input("", value=float(pkg["W"]), min_value=0.0, key=f"W{i}", label_visibility="collapsed", format="%.3f")
    pkg["H"]                = cols[3].number_input("", value=float(pkg["H"]), min_value=0.0, key=f"H{i}", label_visibility="collapsed", format="%.3f")
    pkg["Quantity"]         = cols[4].number_input("", value=int(pkg["Quantity"]), min_value=1, key=f"Q{i}", label_visibility="collapsed")
    pkg["Weight Piece (KG)"]= cols[5].number_input("", value=float(pkg["Weight Piece (KG)"]), min_value=0.0, key=f"WT{i}", label_visibility="collapsed")

    tot_wt = pkg["Quantity"] * pkg["Weight Piece (KG)"]
    cbm    = calc_cbm(pkg["L"], pkg["W"], pkg["H"], pkg["Quantity"])

    # Row-level warnings
    row_warn = []
    if pkg["L"] == 0 or pkg["W"] == 0 or pkg["H"] == 0:
        row_warn.append("missing dims")
    if pkg["Weight Piece (KG)"] == 0:
        row_warn.append("no weight")
    if pkg["Quantity"] <= 0:
        row_warn.append("qty=0")

    # Color-coded CBM display
    cbm_color = "#0f5132" if cbm > 0 else "#842029"
    cols[6].markdown(f"<div style='padding-top:8px;font-size:13px;color:#333;'>{round(tot_wt,2)}</div>", unsafe_allow_html=True)
    cols[7].markdown(f"<div style='padding-top:8px;font-size:13px;font-weight:600;color:{cbm_color};'>{round(cbm,3)}</div>", unsafe_allow_html=True)

    pkg["Rotation Allowed"] = cols[8].checkbox("",  value=pkg["Rotation Allowed"], key=f"R{i}", label_visibility="collapsed")
    pkg["Stacking On Top"]  = cols[9].checkbox("",  value=pkg["Stacking On Top"],  key=f"T{i}", label_visibility="collapsed")
    pkg["Stacking Under"]   = cols[10].checkbox("", value=pkg["Stacking Under"],   key=f"U{i}", label_visibility="collapsed")

    if cols[11].button("🗑", key=f"del{i}"):
        delete_index = i

    if row_warn:
        row_issues.append((i+1, row_warn))

    total_cbm    += cbm
    total_weight += tot_wt
    total_boxes  += pkg["Quantity"]

if delete_index is not None:
    st.session_state.packages.pop(delete_index)
    st.rerun()

# Row warnings summary
if row_issues:
    with st.expander(f"⚠️ {len(row_issues)} row(s) have issues", expanded=False):
        for row_num, issues in row_issues:
            st.markdown(f"**Row {row_num}:** {', '.join(issues)}")

# =========================
# TOTALS DASHBOARD
# =========================
st.markdown("---")
m1, m2, m3, m4 = st.columns(4)

def metric_card(col, val, label, color="#2e6da4"):
    col.markdown(f"""
    <div class="metric-card" style="border-left-color:{color};">
        <div class="metric-val" style="color:{color};">{val}</div>
        <div class="metric-lbl">{label}</div>
    </div>""", unsafe_allow_html=True)

metric_card(m1, round(total_cbm, 3),    "Total CBM",       "#2e6da4")
metric_card(m2, round(total_weight, 2), "Total Weight (kg)","#198754")
metric_card(m3, int(total_boxes),       "Total Boxes",      "#fd7e14")
metric_card(m4, len(st.session_state.packages), "Cargo Rows", "#6f42c1")

# =========================
# SAVE & CALCULATE
# =========================
st.markdown("")
calc_col, _ = st.columns([2, 5])
with calc_col:
    calc_btn = st.button("🔍 Save & Calculate Vehicle Options", type="primary", use_container_width=True)

if calc_btn:
    if total_cbm == 0:
        st.error("⚠️ No valid cargo data — enter dimensions for at least one package")
    else:
        valid_pkgs = [p for p in st.session_state.packages
                      if p["L"] > 0 and p["W"] > 0 and p["H"] > 0 and p["Quantity"] > 0]
        if len(valid_pkgs) < len(st.session_state.packages):
            st.warning(f"⚠️ {len(st.session_state.packages) - len(valid_pkgs)} invalid row(s) ignored in calculation")

        results = suggest_vehicles_for_cbm(total_cbm, total_weight, valid_pkgs)
        st.session_state.vehicle_options = results
        st.session_state.confirmed = None

# =========================
# VEHICLE SUGGESTIONS
# =========================
if st.session_state.vehicle_options:
    results = st.session_state.vehicle_options
    fits_results  = [r for r in results if r["Fits Dims"]]
    other_results = [r for r in results if not r["Fits Dims"]]

    st.markdown('<div class="section-header">🚚 Vehicle Suggestions</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["✅ Best Options (Top 5)", "🔽 All Vehicles", "📊 Row-wise Plan"])

    with tab1:
        if not fits_results:
            st.error("⚠️ No vehicle fits all package dimensions. Check dimensions or allow rotation.")
        else:
            for r in fits_results[:5]:
                util = r["Utilization %"]
                util_color = "#198754" if util >= 70 else "#fd7e14" if util >= 40 else "#dc3545"
                warn_html = "".join([f'<span class="pill-warn">{w}</span> ' for w in r["_warnings"]])
                st.markdown(f"""
                <div class="vehicle-best">
                    <div style="display:flex;justify-content:space-between;align-items:center;">
                        <div>
                            <span style="font-size:16px;font-weight:700;color:#1a3a5c;">🚛 {r['Vehicle']}</span>
                            <span style="margin-left:10px;color:#666;font-size:12px;">{r['Vehicle Size (ft)']} ft &nbsp;|&nbsp; {r['Cap (CBM)']} CBM cap</span>
                        </div>
                        <div style="text-align:right;">
                            <span style="font-size:22px;font-weight:700;color:#2e6da4;">{r['Vehicles Needed']}</span>
                            <span style="color:#666;font-size:13px;"> vehicle(s) needed</span>
                        </div>
                    </div>
                    <div style="margin-top:8px;display:flex;gap:20px;font-size:13px;">
                        <span>📦 Occupied: <strong>{r['Occupied']} CBM</strong></span>
                        <span>🟩 Remaining: <strong>{r['Remaining']} CBM</strong></span>
                        <span>📊 Utilization: <strong style="color:{util_color};">{util}%</strong></span>
                    </div>
                    <div style="margin-top:6px;">{warn_html}</div>
                </div>""", unsafe_allow_html=True)

    with tab2:
        # Selectable table
        st.markdown("**Select vehicle(s) and confirm your plan:**")
        select_map = {}
        for r in fits_results + other_results:
            fits_badge = "✅" if r["Fits Dims"] else "❌ Dim"
            util = r["Utilization %"]
            util_bar = "🟩" * int(util // 20) + "⬜" * (5 - int(util // 20))
            checked = st.checkbox(
                f"**{r['Vehicle']}** — {r['Vehicles Needed']} vehicle(s) | {util}% util {util_bar} | {fits_badge}",
                key=f"sel_{r['Vehicle']}"
            )
            select_map[r['Vehicle']] = checked

        selected_vehicles = [r for r in fits_results + other_results if select_map.get(r['Vehicle'])]

        if st.button("✅ Confirm Selection", type="primary"):
            if not selected_vehicles:
                st.warning("⚠️ Select at least one vehicle before confirming")
            else:
                st.session_state.confirmed = selected_vehicles
                st.success("✅ Plan confirmed! Scroll down to see the Final Plan.")
                st.rerun()

    with tab3:
        st.markdown("**Row-wise Vehicle Suggestion** — best vehicle for each individual cargo row:")
        if not st.session_state.packages:
            st.info("No packages added yet.")
        else:
            for i, pkg in enumerate(st.session_state.packages):
                if pkg["L"] == 0 or pkg["W"] == 0 or pkg["H"] == 0:
                    st.markdown(f"**Row {i+1} ({pkg['Box Name']}):** ⚠️ Missing dimensions")
                    continue
                row_cbm = calc_cbm(pkg["L"], pkg["W"], pkg["H"], pkg["Quantity"])
                row_results = suggest_vehicles_for_cbm(row_cbm, pkg["Weight Piece (KG)"] * pkg["Quantity"], [pkg])
                best = next((r for r in row_results if r["Fits Dims"]), row_results[0] if row_results else None)
                if best:
                    st.markdown(f"""
                    <div class="vehicle-other">
                        <strong>Row {i+1}</strong> — {pkg['Box Name']} ({pkg['Quantity']} pcs, {round(row_cbm,3)} CBM)
                        &nbsp;→&nbsp; 🚛 <strong>{best['Vehicle']}</strong>
                        &nbsp;×&nbsp; <strong>{best['Vehicles Needed']}</strong> &nbsp;|&nbsp;
                        Utilization: {best['Utilization %']}%
                        {'&nbsp; ⚠️ Dim mismatch' if not best['Fits Dims'] else ''}
                    </div>""", unsafe_allow_html=True)

# =========================
# FINAL PLAN
# =========================
if st.session_state.confirmed:
    st.markdown("---")
    st.markdown('<div class="section-header">📋 Final Shipment Plan</div>', unsafe_allow_html=True)

    if job_id:
        st.markdown(f"**Job ID:** `{job_id}`")

    confirmed = st.session_state.confirmed
    for r in confirmed:
        util = r["Utilization %"]
        util_color = "#198754" if util >= 70 else "#fd7e14" if util >= 40 else "#dc3545"
        st.markdown(f"""
        <div style="background:white;border-radius:10px;padding:16px 20px;
        margin-bottom:10px;border-left:5px solid #198754;box-shadow:0 2px 8px rgba(0,0,0,0.08);">
            <div style="display:flex;justify-content:space-between;">
                <div>
                    <span style="font-size:17px;font-weight:700;">🚛 {r['Vehicle']}</span>
                    <span style="color:#666;font-size:12px;margin-left:10px;">{r['Vehicle Size (ft)']} ft</span>
                </div>
                <div>
                    <span style="font-size:24px;font-weight:700;color:#198754;">{r['Vehicles Needed']}</span>
                    <span style="color:#666;"> vehicle(s)</span>
                </div>
            </div>
            <div style="margin-top:8px;display:flex;gap:24px;font-size:13px;color:#444;">
                <span>📦 CBM Used: <strong>{r['Occupied']}</strong></span>
                <span>📊 Capacity: <strong>{r['Total Capacity']}</strong></span>
                <span>📉 Remaining: <strong>{r['Remaining']}</strong></span>
                <span>🎯 Utilization: <strong style="color:{util_color};">{util}%</strong></span>
            </div>
        </div>""", unsafe_allow_html=True)

    # Summary table for export/reference
    st.markdown("**Summary Table:**")
    summary_df = pd.DataFrame([{
        "Vehicle": r["Vehicle"],
        "Size (ft)": r["Vehicle Size (ft)"],
        "Vehicles Needed": r["Vehicles Needed"],
        "CBM Occupied": r["Occupied"],
        "Total Capacity": r["Total Capacity"],
        "Remaining CBM": r["Remaining"],
        "Utilization %": r["Utilization %"],
    } for r in confirmed])
    st.dataframe(summary_df, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div style="background:#d1e7dd;border-radius:8px;padding:12px 16px;margin-top:10px;">
        <strong>📦 Total Cargo:</strong> {round(total_cbm,3)} CBM &nbsp;|&nbsp;
        {round(total_weight,2)} kg &nbsp;|&nbsp; {int(total_boxes)} boxes
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🚀 Submit Plan", type="primary", use_container_width=True):
            st.toast(f"✅ Shipment Plan Submitted Successfully! Job: {job_id or 'N/A'}", icon="🚢")
    with col2:
        if st.button("🔄 Reset & New Plan", use_container_width=False):
            st.session_state.packages = []
            st.session_state.vehicle_options = None
            st.session_state.confirmed = None
            st.rerun()
