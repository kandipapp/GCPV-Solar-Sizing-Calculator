# Design and Sizing of a Grid-Connected Photovoltaic (GCPV) Power System

## 📌 Overview
This repository contains a Python-based computational model developed to automate the mathematical sizing and array configuration of a large-scale, three-phase Grid-Connected Photovoltaic (GCPV) system. 

The program calculates the optimal series and parallel string configurations to maximize energy yield while strictly adhering to the electrical, thermal, and safety constraints of the hardware components. A key feature of this model is its built-in constraint-checking logic, which automatically detects hardware incompatibilities (such as voltage limit conflicts) between the PV modules and the selected grid inverter.

This project was developed by **Group 24**: Eugene Ooi You Qi for the EEEE2049 Electrical Energy Conditioning and Control module.

## ⚙️ Hardware Specifications & Design Parameters
The system was designed and evaluated based on the following assigned specifications:
*   **PV Module:** Trina Solar ALLMAX PLUS 310W 
    *   Maximum System Voltage: 1000V (IEC Limit)
*   **Primary Inverter:** SUNGROW SG250HX (1500V Utility-Scale)
*   **Alternative Inverter:** HUAWEI SUN2000-8KTL (1000V Commercial-Scale)
*   **Target DC/AC Oversizing Ratio:** 1.24
*   **Temperature Range:** 25°C to 72°C
*   **Maximum DC Cable Loss:** 3% (Efficiency Factor: 0.97)

## 🚀 Features
The script automates standard engineering sizing methodologies (Steps A through K), including:
1.  **Array Power Allocation:** Calculates the total PV modules per inverter and MPPT based on the DC/AC ratio.
2.  **Maximum String Sizing Constraints:** Evaluates open-circuit ($V_{oc}$) and maximum power voltages ($V_{mp}$) at the lowest temperatures to ensure strings do not exceed inverter damage limits or the PV cell's absolute 1000V safety limit.
3.  **Minimum String Sizing Constraints:** Evaluates voltage drops at the highest temperatures (accounting for cable loss) to ensure the string provides sufficient voltage to wake the inverter and maintain Maximum Power Point Tracking (MPPT).
4.  **Hardware Mismatch Detection:** Automatically compares the minimum required string length ($N_{s\_min}$) against the maximum safe string length ($N_{s\_max}$). If a conflict is detected (e.g., $N_{s\_min} > N_{s\_max}$), the algorithm interrupts the loop and flags a **CRITICAL DESIGN ERROR**.

## 🛠️ How to Run
This script is written in standard Python and relies only on the built-in `math` library. No external dependencies (like NumPy or Pandas) are required.

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/GCPV-System-Sizing-Calculator.git
Navigate to the directory:
Run the script via your terminal or IDE:
📊 Results Summary
SUNGROW SG250HX Scenario: The script mathematically proves that a functional array is impossible with the Trina Solar 1000V panels, as the inverter's 860V minimum MPPT requirement demands 33 modules in series, violating the PV module's 24-module safety maximum
.
HUAWEI SUN2000-8KTL Scenario: The script validates this alternative 1000V-class inverter, confirming a highly efficient and safe array configuration of 16 modules per string
.
📝 License
This project is for academic coursework purposes (Spring 2025/2026)
.