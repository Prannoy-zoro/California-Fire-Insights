import pandas as pd 
import matplotlib.pyplot as plt 
import streamlit as st 
import plotly.express as px
import requests 

df=pd.read_csv("clean_data.csv")
st.set_page_config(
    page_title="California Fire Dashboard",
    layout="wide"

)
st.title("California Wildfire Dashboard")
st.write("Historical Fire analysis from 2006-2025")
pi=3.1415
rad=(df['Shape__Area']/pi)**0.5
rad_km=rad/1000

df["Alarm Date"] = pd.to_datetime(df["Alarm Date"], errors="coerce")
df["Containment Date"] = pd.to_datetime(df["Containment Date"], errors="coerce")
df["Local Incident Number"] = pd.to_numeric(df["Local Incident Number"], errors="coerce")
avg_dur=(df["Containment Date"]-df["Alarm Date"]).mean()



s1,s2 = st.columns(2)

with s1:
    
    yr=st.selectbox("select Year",list(range(2006,2026)))
    year_data = df[df['Alarm Date'].dt.year == yr]
    year_data["Month"]=year_data["Alarm Date"].dt.month_name()
    monthly = year_data.groupby("Month")["GIS Calculated Acres"].sum()
    fig1=px.histogram(
        
        x=monthly.index,
        y=monthly.values,
        labels={
            "x":f"Month  {yr}",
            "y":"Acers Burned"
        }
    )
    #fig1.update_xaxes(dtick=5)
    st.plotly_chart(fig1)
    total_aceres_burned=df['GIS Calculated Acres'].sum()
    st.subheader("Total Acers Burned in Calfornia")
    st.write(total_aceres_burned)
    st.title("California Fire Live Incident Data")
    
    #url = f"https://www.fire.ca.gov/api/sitecore/Incident/GetFiresByYear?year={yr}"
    #data=requests.get(f"https://www.fire.ca.gov/api/sitecore/Incident/GetFiresByYear?year={yr}")
   
    #df2=pd.DataFrame(data)
    #st.title("This is testing of  API")
    #st.write(df2)
    st.subheader("Total Number of Fire Registered")
    st.write(len(df))   
    min_area=df["Shape__Area"].min()
    max_area=df["Shape__Area"].max()
    
    st.metric("The Max Area Fire", max_area)
    st.metric("The Min Area Fire", min_area)


with s2:
    burned_lessthen= df[df["GIS Calculated Acres"]>50000]
    sum_burned_less=len(burned_lessthen)
    st.subheader("Acers Burned More Then 50000 Acers of land in California")
    st.write(sum_burned_less)
    
    st.subheader("This is the Average Duration Time of a fire Alert start and End Time")
    st.write(avg_dur)
    st.subheader("Agency and There Count of Fire Cases")
    agency=df['Agency'].value_counts()
    fig2 = px.pie(
        agency,
        values=agency.values,
        names=agency.index
    )
    
    st.plotly_chart(fig2)




    
