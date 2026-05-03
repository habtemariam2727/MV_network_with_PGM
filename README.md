# MV Network Power Flow using Power Grid Model

## Overview
This project runs a simple power flow simulation using the Power Grid Model library.  
The network is built from line data, and loads are assigned from node data.

---

## Requirements
- Python 3.10
- Conda (recommended)

---

## Get the Project

Clone the repository:

git clone https://github.com/habtemariam2727/MV_network_with_PGM.git  
cd MV_network_with_PGM


## Setup

Create and activate environment:

conda create -n pgm_env python=3.10  
conda activate pgm_env  

Install dependencies:

pip install -r requirements.txt  

---

## Input Data

Place the following files in the `data/` folder:

- Lines_34.csv → line parameters (from/to, R, X, status)
- Nodes_34.csv → load data (PD, QD)

---

## Run the Simulation

python ppf.py

---

## Output

The script will print:
- Node voltages
- Line flows

---

## Notes

- Load values must be in kW / kVAr  
- The script converts them to W / var  
- Node 1 is used as the slack bus  

---

## Project Structure

MV_network_with_PGM/  
│── data/  
│── network_construction.py  
│── ppf.py  
│── requirements.txt  
│── README.md  