import streamlit as st
import requests

# ---------- Fetch Weather Data ----------
def fetch_data(city, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    data = response.json()
    return response.status_code, data


# ---------- Streamlit UI ----------
st.set_page_config(page_title="Weather App", page_icon="🌦️", layout="centered")

# Header
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>🌤️ Modern Weather Dashboard</h1>
    <p style='text-align: center; color: gray;'>Get real-time weather updates instantly!</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# Sidebar for API Key
st.sidebar.header("⚙️ Settings")
api_key = st.sidebar.text_input("Enter OpenWeatherMap API Key (or leave blank to use default)", type="password")
if not api_key:
    api_key = "97c9591daf3cafef5382c071892bce86"  # default key

# City Input
city = st.text_input("🏙️ Enter City Name", placeholder="e.g., London, Mumbai, New York")

# Fetch Button
if st.button("🔍 Get Weather"):
    if not city:
        st.error("⚠️ Please enter a city name.")
    else:
        status, data = fetch_data(city, api_key)

        if status == 200:
            # Weather Header
            st.markdown(
                f"""
                <div style='text-align:center; padding:10px;'>
                    <h2>📍 {data['name']}, {data['sys']['country']}</h2>
                    <h3 style='color:#2196F3;'>🌡️ {data['main']['temp']} °C | {data['weather'][0]['description'].title()}</h3>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Columns Layout
            col1, col2, col3 = st.columns(3)

            # Main Info
            with col1:
                st.subheader("🌡️ Main Info")
                st.metric("Temperature", f"{data['main']['temp']} °C")
                st.metric("Feels Like", f"{data['main']['feels_like']} °C")
                st.metric("Humidity", f"{data['main']['humidity']} %")

            # Wind Info
            with col2:
                st.subheader("💨 Wind")
                st.metric("Speed", f"{data['wind']['speed']} m/s")
                st.metric("Deg", f"{data['wind'].get('deg', 'N/A')}°")

            # System Info
            with col3:
                st.subheader("🌍 System")
                st.metric("Country", data['sys']['country'])
                st.metric("Sunrise", f"{data['sys']['sunrise']}")
                st.metric("Sunset", f"{data['sys']['sunset']}")

        else:
            st.error(f"❌ Error: {data.get('message', 'Something went wrong')}")



