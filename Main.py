import pandas as pd
import plotly.express as px
import numpy as np
from sqlalchemy import create_engine,text
import mysql.connector
import streamlit as st 
import plotly.graph_objects as go

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Online Food Delivery Analysis",
    page_icon= "🍔",
    layout="wide"
)

st.title("🚚 Online Food Delivery Analysis 🍔")

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = "home"

# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

engine = create_engine("mysql+mysqlconnector://root:0007@localhost")

with engine.connect() as conn:
    conn.execute(text("CREATE DATABASE IF NOT EXISTS Online_Food_Delivery"))
    conn.commit()

db_engine = create_engine("mysql+mysqlconnector://root:0007@localhost/Online_Food_Delivery")

# --------------------------------------------------
# CREATE TABLES
# --------------------------------------------------

with db_engine.connect() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS Food_Order_Details(
            Order_Id VARCHAR(50) PRIMARY KEY,
            Customer_ID VARCHAR(50),
            Customer_Age INT,
            Customer_Gender ENUM('Male','Female','Other'),
            City VARCHAR(50),
            Area VARCHAR(50),
            Restaurant_ID VARCHAR(50),
            Restaurant_Name VARCHAR(50),
            Cuisine_Type VARCHAR(50),
            Order_Date DATE NOT NULL,
            Order_Time TIME NOT NULL,
            Delivery_Time_Min INT,
            Distance_km DECIMAL(10,2),
            Order_Value DECIMAL(10,2) NOT NULL,
            Discount_Applied DECIMAL(10,2) DEFAULT 0,
            Final_Amount DECIMAL(10,2) NOT NULL,
            Payment_Mode VARCHAR(15),
            Order_Status ENUM('Delivered','Cancelled') NOT NULL,
            Cancellation_Reason VARCHAR(50),
            Delivery_Partner_ID VARCHAR(50),
            Delivery_Rating INT,
            Restaurant_Rating DECIMAL(3,2),
            Order_Day ENUM('Weekday','Weekend'),
            Peak_Hour TINYINT(1),
            Profit_Margin DECIMAL(10,2),
            Customer_Age_group ENUM('Youth','Adults'),
            Delivery_Performance ENUM('Good','Moderate','Worst'),
            Profit_Margin_Percent DECIMAL(10,2),
            Peak_Hour_Indicator ENUM('High','Low'),
            Order_day_name VARCHAR(15)
        )
    """))
    conn.commit()



def Food_Delivery_Cleaning(food_df):
    food_df.dropna(subset="Order_Date",inplace=True)
    Replace_value = {"City":"Hyderabad",
                     "Cuisine_Type":"Indian",
                     "Payment_Mode" : "Card",
                     "Customer_Gender" : "Other",
                     "Peak_Hour":"False",
                     "Order_Time" :"0:00",
                     "Area" : "South",
                     "Delivery_Rating" : food_df['Delivery_Rating'].median(),
                     "Discount_Applied" : food_df['Discount_Applied'].median()}
    for key, value in Replace_value.items():
        food_df[key].fillna(value,inplace=True)
        
    Q1 = np.percentile(food_df['Discount_Applied'],25)
    Q2 = np.percentile(food_df['Discount_Applied'],50)
    Q3 = np.percentile(food_df['Discount_Applied'],75)
    
    IQR = Q3 - Q1
    
    upper_bound = Q3 + (1.5*IQR)
    lower_bound = Q1 - (1.5*IQR)
    
    food_df['Discount_Applied'] = food_df['Discount_Applied'].clip(lower_bound, upper_bound)
    
    food_df['Customer_Age']=food_df.groupby(["Customer_Gender","Area"])['Customer_Age'].transform(lambda x: x.fillna(x.median()))
    
    food_df['Order_Value']=food_df.groupby(["City","Area","Cuisine_Type"])['Order_Value'].transform(lambda x: x.fillna(x.median()))
    
    food_df['Final_Amount'] = food_df['Order_Value'] - food_df['Discount_Applied']
    
    food_df.loc[(food_df["Order_Status"] == "Delivered") &
                (food_df["Cancellation_Reason"].isnull()),
                "Cancellation_Reason"
                ] = "No Cancellation"
    food_df.loc[(food_df["Order_Status"] == "Cancelled") &
                (food_df["Cancellation_Reason"].isnull()),
                "Cancellation_Reason"
                ] = "Not Mentioned"
    
    food_df["Delivery_Time_Min"] = food_df.groupby("Delivery_Rating")['Delivery_Time_Min'].transform(lambda x: x.fillna(x.median()))
    
    food_df['Distance_km'] = food_df.groupby(['Delivery_Time_Min','Delivery_Rating'])['Distance_km'].transform(lambda x: x.fillna(x.median()))
    
    food_df[["Customer_Age","Delivery_Time_Min","Delivery_Rating"]]=food_df[["Customer_Age","Delivery_Time_Min","Delivery_Rating"]].astype("int")
    
    food_df['Order_Date']=pd.to_datetime(food_df['Order_Date'])
    
    food_df['Peak_Hour'] = food_df['Peak_Hour'].astype("bool")
    
    food_df['Order_Time'] = pd.to_datetime(food_df['Order_Time']).dt.time
    
    # Feature Engineering
     
    food_df["Customer_Age_group"] = food_df['Customer_Age'].apply(lambda x : "Youth" if x>15 and x<24 else "Adults")
    
    food_df["Delivery_Performance"] = food_df["Delivery_Rating"].apply(lambda x: "Good" 
                                                                       if x >= 4 else "Moderate" 
                                                                       if x >= 2 else "Worst")
    food_df['Profit_Margin_Percent'] = food_df['Profit_Margin']*100
    
    food_df['Peak_Hour_Indicator'] = food_df['Peak_Hour'].apply(lambda x : "High" if x==True else "Low")
    
    food_df['Order_day_name'] = food_df['Order_Date'].dt.day_name()

    return food_df

@st.cache_data
def load_data():
    df = pd.read_csv(r"D:\PROJECTS\Capstone_Project_2\Online-Food-Delivery-Analysis\ONINE_FOOD_DELIVERY_ANALYSIS.csv")
    return df

if st.session_state.page == "home":

    with db_engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM Food_Order_Details"))
        count = result.scalar()

    query = """SELECT * FROM Food_Order_Details"""

    if count == 0:
        with st.spinner("Loading and inserting data..."):
            food_df = Food_Delivery_Cleaning(load_data())
            food_df.to_sql(
                "Food_Order_Details",
                db_engine,
                if_exists="append",
                index=False
            )

        st.success("✅ Data Inserted Successfully")

        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        # 🔹 Show Total Rows
        st.info(f"🗂️ Total Records in Table From 2012 to 2022: {len(df)}")

    else:
        st.warning("🚨 Data Already Inserted")

        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        # 🔹 Show Total Rows
        st.info(f"🗂️ Total Records in Table From 2012 to 2022: {count}")

    if st.button("🔎 Analysis Page"):
        st.session_state.page = "Analysis"
        st.rerun()

# --------------------------------------------------
# ANALYSIS PAGE
# --------------------------------------------------

elif st.session_state.page == "Analysis":

    st.subheader("Online Food Delivery Analysis: Data-Driven Business Insights")

    st.markdown("""
