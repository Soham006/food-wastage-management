import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
from queries import QUERIES, PROVIDER_CONTACTS_BY_CITY

DB = "food.db"
st.set_page_config(page_title="Local Food Wastage Management", layout="wide")

def get_conn():
    return sqlite3.connect(DB, check_same_thread=False)

def run_query(sql, params=None):
    conn = get_conn()
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df

def run_action(sql, params=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(sql, params or {})
    conn.commit()
    conn.close()

st.sidebar.title("Food Wastage System")
page = st.sidebar.radio("Go to", ["Overview", "Browse & Filter Food", "Manage Listings (CRUD)", "SQL Insights", "Contact Directory"])

if page == "Overview":
    st.title("Local Food Wastage Management System")
    st.write("Connecting surplus food providers with people and NGOs in need.")
    total_listings = run_query("SELECT COUNT(*) AS n FROM food_listings")["n"][0]
    total_qty = run_query("SELECT COALESCE(SUM(Quantity),0) AS n FROM food_listings")["n"][0]
    total_providers = run_query("SELECT COUNT(*) AS n FROM providers")["n"][0]
    total_receivers = run_query("SELECT COUNT(*) AS n FROM receivers")["n"][0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Food Listings", total_listings)
    c2.metric("Total Quantity", int(total_qty))
    c3.metric("Providers", total_providers)
    c4.metric("Receivers", total_receivers)
    st.subheader("Claim status breakdown")
    status = run_query("SELECT Status, COUNT(*) AS Count FROM claims GROUP BY Status")
    if not status.empty:
        fig = px.pie(status, names="Status", values="Count", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

elif page == "Browse & Filter Food":
    st.title("Browse available food")
    cities = run_query("SELECT DISTINCT Location FROM food_listings ORDER BY Location")["Location"].dropna().tolist()
    providers = run_query("SELECT DISTINCT Provider_Type FROM food_listings ORDER BY Provider_Type")["Provider_Type"].dropna().tolist()
    food_types = run_query("SELECT DISTINCT Food_Type FROM food_listings ORDER BY Food_Type")["Food_Type"].dropna().tolist()
    meal_types = run_query("SELECT DISTINCT Meal_Type FROM food_listings ORDER BY Meal_Type")["Meal_Type"].dropna().tolist()
    c1, c2, c3, c4 = st.columns(4)
    city = c1.selectbox("City", ["All"] + cities)
    prov = c2.selectbox("Provider type", ["All"] + providers)
    ftype = c3.selectbox("Food type", ["All"] + food_types)
    meal = c4.selectbox("Meal type", ["All"] + meal_types)
    sql = "SELECT * FROM food_listings WHERE 1=1"
    params = {}
    if city != "All":
        sql += " AND Location = :city"
        params["city"] = city
    if prov != "All":
        sql += " AND Provider_Type = :prov"
        params["prov"] = prov
    if ftype != "All":
        sql += " AND Food_Type = :ftype"
        params["ftype"] = ftype
    if meal != "All":
        sql += " AND Meal_Type = :meal"
        params["meal"] = meal
    df = run_query(sql, params)
    st.write(f"**{len(df)} items found**")
    st.dataframe(df, use_container_width=True)

elif page == "Manage Listings (CRUD)":
    st.title("Manage food listings")
    action = st.radio("Action", ["Add", "Update", "Delete"], horizontal=True)
    if action == "Add":
        st.subheader("Add a new food listing")
        food_id = st.number_input("Food_ID (unique)", min_value=1, step=1)
        food_name = st.text_input("Food name")
        quantity = st.number_input("Quantity", min_value=0, step=1)
        expiry = st.date_input("Expiry date")
        provider_id = st.number_input("Provider_ID", min_value=1, step=1)
        provider_type = st.text_input("Provider type")
        location = st.text_input("Location (city)")
        food_type = st.selectbox("Food type", ["Vegetarian", "Non-Vegetarian", "Vegan"])
        meal_type = st.selectbox("Meal type", ["Breakfast", "Lunch", "Dinner", "Snacks"])
        if st.button("Add listing"):
            run_action("INSERT INTO food_listings (Food_ID, Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type, Meal_Type) VALUES (:id,:name,:qty,:exp,:pid,:ptype,:loc,:ftype,:meal)", {"id": food_id, "name": food_name, "qty": quantity, "exp": str(expiry), "pid": provider_id, "ptype": provider_type, "loc": location, "ftype": food_type, "meal": meal_type})
            st.success(f"Added {food_name}.")
    elif action == "Update":
        st.subheader("Update quantity")
        food_id = st.number_input("Food_ID to update", min_value=1, step=1)
        new_qty = st.number_input("New quantity", min_value=0, step=1)
        if st.button("Update"):
            run_action("UPDATE food_listings SET Quantity = :q WHERE Food_ID = :id", {"q": new_qty, "id": food_id})
            st.success(f"Updated listing {food_id}.")
    elif action == "Delete":
        st.subheader("Delete a listing")
        food_id = st.number_input("Food_ID to delete", min_value=1, step=1)
        if st.button("Delete"):
            run_action("DELETE FROM food_listings WHERE Food_ID = :id", {"id": food_id})
            st.success(f"Deleted listing {food_id}.")
    st.divider()
    st.caption("Current listings")
    st.dataframe(run_query("SELECT * FROM food_listings LIMIT 100"), use_container_width=True)

elif page == "SQL Insights":
    st.title("SQL queries and analysis")
    st.subheader("Contact info of providers in a city")
    city = st.text_input("Enter a city name")
    if city:
        df3 = run_query(PROVIDER_CONTACTS_BY_CITY, {"city": city})
        st.dataframe(df3, use_container_width=True)
    st.divider()
    choice = st.selectbox("Pick a query", list(QUERIES.keys()))
    df = run_query(QUERIES[choice])
    st.dataframe(df, use_container_width=True)
    if df.shape[1] == 2 and pd.api.types.is_numeric_dtype(df.iloc[:, 1]):
        fig = px.bar(df, x=df.columns[0], y=df.columns[1])
        st.plotly_chart(fig, use_container_width=True)

elif page == "Contact Directory":
    st.title("Contact directory")
    tab1, tab2 = st.tabs(["Providers", "Receivers"])
    with tab1:
        st.dataframe(run_query("SELECT Name, Type, City, Contact FROM providers"), use_container_width=True)
    with tab2:
        st.dataframe(run_query("SELECT Name, Type, City, Contact FROM receivers"), use_container_width=True)
