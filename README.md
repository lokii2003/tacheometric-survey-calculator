# README: Tacheometric Surveying Solver

This project provides an interactive Python/Streamlit application to solve tangential tacheometry problems. It specifically calculates the Reduced Level (RL) of a station and the horizontal distance between points based on theodolite observations.

## 📌 Problem Overview

Based on **Problem Statement**, the app determines the elevation of **Station B** using observations from **Station A** to a **Benchmark (BM)** and **Station B**.

## 🚀 Key Features

* 
**Manual Inputs**: Adjust RL of BM, vertical angles (elevation/depression), and staff readings via a sidebar.


* 
**Dynamic Calculations**: View step-by-step solutions with updated values in real-time.


* **Geometric Visualization**: Includes a plot of Fig. E.11.2 showing the instrument axis and lines of sight.



## 🛠 Formulas Used

* 
**Staff Intercept ($S$):** $S = \text{Upper Reading} - \text{Lower Reading}$.


* 
**Distance ($D$) - Same Side Angles:** $D = \frac{S}{\tan \alpha_1 - \tan \alpha_2}$.


* 
**Distance ($D$) - Opposite Side Angles:** $D = \frac{S}{\tan \alpha + \tan \beta}$.


* 
**Vertical Component ($V$):** $V = D \times \tan \theta$ (using the angle to the lower cross-hair).



## 💻 Quick Start

1. **Install Dependencies**:
```bash
pip install streamlit matplotlib numpy

```


2. **Run the App**:
```bash
streamlit run app.py

```



## 📊 Sample Results (Problem Statement)

* 
**RL of Station B**: 515.398 m.


* 
**Distance BM to B**: 49.706 m.



---

##  Sample Results 
For a full breakdown of the theory and step-by-step manual calculations, [refer to the Detailed Project Documentation](https://docs.google.com/document/d/1Owj_vA9gmCLcSt9u-i3gFPc42AjVIjDM/edit?usp=sharing&ouid=103860477907296356829&rtpof=true&sd=true).