<style>

/* Button size */
div.stButton > button {
    height: 150px;
    width: 260px;
    border-radius: 15px;
}

/* 🔥 Target inner text */
div.stButton > button p {
    font-size: 22px !important;
    font-weight: bold!important;
}

/* Normal background */
div.stButton > button {
    background: linear-gradient(135deg, #ffffff, #e3f2fd);
    padding: 9px 15px;
    transition: all 0.3s ease-in-out;
}

/* Hover effect */
div.stButton > button:hover {
    background: linear-gradient(
        135deg,
        rgba(230,230,250,0.6),
        rgba(173,216,230,0.45)
    );
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    color: red;
    border-color: blue;
    transform: scale(1.05);
    box-shadow: 0px 0px 8px #1e90ff;
}

</style>
""", unsafe_allow_html=True)
    
    col1, col2, col3,col4,col5 = st.columns([1,2,2,2,1])
    with col2:
        if st.button("👤Customer & 🛎️ Order Analysis") :
            st.session_state.page = "Customer & Order Analysis"
            st.rerun()
    with col2:
        if st.button("💸Revenue & Profit Analysis") :
            st.session_state.page = "Revenue & Profit Analysis"
            st.rerun()
    with col3:
        if st.button(" 🛵 Delivery Performance") :
            st.session_state.page = "Delivery Performance" 
            st.rerun()
    with col3:
        if st.button("🍽️ Restaurant Performance") :
            st.session_state.page = "Restaurant Performance"
            st.rerun()
    with col4:
        if st.button("🛠️ Operational Insights"):
           st.session_state.page = "Operational Insights"
           st.rerun()
        if st.button("🔙 Back to Home"):
            st.session_state.page = "home"
            st.rerun()

# --------------------------------------------------
# Customer & Order Analysis PAGE
# --------------------------------------------------
elif st.session_state.page == "Customer & Order Analysis":

    st.header("👤Customer & 🛎️ Order Analysis")

    topic = st.selectbox(
    "Select Analysis",
    [
        "Select Analysis",
        "Top-spending customers",
        "Age Group vs Order value",
        "Weekend vs Weekday Order patterns"
    ])
    if topic == "Select Analysis":
        st.info("👆 Please select a Analysis")
        query = """SELECT Order_Id,Customer_ID,Customer_Age,Customer_Gender,City,Area,Order_Date,Order_Value,
    Discount_Applied,Final_Amount,Order_day_name FROM food_order_details;"""
        df = pd.read_sql(query,db_engine)
        st.dataframe(df,use_container_width=True)
    
    explanation = None
    if topic == "Top-spending customers":
        st.subheader("🔝Top Spending Customers 👤")
        query = """ 
        select Customer_ID,
        sum(Order_Value) as Total_spent
        from food_order_details
        group by Customer_ID
        order by Total_spent desc
        limit 10;
        """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        fig = px.histogram(data_frame=df,x="Customer_ID",y="Total_spent",color="Customer_ID",title="👨🏻‍💼Customer VS Total Spent🔢")
        fig.update_layout(title_x=0.5,title_font=dict(size=30))
        fig.update_layout(title_x=0.4,
                          hoverlabel=dict(
                              bgcolor="#57F782",   # Background color
                              font_size=14,
                              font_color="black"))

        st.plotly_chart(fig,use_container_width=True)
        explanation = "Customer ID 'CUST5267' is identified as the top Spending customer, indicating strong purchase frequency and high order values."

    elif topic == "Age Group vs Order value":
        st.subheader("Age Group vs Order value")
        query = """
        select Customer_Age_group,
        count(*) as Total_orders,
        sum(Order_Value) as Total_revenue,
        sum(Final_Amount) as Total_order_value
        from food_order_details
        group by Customer_Age_group
        order by Total_order_value desc;
        """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        fig1 = px.bar(data_frame=df,x="Customer_Age_group",y="Total_order_value",title=" 👨🏻‍💼Customer Age Group VS Total Order Value"
                      ,color="Customer_Age_group",
                      color_discrete_map={"Adults":"#EDB7CD","Youth":"#FC4848"})
        fig1.update_layout(title_x=0.2,title_font=dict(size=25),
                          hoverlabel=dict(
                              bgcolor="#57F782",
                              font_color="black"))
        fig2 = px.pie(data_frame=df,values="Total_orders",names="Customer_Age_group",
                      title="🤵🏻Customer Age Group VS Total Orders 📦",color="Customer_Age_group",
                      color_discrete_map={"Adults":"#B7CBED","Youth":"#9F57F7"})
        fig2.update_layout(title_x=0.1,title_font=dict(size=25),
                          hoverlabel=dict(
                              bgcolor="#57F782",
                              font_color="black"))
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        col1,col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1,use_container_width=False)
        with col2:
            st.plotly_chart(fig2,use_container_width=False)
        explanation = """The comparison of total orders and total order value across age groups shows that the Adult segment leads in both metrics. This suggests that adults contribute the highest order volume and revenue compared to the Youth segment."""

    elif topic == "Weekend vs Weekday Order patterns":
        st.subheader("📆 Weekend vs Weekday Order patterns")
        query = """
        select Order_Day, Order_day_name,
        count(*) as Total_orders,
        sum(Order_Value) as Total_Revenue,
        avg(Order_Value) as avg_order_value
        from food_order_details
        group by Order_Day, Order_day_name;
        """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        fig1 = px.bar(data_frame=df,x="Order_Day",y="Total_orders",title="📆 Order Week vs Total Orders",color="Order_day_name")
        fig1.update_layout(title_x=0.3,title_font=dict(size=25),
                          hoverlabel=dict(
                              bgcolor="#57F782",
                              font_color="black"))
        fig2 = px.pie(data_frame=df,values="Total_Revenue",names="Order_day_name",
                      title="Order Day VS Total Revenue 💸",color="Order_day_name")
        fig2.update_layout(title_x=0.2,title_font=dict(size=25),
                          hoverlabel=dict(
                              bgcolor="#57F782",
                              font_color="black"))
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        col1,col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1,use_container_width=False)
        with col2:
            st.plotly_chart(fig2,use_container_width=False)
        explanation = """The analysis indicates that order volume is significantly higher on weekdays than on weekends. As a result, restaurants are likely to earn more revenue during weekdays."""
    if explanation:
        st.subheader("📝 Insights")
        st.info(explanation)

    if st.button("🔙Back to Analysis"):
        st.session_state.page = "Analysis"
        st.rerun()
# --------------------------------------------------
# Revenue & Profit Analysis"PAGE
# --------------------------------------------------

elif st.session_state.page == "Revenue & Profit Analysis" :

    st.subheader("💸 Revenue & 💰Profit Analysis")

    topic = st.selectbox(
    "Select Analysis",
    [
        "Select Analysis",
        "Monthly revenue trends",
        "Impact of discounts on profit",
        "High-revenue cities and cuisines"
    ])

    if topic == "Select Analysis":
        st.info("👆 Please select a Analysis")
        query = """select Order_Id,City,Cuisine_Type,Order_Date,Order_Value,Discount_Applied,
        Final_Amount,Payment_Mode,Profit_Margin,Profit_Margin_Percent from food_order_details;"""
        df = pd.read_sql(query,db_engine)
        st.dataframe(df,use_container_width=True)

    explanation = None
    if topic == "Monthly revenue trends":
        st.subheader("🗓 Monthly Revenue Trends📈")
        query = """ 
        SELECT MONTH(Order_Date) as Month,
        COUNT(*) as Total_orders,
        SUM(Final_Amount) as Total_revenue,
        round(avg(Final_Amount),2) as Avg_Order_Value
        FROM food_order_details
        GROUP BY Month
        ORDER BY Month ASC;
        """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        fig = px.area(data_frame=df,x="Month",y="Total_revenue",markers="circle",title="🗓 Month Vs Total Revenue💲")
        fig.update_layout(title_x=0.45,title_font=dict(size=30),
                          width=500,     # increase width
                          height=550  ,    # increase height
                              hoverlabel=dict(
                              bgcolor="#FA5E5E",
                              font_size=14,
                              font_color="White"))
        st.plotly_chart(fig,use_container_width=True)
        explanation = "The monthly trend analysis shows that July recorded the maximum order volume as well as the highest revenue among all months."

    elif topic == "Impact of discounts on profit":
        st.subheader("🏷️Impact of Discounts on Profit")
        query = """
        SELECT 
        Discount_Applied,
        COUNT(*) AS Total_orders,
        SUM(Final_Amount) AS Total_Revenue,
        AVG(Order_Value) AS Avg_order_value,
        AVG(Profit_Margin) AS Avg_profit_margin,
        AVG(Profit_Margin_Percent) AS Avg_profit_margin_percent
        FROM food_order_details
        GROUP BY Discount_Applied
        ORDER BY Discount_Applied ASC;
        """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        fig = px.line(data_frame=df,x="Discount_Applied",y="Avg_profit_margin_percent",markers="circle",
                      title="🏷️Discount Vs Avg Profit Percent")
        fig.update_layout(title_x=0.4,title_font=dict(size=30),
                          width=500,     # increase width
                          height=550  ,    # increase height
                              hoverlabel=dict(
                              bgcolor="#FA5E5E",
                              font_size=14,
                              font_color="White"))
        st.plotly_chart(fig,use_container_width=True)
        explanation = """The analysis indicates that profit margin remains relatively stable across different discount levels. Both 0% discount and higher discount percentages show approximately the same profit margin, " \
        suggesting that discount strategies are not significantly influencing overall profitability."""

    elif topic == "High-revenue cities and cuisines":
        st.subheader("💹 High Revenue Cities and Cuisines")
        query = """
        select City,
        Cuisine_Type,
        sum(Final_Amount) as Total_Revenue
        from food_order_details 
        group by City, Cuisine_Type
        order by Total_Revenue desc;
        """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        fig1 = px.histogram(data_frame=df,x="City",y="Total_Revenue",color="City",
                      title="🌆City Vs Total Revenue")
        fig1.update_layout(title_x=0.3,title_font=dict(size=30),
                          width=700,     # increase width
                          height=550,    # increase height
                              hoverlabel=dict(
                              bgcolor="#FA5E5E",
                              font_size=14,
                              font_color="White"))
        fig2 = px.pie(data_frame=df,names="Cuisine_Type",values="Total_Revenue",
                      title="Cuisine Vs Total Revenue 💵")
        fig2.update_layout(title_x=0.2,title_font=dict(size=30),
                          width=700,     # increase width
                          height=550,    # increase height
                              hoverlabel=dict(
                              bgcolor="#FA5E5E",
                              font_size=14,
                              font_color="White"))
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        col1,col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1,use_container_width=False)
        with col2:
            st.plotly_chart(fig2,use_container_width=False)
        explanation = """The city-wise analysis shows that Hyderabad accounts for the highest proportion of online orders. Within Hyderabad, 
        Indian cuisine represents approximately 34% of total orders, making it the leading revenue-contributing cuisine in the city."""
    if explanation:
        st.subheader("📝 Insights")
        st.info(explanation)

    if st.button("🔙Back to Analysis"):
        st.session_state.page = "Analysis"
        st.rerun()
