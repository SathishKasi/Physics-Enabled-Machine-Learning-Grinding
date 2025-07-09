# Physics-Enabled-Machine-Learning-Grinding
This repository appears to be a Physics-Enabled Machine Learning project focused on grinding process optimization. Based on the files and code, here's what this repository contains:

Project Overview
This is a research project that combines physics-based models with machine learning to predict and optimize grinding manufacturing processes, specifically for industrial machining operations.

Key Components
1. Data Processing & Preprocessing
CSEMII_DATA_PREPROCESS.py: Handles data cleaning, interpolation, and feature engineering for manufacturing data
SQL.py: Connects to MTConnect database to extract real-time manufacturing data from CNC machines
2. Machine Learning Models
CSEMII_DNN_Hybrid_Model.py: Main hybrid deep neural network that combines physics-based outputs with data-driven predictions
CSEMII_Decision_Tree.py: Traditional machine learning approach using decision trees and SVR
test.py: Active learning implementation using Gaussian Process Regression
3. Model Inference & Optimization
CSEMII_DNN_prediction.py: Loads trained models and makes predictions on new grinding data
Input_Iteration.py: Optimizes input parameters (feed rate, radial infeed, cycles) for grinding operations
4. Key Features
The models predict grinding process outcomes like:

Machining time and energy consumption
Dressing time and energy (wheel conditioning)
Process optimization based on stock removal requirements
5. Technology Stack
Deep Learning: TensorFlow/Keras for neural networks
Data Science: Pandas, NumPy, Scikit-learn
Database: pyodbc for SQL Server connectivity
Visualization: Matplotlib for plotting results
6. Industrial Context
This appears to be related to CESMII (Clean Energy Smart Manufacturing Innovation Institute) research, focusing on smart manufacturing and energy-efficient grinding processes in industrial settings.

The hybrid approach combines traditional physics-based grinding models with modern machine learning to improve prediction accuracy and process optimization in manufacturing environments.
