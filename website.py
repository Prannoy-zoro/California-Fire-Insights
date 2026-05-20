import pandas as pd  
import streamlit as st 
import plotly.express as px
import requests 
st.set_page_config(
    page_title="California Fire Dashboard",
    layout="wide"

)
st.title("California Wildfire Dashboard")
yr=st.selectbox("select Year",list(range(2006,2026)))
url = f"https://www.fire.ca.gov/api/sitecore/Incident/GetFiresByYear?year={yr}"
session=requests.Session()
session.headers.update({'User-Agent': 'curl/8.7.1'})
data=session.get(f"https://www.fire.ca.gov/api/sitecore/Incident/GetFiresByYear?year={yr}",
                verify=False).json()
   
df=pd.DataFrame(data)
#print(df.info())
#df.head()


#df=pd.read_csv("clean_data.csv")


st.write("Historical Fire analysis from 2006-2025")
pi=3.1415
#rad=(df['Shape__Area']/pi)**0.5
#rad_km=rad/1000

df["Started"] = pd.to_datetime(df["Started"], errors="coerce")
df["Updated"] = pd.to_datetime(df["Updated"], errors="coerce")
#df["Local Incident Number"] = pd.to_numeric(df["Local Incident Number"], errors="coerce")
avg_dur=(df["Updated"]-df["Started"]).mean()



s1,s2 = st.columns(2)

with s1:
    
    df = df.sort_values("Started")
    year_data = df[df['Started'].dt.year == yr]
    year_data["Month"]=year_data["Started"].dt.month_name()
    
    monthly = year_data.groupby("Month")["AcresBurned"].mean()
    monthly = monthly.reindex([
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
    ]).fillna(0)
    fig1=px.bar(
        
        x=monthly.index,
        y=monthly.values,
        labels={
            "x":f"Month {yr}",
            "y":"Acres Burned"
        }
    )
    fig1.update_layout(
        yaxis_title="Avg of Acres Burned "
    )
    #fig1.update_xaxes(dtick=5)
    st.plotly_chart(fig1)
    total_acres_burned=df['AcresBurned'].sum()
    st.subheader("Total Acers Burned in Calfornia")
    st.write(total_acres_burned)
    st.title("California Fire Live Incident Data")
    
    #url = f"https://www.fire.ca.gov/api/sitecore/Incident/GetFiresByYear?year={yr}"
    #data=requests.get(f"https://www.fire.ca.gov/api/sitecore/Incident/GetFiresByYear?year={yr}")
   
    #df2=pd.DataFrame(data.json())
    #st.title("This is testing of  API")
    #st.write(df2)
    st.subheader("Total Number of Fire Registered")
    st.write(len(df))   
    #min_area=df["Shape__Area"].min()
    #max_area=df["Shape__Area"].max()
    
    #st.metric("The Max Area Fire", max_area)
    #st.metric("The Min Area Fire", min_area)


with s2:
    burned_lessthen= df[df["AcresBurned"]>50000]
    sum_burned_less=len(burned_lessthen)
    st.subheader("Acers Burned More Then 50000 Acers of land in California")
    st.write(sum_burned_less)
    
    st.subheader("This is the Average Duration Time of a fire Alert start and End Time")
    st.write(avg_dur)
    st.subheader("Agency and There Count of Fire Cases")
    agency=df['AdminUnit'].value_counts()
    pie_data=agency.head(10)
    fig2 = px.pie(
        pie_data,
        values=pie_data.values,
        names=pie_data.index
    )
    
    st.plotly_chart(fig2)




    