# --------------------------------------------------
# Delivery Performance PAGE
# --------------------------------------------------
elif st.session_state.page == "Delivery Performance" :
    st.subheader("🛵💨Delivery Performance")

    topic = st.selectbox(
    "Select Analysis",
    [
        "Select Analysis",
        "Average delivery time by city",
        "Distance vs delivery delay analysis",
        "Delivery rating vs delivery time"
    ])

    if topic == "Select Analysis":
        st.info("👆 Please select a Analysis")
        query = """select Order_Id,City,Final_Amount,Order_Time,Delivery_Time_Min,
        Distance_km,Delivery_Partner_ID,Delivery_Rating,Delivery_Performance from food_order_details;"""
        df = pd.read_sql(query,db_engine)
        st.dataframe(df,use_container_width=True)
    explanation = None

    if topic == "Average delivery time by city":
        st.subheader("⚖️Average Delivery Time by City")
        query = """ 
        select City,
        avg(Delivery_Time_Min) as Avg_delivery_time
        from food_order_details
        group by City
        order by Avg_delivery_time desc;
        """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        fig = px.bar(data_frame=df,x="Avg_delivery_time",y="City",color="City",title="🏙️ City Vs Delivery Time")
        fig.update_layout(title_x=0.4,title_font=dict(size=30),
                          width=500,     # increase width
                          height=650  ,    # increase height
                              hoverlabel=dict(
                              bgcolor="#C9FA5E",
                              font_size=14,
                              font_color="black"))
        st.plotly_chart(fig,use_container_width=True)
        explanation = "The city-wise comparison indicates that delivery time remains relatively uniform across all cities, with an average delivery duration of approximately 2 hours."

    elif topic == "Distance vs delivery delay analysis":
        st.subheader("📏Distance vs 🚛 Delivery Delay Analysis ")
        query = """
        select
        case 
        when Distance_km <= 5 then  '0-5 km'
        when Distance_km <= 10 then '5-10 km'
        when Distance_km <= 15 then '10-15 km'
        when Distance_km <= 20 then '15-20 km'
        when Distance_km <= 30 then '20-30 km'
        else '30+ km'
        end as Distance_range,
        count(*) as total_orders,
        avg(Delivery_Time_Min) as Avg_delivery_time
        from food_order_details
        group by distance_range
        order by Avg_delivery_time;
        """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        fig = px.bar(data_frame=df,x="Distance_range",y="Avg_delivery_time",
                     title="Distance Range Vs 🕒 Delivery Time",color="Distance_range")
        fig.update_layout(title_x=0.4,title_font=dict(size=30),
                          width=500,     # increase width
                          height=650  ,    # increase height
                              hoverlabel=dict(
                              bgcolor="#C9FA5E",
                              font_size=14,
                              font_color="black"))
        st.plotly_chart(fig,use_container_width=True)
        explanation = "The analysis of distance against delivery time indicates that delivery duration does not significantly increase with distance. Orders within 0–5 km and those exceeding 30 km show comparable delivery times."

       
    elif topic == "Delivery rating vs delivery time":
        st.subheader("Delivery Rating vs 🕒 Delivery Time")
        query = """
        select Delivery_Rating,
        count(*) as total_orders,
        avg(Delivery_Time_Min) as Avg_delivery_time
        from food_order_details
        group by Delivery_Rating
        order by Delivery_Rating asc;
        """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)
        fig = px.area(data_frame=df,x="Delivery_Rating",y="Avg_delivery_time",
                     title="Delivery Rating Vs Delivery Time")
        fig.update_layout(title_x=0.4,title_font=dict(size=30),
                          width=500,     # increase width
                          height=650  ,    # increase height
                              hoverlabel=dict(
                              bgcolor="#C9FA5E",
                              font_size=14,
                              font_color="black"))
        st.plotly_chart(fig,use_container_width=True)
        explanation = "The comparison between delivery rating and delivery time indicates no significant variation in delivery duration across different rating levels. This suggests that delivery time alone may not be the primary factor influencing customer ratings."

    if explanation:
        st.subheader("📝 Insights")
        st.info(explanation)
    if st.button("🔙Back to Analysis"):
        st.session_state.page = "Analysis"
        st.rerun()
