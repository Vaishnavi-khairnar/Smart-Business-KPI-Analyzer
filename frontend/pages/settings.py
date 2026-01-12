import streamlit as st
import utils.config as config
   
def show():
       """Display settings page."""
       st.title("Settings")
       
       # API URL configuration
       api_url = st.text_input(
           "API URL", 
           value=config.get_api_url(),
           key="api_url"
       )
       
       # Save settings
       if st.button("Save Settings"):
           config.save_setting("api_url", api_url)
           st.success("Settings saved successfully!")
       
       # Display current settings
       st.write("**Current Settings:**")
       current_settings = config.get_all_settings()
       
       for key, value in current_settings.items():
           st.write(f"- {key}: {value}")