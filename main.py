import streamlit as st
import streamlit_authenticator as stauth
from dotenv import load_dotenv
import os 
from azure.data.tables import TableServiceClient



load_dotenv()
login_link = os.getenv("LOGIN_LINK")

with st.form("Register"):
   st.title("Sign up for Calorie Counter")
   col1,col2 = st.columns([1,1])
   with col1:
      first_name = st.text_input("First name*")
   with col2:
      last_name = st.text_input("Last name*")
   username = st.text_input("Username*")
   email = st.text_input("Email (in case you need to reset your password)*")
   pw = st.text_input("Password*", type="password")
   pw = stauth.Hasher([pw]).generate()

   # Every form must have a submit button.
   submitted = st.form_submit_button("Register")
   if submitted:
      if username != "" and last_name != "" and first_name != "" and email!="" and pw != "":
         connection_string = os.getenv("CONNECTION_STRING")
         service = TableServiceClient.from_connection_string(conn_str=connection_string)
         new_entity = {
            u'PartitionKey': first_name,
            u'RowKey': last_name,
            u'email': email,
            u'hashed_password': pw[0],
            u'username': username}
         table_client = service.get_table_client(table_name="userdetails")
         entity = table_client.create_entity(entity=new_entity)
         st.markdown(f"Congrats {first_name} for signing up! Login [here]({login_link})")
      else:
         st.error(f":red[Registration failed. Please fill in all required fields.]")
