# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie
  """
)

name_on_order = st.text_input('Name on Smoothie:', help='Use your full name')
st.write('The name on your smoothie will be',name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe,use_container_width=True)

ingredients_list = st. multiselect(
    'Chose up to 5 ingredients:'
    , my_dataframe
    , max_selections=5
)
if ingredients_list:
   # st.write(ingredients_list)
   # st.text(ingredients_list)

    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        #ingredients_string += ', '

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values('""" + ingredients_string + """', '"""+name_on_order+ ''"')"""
    time_to_insert =  st.button('Submit Order'
                                ,help="Don't click until you've chosen all your fruits!"
                               )
    st.write(my_insert_stmt)

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("""Your Smoothie is ordered, """+ name_on_order +"""!""", icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
# st.text(smoothiefroot_response.json())
sf_df =  st.dataframe(data=smoothiefroot_response,json().use_container_width=True)

