import streamlit as st
import math
import matplotlib.pyplot as plt


st.set_page_config(page_title="Tacheometric RL Calculator", layout="centered")

st.title("📐 Tacheometric Surveying Calculator")
st.write("Enter the observation values to compute RL and distance.")

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


# ---------------- INPUT SECTION ----------------
st.header("First Observation (Benchmark BM)")

lower1 = st.number_input("Lower staff reading (BM)", value=0.655, format="%.3f")
upper1 = st.number_input("Upper staff reading (BM)", value=2.655, format="%.3f")


col1, col2 = st.columns(2)
deg1u = col1.number_input("BM Upper angle (degree)", value=-7, step=1)
min1u = col2.number_input("BM Upper angle (minute)", value=0, step=1)

col3, col4 = st.columns(2)
deg1l = col3.number_input("BM Lower angle (degree)", value=-10, step=1)
min1l = col4.number_input("BM Lower angle (minute)", value=0, step=1)

RL_BM = st.number_input("RL of Benchmark (m)", value=510.500, format="%.3f")


st.header("Second Observation (Station B)")

lower2 = st.number_input("Lower staff reading (B)", value=1.250, format="%.3f") 
upper2 = st.number_input("Upper staff reading (B)", value=3.200, format="%.3f")


col5, col6 = st.columns(2)
deg2u = col5.number_input("B Upper angle (degree)", value=4, step=1)   
min2u = col6.number_input("B Upper angle (minute)", value=0, step=1)

col7, col8 = st.columns(2)
deg2l = col7.number_input("B Lower angle (degree)", value=-5, step=1)
min2l = col8.number_input("B Lower angle (minute)", value=0, step=1)


# ---------------- CALCULATION ----------------
if st.button("Calculate RL and Distance"):

    # Convert angles (signed)
    angle1_upper = deg_min_to_decimal(deg1u, min1u)
    angle1_lower = deg_min_to_decimal(deg1l, min1l)
    angle2_upper = deg_min_to_decimal(deg2u, min2u)
    angle2_lower = deg_min_to_decimal(deg2l, min2l)

    # ---------- First Observation ----------
    S1 = round(upper1 - lower1, 3)
    h1 = lower1

    value_upper=(math.tan(math.radians(abs(angle1_upper))))
    truncated_upper = int(value_upper * 10000) / 10000
    
    value_lower=(math.tan(math.radians(abs(angle1_lower))))
    truncated_lower = int(value_lower * 10000) / 10000
    
    D1 = round(S1 / abs(truncated_upper - truncated_lower), 2)

    def truncate(value, decimals=3):
        factor = 10 ** decimals
        
        return int(value * factor) / factor
    
    V1 = truncate(D1 * math.tan(math.radians(abs(angle1_lower))), 3)

    RL_instrument = RL_BM + h1 + V1


    # ---------- Second Observation ----------
    S2 = round(upper2 - lower2, 3)
    h2 = lower2

    value2_upper=(math.tan(math.radians(abs(angle2_upper))))
    truncated2_upper = int(value2_upper * 10000) / 10000

    value2_lower=(math.tan(math.radians(abs(angle2_lower))))
    truncated2_lower = int(value2_lower * 10000) / 10000

    D2 = truncate(S2 / (truncated2_upper + truncated2_lower), 3)

    V2 = round(D2 * math.tan(math.radians(abs(angle2_lower))), 3)

    RL_B = RL_instrument - V2 - h2
    distance_BM_B = D1 + D2


    # ---------- ROUND TO 3 DECIMAL ----------
    D1, V1, RL_instrument = round(D1, 2), round(V1, 3), round(RL_instrument, 3)
    D2, V2, RL_B = round(D2, 3), round(V2, 3), round(RL_B, 3)
    distance_BM_B = round(distance_BM_B, 3)


    # ---------------- OUTPUT ----------------
    st.success("Calculation Completed ✅")

    st.subheader("Results")
    st.write(f"**D1 = {D1} m**")
    st.write(f"**V1 = {V1} m**")
    st.write(f"**RL of Instrument Axis = {RL_instrument} m**")

    st.write("---")

    st.write(f"**D2 = {D2} m**")
    st.write(f"**V2 = {V2} m**")
    st.write(f"**RL of Station B = {RL_B} m**")

    st.write("---")
    st.write(f"### Distance between BM and B = {distance_BM_B} m")


    # ---------------- DYNAMIC SURVEY FIGURE ----------------
    st.subheader("Survey Figure with Calculated Values")

    fig, ax = plt.subplots(figsize=(10, 4))

    # Coordinates
    x_BM = 0
    x_A = D1
    x_B = D1 + D2

# Ground line
    ax.plot([x_BM, x_A, x_B], [0, 0, 0])

# Points
    ax.scatter([x_BM, x_A, x_B], [0, 0, 0])

# Labels
    ax.text(x_BM, -0.5, "BM", ha="center")
    ax.text(x_A, -0.5, "A", ha="center")
    ax.text(x_B, -0.5, "B", ha="center")

# Distance labels
    ax.text(x_A/2, 0.5, f"D1 = {D1:.3f} m", ha="center")
    ax.text(x_A + D2/2, 0.5, f"D2 = {D2:.3f} m", ha="center")

# Vertical lines (V1 and V2)
    ax.plot([x_A, x_A], [0, V1])
    ax.plot([x_B, x_B], [0, V2])

    ax.text(x_A + 0.5, V1/2, f"V1 = {V1:.3f}", color="blue")
    ax.text(x_B + 0.5, V2/2, f"V2 = {V2:.3f}", color="red")

# RL values
    ax.text(x_A, V1 + 0.5, f"RL A = {RL_instrument:.3f}", ha="center")
    ax.text(x_B, V2 + 0.5, f"RL B = {RL_B:.3f}", ha="center")

    ax.set_title("Tacheometric Survey Layout")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Elevation (m)")
    ax.grid(True)

    st.pyplot(fig)