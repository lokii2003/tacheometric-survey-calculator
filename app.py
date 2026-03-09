import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe
from matplotlib.lines import Line2D

st.set_page_config(page_title="Tacheometric Surveying – Problem Statement", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Source+Code+Pro&family=Lato:wght@300;400;700&display=swap');
html, body, [class*="css"] { font-family: 'Lato', sans-serif; background: #0d1117; color: #e6edf3; }
h1,h2,h3 { font-family: 'Playfair Display', serif; }
.main-title { font-family:'Playfair Display',serif; font-size:2.2rem; color:#f0c040; text-align:center; margin-bottom:0.1rem; }
.subtitle   { text-align:center; color:#8b949e; font-size:0.95rem; margin-bottom:1.5rem; }
.step-card  { background:#161b22; border-left:4px solid #f0c040; border-radius:6px; padding:1rem 1.3rem; margin-bottom:1rem; }
.step-title { font-family:'Playfair Display',serif; color:#f0c040; font-size:1.05rem; margin-bottom:0.4rem; }
.formula-box{ background:#1c2128; border:1px solid #30363d; border-radius:4px; padding:0.6rem 0.9rem;
              font-family:'Source Code Pro',monospace; font-size:0.88rem; color:#79c0ff; margin:0.4rem 0; }
.result-hl  { background:#1f2f1f; border-left:4px solid #3fb950; border-radius:4px; padding:0.5rem 0.9rem;
              color:#3fb950; font-family:'Source Code Pro',monospace; font-size:0.95rem; font-weight:bold; margin-top:0.4rem; }
.final-box  { background:linear-gradient(135deg,#1a2a1a,#1a1a2a); border:2px solid #f0c040;
              border-radius:8px; padding:1.4rem; text-align:center; margin-top:1.2rem; }
div[data-testid="stNumberInput"] label { color:#e6edf3 !important; }
div[data-testid="stDataFrame"] { border:1px solid #30363d; border-radius:6px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Tacheometric Surveying</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Problem Statement — RL of Station B &amp; Distance between BM and B </div>', unsafe_allow_html=True)

# ---------------- ANGLE CONVERSION (WITH SIGN) ----------------
def deg_min_to_decimal(deg, minute):
    """
    Keeps + or − sign exactly as entered.
    Example:
    -10° 30′ → -10.5
    +4° 0′ → 4
    """
    if deg >= 0:
        return deg + (minute / 60)
    else:
        return deg - (minute / 60)
    
# ══════════════════════════════════════════════════════════
#  EDITABLE INPUT TABLE
# ══════════════════════════════════════════════════════════
st.markdown("## 📋 Input Observations  ")

c1, c2 = st.columns(2)

with c1:
    st.markdown("#### 🔵 Observation 1 — A → BM")
    RL_BM     = st.number_input("RL of BM (m)",            value=510.500, step=0.001, format="%.3f")
    a1_lower  = st.number_input("Vertical angle Lower (°) depression", value=10.0, step=1.0, format="%.1f")
    a1_upper  = st.number_input("Vertical angle Upper (°) depression", value=7.0,  step=1.0, format="%.1f")
    sr1_lower = st.number_input("Staff reading — Lower cross-hair (m)",value=0.655, step=0.001, format="%.3f")
    sr1_upper = st.number_input("Staff reading — Upper cross-hair (m)",value=2.655, step=0.001, format="%.3f")

with c2:
    st.markdown("#### 🟣 Observation 2 — A → B")
    a2_lower  = st.number_input("Vertical angle Lower (°) depression", value=5.0,  step=0.5, format="%.1f", key="a2l")
    a2_upper  = st.number_input("Vertical angle Upper (°) elevation",  value=4.0,  step=0.5, format="%.1f", key="a2u")
    sr2_lower = st.number_input("Staff reading — Lower cross-hair (m)",value=1.250, step=0.001, format="%.3f", key="sr2l")
    sr2_upper = st.number_input("Staff reading — Upper cross-hair (m)",value=3.200, step=0.001, format="%.3f", key="sr2u")




# ══════════════════════════════════════════════════════════
#  CALCULATIONS
# ══════════════════════════════════════════════════════════
S1 = round(sr1_upper - sr1_lower, 3)
h1 = sr1_lower

value_upper=(math.tan(math.radians(abs(a1_upper))))
truncated_upper = int(value_upper * 10000) / 10000
    
value_lower=(math.tan(math.radians(abs(a1_lower))))
truncated_lower = int(value_lower * 10000) / 10000

denom1 = round(S1 / abs(truncated_upper - truncated_lower), 2)
D1 = denom1 if denom1 != 0 else 0

def truncate(value, decimals=3):
    factor = 10 ** decimals
        
    return int(value * factor) / factor

V1 = truncate(D1 * math.tan(math.radians(abs(a1_lower))), 3)

RL_inst = RL_BM + h1 + V1

S2 = round(sr2_upper - sr2_lower, 3)
h2 = sr2_lower

value2_upper=(math.tan(math.radians(abs(a2_upper))))
truncated2_upper = int(value2_upper * 10000) / 10000

value2_lower=(math.tan(math.radians(abs(a2_lower))))
truncated2_lower = int(value2_lower * 10000) / 10000

denom2 =  truncate(S2 / (truncated2_upper + truncated2_lower), 3)
D2 = denom2 if denom2 != 0 else 0

V2 = round(D2 * math.tan(math.radians(abs(a2_lower))), 3)

RL_B = RL_inst - V2 - h2

dist_BM_B = D1 + D2

# =========================================================
#   Input Table 
#=========================================================

st.markdown("## 📋 Observation Table")

table_html = f"""
<table style="
width:100%;
border-collapse:collapse;
text-align:center;
font-family:serif;
background:#161b22;
color:#e6edf3;
">

<tr>
<th style="border:2px solid white;padding:8px;">Inst.<br>station</th>
<th style="border:2px solid white;padding:8px;">Staff<br>station</th>
<th style="border:2px solid white;padding:8px;">Target</th>
<th style="border:2px solid white;padding:8px;">Vertical<br>angle</th>
<th style="border:2px solid white;padding:8px;">Staff<br>reading</th>
<th style="border:2px solid white;padding:8px;">Remark</th>
</tr>

<tr>
<td style="border:1px solid white;">A</td>
<td style="border:1px solid white;">BM</td>
<td style="border:1px solid white;">Lower</td>
<td style="border:1px solid white;">-{a1_lower:.1f}°</td>
<td style="border:1px solid white;">{sr1_lower:.3f}</td>
<td style="border:1px solid white;">RL of BM = {RL_BM:.3f} m</td>
</tr>

<tr>
<td style="border:1px solid white;">A</td>
<td style="border:1px solid white;">BM</td>
<td style="border:1px solid white;">Upper</td>
<td style="border:1px solid white;">-{a1_upper:.1f}°</td>
<td style="border:1px solid white;">{sr1_upper:.3f}</td>
<td style="border:1px solid white;"></td>
</tr>

<tr>
<td style="border:1px solid white;">A</td>
<td style="border:1px solid white;">B</td>
<td style="border:1px solid white;">Lower</td>
<td style="border:1px solid white;">-{a2_lower:.1f}°</td>
<td style="border:1px solid white;">{sr2_lower:.3f}</td>
<td style="border:1px solid white;"></td>
</tr>

<tr>
<td style="border:1px solid white;">A</td>
<td style="border:1px solid white;">B</td>
<td style="border:1px solid white;">Upper</td>
<td style="border:1px solid white;">+{a2_upper:.1f}°</td>
<td style="border:1px solid white;">{sr2_upper:.3f}</td>
<td style="border:1px solid white;"></td>
</tr>

</table>
"""

st.markdown(table_html, unsafe_allow_html=True)
# ══════════════════════════════════════════════════════════
#  ACCURATE FIGURE  (matches textbook Fig E.11.2)
# ══════════════════════════════════════════════════════════
st.markdown("## 🗺️ Tacheometric Diagram")

fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

# ---- coordinate system: horizontal axis = distance, vertical = height ----
# We place instrument station A at x=0, ground y=0
# BM is at x = +D1  (to the RIGHT)
# B  is at x = -D2  (to the LEFT)

hi = 1.4   # instrument height above ground (for drawing only)
Ax, Ay   = 0.0, 0.0
BMx, BMy = D1,  0.0
Bx,  By  = -D2, 0.0

inst_x, inst_y = Ax, Ay + hi     # instrument axis point A'

# ---- ground line ----
ground_left  = Bx  - D2*0.18
ground_right = BMx + D1*0.18
ax.plot([ground_left, ground_right], [0, 0], color='#5a6270', lw=1.5, zorder=1)
# ground hatch
for xh in np.arange(ground_left, ground_right+0.5, (ground_right-ground_left)/28):
    ax.plot([xh, xh-0.4], [0, -0.25], color='#3a4050', lw=0.8, zorder=1)

# ---- staff at BM ----
# staff drawn from ground upwards; lower CH = h1, upper CH = S1_upper
bm_staff_h = sr1_upper + 0.3
ax.plot([BMx, BMx], [0, bm_staff_h], color='#58a6ff', lw=5, solid_capstyle='round', zorder=3)
ax.plot([BMx-0.15, BMx+0.15], [sr1_lower, sr1_lower], color='#ff7b72', lw=2, zorder=4)
ax.plot([BMx-0.15, BMx+0.15], [sr1_upper, sr1_upper], color='#ffa657', lw=2, zorder=4)
# labels
ax.text(BMx + D1*0.06, sr1_lower, f' S₁ lower = {sr1_lower:.3f} m', color='#ff7b72', fontsize=9, va='center')
ax.text(BMx + D1*0.06, sr1_upper, f' S₁ upper = {sr1_upper:.3f} m', color='#ffa657', fontsize=9, va='center')
# h1 brace
ax.annotate('', xy=(BMx + D1*0.04, sr1_lower), xytext=(BMx + D1*0.04, 0),
            arrowprops=dict(arrowstyle='<->', color='#8b949e', lw=1.2))
ax.text(BMx + D1*0.09, sr1_lower/2, f'h₁={sr1_lower:.3f}', color='#8b949e', fontsize=8, va='center')

# ---- staff at B ----
b_staff_h = sr2_upper + 0.3
ax.plot([Bx, Bx], [0, b_staff_h], color='#58a6ff', lw=5, solid_capstyle='round', zorder=3)
ax.plot([Bx-0.15, Bx+0.15], [sr2_lower, sr2_lower], color='#d2a8ff', lw=2, zorder=4)
ax.plot([Bx-0.15, Bx+0.15], [sr2_upper, sr2_upper], color='#f778ba', lw=2, zorder=4)
ax.text(Bx - D2*0.06, sr2_lower, f'S₂ lower = {sr2_lower:.3f} m ', color='#d2a8ff', fontsize=9, va='center', ha='right')
ax.text(Bx - D2*0.06, sr2_upper, f'S₂ upper = {sr2_upper:.3f} m ', color='#f778ba', fontsize=9, va='center', ha='right')
ax.annotate('', xy=(Bx - D2*0.04, sr2_lower), xytext=(Bx - D2*0.04, 0),
            arrowprops=dict(arrowstyle='<->', color='#8b949e', lw=1.2))
ax.text(Bx - D2*0.10, sr2_lower/2, f'h₂={sr2_lower:.3f}', color='#8b949e', fontsize=8, va='center', ha='right')

# ---- instrument at A ----
# tripod legs
for dx in [-0.5, 0, 0.5]:
    ax.plot([Ax, Ax+dx], [hi, 0], color='#8b949e', lw=1.2, zorder=2)
# instrument body
ax.plot(inst_x, inst_y, 's', color='#3fb950', markersize=10, zorder=6)
ax.text(inst_x, inst_y + hi*0.12, "A′", ha='center', va='bottom', color='#3fb950',
        fontsize=10, fontweight='bold')
# hi brace
ax.annotate('', xy=(Ax - D2*0.06, hi), xytext=(Ax - D2*0.06, 0),
            arrowprops=dict(arrowstyle='<->', color='#3fb950', lw=1.2))
ax.text(Ax - D2*0.09, hi/2, f'hᵢ', color='#3fb950', fontsize=8.5, va='center', ha='right')

# ---- lines of sight ----
# To BM lower (depression a1_lower)
ax.annotate('', xy=(BMx, sr1_lower), xytext=(inst_x, inst_y),
            arrowprops=dict(arrowstyle='->', color='#ff7b72', lw=1.8))
# To BM upper (depression a1_upper)
ax.annotate('', xy=(BMx, sr1_upper), xytext=(inst_x, inst_y),
            arrowprops=dict(arrowstyle='->', color='#ffa657', lw=1.8, linestyle='dashed'))

# To B lower (depression a2_lower)
ax.annotate('', xy=(Bx, sr2_lower), xytext=(inst_x, inst_y),
            arrowprops=dict(arrowstyle='->', color='#d2a8ff', lw=1.8))
# To B upper (elevation a2_upper)
ax.annotate('', xy=(Bx, sr2_upper), xytext=(inst_x, inst_y),
            arrowprops=dict(arrowstyle='->', color='#f778ba', lw=1.8, linestyle='dashed'))

# horizontal through instrument axis (dashed reference)
ax.plot([Bx - D2*0.1, BMx + D1*0.1], [inst_y, inst_y],
        color='#8b949e', lw=1, linestyle=':', zorder=2)

# ---- angle arcs ----
arc_r = min(D1, D2) * 0.28
# angle labels on BM side
theta1 = -np.degrees(np.arctan2(inst_y - sr1_lower, BMx - inst_x))
theta2 = -np.degrees(np.arctan2(inst_y - sr1_upper, BMx - inst_x))
arc1 = mpatches.Arc((inst_x, inst_y), arc_r*2, arc_r*2,
                     angle=0, theta1=-theta1, theta2=0, color='#ff7b72', lw=1.2)
arc2 = mpatches.Arc((inst_x, inst_y), arc_r*1.5*2, arc_r*1.5*2,
                     angle=0, theta1=-theta2, theta2=0, color='#ffa657', lw=1.2, linestyle='--')
ax.add_patch(arc1)
ax.add_patch(arc2)
ax.text(inst_x + arc_r*1.3, inst_y - arc_r*0.55, f'{a1_lower:.0f}°', color='#ff7b72', fontsize=9)
ax.text(inst_x + arc_r*1.8, inst_y - arc_r*0.3, f'{a1_upper:.0f}°', color='#ffa657', fontsize=9)

# angle labels on B side
theta3 = np.degrees(np.arctan2(inst_y - sr2_lower, inst_x - Bx))
theta4 = np.degrees(np.arctan2(sr2_upper - inst_y, inst_x - Bx))
arc3 = mpatches.Arc((inst_x, inst_y), arc_r*2, arc_r*2,
                     angle=0, theta1=180, theta2=180+theta3, color='#d2a8ff', lw=1.2)
arc4 = mpatches.Arc((inst_x, inst_y), arc_r*1.5*2, arc_r*1.5*2,
                     angle=0, theta1=180-theta4, theta2=180, color='#f778ba', lw=1.2, linestyle='--')
ax.add_patch(arc3)
ax.add_patch(arc4)
ax.text(inst_x - arc_r*1.8, inst_y - arc_r*0.55, f'{a2_lower:.0f}°', color='#d2a8ff', fontsize=9)
ax.text(inst_x - arc_r*2.3, inst_y + arc_r*0.2, f'{a2_upper:.0f}°', color='#f778ba', fontsize=9)

# ---- D1 and D2 dimension lines ----
dim_y = -0.55
ax.annotate('', xy=(BMx, dim_y), xytext=(Ax, dim_y),
            arrowprops=dict(arrowstyle='<->', color='#f0c040', lw=1.6))
ax.text((Ax+BMx)/2, dim_y - 0.3, f'D₁ = {D1:.3f} m', ha='center', color='#f0c040', fontsize=9.5, fontweight='bold')

ax.annotate('', xy=(Bx, dim_y), xytext=(Ax, dim_y),
            arrowprops=dict(arrowstyle='<->', color='#f0c040', lw=1.6))
ax.text((Ax+Bx)/2, dim_y - 0.3, f'D₂ = {D2:.3f} m', ha='center', color='#f0c040', fontsize=9.5, fontweight='bold')

# ---- total distance BM–B ----
ax.annotate('', xy=(BMx, dim_y - 0.7), xytext=(Bx, dim_y - 0.7),
            arrowprops=dict(arrowstyle='<->', color='#58a6ff', lw=1.8))
ax.text((Bx+BMx)/2, dim_y - 1.0, f'BM to B = {dist_BM_B:.3f} m', ha='center',
        color='#58a6ff', fontsize=10, fontweight='bold')

# ---- ground station labels ----
for px, py, lbl, col in [(Ax, Ay, 'A', '#3fb950'), (BMx, BMy, 'BM', '#ff7b72'), (Bx, By, 'B', '#d2a8ff')]:
    ax.plot(px, py, 'o', color=col, markersize=9, zorder=7)
    ax.text(px, py + 0.15, lbl, ha='center', va='bottom', color=col, fontsize=11, fontweight='bold')

# ---- V1, V2 vertical arrows ----
ax.annotate('', xy=(BMx - D1*0.08, sr1_lower), xytext=(BMx - D1*0.08, inst_y),
            arrowprops=dict(arrowstyle='->', color='#ff7b72', lw=1.2, linestyle='dotted'))
ax.text(BMx - D1*0.12, (sr1_lower+inst_y)/2, f'V₁={V1:.3f}', color='#ff7b72', fontsize=8, ha='right')

ax.annotate('', xy=(Bx + D2*0.08, sr2_lower), xytext=(Bx + D2*0.08, inst_y),
            arrowprops=dict(arrowstyle='->', color='#d2a8ff', lw=1.2, linestyle='dotted'))
ax.text(Bx + D2*0.12, (sr2_lower+inst_y)/2, f'V₂={V2:.3f}', color='#d2a8ff', fontsize=8)

# ---- legend ----
legend_elements = [
    Line2D([0],[0], color='#ff7b72', lw=2, label=f'Sight to BM lower (−{a1_lower:.0f}°)'),
    Line2D([0],[0], color='#ffa657', lw=2, linestyle='--', label=f'Sight to BM upper (−{a1_upper:.0f}°)'),
    Line2D([0],[0], color='#d2a8ff', lw=2, label=f'Sight to B lower (−{a2_lower:.0f}°)'),
    Line2D([0],[0], color='#f778ba', lw=2, linestyle='--', label=f'Sight to B upper (+{a2_upper:.0f}°)'),
    Line2D([0],[0], color='#3fb950', marker='s', markersize=8, lw=0, label='Instrument axis A′'),
]
leg = ax.legend(handles=legend_elements, facecolor='#161b22', edgecolor='#30363d',
                labelcolor='#e6edf3', fontsize=8.5, loc='upper right')

ax.set_title('Tacheometric Survey from A to BM (right) and B (left)',
             color='#e6edf3', fontsize=11, pad=10, fontfamily='serif')

# axis formatting
ax.set_xlabel('Horizontal Distance from A (m)', color='#8b949e', fontsize=9)
ax.set_ylabel('Height (m)', color='#8b949e', fontsize=9)
ax.tick_params(colors='#8b949e')
for sp in ax.spines.values():
    sp.set_edgecolor('#30363d')

margin_x = max(D1, D2) * 0.22
ax.set_xlim(Bx - margin_x, BMx + margin_x)
ax.set_ylim(-1.8, max(inst_y, sr1_upper, sr2_upper) + 0.8)
ax.axvline(0, color='#3fb950', lw=0.6, linestyle=':', alpha=0.4)

st.pyplot(fig)
plt.close()

# ══════════════════════════════════════════════════════════
#  STEP-BY-STEP SOLUTION
# ══════════════════════════════════════════════════════════
st.markdown("## 🔢 Step-by-Step Solution")

with st.expander("📌 First Observation — A → BM", expanded=True):
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="step-title">Staff Intercept  S₁</div>'
                f'<div class="formula-box">S₁ = {sr1_upper:.3f} − {sr1_lower:.3f} = {S1:.3f} m</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="step-title">Horizontal Distance D₁</div>'
                f'<div class="formula-box">'
                f'S₁ = D₁ (tan {a1_lower:.0f}° − tan {a1_upper:.0f}°)<br>'
                f'D₁ = {S1:.3f} / (tan {a1_lower:.0f}° − tan {a1_upper:.0f}°) = {S1:.3f} / {denom1:.6f}'
                f'</div>'
                f'<div class="result-hl">D₁ = {D1:.3f} m</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="step-title">Vertical Component V₁</div>'
                f'<div class="formula-box">V₁ = D₁ × tan {a1_lower:.0f}° = {D1:.3f} × {np.tan(np.radians(a1_lower)):.5f}</div>'
                f'<div class="result-hl">V₁ = {V1:.3f} m</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="step-title">RL of Instrument Axis</div>'
                f'<div class="formula-box">RL = RL(BM) + h₁ + V₁ = {RL_BM:.3f} + {h1:.3f} + {V1:.3f}</div>'
                f'<div class="result-hl">RL of instrument axis = {RL_inst:.3f} m</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with st.expander("📌 Second Observation — A → B", expanded=True):
    st.markdown('<div class="step-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="step-title">Staff Intercept  S₂</div>'
                f'<div class="formula-box">S₂ = {sr2_upper:.3f} − {sr2_lower:.3f} = {S2:.3f} m</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="formula-box" style="color:#ffa657;">⚠ Lower = depression (−{a2_lower:.0f}°), Upper = elevation (+{a2_upper:.0f}°) → angles on opposite sides → use (tan {a2_lower:.0f}° + tan {a2_upper:.0f}°)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="step-title">Horizontal Distance D₂</div>'
                f'<div class="formula-box">'
                f'S₂ = D₂ (tan {a2_lower:.0f}° + tan {a2_upper:.0f}°)<br>'
                f'D₂ = {S2:.3f} / (tan {a2_lower:.0f}° + tan {a2_upper:.0f}°) = {S2:.3f} / {denom2:.6f}'
                f'</div>'
                f'<div class="result-hl">D₂ = {D2:.3f} m</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="step-title">Vertical Component V₂</div>'
                f'<div class="formula-box">V₂ = D₂ × tan {a2_lower:.0f}° = {D2:.3f} × {np.tan(np.radians(a2_lower)):.5f}</div>'
                f'<div class="result-hl">V₂ = {V2:.3f} m</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="step-title">RL of Station B</div>'
                f'<div class="formula-box">RL of B = RL(inst axis) − V₂ − h₂ = {RL_inst:.3f} − {V2:.3f} − {h2:.3f}</div>'
                f'<div class="result-hl">RL of B = {RL_B:.3f} m</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════
#  FINAL ANSWERS
# ══════════════════════════════════════════════════════════
st.markdown(f"""
<div class="final-box">
  <h3 style="color:#f0c040;font-family:'Playfair Display',serif;margin-bottom:1rem;">✅ Final Answers</h3>
  <p style="font-size:1.2rem;color:#3fb950;font-family:'Source Code Pro',monospace;">
    RL of Station B &nbsp;=&nbsp; <strong>{RL_B:.3f} m</strong>
  </p>
  <p style="font-size:1.2rem;color:#58a6ff;font-family:'Source Code Pro',monospace;">
    Distance BM → B &nbsp;=&nbsp; D₁ + D₂ &nbsp;=&nbsp; {D1:.3f} + {D2:.3f} &nbsp;=&nbsp; <strong>{dist_BM_B:.3f} m</strong>
  </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("Tacheometric Surveying | Problem Statement | All answers update live when inputs change")