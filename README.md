# Predicting Demand at EV Charging Stations Using Machine Learning

*Used Python to analyze EV charging data and forecast station demand by time and location. Leveraged machine learning models to identify peak usage patterns and built visual summaries to support smarter infrastructure planning — all as part of the AI4ALL Ignite accelerator program.*


## Problem Statement
As electric vehicles (EVs) become more common, cities and providers face challenges in maintaining efficient charging infrastructure. Many stations are either overwhelmed during peak times or left idle during off peak periods due to poor demand forecasting.

This project addresses the need for reliable, data driven predictions to optimize EV station deployment and operations. By forecasting usage trends by hour, weekday, and location, we aim to reduce congestion, wait times, and operational inefficiencies. 

## Key Results <!--- do not change this line -->

1. Cleaned and preprocessed timestamped charging data from California EV stations

2. Engineered temporal features such as hour of day, day of week, and session count

3. Trained regression models to predict:

   * Number of charging sessions per hour

   * Total energy consumed per time window

4. Visualized high-demand time periods and locations through:

   * Peak hour charts by day

   * Geo heatmaps of usage across cities

5. Found significant differences in weekday vs. weekend usage patterns and location-specific demand spikes




## Methodologies 

*We conducted a literature review and used open datasets to identify patterns and needs. Cleaned and processed data using pandas, removing inconsistencies and standardizing formats. Engineered features based on time, location, and usage trends. Built and tested prototypes iteratively, incorporating user feedback and refining based on performance metrics. Final models were evaluated using [insert metric, e.g., RMSE or accuracy], then deployed with clear documentation and Git integration for reproducibility.*


## Data Sources <!--- do not change this line -->

*Kaggle Dataset: [Link to EV Charging Station Usage of California City (Kaggle)](https://www.kaggle.com/datasets/venkatsairo4899/ev-charging-station-usage-of-california-city)*

## Technologies Used <!--- do not change this line -->

- *Python*
- *pandas*
- *numpy*
- *Google Colab*
- *LightGBM*
- *Scikit-learn*


## Authors <!--- do not change this line -->
*This project was completed in collaboration with:*

- *Ming-Lang Qin ([minglangq21@gmail.com](mailto:minglangq21@gmail.com))*
- *Clarissa Ramirez-Chavez  ([clarissaramirez-chavez@my.unt.edu](mailto:clarissaramirez-chavez@my.unt.edu))*
- *Daniela Gallego ([ddgallego99@gmail.com](mailto:ddgallego@gmail.com))*
- *Serena Li ([li228s@mtholyoke.edu](mailto:li228s@mtholyoke.edu))*
