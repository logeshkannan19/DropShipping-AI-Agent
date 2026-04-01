"""
Streamlit Frontend Application

Dashboard for the DropShipping AI Agent system.
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

st.set_page_config(
    page_title="DropShipping AI Agent",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE = "http://localhost:8000"


def api_request(method, endpoint, data=None, params=None):
    """Make API request with error handling."""
    url = f"{API_BASE}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, params=params, timeout=30)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=30)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to API at {API_BASE}. Please ensure the backend is running.")
        return None
    except requests.exceptions.RequestException as e:
        st.error(f"API error: {str(e)}")
        return None


st.title("📦 DropShipping AI Agent Dashboard")
st.markdown("AI-powered autonomous dropshipping business system")


with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Go to",
        ["Overview", "Products", "Analytics", "AI Agent", "Suppliers", "Store"]
    )
    
    st.divider()
    
    st.markdown("### System Status")
    if api_request("GET", "/health"):
        st.success("✅ API Connected")
    else:
        st.error("❌ API Disconnected")


if page == "Overview":
    st.header("Business Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    analytics = api_request("GET", "/analytics")
    
    if analytics:
        with col1:
            st.metric("Total Revenue", f"${analytics['total_revenue']:,.2f}")
        with col2:
            st.metric("Total Profit", f"${analytics['total_profit']:,.2f}")
        with col3:
            st.metric("Total Sales", analytics['total_sales'])
        with col4:
            st.metric("Conversion Rate", f"{analytics.get('conversion_rate', 0):.2f}%")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Product Status")
            product_data = {
                "Status": ["Active", "Published"],
                "Count": [analytics['active_products'], analytics['published_products']]
            }
            fig = px.pie(
                product_data, 
                values="Count", 
                names="Status",
                title="Product Distribution",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Daily Revenue")
            if analytics['daily_stats']:
                df = pd.DataFrame(analytics['daily_stats'])
                fig = px.bar(
                    df, 
                    x="date", 
                    y="revenue",
                    title="Revenue by Day",
                    color="revenue",
                    color_continuous_scale="Viridis"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No daily data available")
    else:
        st.warning("Waiting for API connection...")


elif page == "Products":
    st.header("Product Management")
    
    tab1, tab2 = st.tabs(["Product List", "Add Product"])
    
    with tab1:
        products = api_request("GET", "/products?limit=100")
        
        if products and products['products']:
            df = pd.DataFrame([
                {
                    "ID": p['id'],
                    "Name": p['name'],
                    "Category": p['category'] or "N/A",
                    "Cost": f"${p['cost_price']:.2f}",
                    "Selling": f"${p['selling_price']:.2f}" if p['selling_price'] else "Not set",
                    "Rating": p['rating'] or "N/A",
                    "Demand": f"{p['demand_score']:.2f}" if p['demand_score'] else "N/A",
                    "Published": "✅" if p['is_published'] else "❌"
                }
                for p in products['products']
            ])
            
            st.dataframe(df, use_container_width=True)
            
            st.subheader("Filter Products")
            col1, col2 = st.columns(2)
            with col1:
                category_filter = st.selectbox("Category", ["All"] + list(df['Category'].unique()))
            with col2:
                published_filter = st.selectbox("Published", ["All", "Published", "Not Published"])
            
            if category_filter != "All":
                df = df[df['Category'] == category_filter]
            if published_filter == "Published":
                df = df[df['Published'] == "✅"]
            elif published_filter == "Not Published":
                df = df[df['Published'] == "❌"]
            
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No products found")
    
    with tab2:
        with st.form("add_product"):
            name = st.text_input("Product Name")
            description = st.text_area("Description")
            category = st.selectbox("Category", ["Electronics", "Home & Garden", "Fashion", "Beauty", "Sports", "Toys", "Automotive", "Health"])
            cost_price = st.number_input("Cost Price", min_value=0.0, step=0.01)
            
            submitted = st.form_submit_button("Add Product")
            
            if submitted and name and cost_price:
                result = api_request("POST", "/products", data={
                    "name": name,
                    "description": description,
                    "category": category,
                    "cost_price": cost_price
                })
                
                if result:
                    st.success(f"Product {name} added successfully!")
                    time.sleep(1)
                    st.rerun()


elif page == "Analytics":
    st.header("Business Analytics")
    
    summary = api_request("GET", "/analytics/summary")
    
    if summary:
        st.subheader("Key Metrics")
        
        metrics = summary['metrics']
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Revenue", f"${metrics['total_revenue']:,.2f}")
        with col2:
            st.metric("Total Profit", f"${metrics['total_profit']:,.2f}")
        with col3:
            st.metric("Avg Order Value", f"${metrics.get('avg_order_value', 0):.2f}")
        with col4:
            st.metric("Profit Margin", f"{metrics.get('profit_margin', 0):.1f}%")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top Products by Revenue")
            if summary['top_products']:
                top_df = pd.DataFrame(summary['top_products'])
                fig = px.bar(
                    top_df, 
                    x="name", 
                    y="revenue",
                    title="Top Products",
                    color="revenue",
                    color_continuous_scale="Blues"
                )
                fig.update_layout(xaxis_title="Product", yaxis_title="Revenue ($)")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("Category Performance")
            if summary['category_performance']:
                cat_df = pd.DataFrame(summary['category_performance'])
                fig = px.pie(
                    cat_df,
                    values="revenue",
                    names="category",
                    title="Revenue by Category",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(fig, use_container_width=True)
        
        st.divider()
        
        st.subheader("Daily Statistics")
        if summary['daily_stats']:
            daily_df = pd.DataFrame(summary['daily_stats'])
            
            fig = go.Figure()
            fig.add_trace(go.Bar(x=daily_df['date'], y=daily_df['revenue'], name="Revenue"))
            fig.add_trace(go.Scatter(x=daily_df['date'], y=daily_df['profit'], name="Profit", line=dict(color="green")))
            fig.update_layout(title="Revenue and Profit by Day", xaxis_title="Date", yaxis_title="Amount ($)")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"*Data generated at: {summary['generated_at']}*")
    else:
        st.warning("Loading analytics data...")


elif page == "AI Agent":
    st.header("AI Decision Agent")
    
    tab1, tab2, tab3 = st.tabs(["Run Agent", "Performance", "Decisions"])
    
    with tab1:
        st.subheader("Run Full AI Pipeline")
        
        with st.form("run_agent"):
            max_products = st.slider("Max Products to Analyze", 5, 50, 10)
            min_demand_score = st.slider("Min Demand Score", 0.0, 1.0, 0.5)
            auto_publish = st.checkbox("Auto-publish Selected Products", value=True)
            
            run_button = st.form_submit_button("🚀 Run Agent Pipeline")
            
            if run_button:
                with st.spinner("Running AI agent pipeline..."):
                    result = api_request("POST", "/run-agent", data={
                        "max_products": max_products,
                        "min_demand_score": min_demand_score,
                        "auto_publish": auto_publish
                    })
                
                if result:
                    st.success(f"✅ {result['message']}")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Analyzed", result['products_analyzed'])
                    with col2:
                        st.metric("Selected", result['products_selected'])
                    with col3:
                        st.metric("Published", result['products_published'])
                    with col4:
                        st.metric("Revenue Potential", f"${result['revenue_generated']:.2f}")
    
    with tab2:
        st.subheader("Agent Performance Metrics")
        
        perf = api_request("GET", "/agent/performance")
        
        if perf:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Products Analyzed", perf['products_analyzed'])
            with col2:
                st.metric("Products Selected", perf['products_selected'])
            with col3:
                st.metric("Products Published", perf['products_published'])
            
            st.subheader("Decision Breakdown")
            if perf['decision_breakdown']:
                decision_df = pd.DataFrame([
                    {"Action": k, "Count": v}
                    for k, v in perf['decision_breakdown'].items()
                ])
                fig = px.bar(decision_df, x="Action", y="Count", title="Agent Decisions", color="Count")
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Recent Agent Decisions")
        
        decisions = api_request("GET", "/agent/decisions?limit=20")
        
        if decisions and decisions.get('decisions'):
            decision_df = pd.DataFrame(decisions['decisions'])
            st.dataframe(decision_df, use_container_width=True)
        else:
            st.info("No decisions recorded yet")


elif page == "Suppliers":
    st.header("Supplier Management")
    
    suppliers = api_request("GET", "/suppliers")
    
    if suppliers and suppliers.get('suppliers'):
        for supplier in suppliers['suppliers']:
            with st.expander(f"{supplier['name']} ({supplier['supplier_id']})"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Rating", f"⭐ {supplier['rating']}")
                with col2:
                    st.metric("Shipping Time", f"{supplier['shipping_time_days']} days")
                with col3:
                    st.metric("Location", supplier['location'])
                
                st.subheader("Products from this supplier")
                products = api_request("GET", f"/suppliers/{supplier['supplier_id']}/products")
                
                if products and products.get('products'):
                    df = pd.DataFrame(products['products'])
                    st.dataframe(df[['product_id', 'name', 'cost_price', 'stock_quantity', 'supplier_rating']], use_container_width=True)
                else:
                    st.info("No products available")
    else:
        st.info("No suppliers found")


elif page == "Store":
    st.header("Store Management")
    
    tab1, tab2 = st.tabs(["Store Products", "Statistics"])
    
    with tab1:
        store_products = api_request("GET", "/store/products?limit=50")
        
        if store_products and store_products.get('products'):
            df = pd.DataFrame(store_products['products'])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No products in store")
    
    with tab2:
        stats = api_request("GET", "/store/stats")
        
        if stats:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Products", stats['total_products'])
            with col2:
                st.metric("Active Products", stats['active_products'])
            with col3:
                st.metric("Draft Products", stats['draft_products'])
            with col4:
                st.metric("Total Orders", stats['total_orders'])


st.divider()
st.markdown("---")
st.markdown("*DropShipping AI Agent v1.0.0 | Powered by FastAPI & Streamlit*")