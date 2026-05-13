import streamlit as st
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Custom Smoothie Order Form :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your smoothie will be:", name_on_order)

session = st.connection("snowflake").session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
ingredients_list = st.multiselect("Choose up to 5 ingredients:", my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string = ' '.join(ingredients_list)
    st.write(ingredients_string)

    my_insert_stmt = """
    INSERT INTO smoothies.public.orders (name_on_order, ingredients)
    VALUES (?, ?)
"""

    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt, params=[name_on_order, ingredients_string]).collect()
        st.success("Your Smoothie is ordered, " + name_on_order + "!", icon="✅")
