import json, streamlit as st
from ai_processing import categorise_transaction
from csv_processing import csv_data_extraction, load_settings
from database import initialise_database, add_member, get_members

initialise_database()

def setup_screen():
    settings = load_settings()
    
    st.title("Welcome to Household Audit")
    household_name = st.text_input("Please enter household name:")
     
    if "member_count" not in st.session_state:
        st.session_state.member_count = 1
        
    members = []
    for i in range(st.session_state.member_count):
        name = st.text_input(f"Member {i + 1} name:", key=f"member_{i}")
        members.append(name)
        
    if st.button("+", on_click=lambda: st.session_state.update(member_count=st.session_state.member_count + 1)):
        pass   
    
    if st.button("Next"):
        settings["household_name"] = household_name
        settings["members"] = members
        with open("config/settings.json", "w") as f:
            json.dump(settings, f, indent=4)
        for member in members:
            add_member(member)
        st.success("Household Profile Created")

def first_time_user():
    settings = load_settings()
    if settings["household_name"] == "":
        setup_screen()
    #else:
        #continue to main screen

first_time_user()