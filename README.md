# **🛵💨 Online Food Delivery Analysis 🍔** 
## **📖 About the Project**
> This project is a comprehensive Online Food Delivery Data Analysis system built with Python, Streamlit, Plotly, and MySQL. It provides data-driven insights for restaurants, delivery partners, and business stakeholders by analyzing order patterns, customer behavior, revenue, profit, and operational performance from 2012 to 2022.
## **🔨 Development Process**
The development of the Online Food Delivery Analysis project followed a structured workflow to ensure clean data, efficient storage, and actionable insights:

> ### **1. Data Collection & Loading**

* Collected historical online food delivery data from CSV files spanning 2012–2022.
* Loaded the dataset into Pandas DataFrames for initial inspection and preprocessing.

> ### **2. Data Cleaning & Preprocessing**

* Handled missing values using median imputation for numerical columns and default values for categorical fields.
* Outliers in Discount_Applied and other metrics were managed using the Interquartile Range (IQR) method.
* Standardized formats for date, time, and boolean columns.

> ### **3. Feature Engineering**

* Created new columns for customer segmentation, e.g., Customer_Age_group (Youth/Adults).
* Defined delivery performance categories (Good, Moderate, Worst) based on ratings.
* Calculated Profit_Margin_Percent and Peak_Hour_Indicator for business analysis.
* Derived Order_day_name from Order_Date to study weekday/weekend patterns.

> ### **4. Database Design & Integration**

* Set up a MySQL database to store cleaned and processed data.
* Designed the Food_Order_Details table with optimized data types and constraints.
* Connected Python to the database using SQLAlchemy for querying and storage.

> ### **5. Dashboard Development with Streamlit**

* Created a multi-page interactive dashboard: Home, Analysis, Customer & Order Analysis, Revenue & Profit Analysis, Delivery Performance, Restaurant Performance, Operational Insights.
* Integrated Plotly and Plotly Express for interactive visualizations (bar charts, pie charts, sunburst, area plots).
* Added real-time metrics, filtering, and insights alongside charts for user-friendly interpretation.

> ### **6. Testing & Validation**

* Verified data accuracy after cleaning and database insertion.
* Tested dashboard functionality across different pages and visualizations.
* Ensured calculations such as total revenue, profit, and cancellations were correct.

> ### **7. Deployment**

* Prepared the project for local deployment with requirements.txt.
* Streamlit app structured to allow easy navigation and intuitive insights for stakeholders.
  
## **✨ Key Features**
> #### 1. Automated Data Cleaning 🧹:
* Handles missing values, corrects inconsistencies, and removes outliers using robust statistical methods.

> #### 2. Feature Engineering 🔧
* Creates actionable metrics like Customer_Age_group, Delivery_Performance, Profit_Margin_Percent, Peak_Hour_Indicator, and Order_day_name.

> #### 3. Multi-Page Interactive Dashboard 📊
* Provides separate pages for Customer Analysis, Revenue & Profit, Delivery Performance, Restaurant Performance, and Operational Insights.

> #### 4. Visualizations Galore 🎨
* Includes bar charts, pie charts, sunburst charts, and area plots for intuitive data understanding.

> #### 5. Database Integration 💾
* Stores cleaned data in MySQL for efficient querying and scalability.

> #### 6. Real-Time Metrics ⏱
* Displays live summaries such as total orders, total revenue, and top-performing customers or cuisines.

> #### 7. Actionable Insights 📝
* Provides business insights alongside visualizations to guide decision-making.

> #### 8. User-Friendly Navigation 🧭
* Streamlit interface allows seamless switching between analysis pages with dynamic filtering.
## **⚙️ Tech Stack**
> * Programming Language 🐍:>Python 3.10+

> * Data Analysis & Manipulation 📊: Pandas, NumPy

> * Visualization & Dashboard 🎨: Plotly, Plotly Express, Streamlit

> * Database & Storage 💾: MySQL, SQLAlchemy

> * Data Cleaning & Preprocessing 🧹: Python (Pandas, NumPy)

> * Web Framework / Deployment 🌐: Streamlit

> * Version Control & Collaboration 🔗: Git & GitHub

## **🎯 Features**

> #### 1. Customer & Order Analysis 👤🛎️

* Identify top-spending customers and their purchase patterns.
* Analyze order volume and revenue by age groups.
* Compare weekend vs. weekday order trends.

