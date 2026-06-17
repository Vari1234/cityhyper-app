"""
CityHyper Hypermarket — Product Lookup App
Run: streamlit run app.py
"""
import streamlit as st
import sqlite3, os, pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH  = os.path.join(os.path.dirname(__file__), "cityhyper.db")  # local fallback

st.set_page_config(page_title="CityHyper Hypermarket", page_icon="🏬", layout="wide")

# ── CSS — exact match to HBA_CityHyper.html ──────────────────────────────────
st.markdown("""
<style>
/* ── Global reset ── */
*{box-sizing:border-box;margin:0;padding:0}
html,body,.stApp{font-family:Arial,sans-serif!important;background:#f5f9fc!important}
[data-testid="stAppViewContainer"]{background:#f5f9fc!important}
[data-testid="stHeader"],[data-testid="stToolbar"]{display:none!important}
.block-container{padding:0!important;max-width:100%!important}
section[data-testid="stMain"]>div{padding:0!important}
div[data-testid="stVerticalBlock"]{gap:0!important}
/* Remove all top padding from column inner blocks */
div[data-testid="stColumn"]>div{padding-top:0!important}
div[data-testid="stColumn"] div[data-testid="stVerticalBlock"]{padding-top:0!important}
#MainMenu,footer{display:none!important}

/* ── Outer centering shell ── */
.ch-shell{max-width:680px;margin:0 auto}

/* ── Top bar ── */
.ch-h1{background:#0F5A7A;color:#fff;padding:14px 18px;font-size:17px;
       font-weight:700;font-family:Arial,sans-serif;margin:0;
       border-radius:0 0 0 0}
.ch-h1 em{color:#F5C500;font-style:normal}

/* ── Tags bar ── */
.tags{display:flex;gap:6px;flex-wrap:wrap;align-items:center;
      padding:8px 16px 6px;background:#f5f9fc}
.tag{font-size:11px;font-weight:700;padding:4px 10px;border-radius:5px;
     background:#e8f4fb;color:#0F5A7A;border:1px solid #C8E2EF}

/* ── Wrap ── */
.wrap{padding:10px 0 60px}

/* ── Search card ── */
.bar{background:#fff;border:1px solid #C8E2EF;border-radius:10px;
     padding:10px 14px 14px;margin-bottom:10px}
.lbl-block{display:block;font-size:10px;font-weight:800;text-transform:uppercase;
           letter-spacing:.5px;color:#0F5A7A;margin-bottom:4px;
           font-family:Arial,sans-serif}

/* ── Remove top padding from Streamlit main & columns ── */
section[data-testid="stMain"]>div{padding-top:0!important}
div[data-testid="stColumn"]>div{padding-top:0!important;margin-top:0!important}
div[data-testid="stColumn"] div[data-testid="stVerticalBlock"]{gap:0!important;padding-top:0!important}
div[data-testid="element-container"]{margin-top:0!important;padding-top:0!important}

/* ── Hide widget labels ── */
div[data-testid="stSelectbox"]>label,
div[data-testid="stTextInput"]>label{display:none!important}

/* ── Style text input only (leave selectbox default so value shows) ── */
div[data-testid="stTextInput"] input{
  border:1.5px solid #C8E2EF!important;
  border-radius:7px!important;padding:10px 12px!important;
  font-size:15px!important;background:#fff!important;
  font-family:Arial,sans-serif!important}
div[data-testid="stTextInput"] input:focus{border-color:#2196C4!important}

/* ── Selectbox: style only the outer wrapper border ── */
div[data-testid="stSelectbox"] div[data-baseweb="select"] div[class]{
  border-color:#C8E2EF!important;border-radius:7px!important;
  font-size:15px!important;font-family:Arial,sans-serif!important}

/* ── Buttons ── */
div[data-testid="stHorizontalBlock"]{gap:8px!important}
div[data-testid="stHorizontalBlock"] div[data-testid="stColumn"]{padding-top:0!important}
.scan-btn button{background:#F07820!important;color:#fff!important;
  font-weight:800!important;font-size:15px!important;border:none!important;
  border-radius:8px!important;padding:11px 0!important;
  font-family:Arial,sans-serif!important;width:100%}
.scan-btn button:hover{background:#c75f10!important}
.go-btn button{background:#2196C4!important;color:#fff!important;
  font-weight:800!important;font-size:15px!important;border:none!important;
  border-radius:8px!important;padding:11px 0!important;
  font-family:Arial,sans-serif!important;width:100%}
.go-btn button:hover{background:#0F5A7A!important}
.clr-btn button{background:#eee!important;color:#555!important;
  font-weight:800!important;font-size:15px!important;
  border:none!important;border-radius:8px!important;padding:11px 0!important;
  font-family:Arial,sans-serif!important;width:100%}
.clr-btn button:hover{background:#ddd!important}

/* ── Result card ── */
#res{background:#fff;border:1px solid #C8E2EF;border-radius:10px;
     overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.08);margin-bottom:10px}
.rhead{background:linear-gradient(135deg,#0F5A7A,#2196C4);color:#fff;
       padding:16px 18px}
.rhead-bar{height:3px;background:linear-gradient(90deg,#F5C500,#F07820);
           margin:12px -18px 0}
.rtitle{font-size:17px;font-weight:800;line-height:1.3;font-family:Arial,sans-serif}
.rcode{font-size:11px;opacity:.55;margin-top:3px;font-family:monospace}
.sec{padding:12px 18px;border-bottom:1px solid #eef5fb;font-family:Arial,sans-serif}
.sec:last-child{border-bottom:none}
.sec.yel{border-left:4px solid #F5C500}
.sec.blu{border-left:4px solid #2196C4}
.sec.org{border-left:4px solid #F07820}
.sec.grey{border-left:4px solid #90A4AE}
.stitle{font-size:10px;font-weight:800;text-transform:uppercase;
        letter-spacing:.8px;color:#2196C4;margin-bottom:9px;
        font-family:Arial,sans-serif}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:8px}
.kv{display:flex;flex-direction:column;gap:2px}
.k{font-size:10px;color:#888;font-weight:700;text-transform:uppercase;
   letter-spacing:.3px;font-family:Arial,sans-serif}
.v{font-size:14px;font-weight:600;color:#222;font-family:Arial,sans-serif}
.big{font-size:22px;font-weight:900;color:#0F5A7A;font-family:Arial,sans-serif}
.med{font-size:17px;font-weight:700;color:#333;font-family:Arial,sans-serif}
.blue{font-size:19px;font-weight:900;color:#2196C4;font-family:Arial,sans-serif}
.oran{font-size:16px;font-weight:700;color:#F07820;font-family:Arial,sans-serif}
.green{font-size:16px;font-weight:700;color:#2e7d32;font-family:Arial,sans-serif}
.red-v{font-size:16px;font-weight:700;color:#c62828;font-family:Arial,sans-serif}
.grey-v{font-size:15px;font-weight:600;color:#888;font-family:Arial,sans-serif}
.badge{display:inline-block;font-size:10px;font-weight:700;
       padding:2px 6px;border-radius:3px;margin-left:4px}
.badge-up{background:#e8f5e9;color:#1b5e20}
.badge-dn{background:#fce4ec;color:#b71c1c}

/* ── Not found ── */
.nf{text-align:center;padding:28px 16px;background:#fff;border:1px solid #C8E2EF;
    border-radius:10px;margin-bottom:10px}
.nf p{font-size:16px;font-weight:700;color:#c62828;margin-bottom:4px;
      font-family:Arial,sans-serif}
.nf small{font-size:12px;color:#888;font-family:Arial,sans-serif}

/* ── Empty state ── */
.empty{text-align:center;padding:40px 16px;color:#aaa;font-family:Arial,sans-serif}
.empty-icon{font-size:2.8rem;margin-bottom:10px}
.empty-title{font-size:15px;font-weight:700;color:#0F5A7A;margin-bottom:6px}
.empty-sub{font-size:12px;color:#888}

/* ── Footer ── */
.ch-footer{text-align:center;padding:14px;color:#aaa;font-size:11px;
           border-top:1px solid #e8f0f5;margin-top:16px;
           font-family:Arial,sans-serif}

/* ── Mobile ── */
@media(max-width:480px){
  .big{font-size:18px}.blue{font-size:16px}
  .wrap{padding:10px 10px 60px}
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
if not os.path.exists(DB_PATH):
    st.error("**Database not found.** Run `python setup_database.py` first.")
    st.stop()

# ── Header ────────────────────────────────────────────────────────────────────
n_prod, n_mon, n_stores = get_stats()

# Centre everything in a narrow column
_L, _C, _R = st.columns([1, 4, 1])

with _C:
    st.markdown(f"""
    <div class="ch-shell">
      <div class="ch-h1">CityHyper – <em>Hypermarket</em></div>
      <div class="tags">
        <span class="tag">✅ {n_prod:,} products</span>
        <span class="tag">✅ {n_mon} months · {n_stores} stores</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    stores      = get_stores()
    store_names = [name for _, name in stores]
    store_locs  = [loc  for loc,  _ in stores]

    st.markdown('<div class="ch-shell"><div class="wrap">', unsafe_allow_html=True)
    st.markdown('<div class="bar">', unsafe_allow_html=True)

    st.markdown('<span class="lbl-block">Store</span>', unsafe_allow_html=True)
    store_sel = st.selectbox("Store", options=store_names, index=0,
                             label_visibility="collapsed", key="store_sel")
    sel_loc = store_locs[store_names.index(store_sel)]

    st.markdown('<span class="lbl-block" style="margin-top:10px">Barcode</span>', unsafe_allow_html=True)
    query = st.text_input("Barcode", placeholder="Scan or type barcode…",
                          label_visibility="collapsed", key="bc_input",
                          value=st.session_state.get("bc_val",""))

    c1, c2, c3 = st.columns([2, 5, 1])
    with c1:
        st.markdown('<div class="scan-btn">', unsafe_allow_html=True)
        st.button("📷 Scan", use_container_width=True, key="btn_scan")
        st.markdown('</div>', unsafe_allow_html=True)
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
        st.session_state["bc_val"] = ""
        st.rerun()

    # ── Results ───────────────────────────────────────────────────────────────
    q = query.strip()

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
      <div class="kv"><div class="k">Avg Monthly Purchase</div><div class="v oran">{fkwd(avg_pur)}</div></div>
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
