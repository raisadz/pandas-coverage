import streamlit as st

# Create a sidebar on the right side of the screen
sidebar = st.sidebar

# Add a dropdown button to the sidebar
selected_line = sidebar.selectbox("Select a line:", ["line 1", "line 2", "line 3"])

# Display output in the sidebar
sidebar.markdown("You selected: " + selected_line)