> #### 2. Revenue & Profit Analysis 💸💰

* Track monthly revenue trends with interactive visualizations.
* Evaluate the impact of discounts on profit margins.
* Identify high-revenue cities and top-performing cuisines.

> #### 3. Delivery Performance 🛵💨

* Calculate average delivery times across cities.
* Analyze the effect of delivery distance on time.
* Compare delivery ratings with delivery duration.

> #### 4. Restaurant Performance 🍽️

* Determine top-rated restaurants and their order volumes.
* Monitor cancellation rates by restaurant.
* Assess cuisine-wise performance and profitability.

> #### 5. Operational Insights 🛠️

* Analyze peak hour demand and revenue generation.
* Understand customer payment mode preferences.
* Explore cancellation reasons by city for operational improvements.

> #### 6. Interactive Visualizations 📊

* Includes bar charts, pie charts, sunburst charts, and area plots for clear insights.
* Dynamic filtering and multi-page dashboard for easy exploration.

## **⚙️ Setup & Installation**
**1. Clone the Repository:**
```
git clone https://github.com/yourusername/online-food-delivery-analysis.git
cd online-food-delivery-analysis
```
**2. Create a Virtual Environment:**
```
python -m venv OFD
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
**3. Install Dependencies:**

`pip install -r requirements.txt`

**4. Run the Streamlit App:**

`streamlit run app.py`

## **📊 Dataset Setup**
The project uses a historical dataset of online food delivery orders, which contains detailed information about customers, restaurants, orders, and deliveries.

**Dataset Details**

* File Format: `CSV (ONINE_FOOD_DELIVERY_ANALYSIS.csv)`
* Number of Records: ~[Insert total number of rows after cleaning]

#### Columns / Features Include:

* `Order_Id` – Unique identifier for each order
* `Customer_ID` – Unique customer identifier
* `Customer_Age`, Customer_Gender – Demographic details
* `City, Area` – Location details
* `Restaurant_ID, Restaurant_Name, Cuisine_Type` – Restaurant information
* `Order_Date, Order_Time` – Timing of orders
* `Delivery_Time_Min, Distance_km` – Delivery metrics
* `Order_Value, Discount_Applied, Final_Amount` – Financial metrics
* `Payment_Mode` – Mode of payment
* `Order_Status, Cancellation_Reason` – Order completion info
* `Delivery_Rating, Restaurant_Rating` – Ratings for service and restaurant
* `Order_Day, Peak_Hour, Customer_Age_group, Delivery_Performance, Profit_Margin_Percent, Peak_Hour_Indicator, Order_day_name` – Engineered features

#### Setup Steps

* Place the CSV file in a known directory (e.g., D:\PROJECTS\Capstone_Project_2\Online-Food-Delivery-Analysis\).
* The Streamlit app automatically reads the CSV using pandas.read_csv().
* Data cleaning and preprocessing are handled via the Food_Delivery_Cleaning() function:
* Missing values filled
* Outliers managed
* Feature engineering applied
* Cleaned data is then loaded into MySQL for querying and visualization in the dashboard.
## **🔄 How It Works**                     
                                                                                                        ┌───────────────────────────┐  
          ┌──────────────────────────────────┐              ┌──────────────────────────────┐            │ Feature Engineering       │
          │   Load Raw CSV Dataset           │              │ Data Cleaning & Preprocessing│            │ - Customer_Age_group      │
          │ ONINE_FOOD_DELIVERY_ANALYSIS.csv |------------> │ - Handle missing values      │----------->│ - Delivery_Performance    │ 
          │                                  |              │ - Remove outliers            │            │ - Profit_Margin_Percent   │
          └──────────────────────────────────┘              │ - Type conversion            │            │ - Peak_Hour_Indicator     │
                                                            └──────────────────────────────┘            │ - Order_day_name          │
                                                                                                        └─────────────┬─────────────┘
                                                                                                                      │
                                                                                                                      │
                                                                                                                      ▼
                                                                                                        ┌────────────────────────────┐
                                                                                                        │ Load Cleaned Data to MySQL │
                                                                                                        │ - Table: Food_Order_Details│
                                                                                                        └─────────────┬──────────────┘
                                                                                                                      │
                                                                                                                      ▼
                                                                                                        ┌────────────────────────────┐
        ┌──────────────────────────────┐                    ┌───────────────────────────┐               │ Streamlit Dashboard        │
        │ Insights & Business Decisions│                    │ Interactive Visualizations│               │ - Home Page                │
        │ - Customer behavior analysis │                    │ - Bar Charts              │               │ - Customer & Order Analysis│
        │ - Revenue optimization       │<-------------------│ - Pie Charts              │<--------------│ - Revenue & Profit Analysis│ 
        │ - Operational improvements   │                    │ - Sunburst Charts         │               │ - Delivery Performance     │  
        └──────────────────────────────┘                    │ - Area Plots              │               │ - Restaurant Performance   │   
                                                            └───────────────────────────┘               │ - Operational Insights     │
                                                                                                        └────────────────────────────┘ 

## **🎯 Use Case**
The Online Food Delivery Analysis project is designed to provide actionable insights for multiple stakeholders in the online food delivery ecosystem:

#### 1. Restaurant Owners 🍴

* Identify top-performing dishes and cuisines.
* Monitor restaurant ratings and cancellation rates.
* Optimize staffing and operations during peak hours.

#### 2. Delivery Partners 🛵

* Track average delivery times and performance ratings.
* Understand distance vs delivery time patterns to improve efficiency.
* Identify high-demand zones for better resource allocation.

#### 3. Business Analysts & Decision Makers 📊

* Analyze revenue and profit trends across cities, cuisines, and discount strategies.
* Detect patterns in customer spending and age-group behavior.
* Make data-driven decisions to maximize revenue and reduce operational inefficiencies.

#### 4. Customers 👤 (Indirect Use Case)

* Improved delivery performance and service quality.
* Better availability of popular cuisines during peak hours.
* Reduction in order cancellations and delays.

This project provides a complete end-to-end solution for improving operational efficiency, revenue growth, and customer satisfaction in the online food delivery industry.
## 🚀 Future Enhancements

The Online Food Delivery Analysis project can be further improved and extended in the following ways:

#### 1. Real-Time Data Integration ⏱️

* Connect the dashboard to live order data for real-time insights and monitoring.

#### 2. Predictive Analytics & ML Models 🤖

* Predict high-demand hours, peak order times, and potential cancellations.
* Forecast revenue trends and customer lifetime value.

#### 3. Customer Segmentation & Personalization 🎯

* Cluster customers based on order patterns, preferences, and spending.
* Provide personalized recommendations for offers and cuisines.

#### 4. Geospatial Analysis 🌐

* Integrate maps for delivery zones, distance optimization, and route planning.
* Identify high-performing areas and under-served regions.

#### 5. Enhanced Visualizations 📊

* Add interactive dashboards with drill-down capabilities.
* Implement heatmaps, scatter plots, and multi-metric comparisons.

#### 6. Integration with Other Data Sources 🔗

* Include social media trends, customer feedback, and competitor analysis.
* Combine weather, holidays, and local events to understand order fluctuations.

#### 7. Automated Reporting & Alerts ⚡

* Generate daily/weekly reports for stakeholders.
* Send alerts for unusual activity, high cancellations, or low delivery performance.
These enhancements will make the platform smarter, predictive, and more actionable, empowering restaurants and delivery services to optimize operations and maximize customer satisfaction.

## **📋 Project Overview**
> The Online Food Delivery Analysis project is designed to provide comprehensive insights into the online food delivery ecosystem. It combines data cleaning, feature engineering, and interactive visualizations to help businesses understand customer behavior, revenue patterns, delivery efficiency, and restaurant performance.

**Key highlights:**

* Centralized **MySQL database** stores cleaned historical order data spanning multiple years.
* **Streamlit dashboard** enables multi-page interactive exploration of customer, order, revenue, and operational metrics.
* Provides actionable insights for **business strategy, operational improvements, and customer engagement**.
* Covers various dimensions including age group behavior, peak hour demand, cuisine performance, delivery efficiency, and cancellation trends.
* Designed for **data-driven decision making** for restaurants, delivery partners, and online food platforms

## 📌 Author
```
Saran K
Data Analytics & Visualization Enthusiast
Capstone Project – Online Food Delivery Analysis
```
## ⭐ If You Like This Project

```
Give it a ⭐ on GitHub and feel free to fork it!
```
