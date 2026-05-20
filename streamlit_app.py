# Import python packages
import streamlit as st
import pandas as pd
import os
import requests
# Import from SnowPark
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie!")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)
name_on_order = st.text_input('Name on Smoothie:', '')


# Create a database connection to Snowflake.
conn = st.connection("snowflake")

# Create a Snowpark session from the connection.
# This provides a few helpers on top of a standard Python connection.
# If you want to use a plain Snowflake connection instead, you can create
# one with conn.cursor().
session = conn.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
    ingredients_string = ''
    
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' - Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on) 
        if smoothiefroot_response.status_code == 200:
            sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
        else:
            st.write('no nutrition information found')

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order, order_filled)
                    values ('""" + ingredients_string + """','"""+ name_on_order + """','false')"""
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')


  
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order +'!', icon="✅")
