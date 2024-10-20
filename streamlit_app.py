# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas


# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """)

#import streamlit as st

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

cnx=st.connection("snowflake")
session=cnx.session()

#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',my_dataframe,max_selections=5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen+' '
        st.subheader(fruit_chosen + 'Nutrition information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"  + fruit_chosen)
        fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        #fruityvice_normalized=pandas.json_normalize(fruityvice_response.json())
    st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+ """')"""
    
    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button('Submit Order')
    
    #if ingredients_string:
    if time_to_insert:
      session.sql(my_insert_stmt).collect()
      st.success('Your Smoothie is ordered,'+name_on_order+'!')
