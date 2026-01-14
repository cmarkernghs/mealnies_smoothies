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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe,use_container_width=True)
#st.stop

#Convert the Snowpark dataframe to a Pandas Dataframe wso we can use the LOC function
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop

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

        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,  ' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        #ingredients_string += ', '
        smoothiefroot_response = requests.get("f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df =  st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                values('""" + ingredients_string + """', '"""+name_on_order+ ''"')"""
    time_to_insert =  st.button('Submit Order'
                                ,help="Don't click until you've chosen all your fruits!"
                               )
    st.write(my_insert_stmt)

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success("""Your Smoothie is ordered, """+ name_on_order +"""!""", icon="✅")



