import streamlit as st
from graph_data import karachi_graph, heuristic
from a_star import a_star_search
import folium
from streamlit_folium import st_folium
from location_coords import location_coords

st.set_page_config(page_title="Commute Planner (KHI-based)", page_icon="🧭", layout="centered")

# Custom Header
st.markdown("""
    <h1 style='text-align: center; color: #1f77b4;'>🧭 Commute Planner (KHI-based)</h1>
    <p style='text-align: center; font-size: 18px; color: #FFFFFF;'>
        🚦 Plan your route across Karachi using smart A* Search – find the best path with estimated time & distance!
    </p>
""", unsafe_allow_html=True)

st.markdown("---")

locations = list(karachi_graph.keys())

# Select inputs
st.subheader("🔍 Choose Your Route")
col1, col2 = st.columns(2)
with col1:
    source = st.selectbox("📍 From:", locations, key="source")
with col2:
    destination = st.selectbox("🏁 To:", locations, index=locations.index("DHA"), key="destination")

st.markdown("")

# Init session state
if "path" not in st.session_state:
    st.session_state.path = None
    st.session_state.total_distance = 0
    st.session_state.est_time = 0

# Button logic
if st.button("🚀 Plan My Commute"):
    if source == destination:
        st.warning("⚠️ Source and destination can't be the same!")
        st.session_state.path = None
    else:
        path = a_star_search(karachi_graph, source, destination, heuristic)
        if path:
            st.session_state.path = path
            st.session_state.total_distance = sum(karachi_graph[path[i]][path[i+1]] for i in range(len(path)-1))
            st.session_state.est_time = st.session_state.total_distance / 30 * 60  # assuming 30 km/h
        else:
            st.error("❌ No route found between these areas.")
            st.session_state.path = None

# If a path was found previously, show everything
if st.session_state.path:
    path = st.session_state.path

    st.success("✅ Route Found!")

    st.markdown(f"""
    <div style='background-color: #000000; padding: 15px; border-radius: 10px; margin-top: 10px;'>
        <h4 style='color: #1a73e8;'>🛣️ Best Route:</h4>
        <p style='font-size: 18px;'>{" → ".join(path)}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background-color: #000000; padding: 15px; border-radius: 10px; margin-top: 20px;'>
        <p style='font-size: 16px;'>📏 <b>Total Distance:</b> {st.session_state.total_distance} km</p>
        <p style='font-size: 16px;'>⏱️ <b>Estimated Time:</b> {int(st.session_state.est_time)} minutes</p>
    </div>
    """, unsafe_allow_html=True)

    # Show map
    st.subheader("🗺️ Route Map")

    coords = [location_coords[loc] for loc in path if loc in location_coords]
    avg_lat = sum(lat for lat, lon in coords) / len(coords)
    avg_lon = sum(lon for lat, lon in coords) / len(coords)

    m = folium.Map(location=(avg_lat, avg_lon), zoom_start=12)

    for i in range(len(coords) - 1):
        folium.PolyLine([coords[i], coords[i + 1]], color="blue", weight=5).add_to(m)

    for i, loc in enumerate(path):
        if loc in location_coords:
            folium.Marker(
                location_coords[loc],
                popup=loc,
                tooltip=f"{i+1}. {loc}",
                icon=folium.Icon(color="green" if i == 0 else "red" if i == len(path)-1 else "blue")
            ).add_to(m)

    st_folium(m, width=700, height=500)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Made by MRK</p>", unsafe_allow_html=True)
