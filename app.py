"""
CityHyper Hypermarket — Product Lookup App
Run: streamlit run app.py
"""
import streamlit as st
import sqlite3, os, pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH  = os.path.join(os.path.dirname(__file__), "cityhyper.db")  # local fallback

st.set_page_config(page_title="CityHyper Hypermarket", page_icon="🏬", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
*{box-sizing:border-box;margin:0;padding:0}
html,body,.stApp{font-family:'Inter',Arial,sans-serif!important;background:#EEF4F8!important}
[data-testid="stAppViewContainer"]{background:#EEF4F8!important}
[data-testid="stHeader"],[data-testid="stToolbar"]{display:none!important}
.block-container{padding:0!important;max-width:100%!important}
section[data-testid="stMain"]>div{padding:0!important}
div[data-testid="stVerticalBlock"]{gap:0!important}
div[data-testid="stColumn"]>div{padding-top:0!important;padding-bottom:0!important}
div[data-testid="stColumn"] div[data-testid="stVerticalBlock"]{padding-top:0!important;gap:0!important}
div[data-testid="element-container"]{margin-top:0!important;padding-top:0!important}
div[data-testid="stVerticalBlock"]>div:first-child{padding-top:0!important;margin-top:0!important}
.stSelectbox,[data-testid="stSelectbox"]{margin-top:0!important;padding-top:0!important}
#MainMenu,footer{display:none!important}

/* ── Shell ── */
.ch-shell{max-width:700px;margin:0 auto}

/* ── Header ── */
.ch-header{background:linear-gradient(135deg,#0A3D52 0%,#0F5A7A 50%,#1A7AA8 100%);
  padding:0;overflow:hidden;border-radius:0 0 16px 16px;
  box-shadow:0 4px 20px rgba(15,90,122,0.35)}
.ch-header-inner{padding:20px 22px 16px}
.ch-logo-row{display:flex;align-items:center;gap:12px;margin-bottom:6px}
.ch-logo-icon{width:44px;height:44px;background:#fff;
  border-radius:10px;display:flex;align-items:center;justify-content:center;
  padding:4px;box-shadow:0 2px 8px rgba(0,0,0,0.2)}
.ch-title{font-size:20px;font-weight:900;color:#fff;letter-spacing:-0.3px}
.ch-title span{color:#F5C500}
.ch-subtitle{font-size:11px;color:rgba(255,255,255,0.6);font-weight:500;
  text-transform:uppercase;letter-spacing:1.5px}
.ch-header-bar{height:4px;background:linear-gradient(90deg,#F5C500,#F07820,#E91E63)}
.ch-stats{display:flex;gap:0;border-top:1px solid rgba(255,255,255,0.1)}
.ch-stat{flex:1;padding:10px 16px;text-align:center;
  border-right:1px solid rgba(255,255,255,0.1)}
.ch-stat:last-child{border-right:none}
.ch-stat-n{font-size:16px;font-weight:800;color:#F5C500}
.ch-stat-l{font-size:9px;color:rgba(255,255,255,0.55);text-transform:uppercase;
  letter-spacing:1px;font-weight:600}

/* ── Wrap ── */
.wrap{padding:12px 0 60px}

/* ── Search card ── */
.bar{background:#fff;border-radius:14px;padding:16px 16px 18px;
  margin-bottom:12px;box-shadow:0 2px 16px rgba(15,90,122,0.1);
  border:1px solid rgba(15,90,122,0.08)}
.lbl-block{display:block;font-size:10px;font-weight:700;text-transform:uppercase;
  letter-spacing:1px;color:#0F5A7A;margin-bottom:6px}

/* ── Hide widget labels ── */
div[data-testid="stSelectbox"]>label,
div[data-testid="stTextInput"]>label{display:none!important}

/* ── Text input ── */
div[data-testid="stTextInput"] input{
  border:2px solid #E0EDF5!important;border-radius:10px!important;
  padding:12px 14px!important;font-size:15px!important;background:#F8FBFD!important;
  font-family:'Inter',Arial,sans-serif!important;color:#1a1a2e!important;
  transition:border-color .2s}
div[data-testid="stTextInput"] input:focus{border-color:#2196C4!important;background:#fff!important}

/* ── Selectbox ── */
div[data-testid="stSelectbox"] div[data-baseweb="select"] div[class]{
  border-color:#E0EDF5!important;border-radius:10px!important;
  font-size:15px!important;background:#F8FBFD!important}

/* ── Buttons ── */
div[data-testid="stHorizontalBlock"]{gap:8px!important}
div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]{padding-top:0!important}
.scan-btn button{background:linear-gradient(135deg,#F07820,#E05010)!important;
  color:#fff!important;font-weight:700!important;font-size:14px!important;
  border:none!important;border-radius:10px!important;padding:12px 0!important;
  font-family:'Inter',Arial,sans-serif!important;width:100%;
  box-shadow:0 3px 10px rgba(240,120,32,0.4)!important}
.go-btn button{background:linear-gradient(135deg,#2196C4,#0F5A7A)!important;
  color:#fff!important;font-weight:700!important;font-size:14px!important;
  border:none!important;border-radius:10px!important;padding:12px 0!important;
  font-family:'Inter',Arial,sans-serif!important;width:100%;
  box-shadow:0 3px 10px rgba(33,150,196,0.4)!important}
.clr-btn button{background:#F0F4F8!important;color:#666!important;
  font-weight:600!important;font-size:14px!important;
  border:none!important;border-radius:10px!important;padding:12px 0!important;
  font-family:'Inter',Arial,sans-serif!important;width:100%}

/* ── Result card ── */
#res{background:#fff;border-radius:14px;overflow:hidden;
  box-shadow:0 4px 24px rgba(15,90,122,0.12);margin-bottom:12px;
  border:1px solid rgba(15,90,122,0.08)}
.rhead{background:linear-gradient(135deg,#0A3D52,#0F5A7A,#1A7AA8);color:#fff;padding:18px 20px}
.rhead-bar{height:4px;background:linear-gradient(90deg,#F5C500,#F07820,#E91E63);margin:14px -20px 0}
.rtitle{font-size:18px;font-weight:800;line-height:1.3;letter-spacing:-0.2px}
.rcode{font-size:11px;opacity:.5;margin-top:4px;font-family:monospace}
.sec{padding:14px 20px;border-bottom:1px solid #F0F5FA}
.sec:last-child{border-bottom:none}
.sec.yel{border-left:5px solid #F5C500;background:linear-gradient(90deg,#FFFDF0,#fff)}
.sec.blu{border-left:5px solid #2196C4;background:linear-gradient(90deg,#F0F8FF,#fff)}
.sec.org{border-left:5px solid #F07820;background:linear-gradient(90deg,#FFF8F0,#fff)}
.sec.grey{border-left:5px solid #90A4AE;background:linear-gradient(90deg,#F5F8FA,#fff)}
.stitle{font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:1.2px;
  color:#2196C4;margin-bottom:12px;display:flex;align-items:center;gap:6px}
.stitle::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,#E0EDF5,transparent)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px}
.kv{display:flex;flex-direction:column;gap:3px;padding:8px 10px;
  background:#F8FBFD;border-radius:8px}
.k{font-size:9px;color:#8899AA;font-weight:700;text-transform:uppercase;letter-spacing:.5px}
.v{font-size:14px;font-weight:600;color:#1a2a3a}
.big{font-size:24px;font-weight:900;color:#0F5A7A;letter-spacing:-0.5px}
.med{font-size:18px;font-weight:700;color:#1a2a3a}
.blue{font-size:20px;font-weight:900;color:#2196C4}
.oran{font-size:17px;font-weight:700;color:#F07820}
.green{font-size:17px;font-weight:700;color:#1B8A3C}
.red-v{font-size:17px;font-weight:700;color:#D32F2F}
.grey-v{font-size:15px;font-weight:600;color:#8899AA}
.badge{display:inline-block;font-size:9px;font-weight:700;padding:2px 7px;
  border-radius:20px;margin-left:4px;vertical-align:middle}
.badge-up{background:#E8F5E9;color:#1B5E20}
.badge-dn{background:#FCE4EC;color:#B71C1C}

/* ── Not found ── */
.nf{text-align:center;padding:32px 20px;background:#fff;border-radius:14px;
  margin-bottom:12px;box-shadow:0 2px 16px rgba(15,90,122,0.08)}
.nf-icon{font-size:2.5rem;margin-bottom:10px}
.nf p{font-size:16px;font-weight:700;color:#D32F2F;margin-bottom:4px}
.nf small{font-size:12px;color:#8899AA}

/* ── Empty state ── */
.empty{text-align:center;padding:48px 20px;color:#aaa}
.empty-icon{font-size:3rem;margin-bottom:12px}
.empty-title{font-size:16px;font-weight:700;color:#0F5A7A;margin-bottom:6px}
.empty-sub{font-size:12px;color:#8899AA}

/* ── Footer ── */
.ch-footer{text-align:center;padding:16px;color:#AABBCC;font-size:11px;
  border-top:1px solid #E8F0F5;margin-top:16px;letter-spacing:.5px}

/* ── Mobile ── */
@media(max-width:480px){
  .ch-title{font-size:17px}.big{font-size:20px}.blue{font-size:17px}
  .wrap{padding:12px 10px 60px}.grid{grid-template-columns:1fr 1fr}
}
</style>
""", unsafe_allow_html=True)


# ── Data helpers (Parquet preferred, SQLite fallback) ─────────────────────────
def _use_parquet():
    return os.path.exists(os.path.join(DATA_DIR, "master.parquet"))

@st.cache_data(show_spinner=False)
def _load_master():
    if _use_parquet():
        return pd.read_parquet(os.path.join(DATA_DIR, "master.parquet"))
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM master", conn); conn.close(); return df

@st.cache_data(show_spinner=False)
def _load_sales():
    if _use_parquet():
        return pd.read_parquet(os.path.join(DATA_DIR, "sales.parquet"))
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM sales", conn); conn.close(); return df

@st.cache_data(show_spinner=False)
def _load_stores():
    if _use_parquet():
        return pd.read_parquet(os.path.join(DATA_DIR, "stores.parquet"))
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM stores", conn); conn.close(); return df

@st.cache_data(ttl=600)
def get_stats():
    m = _load_master(); s = _load_stores()
    return len(m), 5, len(s)

@st.cache_data(ttl=600)
def get_stores():
    df = _load_stores().sort_values("LOCATION NAME")
    return [("ALL","— All Stores —")] + list(zip(df["LOCATION"].tolist(), df["LOCATION NAME"].tolist()))

@st.cache_data(ttl=300)
def lookup(query, store_loc):
    q   = query.strip()
    q_n = q.lstrip("0") or q
    master = _load_master()

    mrow = master[master["BARCODE"].astype(str).str.strip().isin([q, q_n]) |
                  master["PRODUCT CODE"].astype(str).str.strip().isin([q, q_n])]
    if mrow.empty:
        mrow = master[master["DESCRIPTION"].astype(str).str.upper().str.contains(q.upper(), na=False)]
    if mrow.empty:
        return None, None

    pc = str(mrow.iloc[0]["PRODUCT CODE"]).strip().lstrip("0") or str(mrow.iloc[0]["PRODUCT CODE"]).strip()
    sales = _load_sales()
    srow = sales[sales["PRODUCT CODE"].astype(str).str.strip() == pc]
    if store_loc and store_loc != "ALL":
        s_store = srow[srow["LOCATION"] == store_loc]
        if not s_store.empty:
            srow = s_store

    if len(srow) > 1:
        nc = ["YTD_SALES_VALUE","YTD_SALES_QTY","YTD_COGS","YTD_PURCHASE",
              "AVG_MONTHLY_SALES_QTY","AVG_MONTHLY_PURCHASE"]
        agg = {c:"sum" for c in nc if c in srow.columns}
        for c in ["LOCATION NAME","CATEGORY","CATEGORY NAME","SUB CATEGORY",
                  "SUB CATEGORY NAME","BRAND","SUPPLIER CODE","SUPPLIER NAME"]:
            if c in srow.columns: agg[c] = "first"
        sa = srow.agg(agg)
        ys, yc = float(sa.get("YTD_SALES_VALUE",0)), float(sa.get("YTD_COGS",0))
        sa["MARGIN_PCT"] = round((ys-yc)/ys*100,2) if ys else 0
        srow = pd.DataFrame([sa])

    return mrow.iloc[0], srow.iloc[0] if not srow.empty else None

def sf(v, d=0.0):
    try: return float(v)
    except: return d

def fkwd(v):
    try: return f"KD {float(v):.3f}"
    except: return "—"

def fqty(v):
    try:
        f = float(v)
        return f"{f:,.0f}" if f else "0"
    except: return "—"

def fpct(v):
    try: return f"{float(v):.1f}%"
    except: return "—"

def d(v):
    s = str(v).strip()
    return s if s and s not in ("nan","None","") else "—"

def esc(v):
    return str(v).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")


# ── DB check ──────────────────────────────────────────────────────────────────
if not _use_parquet() and not os.path.exists(DB_PATH):
    st.error("**Database not found.** Run `python setup_database.py` first.")
    st.stop()

# ── Handle clear request (must happen before widgets render) ──────────────────
if st.session_state.pop("_clear_requested", False):
    st.session_state["bc_input"] = ""

# ── Apply barcode detected by the camera scanner (set before widget renders) ──
if "_pending_bc" in st.session_state:
    st.session_state["bc_input"] = st.session_state.pop("_pending_bc")

# ── Header ────────────────────────────────────────────────────────────────────
n_prod, n_mon, n_stores = get_stats()

# Centre everything in a narrow column
_L, _C, _R = st.columns([1, 4, 1])

with _C:
    st.markdown(f"""
    <div class="ch-shell">
      <div class="ch-header">
        <div class="ch-header-inner">
          <div class="ch-logo-row">
            <div class="ch-logo-icon">
              <img src="data:image/png;base64,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" width="46" height="46" style="object-fit:contain;border-radius:6px">
            </div>
            <div>
              <div class="ch-title">CityHyper <span>Hypermarket</span></div>
              <div class="ch-subtitle">Product Intelligence System</div>
            </div>
          </div>
        </div>
        <div class="ch-header-bar"></div>
        <div class="ch-stats">
          <div class="ch-stat"><div class="ch-stat-n">{n_prod:,}</div><div class="ch-stat-l">Products</div></div>
          <div class="ch-stat"><div class="ch-stat-n">{n_mon}</div><div class="ch-stat-l">Months</div></div>
          <div class="ch-stat"><div class="ch-stat-n">{n_stores}</div><div class="ch-stat-l">Stores</div></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    stores      = get_stores()
    store_names = [name for _, name in stores]
    store_locs  = [loc  for loc,  _ in stores]

    st.markdown('<div class="ch-shell"><div class="wrap"><div class="bar">', unsafe_allow_html=True)

    st.markdown('<span class="lbl-block">Store</span>', unsafe_allow_html=True)
    store_sel = st.selectbox("Store", options=store_names, index=0,
                             label_visibility="collapsed", key="store_sel")
    sel_loc = store_locs[store_names.index(store_sel)]

    st.markdown('<span class="lbl-block" style="margin-top:10px">Barcode</span>', unsafe_allow_html=True)
    query = st.text_input("Barcode", placeholder="Scan or type barcode…",
                          label_visibility="collapsed", key="bc_input")

    c2, c3 = st.columns([6, 1])
    with c2:
        st.markdown('<div class="go-btn">', unsafe_allow_html=True)
        st.button("🔍  Search", use_container_width=True, key="btn_go")
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="clr-btn">', unsafe_allow_html=True)
        clear = st.button("✕", use_container_width=True, key="btn_clr")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # .bar

    if clear:
        st.session_state["_clear_requested"] = True
        st.rerun()

    # ── Camera scanner (st.camera_input + pyzbar) ───────────────────────────
    with st.expander("📷  Scan barcode with camera"):
        st.caption("Tap below to open the camera, fill the frame with the barcode, then snap. "
                   "It reads automatically.")
        _img = st.camera_input("Scan barcode", key="cam", label_visibility="collapsed")
        if _img is not None:
            try:
                from pyzbar.pyzbar import decode as _zbar_decode
                from PIL import Image as _PILImage, ImageOps as _ImageOps
                _pic = _PILImage.open(_img)
                _res = _zbar_decode(_pic)
                if not _res:  # retry on a grayscale, auto-contrast version
                    _res = _zbar_decode(_ImageOps.autocontrast(_pic.convert("L")))
                if _res:
                    _code = _res[0].data.decode("utf-8", "ignore").strip()
                    if _code and _code != st.session_state.get("bc_input", ""):
                        st.session_state["_pending_bc"] = _code
                        st.rerun()
                    else:
                        st.success(f"Detected: {_code}")
                else:
                    st.warning("No barcode detected — get closer, hold steady, and ensure good lighting, then snap again.")
            except Exception as _e:
                st.error(f"Scanner error: {_e}")


    # ── Results ───────────────────────────────────────────────────────────────
    q = st.session_state.get("bc_input", "").strip()

    if q:
        mrow, srow = lookup(q, sel_loc)

        if mrow is None:
            st.markdown(f"""
            <div class="nf">
              <p>"{esc(q)}" not found</p>
              <small>Not found in CityHyper Master Data</small>
            </div>""", unsafe_allow_html=True)
        else:
            desc    = d(mrow.get("DESCRIPTION",""))
            barcode = d(mrow.get("BARCODE",""))
            pcode   = d(mrow.get("PRODUCT CODE",""))
            brand_m = d(mrow.get("BRAND",""))
            rsp     = sf(mrow.get("RSP",0))
            pp      = sf(mrow.get("PURCHASE PRICE",0))
            sup_c   = d(mrow.get("SUPPLIER CODE",""))
            sup_n   = d(mrow.get("SUPPLIER NAME",""))
            country = d(mrow.get("COUNTRY NAME",""))
            gm      = ((rsp-pp)/rsp*100) if rsp else 0

            if srow is not None:
                brand   = d(srow.get("BRAND", brand_m))
                sup_c   = d(srow.get("SUPPLIER CODE", sup_c))
                sup_n   = d(srow.get("SUPPLIER NAME", sup_n))
                cat     = d(srow.get("CATEGORY NAME", srow.get("CATEGORY","")))
                subcat  = d(srow.get("SUB CATEGORY NAME", srow.get("SUB CATEGORY","")))
                q6      = sf(srow.get("YTD_SALES_QTY",0))
                ytd_val = sf(srow.get("YTD_SALES_VALUE",0))
                margin  = sf(srow.get("MARGIN_PCT",0))
                avg_q   = sf(srow.get("AVG_MONTHLY_SALES_QTY",0))
                ytd_pur = sf(srow.get("YTD_PURCHASE",0))
                avg_pur = sf(srow.get("AVG_MONTHLY_PURCHASE",0))
                store_l = d(srow.get("LOCATION NAME", store_sel))
            else:
                brand   = brand_m
                cat     = subcat = "—"
                q6      = ytd_val = margin = avg_q = ytd_pur = avg_pur = 0.0
                store_l = store_sel

            store_txt = "All Stores" if sel_loc == "ALL" else store_l
            gm_cls    = "green" if gm >= 0 else "red-v"
            mar_cls   = "green" if margin >= 0 else "red-v"
            loc_line  = f" &nbsp;·&nbsp; 📍{esc(store_txt)}" if sel_loc != "ALL" else ""

            st.markdown(f"""
<div id="res">
  <div class="rhead">
    <div class="rtitle">{esc(desc)}</div>
    <div class="rcode">Barcode: {esc(barcode)} &nbsp;·&nbsp; Code: {esc(pcode)}{loc_line}</div>
    <div class="rhead-bar"></div>
  </div>
  <div class="sec yel">
    <div class="stitle">💰 Pricing</div>
    <div class="grid">
      <div class="kv"><div class="k">Selling Price (RSP)</div><div class="v big">{fkwd(rsp)}</div></div>
      <div class="kv"><div class="k">Purchase Price</div><div class="v med">{fkwd(pp)}</div></div>
      <div class="kv"><div class="k">Gross Margin</div><div class="v {gm_cls}">{fpct(gm)}</div></div>
    </div>
  </div>
  <div class="sec blu">
    <div class="stitle">📈 Sales — {esc(store_txt)}</div>
    <div class="grid">
      <div class="kv"><div class="k">YTD 2026 (Qty)</div><div class="v blue">{fqty(q6)}</div></div>
      <div class="kv"><div class="k">YTD 2026 (Value)</div><div class="v grey-v">{fkwd(ytd_val)}</div></div>
      <div class="kv"><div class="k">Sales Margin %</div><div class="v {mar_cls}">{fpct(margin)}</div></div>
      <div class="kv"><div class="k">Avg / Month</div><div class="v oran">{fqty(avg_q)}</div></div>
    </div>
  </div>
  <div class="sec org">
    <div class="stitle">🛒 Purchasing</div>
    <div class="grid">
      <div class="kv"><div class="k">Purchase YTD</div><div class="v oran">{fkwd(ytd_pur)}</div></div>
    </div>
  </div>
  <div class="sec" style="border-left:4px solid #F5C500">
    <div class="stitle">🏷 Classification</div>
    <div class="grid">
      <div class="kv"><div class="k">Category</div><div class="v">{esc(cat)}</div></div>
      <div class="kv"><div class="k">Sub-Category</div><div class="v">{esc(subcat)}</div></div>
      <div class="kv"><div class="k">Brand</div><div class="v">{esc(brand)}</div></div>
      <div class="kv"><div class="k">Country</div><div class="v">{esc(country)}</div></div>
    </div>
  </div>
  <div class="sec grey">
    <div class="stitle">🚚 Supplier</div>
    <div class="grid">
      <div class="kv"><div class="k">Code</div><div class="v">{esc(sup_c)}</div></div>
      <div class="kv"><div class="k">Name</div><div class="v">{esc(sup_n)}</div></div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)

            if srow is None:
                st.info("No sales data for this product in the selected period.")

    else:
        st.markdown("""
        <div class="empty">
          <div class="empty-icon">🏬</div>
          <div class="empty-title">Scan a barcode or enter a product code</div>
          <div class="empty-sub">USB barcode scanners type directly into the field above</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)  # .wrap .ch-shell

    st.markdown("""
    <div class="ch-footer">CityHyper Hypermarket &nbsp;·&nbsp; Internal Use Only</div>
    """, unsafe_allow_html=True)
