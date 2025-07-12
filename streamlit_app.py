# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests




# Write directly to the app
st.title(f"Customize your smoothie:cup_with_straw:")
st.write(
  """Choose the fruits you want in your
  **Smoothie:**:cup_with_straw:
  """
)

cxn=st.connection("snowflake")
session = cxn.session()
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/all")

name_on_order=st.text_input("Name on Smoothie")

ingirdent_list=st.multiselect('Choose upto 5 ingredents', smoothiefroot_response[3], max_selections=5)
ssf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

if ingirdent_list:
    #st.text(ingirdent_list)

    ingredients_string=''

    for fruit_chosen in  ingirdent_list: 
      ingredients_string+= fruit_chosen
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/all")
      ssf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    

      my_insert_stmt = """ insert into smoothies.public.orders(Ingredients,NAME_ON_ORDER)
                values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
      st.write(my_insert_stmt)
        
      time_to_insert=st.button('Submit Order')
      sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=TRUE)
    
      #st.write(my_insert_stmt)
      if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Hi,'+name_on_order+',Your Smoothie is ordered!', icon="✅")

    
