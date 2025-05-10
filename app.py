import streamlit as st
from agents.memory_agent import MemoryAgent
from agents.customer_agent import CustomerAgent
from agents.product_agent import ProductAgent
from agents.recommendation_agent import RecommendationAgent

# Init agents
memory = MemoryAgent()
recommender = RecommendationAgent(memory)
product_agent = ProductAgent(memory)

st.title("🛍️ Hyper-Personalized Product Recommender (Multi-Agent System)")

# Fetch customers
st.sidebar.header("Select Customer")
customers = memory.cursor.execute("SELECT customer_id, name FROM customers").fetchall()
customer_map = {f"{c[1]} ({c[0]})": c[0] for c in customers}
selected_customer_label = st.sidebar.selectbox("Customer", list(customer_map.keys()))
customer_id = customer_map[selected_customer_label]

customer_agent = CustomerAgent(customer_id, memory)

st.markdown(f"### 👤 Selected Customer: `{customer_id}`")

# Browsing simulation
st.subheader("🛒 Simulate Browsing a Product")
products = memory.get_all_products()
product_map = {f"{p[1]} - {p[0]}": p[0] for p in products}
selected_product_label = st.selectbox("Product", list(product_map.keys()))
selected_product_id = product_map[selected_product_label]

if st.button("Simulate Browsing"):
    customer_agent.browse_product(selected_product_id)
    st.success(f"Simulated browsing of product `{selected_product_id}`")

# Get recommendations
st.subheader("🤖 Get Recommendations")

# Regular Customer Recommendation button
if st.button("Get Personalized Recommendations (Regular Customer)"):
    recommendations = recommender.recommend(customer_id, selected_product_id)
    customer_agent.receive_recommendations([r['product_id'] for r in recommendations])
    st.success("Personalized recommendations generated!")
    st.write("### 🔮 Personalized Recommendations:")
    for r in recommendations:
        st.write(f"- {r['subcategory']} (`{r['product_id']}`)")


# New Customer Recommendation button
if st.button("Get Trending Recommendations (New Customer)"):
    recommendations = memory.get_trending_products()
    st.success("Trending recommendations generated!")
    st.write("### 📈 Trending Recommendations:")
    for r in recommendations:
        st.write(f"- {r['subcategory']} (`{r['product_id']}`)")


# Logs
st.subheader("📊 Logs")
if st.checkbox("Show Browsing History"):
    logs = memory.cursor.execute("SELECT * FROM browsing_history WHERE customer_id = ?", (customer_id,)).fetchall()
    st.dataframe(logs, use_container_width=True)

if st.checkbox("Show Recommendation Log"):
    rec_logs = memory.cursor.execute("SELECT * FROM recommendations_log WHERE customer_id = ?", (customer_id,)).fetchall()
    st.dataframe(rec_logs, use_container_width=True)