# --------------------------------------------------
# Restaurant Performance PAGE
# --------------------------------------------------
elif st.session_state.page == "Restaurant Performance":
    
    st.subheader("🍴Restaurant Performance")
        
    topic = st.selectbox(
    "Select Analysis",
    [
        "Select Analysis",
        "Top-rated restaurants",
        "Cancellation rate by restaurant",
        "Cuisine-wise performance"
    ])

    if topic == "Select Analysis":
        st.info("👆 Please select a Analysis")
        query = """select Order_Id,Restaurant_ID,Restaurant_Name,City,Cuisine_Type,Order_Date,Restaurant_Rating,Final_Amount,
        Cancellation_Reason,Profit_Margin,Profit_Margin_Percent from food_order_details;"""
        df = pd.read_sql(query,db_engine)
        st.dataframe(df,use_container_width=True)
    explanation = None
    if topic == "Top-rated restaurants":
        st.subheader("🔝Top Rated Restaurants")
        query = """ 
        select Restaurant_Name,
       count(*) as Total_orders,
       avg(Restaurant_Rating) as Avg_rating
       from food_order_details
       group by Restaurant_Name
       order by Avg_rating desc;
       """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        Top_10_df = df.head(10)
        fig1 = px.bar(data_frame=Top_10_df,x="Restaurant_Name",y="Avg_rating",title="🍴Restaurant Name Vs Avg Rating",color="Restaurant_Name")
        fig1.update_layout(title_x=0.2,title_font=dict(size=30),
                          width=650,     # increase width
                          height=550  ,    # increase height
                              hoverlabel=dict(
                              bgcolor="#5EFABE",
                              font_size=14,
                              font_color="black"))
        colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
        fig2 = go.Figure(data=[go.Pie(labels=Top_10_df["Restaurant_Name"],
                             values=Top_10_df["Total_orders"],hole=0.5)])
        fig2.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=colors, line=dict(color='#000000', width=2)))
        fig2.update_layout(title=dict(text="Restaurant Name VS Total Orders",x=0.5, xanchor="center"),title_font=dict(size=30),
                          width=600,     # increase width
                          height=600  ,    # increase height
                          hoverlabel=dict(
                              bgcolor="#5EFABE",   # Background color
                              font_size=14,
                              font_color="black"))
        col1,col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1,use_container_width=False)
        with col2:
            st.plotly_chart(fig2,use_container_width=False)
        explanation = "The analysis indicates that customer ratings remain relatively consistent across all restaurants, with no significant variation."


    elif topic == "Cancellation rate by restaurant":
        st.subheader("Cancellation Rate by Restaurant")
        query = """
        select Restaurant_Name,
        count(*) as total_orders,
        sum(case when Order_Status = 'Cancelled' then 1 else 0 end) as cancelled_orders,
        round(
        sum(case when Order_Status = 'Cancelled' then 1 else 0 end) * 100.0 / count(*),2
        ) as cancellation_percent
        from food_order_details
        group by Restaurant_Name
        order by cancellation_percent desc;
        """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        Top_10_df = df.head(10)

        fig = px.bar(data_frame=Top_10_df,x="Restaurant_Name",y="cancellation_percent",color="Restaurant_Name",
                           title= "Restaurant Name Vs Cancelled Orders")

        fig.update_layout(title_x=0.35,title_font=dict(size=30),
                          width=500,     # increase width
                          height=550  ,    # increase height
                              hoverlabel=dict(
                              bgcolor="#5EFABE",
                              font_size=14,
                              font_color="black"))
        st.plotly_chart(fig,use_container_width=True)
        explanation = "The analysis indicates that order cancellations are present across most restaurants. Notably, Restaurant_202 records the highest cancellation rate, approximately 22%, making it the most affected restaurant."


    elif topic == "Cuisine-wise performance":
        st.subheader("Cuisine-wise performance")
        query = """
        select Cuisine_Type,
        count(*) as Total_orders,
        sum(Final_Amount) as Total_revenue,
        avg(Final_Amount) as Avg_order_value,
        avg(Profit_Margin) as Avg_profit,
        avg(Profit_Margin_Percent) as Avg_profit_percent
        from food_order_details
        group by Cuisine_Type
        order by Avg_profit_percent desc;
        """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        fig1 = px.bar(data_frame=df,x="Cuisine_Type",y="Avg_profit_percent",title="Cuisine Type Vs Profit Percent",color="Cuisine_Type")
        fig1.update_layout(title_x=0.25,title_font=dict(size=30),
                          width=700,     # increase width
                          height=550  ,    # increase height
                              hoverlabel=dict(
                              bgcolor="#5EFABE",
                              font_size=14,
                              font_color="black"))

        fig2 = px.pie(data_frame=df,values="Total_orders",names="Cuisine_Type",hole=0.5,title="Cuisine Type Vs Total Orders")
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        fig2.update_layout(title_x=0.2,title_font=dict(size=30),
                          width=600,     # increase width
                          height=600  ,    # increase height
                          hoverlabel=dict(
                              bgcolor="#5EFABE",   # Background color
                              font_size=14,
                              font_color="black"))
        col1,col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1,use_container_width=False)
        with col2:
            st.plotly_chart(fig2,use_container_width=False)
        explanation = "The cuisine-wise analysis indicates that Indian food leads in order volume. However, Italian cuisine generates the highest profit margin percentage among all cuisine types."

    if explanation:
        st.subheader("📝 Insights")
        st.info(explanation)
    if st.button("🔙Back to Analysis"):
        st.session_state.page = "Analysis"
        st.rerun()

