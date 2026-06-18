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
              <img src="data:image/png;base64,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" width="44" height="44" style="object-fit:contain">
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

    c1, c2, c3 = st.columns([2, 5, 1])
    with c1:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#0F5A7A,#2196C4);color:#fff;
          border-radius:10px;padding:10px 8px;font-size:11px;font-weight:600;
          text-align:center;line-height:1.5;box-shadow:0 3px 10px rgba(15,90,122,0.3)">
          📷 Use phone camera<br>to scan → copy → paste
        </div>""", unsafe_allow_html=True)
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
