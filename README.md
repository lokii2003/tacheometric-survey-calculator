# 📐 Tacheometric RL Calculator

A **Streamlit-based web application** for performing **Tacheometric Surveying calculations**.
The app calculates **distance, vertical height difference, and Reduced Level (RL)** using staff readings and vertical angles.

---

## 🚀 Features

* Calculate **distance between stations**
* Compute **vertical height difference (V1, V2)**
* Determine **RL of Instrument Axis**
* Compute **RL of Station B**
* Automatically calculate **total distance between BM and B**
* Visualize the survey layout using **Matplotlib**

---

## 🧮 Calculations Performed

The application performs the following surveying calculations:

### 1. Staff Intercept

[
S = Upper\ Reading - Lower\ Reading
]

### 2. Horizontal Distance

[
D = \frac{S}{tan(\theta_u) - tan(\theta_l)}
]

### 3. Vertical Height Difference

[
V = D \times tan(\theta)
]

### 4. Reduced Level

[
    RL_{instrument} = RL_{BM} + h + V
]

[
RL_B = RL_{instrument} - V_2 - h_2
]

---

## 🖥️ App Interface

The application allows users to input:

### Benchmark (BM) Observation

* Lower staff reading
* Upper staff reading
* Upper angle (degree & minute)
* Lower angle (degree & minute)
* RL of Benchmark

### Station B Observation

* Lower staff reading
* Upper staff reading
* Upper angle (degree & minute)
* Lower angle (degree & minute)

---

## 📊 Visualization

After calculation, the app generates a **survey diagram** showing:

* Benchmark (BM)
* Instrument station (A)
* Station B
* Horizontal distances (D1, D2)
* Vertical heights (V1, V2)
* Reduced Levels

---

## 🛠️ Technologies Used

* Python
* Streamlit
* Matplotlib
* Math library

---

## 📦 Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/tacheometric-calculator.git
cd tacheometric-calculator
```

2. Install dependencies

```bash
pip install streamlit matplotlib
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

The app will open automatically in your browser:

```
http://localhost:8501
```

---

## 📂 Project Structure

```
tacheometric-calculator
│
├── app.py
├── README.md
└── requirements.txt
```

---

## 📌 Example Output

The app calculates:

* **D1 – Distance from BM to instrument**
* **V1 – Vertical difference**
* **RL of Instrument Axis**
* **D2 – Distance from instrument to station B**
* **V2 – Vertical difference**
* **RL of Station B**
* **Total distance BM → B**

---

## 📜 License

This project is for **educational and surveying purposes**.

---

## 👨‍💻 Author

Developed using **Python & Streamlit for surveying calculations**.