# --------------------------------------------------
# Operational Insights PAGE
# --------------------------------------------------
elif st.session_state.page == "Operational Insights":

    st.header("🛠️Operational Insights")

    topic = st.selectbox(
    "Select Analysis",
    [
        "Select Analysis",
        "Peak hour demand analysis",
        "Payment mode preferences",
        "Cancellation reason analysis"
    ])

    if topic == "Select Analysis":
        st.info("👆 Please select a Analysis")
        query = """select Order_Id,Order_Date,Final_Amount,Peak_Hour,
        Peak_Hour_Indicator,Payment_Mode,Cancellation_Reason from food_order_details;"""
        df = pd.read_sql(query,db_engine)
        
    explanation = None  
    if topic == "Peak hour demand analysis":
        st.subheader("⏳Peak Hour Demand Analysis")
        query = """ 
        select Peak_Hour,
        count(*) as total_orders,
        sum(Final_Amount) as total_revenue,
        avg(Final_Amount) as avg_order_value
        from food_order_details
        group by Peak_Hour
        order by total_orders desc;
        """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        fig1= px.bar(data_frame=df,
                     x="Peak_Hour",y="total_orders",color="Peak_Hour",title="⏱Peak Hour VS Total orders")
        fig1.update_layout(title_x=0.3,title_font=dict(size=30),
                          hoverlabel=dict(
                              bgcolor="#9325FB",   # Background color
                              font_size=14,
                              font_color="white"))
        fig2= px.bar(data_frame=df,
                     x="Peak_Hour",y="total_revenue",title="🕰️Peak Hour VS Total Revenue")
        fig2.update_layout(title_x=0.3,title_font=dict(size=30),
                          hoverlabel=dict(
                              bgcolor="#9325FB",   # Background color
                              font_size=14,
                              font_color="white"))
        col1,col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1,use_container_width=False)
        with col2:
            st.plotly_chart(fig2,use_container_width=False)
        explanation = "Analysis shows that peak hours drive the majority of orders and revenue, indicating that restaurants generate most of their business during these high-demand periods."
        
    elif topic == "Payment mode preferences":
        st.subheader("📲Payment Mode Preferences")
        query = """
        SELECT Payment_Mode,
        COUNT(*) AS total_orders,
        ROUND(SUM(Final_Amount), 2) AS Revenue_amount
        FROM food_order_details
        GROUP BY Payment_Mode
        ORDER BY Revenue_amount DESC;
        """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        fig1 = go.Figure(data=[go.Pie(labels=df["Payment_Mode"], values=df["total_orders"], pull=[0.1, 0, 0, 0])])
        fig1.update_traces(textposition='inside', textinfo='percent+label')
        fig1.update_layout(title=dict(text="Payment Mode VS Total Orders📦",x=0.5, xanchor="center"),title_font=dict(size=25),
                          width=600,     # increase width
                          height=500  ,    # increase height
                          hoverlabel=dict(
                              bgcolor="#9325FB",   # Background color
                              font_size=14,
                              font_color="white"))
        fig2 = px.pie(data_frame=df,values="Revenue_amount",names="Payment_Mode",
                     title="🌐Payment Mode VS Revenue Amount",hole=0.5,color_discrete_sequence=px.colors.sequential.RdBu)
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        fig2.update_layout(title_x=0.1,title_font=dict(size=25),
                          width=600,     # increase width
                          height=500  ,    # increase height
                          hoverlabel=dict(
                              bgcolor="#9325FB",   # Background color
                              font_size=14,
                              font_color="white"))
        col1,col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig1,use_container_width=False)
        with col2:
            st.plotly_chart(fig2,use_container_width=False)
        explanation = "The analysis indicates that while UPI widely available for online orders, most customers prefer to pay using cards."
    elif topic == "Cancellation reason analysis":
        st.subheader("❌Cancellation Reason Analysis")
        query = """
        select City,
        Cancellation_Reason,
        count(*) as count
        from food_order_details
        where Cancellation_Reason != "No Cancellation"
        group by Cancellation_Reason, City
        order by count desc;
        """
        df = pd.read_sql(query, db_engine)
        st.dataframe(df, use_container_width=True)

        fig = px.sunburst(df,path=["City", "Cancellation_Reason"],values="count",title="⛔Cancellation Reason Analysis by City",)
        fig.update_traces(textinfo="label+percent parent",textfont_size=15)
        fig.update_layout(title_x=0.25,title_font=dict(size=40),
                          
                          width=1200,     # increase width
                          height=800 ,    # increase height
                          hoverlabel=dict(
                              bgcolor="#9325FB",   # Background color
                              font_size=14,
                              font_color="white"))
        st.plotly_chart(fig, use_container_width=True)
        explanation = "The city generating the most orders and revenue also experiences the highest proportion of order cancellations, indicating potential operational challenges in high-demand areas."
        
    if explanation:
        st.subheader("📝 Insights")
        st.info(explanation)
    if st.button("🔙Back to Analysis"):
        st.session_state.page = "Analysis"
        st.rerun()