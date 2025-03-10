import streamlit as st
import pandas as pd
import plotly.express as px  

# Load the dataset
df = pd.read_csv('Airbnb_Open_Data.csv', low_memory=False)

# Clean 'price' column
df['price'] = df['price'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
df['price'] = pd.to_numeric(df['price'], errors='coerce')
df['price'].fillna(0, inplace=True)

# Rename "long" to "longitude" for Streamlit map
if "long" in df.columns:
    df.rename(columns={"long": "longitude"}, inplace=True)

# Min & Max Price for Slider
min_price = int(df['price'].min())
max_price = int(df['price'].max())

def main():
    st.set_page_config(page_title="Airbnb Data Dashboard", layout="wide")  
    st.title("🏡 Airbnb Insights Dashboard")
    
    # Sidebar Filters
    st.sidebar.header("🔍 Filters")
    price_range = st.sidebar.slider("Select Price Range", min_price, max_price, (min_price, max_price))
    
    if 'room type' in df.columns:
        room_types = st.sidebar.multiselect("Select Room Type", df['room type'].dropna().unique(), default=df['room type'].dropna().unique())
    else:
        room_types = []
    
    # Filter Data
    filtered_df = df[(df['price'] >= price_range[0]) & (df['price'] <= price_range[1])]
    if room_types:
        filtered_df = filtered_df[filtered_df['room type'].isin(room_types)]
    
    # KPIs
    total_listings = len(filtered_df)
    avg_price = round(filtered_df['price'].mean(), 2)
    
    kpi1, kpi2 = st.columns(2)
    kpi1.metric("🏠 Total Listings", total_listings)
    kpi2.metric("💰 Avg. Price", f"${avg_price}")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 💰 Price Distribution")
        fig_price = px.histogram(filtered_df, x="price", nbins=50, title="Distribution of Airbnb Prices", color_discrete_sequence=['#FF5733'])
        st.plotly_chart(fig_price, use_container_width=True)
    
    with col2:
        if 'room type' in df.columns:
            st.write("### 🏠 Room Type Breakdown")
            fig_room_type = px.pie(filtered_df, names='room type', title="Room Type Distribution", color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_room_type, use_container_width=True)
    
    # Map Visualization
    if "lat" in df.columns and "longitude" in df.columns:
        st.write("### 🗺 Airbnb Listings Map")
        filtered_map_df = filtered_df.dropna(subset=['lat', 'longitude'])
        if not filtered_map_df.empty:
            st.map(filtered_map_df[['lat', 'longitude']])
        else:
            st.warning("No valid latitude/longitude data available.")
    
    # Show Dataset at the Bottom
    st.write("### 📊 Dataset Sample")
    st.dataframe(filtered_df)
    
if __name__ == "__main__":
    main()
