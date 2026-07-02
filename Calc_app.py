import streamlit as st
import plotly.graph_objects as go

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LoanIQ — EMI Calculator",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
#  SESSION STATE  (for reset)
# ─────────────────────────────────────────────
defaults = dict(principle=500000.0, rate=1.0, time_years=5, time_months=0)
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─────────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600&display=swap');

/* ── Global ── */
html, body, [class*="css"], .stApp {
    font-family: 'Outfit', sans-serif !important;
    background-color: #07071a !important;
    color: #E2E8F0 !important;
}

/* Animated background blobs */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 70% 50% at 15% 10%, rgba(109,40,217,0.20) 0%, transparent 65%),
        radial-gradient(ellipse 55% 45% at 85% 85%, rgba(234,130,0,0.14) 0%, transparent 65%),
        radial-gradient(ellipse 60% 40% at 55% 45%, rgba(16,185,129,0.05) 0%, transparent 65%);
    pointer-events: none;
    z-index: 0;
}
.block-container { position: relative; z-index: 1; padding-top: 0 !important; max-width: 100% !important; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.12); border-radius: 99px; }

/* ─────────────────────────────────
   NAVBAR
───────────────────────────────── */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2.5rem;
    background: rgba(7,7,26,0.85);
    border-bottom: 1px solid rgba(255,255,255,0.07);
    backdrop-filter: blur(24px);
    position: sticky; top: 0; z-index: 999;
}
.nav-brand { display: flex; align-items: center; gap: .65rem; }
.nav-gem {
    width: 34px; height: 34px; border-radius: 10px;
    background: linear-gradient(135deg, #6D28D9, #F59E0B);
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem; box-shadow: 0 4px 16px rgba(109,40,217,.45);
}
.nav-title {
    font-size: 1.2rem; font-weight: 800; letter-spacing: -0.5px;
    background: linear-gradient(90deg, #fff 30%, #F59E0B);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.nav-right { display: flex; gap: .5rem; }
.nav-chip {
    padding: .3rem .85rem; border-radius: 99px; font-size: .72rem;
    font-weight: 600; letter-spacing: .5px; text-transform: uppercase;
    background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
    color: #64748B;
}
.nav-chip.on {
    background: rgba(109,40,217,.2); border-color: rgba(109,40,217,.5); color: #C4B5FD;
}

/* ─────────────────────────────────
   HERO
───────────────────────────────── */
.hero {
    text-align: center;
    padding: 3.5rem 1.5rem 2rem;
}
.hero-badge {
    display: inline-flex; align-items: center; gap: .45rem;
    background: linear-gradient(90deg, rgba(109,40,217,.18), rgba(245,158,11,.12));
    border: 1px solid rgba(109,40,217,.4);
    border-radius: 99px; padding: .38rem 1rem;
    font-size: .73rem; font-weight: 700; letter-spacing: 1px;
    text-transform: uppercase; color: #C4B5FD; margin-bottom: 1.3rem;
}
.pulse {
    width: 7px; height: 7px; border-radius: 50%; background: #A78BFA;
    animation: blink 1.8s ease-in-out infinite;
}
@keyframes blink { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.3;transform:scale(.65)} }
.hero h1 {
    font-size: clamp(2.2rem, 5vw, 3.8rem); font-weight: 900;
    letter-spacing: -2px; line-height: 1.08; margin-bottom: .9rem;
    background: linear-gradient(135deg, #fff 0%, #C4B5FD 45%, #F59E0B 85%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero p {
    font-size: 1.02rem; color: #64748B; max-width: 460px;
    margin: 0 auto 2rem; line-height: 1.75; font-weight: 400;
}
.hero-stats { display: flex; justify-content: center; gap: 3rem; margin-bottom: 2.5rem; }
.hs { text-align: center; }
.hs-v {
    font-size: 1.55rem; font-weight: 800;
    background: linear-gradient(90deg, #A78BFA, #F59E0B);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hs-l { font-size: .7rem; color: #475569; font-weight: 600; letter-spacing: .8px; text-transform: uppercase; margin-top: .1rem; }

/* ─────────────────────────────────
   SECTION CONTAINER
───────────────────────────────── */
.section { max-width: 1180px; margin: 0 auto; padding: 0 1.5rem 3rem; }

/* ─────────────────────────────────
   CARD
───────────────────────────────── */
.card {
    background: linear-gradient(145deg, rgba(255,255,255,0.055), rgba(255,255,255,0.015));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 1.8rem 1.8rem 1.4rem;
    box-shadow: 0 20px 60px rgba(0,0,0,.45), 0 1px 0 rgba(255,255,255,.06) inset;
    position: relative; overflow: hidden; margin-bottom: 1.2rem;
}
.card::before {
    content: '';
    position: absolute; top: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,.12), transparent);
}
.card-hd { display: flex; align-items: center; gap: .75rem; margin-bottom: 1.5rem; }
.card-ic {
    width: 38px; height: 38px; border-radius: 11px;
    display: flex; align-items: center; justify-content: center; font-size: 1rem; flex-shrink: 0;
}
.ic-v { background: linear-gradient(135deg, #3B0764, #7C3AED); box-shadow: 0 4px 14px rgba(109,40,217,.4); }
.ic-g { background: linear-gradient(135deg, #78350F, #D97706); box-shadow: 0 4px 14px rgba(217,119,6,.4); }
.ic-t { background: linear-gradient(135deg, #064E3B, #059669); box-shadow: 0 4px 14px rgba(5,150,105,.4); }
.ic-p { background: linear-gradient(135deg, #7F1D1D, #DC2626); box-shadow: 0 4px 14px rgba(220,38,38,.3); }
.card-lbl { font-size: .65rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #475569; }
.card-ttl { font-size: 1.05rem; font-weight: 700; color: #fff; margin-top: .1rem; }

/* ─────────────────────────────────
   INPUT OVERRIDES
───────────────────────────────── */
div[data-testid="stNumberInput"] label,
div[data-testid="stTextInput"] label {
    color: #94A3B8 !important;
    font-size: .78rem !important;
    font-weight: 700 !important;
    letter-spacing: .8px !important;
    text-transform: uppercase !important;
    font-family: 'Outfit', sans-serif !important;
}
div[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1.5px solid rgba(255,255,255,0.09) !important;
    border-radius: 13px !important;
    color: #fff !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    padding: .65rem 1rem !important;
    transition: border-color .2s, box-shadow .2s !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: #7C3AED !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,.2), 0 0 18px rgba(124,58,237,.12) !important;
    background: rgba(124,58,237,.07) !important;
}

/* ─────────────────────────────────
   BUTTONS
───────────────────────────────── */
.stButton > button {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 14px !important;
    border: none !important;
    width: 100% !important;
    transition: transform .2s, box-shadow .2s !important;
    font-size: .95rem !important;
    padding: .8rem 1.5rem !important;
    letter-spacing: .2px !important;
}
/* Primary = Calculate */
div[data-testid="stButton"]:nth-of-type(1) .stButton > button,
.calc-btn .stButton > button {
    background: linear-gradient(135deg, #4C1D95 0%, #7C3AED 55%, #8B5CF6 100%) !important;
    color: #fff !important;
    box-shadow: 0 8px 28px rgba(109,40,217,.50), 0 1px 0 rgba(255,255,255,.15) inset !important;
}
.calc-btn .stButton > button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 14px 40px rgba(109,40,217,.65) !important;
}
/* Secondary = Reset */
.reset-btn .stButton > button {
    background: rgba(255,255,255,0.05) !important;
    color: #64748B !important;
    border: 1px solid rgba(255,255,255,0.09) !important;
}
.reset-btn .stButton > button:hover {
    background: rgba(255,255,255,0.09) !important;
    color: #fff !important;
}

/* ─────────────────────────────────
   EMI SPOTLIGHT
───────────────────────────────── */
.emi-box {
    background: linear-gradient(145deg, #1e0545, #3b0764);
    border: 1px solid rgba(124,58,237,.35);
    border-radius: 22px; padding: 2rem 1.5rem;
    text-align: center; position: relative; overflow: hidden;
    box-shadow: 0 20px 60px rgba(109,40,217,.3), 0 0 0 1px rgba(255,255,255,.05) inset;
    margin-bottom: 1.2rem;
}
.emi-box::before {
    content:''; position:absolute;
    width:220px;height:220px; border-radius:50%;
    background: radial-gradient(circle,rgba(109,40,217,.45),transparent 70%);
    top:-80px;left:-60px;
}
.emi-box::after {
    content:''; position:absolute;
    width:160px;height:160px; border-radius:50%;
    background: radial-gradient(circle,rgba(245,158,11,.22),transparent 70%);
    bottom:-50px;right:-40px;
}
.emi-tag {
    position:relative;z-index:1;
    display:inline-block;
    background:rgba(255,255,255,.09); border:1px solid rgba(255,255,255,.14);
    border-radius:99px; padding:.28rem .85rem;
    font-size:.68rem; font-weight:700; letter-spacing:2px;
    text-transform:uppercase; color:#C4B5FD; margin-bottom:.9rem;
}
.emi-num {
    position:relative;z-index:1;
    font-family:'JetBrains Mono',monospace;
    font-size:clamp(2rem,5vw,3.2rem); font-weight:600; line-height:1;
    background: linear-gradient(90deg,#C4B5FD,#fff 50%,#FCD34D);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    margin-bottom:.45rem;
}
.emi-note { position:relative;z-index:1; font-size:.8rem; color:#475569; font-weight:500; }

/* ─────────────────────────────────
   METRIC 2x2
───────────────────────────────── */
.m2 { display:grid; grid-template-columns:1fr 1fr; gap:.85rem; margin-bottom:1.2rem; }
.mc {
    background:linear-gradient(145deg,rgba(255,255,255,.057),rgba(255,255,255,.015));
    border:1px solid rgba(255,255,255,.07); border-radius:18px; padding:1.3rem 1.1rem;
    position:relative; overflow:hidden;
    transition:transform .2s, box-shadow .2s;
}
.mc:hover { transform:translateY(-3px); box-shadow:0 12px 36px rgba(0,0,0,.35); }
.mc::before { content:''; position:absolute; top:0;left:0;right:0; height:2.5px; border-radius:99px; }
.mc-v::before { background:linear-gradient(90deg,#6D28D9,#A78BFA); }
.mc-g::before { background:linear-gradient(90deg,#D97706,#FCD34D); }
.mc-t::before { background:linear-gradient(90deg,#059669,#34D399); }
.mc-p::before { background:linear-gradient(90deg,#DC2626,#FB7185); }
.mc-ico { font-size:1.3rem; margin-bottom:.5rem; }
.mc-lbl { font-size:.65rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#475569;margin-bottom:.4rem; }
.mc-val { font-family:'JetBrains Mono',monospace; font-size:1.1rem;font-weight:600;color:#fff; }

/* ─────────────────────────────────
   BREAKDOWN BAR
───────────────────────────────── */
.bb-wrap { margin:1.2rem 0 .2rem; }
.bb-title { font-size:.67rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#475569;margin-bottom:.75rem; }
.bb-track { background:rgba(255,255,255,.07); border-radius:99px; height:11px; overflow:hidden; margin-bottom:.7rem; }
.bb-fill { height:100%;border-radius:99px;background:linear-gradient(90deg,#7C3AED,#F59E0B); position:relative; }
.bb-fill::after { content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent 55%,rgba(255,255,255,.25));border-radius:99px; }
.bb-leg { display:flex;gap:1.5rem;flex-wrap:wrap; }
.bb-leg span { font-size:.77rem;font-weight:500;color:#475569;display:flex;align-items:center;gap:.4rem; }
.bb-leg span b { color:#fff;font-weight:700; }
.dot { width:8px;height:8px;border-radius:50%;display:inline-block; }
.dot-v { background:linear-gradient(90deg,#7C3AED,#A78BFA); }
.dot-g { background:linear-gradient(90deg,#D97706,#FCD34D); }

/* placeholder */
.placeholder {
    min-height:340px; display:flex; flex-direction:column;
    align-items:center; justify-content:center; gap:1rem; text-align:center;
    color:#334155;
}
.placeholder-icon { font-size:3.5rem; opacity:.5; }

/* ─────────────────────────────────
   SUMMARY TABLE
───────────────────────────────── */
.sum-row {
    display:flex; justify-content:space-between; align-items:center;
    padding:.8rem 0; border-bottom:1px solid rgba(255,255,255,0.05);
}
.sum-row:last-child { border:none; }
.sum-k { font-size:.82rem;color:#475569;font-weight:500;display:flex;align-items:center;gap:.45rem; }
.sum-v { font-family:'JetBrains Mono',monospace;font-size:.88rem;font-weight:600;color:#fff; }
.sum-v.hi { color:#FCD34D;font-size:.98rem; }

/* ─────────────────────────────────
   SCHEDULE TABLE
───────────────────────────────── */
.tbl-wrap { border-radius:16px;overflow:hidden;border:1px solid rgba(255,255,255,0.07); }
.tbl { width:100%;border-collapse:collapse;font-size:.8rem; }
.tbl thead th {
    background:rgba(255,255,255,.045);
    padding:.7rem 1rem; text-align:left;
    font-size:.63rem;font-weight:700;letter-spacing:1.5px;
    text-transform:uppercase;color:#475569;
    border-bottom:1px solid rgba(255,255,255,.07);
}
.tbl tbody tr { border-bottom:1px solid rgba(255,255,255,.04); transition:background .15s; }
.tbl tbody tr:hover { background:rgba(255,255,255,.04); }
.tbl tbody tr:last-child { border:none; }
.tbl tbody td { padding:.65rem 1rem;color:#CBD5E1;font-family:'JetBrains Mono',monospace;font-size:.78rem; }
.tbl tbody td:first-child { font-family:'Outfit',sans-serif;font-weight:600; }
.mo-badge {
    display:inline-block; background:rgba(124,58,237,.18);
    border:1px solid rgba(124,58,237,.3); border-radius:6px;
    padding:.12rem .48rem; font-size:.7rem;color:#C4B5FD;
}
.tbl-note { padding:.65rem 1rem;font-size:.72rem;color:#475569;border-top:1px solid rgba(255,255,255,.05); }

/* Plotly transparent */
.js-plotly-plot .plotly, .js-plotly-plot .plotly svg { background:transparent!important; }

/* Footer */
.footer { text-align:center;padding:2.5rem 1rem 1rem;font-size:.75rem;color:#1E293B; }
.footer b { color:#475569; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  NAVBAR
# ─────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div class="nav-brand">
    <div class="nav-gem">💎</div>
    <div class="nav-title">LoanIQ</div>
  </div>
  <div class="nav-right">
    <div class="nav-chip on">EMI Calculator</div>
    <div class="nav-chip">Amortisation</div>
    <div class="nav-chip">Compare</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HERO
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge"><div class="pulse"></div>Smart Loan Intelligence</div>
  <h1>Calculate Your<br>Perfect EMI</h1>
  <p>Instant insights into your loan — interest, closing amount &amp; monthly repayments in one place.</p>
  <div class="hero-stats">
    <div class="hs"><div class="hs-v">100%</div><div class="hs-l">Accurate</div></div>
    <div class="hs"><div class="hs-v">Instant</div><div class="hs-l">Results</div></div>
    <div class="hs"><div class="hs-v">Free</div><div class="hs-l">Always</div></div>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  COMPUTE HELPER
# ─────────────────────────────────────────────
def compute(p, r, ty, tm):
    rate_yr  = r * 12
    t        = ty + (tm / 12)
    interest = (p * rate_yr * t) / 100
    closing  = p + interest
    emi      = (closing / t) / 12
    return rate_yr, t, interest, closing, emi


# ─────────────────────────────────────────────
#  TWO-COLUMN LAYOUT  (inputs | live preview)
# ─────────────────────────────────────────────
left, right = st.columns([1, 1])

with left:
    st.markdown("""
    <div class="card">
      <div class="card-hd">
        <div class="card-ic ic-v">📋</div>
        <div><div class="card-lbl">Step 1</div><div class="card-ttl">Loan Details</div></div>
      </div>
    </div>""", unsafe_allow_html=True)

    principle = st.number_input(
        "Principal Amount (₹)", min_value=0.0,
        max_value=100_000_000.0, value=float(st.session_state.principle),
        step=10_000.0, format="%.0f", help="Total loan amount borrowed",
        key="principle_inp"
    )

    st.write("")
    rate = st.number_input(
        "Monthly Interest Rate (%)", min_value=0.0, max_value=10.0,
        value=float(st.session_state.rate), step=0.05, format="%.2f",
        help="e.g. 1% per month = 12% per year", key="rate_inp"
    )

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        time_years = st.number_input(
            "Years", min_value=0, max_value=30,
            value=int(st.session_state.time_years), step=1, key="yr_inp"
        )
    with c2:
        time_months = st.number_input(
            "Months", min_value=0, max_value=11,
            value=int(st.session_state.time_months), step=1, key="mo_inp"
        )

    st.write("")

    # Calculate button
    st.markdown('<div class="calc-btn">', unsafe_allow_html=True)
    calc = st.button("⚡  Calculate EMI Now", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Reset button
    st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
    reset = st.button("↺  Reset Values", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if reset:
        for k, v in defaults.items():
            st.session_state[k] = v
        st.rerun()


# ─────────────────────────────────────────────
#  VALIDATION
# ─────────────────────────────────────────────
valid = principle > 0 and rate > 0 and (time_years > 0 or time_months > 0)

with right:
    if not valid:
        st.markdown("""
        <div class="card placeholder">
          <div class="placeholder-icon">📊</div>
          <div style="font-size:.95rem;line-height:1.7;color:#334155;">
            Fill in your loan details on the left<br>and your results appear here live.
          </div>
        </div>""", unsafe_allow_html=True)
    else:
        rate_yr, t_total, interest, closing, emi = compute(principle, rate, time_years, time_months)
        total_mo = int(t_total * 12)
        pct_p = (principle / closing) * 100
        pct_i = (interest  / closing) * 100

        # EMI spotlight
        st.markdown(f"""
        <div class="emi-box">
          <div class="emi-tag">Monthly EMI</div>
          <div class="emi-num">₹ {emi:,.2f}</div>
          <div class="emi-note">per month &nbsp;·&nbsp; {total_mo} instalments</div>
        </div>""", unsafe_allow_html=True)

        # 2×2 metrics
        st.markdown(f"""
        <div class="m2">
          <div class="mc mc-v"><div class="mc-ico">🏦</div><div class="mc-lbl">Total Interest</div><div class="mc-val">₹ {interest:,.0f}</div></div>
          <div class="mc mc-g"><div class="mc-ico">💰</div><div class="mc-lbl">Final Payable</div><div class="mc-val">₹ {closing:,.0f}</div></div>
          <div class="mc mc-t"><div class="mc-ico">📅</div><div class="mc-lbl">Total Months</div><div class="mc-val">{total_mo}</div></div>
          <div class="mc mc-p"><div class="mc-ico">📈</div><div class="mc-lbl">Annual Rate</div><div class="mc-val">{rate_yr:.1f}%</div></div>
        </div>""", unsafe_allow_html=True)

        # Breakdown bar
        st.markdown(f"""
        <div class="card" style="padding:1.4rem 1.6rem;">
          <div class="bb-title">Principal vs Interest</div>
          <div class="bb-track"><div class="bb-fill" style="width:{pct_p:.1f}%"></div></div>
          <div class="bb-leg">
            <span><span class="dot dot-v"></span>Principal &nbsp;<b>{pct_p:.1f}%</b></span>
            <span><span class="dot dot-g"></span>Interest &nbsp;<b>{pct_i:.1f}%</b></span>
          </div>
        </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  FULL RESULTS  (shown after Calculate)
# ─────────────────────────────────────────────
if calc:
    if not valid:
        st.error("⚠️  Please enter valid values for all fields before calculating.")
    else:
        rate_yr, t_total, interest, closing, emi = compute(principle, rate, time_years, time_months)
        total_mo = int(t_total * 12)
        monthly_rate = rate / 100

        st.write("")
        r1, r2 = st.columns([1, 1])

        # ── Donut chart ──
        with r1:
            st.markdown("""
            <div class="card">
              <div class="card-hd">
                <div class="card-ic ic-g">🥧</div>
                <div><div class="card-lbl">Visual</div><div class="card-ttl">Loan Composition</div></div>
              </div>
            </div>""", unsafe_allow_html=True)

            fig = go.Figure(go.Pie(
                labels=["Principal", "Interest"],
                values=[round(principle, 2), round(interest, 2)],
                hole=0.72,
                marker=dict(
                    colors=["#7C3AED", "#D97706"],
                    line=dict(color="#07071a", width=4)
                ),
                textinfo="none",
                hovertemplate="<b>%{label}</b><br>₹ %{value:,.2f}<br>%{percent}<extra></extra>"
            ))
            lakh = closing / 100_000
            fig.add_annotation(
                text=f"₹{lakh:.1f}L<br><span style='font-size:11px;color:#475569'>TOTAL</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=18, color="#ffffff", family="Outfit")
            )
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                showlegend=True,
                legend=dict(
                    orientation="h", x=0.5, y=-0.06, xanchor="center",
                    font=dict(color="#64748B", size=12, family="Outfit"),
                    bgcolor="rgba(0,0,0,0)"
                ),
                margin=dict(t=5, b=10, l=5, r=5),
                height=270
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # ── Summary ──
        with r2:
            rows = [
                ("💳", "Principal Borrowed",   f"₹ {principle:,.2f}", ""),
                ("📈", "Monthly Rate",         f"{rate:.2f}%",        ""),
                ("📊", "Annual Rate",          f"{rate_yr:.2f}%",     ""),
                ("🗓️", "Tenure",              f"{time_years}y {time_months}m ({total_mo} mo)", ""),
                ("🏦", "Total Interest",       f"₹ {interest:,.2f}",  ""),
                ("💰", "Final Closing Amount", f"₹ {closing:,.2f}",   "hi"),
                ("📆", "Monthly EMI",          f"₹ {emi:,.2f}",       "hi"),
            ]
            rows_html = "".join(
                f'<div class="sum-row"><div class="sum-k">{ic} {k}</div>'
                f'<div class="sum-v {cls}">{v}</div></div>'
                for ic, k, v, cls in rows
            )
            st.markdown(f"""
            <div class="card">
              <div class="card-hd">
                <div class="card-ic ic-t">📋</div>
                <div><div class="card-lbl">Summary</div><div class="card-ttl">Full Breakdown</div></div>
              </div>
              {rows_html}
            </div>""", unsafe_allow_html=True)

        # ── Amortisation schedule ──
        st.write("")
        st.markdown("""
        <div class="card">
          <div class="card-hd">
            <div class="card-ic ic-p">📆</div>
            <div><div class="card-lbl">Amortisation</div><div class="card-ttl">Monthly Payment Schedule</div></div>
          </div>
        </div>""", unsafe_allow_html=True)

        show = min(total_mo, 24)
        bal  = principle
        rows_s = ""
        for m in range(1, show + 1):
            mi  = bal * monthly_rate
            mp  = emi - mi
            bal = max(bal - mp, 0)
            rows_s += (
                f'<tr><td><span class="mo-badge">#{m:02d}</span></td>'
                f'<td>₹ {emi:,.2f}</td>'
                f'<td>₹ {mp:,.2f}</td>'
                f'<td>₹ {mi:,.2f}</td>'
                f'<td>₹ {bal:,.2f}</td></tr>'
            )
        note = (f'<div class="tbl-note">Showing first {show} of {total_mo} months</div>'
                if total_mo > 24 else "")
        st.markdown(f"""
        <div class="tbl-wrap">
          <table class="tbl">
            <thead><tr><th>Month</th><th>EMI</th><th>Principal</th><th>Interest</th><th>Balance</th></tr></thead>
            <tbody>{rows_s}</tbody>
          </table>
          {note}
        </div>""", unsafe_allow_html=True)

        # ── Stacked bar chart ──
        st.write("")
        m_labels, p_vals, i_vals = [], [], []
        bal = principle
        for m in range(1, show + 1):
            mi = bal * monthly_rate
            mp = emi - mi
            bal = max(bal - mp, 0)
            m_labels.append(f"M{m:02d}")
            p_vals.append(round(mp, 2))
            i_vals.append(round(mi, 2))

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(name="Principal", x=m_labels, y=p_vals,
                              marker_color="#7C3AED", marker_line_width=0))
        fig2.add_trace(go.Bar(name="Interest",  x=m_labels, y=i_vals,
                              marker_color="#D97706", marker_line_width=0))
        fig2.update_layout(
            barmode="stack",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Outfit", color="#64748B", size=11),
            title=dict(text="Principal &amp; Interest per Month",
                       font=dict(color="#CBD5E1", size=14, family="Outfit"), x=0.01),
            legend=dict(orientation="h", x=1, xanchor="right", y=1.1,
                        font=dict(color="#94A3B8"), bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(showgrid=False, tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)",
                       tickprefix="₹", tickfont=dict(size=10)),
            margin=dict(t=40, b=20, l=10, r=10), height=310
        )
        st.markdown('<div class="card" style="padding:1.4rem 1.6rem">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Built with <b>LoanIQ</b> &nbsp;·&nbsp; Results are indicative and for planning purposes only.
</div>""", unsafe_allow_html=True)