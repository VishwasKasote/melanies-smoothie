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
covert_tojson=smoothiefroot_response.json()
name_list = [item["name"] for item in covert_tojson if "name" in item]
name_on_order=st.text_input("Name on Smoothie")
ingirdent_list=st.multiselect('Choose upto 5 ingredents', name_list, max_selections=5)

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
ssf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

if ingirdent_list:
    #st.text(ingirdent_list)
    ingredients_string=''
    for fruit_chosen in  ingirdent_list: 
      ingredients_string+= fruit_chosen+' '
      search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
      st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      st.subheader(fruit_chosen+'Nutrition Information')
      smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruit_chosen)
      ssf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
      my_insert_stmt = """ insert into smoothies.public.orders(Ingredients,NAME_ON_ORDER)
                values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
      #st.write(my_insert_stmt)
    time_to_insert=st.button('Submit Order')
    if time_to_insert:
      session.sql(my_insert_stmt).collect()
      st.success('Hi,'+name_on_order+',Your Smoothie is ordered!', icon="✅")

    
