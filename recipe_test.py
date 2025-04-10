import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt

# Set page configuration
st.set_page_config(
    page_title="PDQ CS Recipe Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling with PDQ brand colors
st.markdown("""
<style>
    /* PDQ Color Palette */
    :root {
        --pdq-primary: #6c2cef;
        --pdq-secondary: #884dff;
        --pdq-dark: #231434;
        --pdq-light: #f5f3ff;
        --pdq-accent: #42d9c8;
        --pdq-warning: #ff7b54;
        --pdq-background: #ffffff;
        --pdq-text: #231434;
        --pdq-text-light: #6c6684;
        --pdq-border: #e6e1f9;
    }
    
    /* Global styling */
    .main {
        background-color: var(--pdq-light);
        color: var(--pdq-text);
    }
    h1, h2, h3, h4, h5, h6 {
        color: var(--pdq-dark);
        font-weight: 600;
    }
    .stButton > button {
        background-color: var(--pdq-primary);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton > button:hover {
        background-color: var(--pdq-secondary);
    }
    
    /* Card styling */
    .recipe-card {
        background-color: white;
        border-left: 4px solid var(--pdq-primary);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 10px rgba(108, 44, 239, 0.1);
    }
    .shipping-card {
        background-color: white;
        border-left: 4px solid var(--pdq-accent);
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 2px 10px rgba(108, 44, 239, 0.1);
    }
    .metric-card {
        background-color: white;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 15px;
        box-shadow: 0 2px 10px rgba(108, 44, 239, 0.1);
        height: 100%;
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    /* Text styling */
    .highlight {
        color: var(--pdq-primary);
        font-weight: 600;
    }
    .positive {
        color: #28a745;
        font-weight: 500;
    }
    .negative {
        color: var(--pdq-warning);
        font-weight: 500;
    }
    .neutral {
        color: var(--pdq-text-light);
    }
    
    /* Alert styling */
    .success-alert {
        padding: 10px;
        background-color: #d4edda;
        color: #155724;
        border-radius: 4px;
        margin: 10px 0;
    }
    
    /* Recommendation styling */
    .recommendation-text {
        background-color: var(--pdq-light);
        border-left: 3px solid var(--pdq-primary);
        padding: 15px;
        margin: 10px 0;
        border-radius: 4px;
    }
    .top-recipe {
        border-left-color: var(--pdq-primary);
    }
    .medium-recipe {
        border-left-color: var(--pdq-secondary);
    }
    .low-recipe {
        border-left-color: var(--pdq-accent);
    }
    
    /* Tab styling */
    .stTabs {
        background-color: white;
        border-radius: 8px;
        padding: 10px;
        box-shadow: 0 2px 10px rgba(108, 44, 239, 0.1);
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 4px;
    }
    .stTabs [aria-selected="true"] {
        background-color: var(--pdq-primary);
        color: white;
    }
    
    /* Container styling */
    .tab-container {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(108, 44, 239, 0.1);
        margin-bottom: 20px;
    }
    
    /* Time period text */
    .time-period {
        font-size: 14px;
        color: var(--pdq-text-light);
        margin-top: -5px;
        margin-bottom: 20px;
    }
    
    /* Tooltip styling */
    .tooltip {
        position: relative;
        display: inline-block;
        border-bottom: 1px dotted var(--pdq-border);
        cursor: help;
    }
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 240px;
        background-color: var(--pdq-dark);
        color: white;
        text-align: center;
        border-radius: 6px;
        padding: 10px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -120px;
        opacity: 0;
        transition: opacity 0.3s;
        font-size: 14px;
    }
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    
    /* Header with tooltip */
    .header-with-tooltip {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    .tooltip-icon {
        color: var(--pdq-text-light);
        margin-left: 5px;
        cursor: help;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: var(--pdq-dark);
    }
    .css-1d391kg .stSelectbox label, 
    .css-1d391kg span {
        color: white !important;
    }
    [data-testid="stSidebar"] {
        background-color: var(--pdq-dark);
        color: white;
    }
    [data-testid="stSidebar"] .stMarkdown p {
        color: white;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4 {
        color: white;
    }
    
    /* Filter badge styling */
    .filter-badge {
        display: inline-block;
        background-color: var(--pdq-light);
        color: var(--pdq-primary);
        border: 1px solid var(--pdq-primary);
        border-radius: 20px;
        padding: 5px 15px;
        margin-right: 10px;
        margin-bottom: 10px;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .filter-badge:hover, .filter-badge.active {
        background-color: var(--pdq-primary);
        color: white;
    }
    
    /* Number indicators */
    .metric-number {
        font-size: 2rem;
        font-weight: 700;
        color: var(--pdq-primary);
    }
    
    /* Table styling */
    .dataframe {
        border-radius: 8px;
        overflow: hidden !important;
    }
    .dataframe th {
        background-color: var(--pdq-primary) !important;
        color: white !important;
    }
    
    /* Dashboard title */
    .dashboard-title {
        color: var(--pdq-primary);
        font-weight: 700;
        margin-bottom: 5px;
    }
    
    /* Logo styling */
    .pdq-logo {
        max-width: 100px;
        margin-bottom: 20px;
    }
    
    /* KPI number styling */
    .kpi-container {
        text-align: center;
    }
    .kpi-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--pdq-primary);
        margin: 0;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: var(--pdq-text-light);
        margin: 0;
    }
    
    /* Chart container */
    .chart-container {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(108, 44, 239, 0.1);
    }
    
    /* Segment filter badge styling */
    .segment-filter {
        display: inline-block;
        background-color: var(--pdq-light);
        color: var(--pdq-primary);
        border: 1px solid var(--pdq-border);
        border-radius: 20px;
        padding: 8px 16px;
        margin-right: 10px;
        margin-bottom: 10px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .segment-filter:hover, .segment-filter.active {
        background-color: var(--pdq-primary);
        color: white;
    }
    
    /* Section headers */
    .section-header {
        color: var(--pdq-primary);
        border-bottom: 1px solid var(--pdq-border);
        padding-bottom: 8px;
        margin-top: 30px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.markdown('<h1 class="dashboard-title">CS Recipe Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p>Helping CS teams identify and recommend high-impact checkout optimizations</p>', unsafe_allow_html=True)

# Modified to use generated data instead of Snowflake queries
def generate_segments_data(merchant_name):
    """Generate realistic demo recipe segments data"""
    np.random.seed(hash(merchant_name) % 100)  # For reproducible results
    
    # Create segment pairs
    segment_pairs = [
        ("Without Coupon", "With Coupon"),
        ("First Time User without Coupon", "First Time User with Coupon"),
        ("Below Threshold", "Above Threshold"),
        ("Below Threshold without Coupon", "Above Threshold without Coupon"),
        ("Returning User without Coupon", "Returning User with Coupon"),
        ("First Time User Below Threshold", "First Time User Above Threshold"),
        ("Returning User Below Threshold", "Returning User Above Threshold")
    ]
    
    data = []
    
    # Create realistic conversion rates
    base_cvr = 0.75  # 75% base conversion rate
    
    for segment, opposite in segment_pairs:
        # Create realistic segment data with negative delta CVR
        checkout_pct = round(np.random.uniform(0.2, 0.8), 2)
        segment_checkouts = int(10000 * checkout_pct)
        delta_cvr = round(np.random.uniform(-0.18, -0.04), 2)  # always negative for opportunities
        cvr = base_cvr + delta_cvr
        opposite_cvr = base_cvr
        aov = round(np.random.uniform(80, 200), 2)
        asr = round(np.random.uniform(5, 30), 2)
        daily_potential = round(abs(delta_cvr) * segment_checkouts / 30, 2)
        revenue_potential = round(daily_potential * (aov + asr) * 365, 0)
        
        suggestion = f"Improving the conversion rate of the {segment} segment is recommended, as it is {abs(delta_cvr)*100}% lower than the {opposite} segment and accounts for {checkout_pct*100}% of total checkouts. The potential annual revenue for this improvement is ${revenue_potential:,.0f}"
        
        data.append({
            'SHOP_NAME': merchant_name,
            'TOP_DELIVERY_COUNTRY': 'US',
            'SEGMENT': segment,
            'OPPOSITE_SEGMENT': opposite,
            'CVR': cvr,
            'OPPOSITE_CVR': opposite_cvr,
            'DELTA_CVR_ROUND': delta_cvr,
            'SEGMENT_CHECKOUTS': segment_checkouts,
            'CHECKOUT_PERCENTAGE_ROUND': checkout_pct,
            'AOV_SEGMENT': aov,
            'ASR_SEGMENT': asr,
            'DAILY_POTENTIAL_CHECKOUTS': daily_potential,
            'Revenue Potential (Annual)': revenue_potential,
            'OPTIMIZATION_SUGGESTION': suggestion
        })
        
        # Also create the opposite relationship with positive delta CVR (price sensitivity test)
        checkout_pct_opp = round(1 - checkout_pct, 2)
        segment_checkouts_opp = int(10000 * checkout_pct_opp)
        delta_cvr_opp = abs(delta_cvr)  # positive delta
        cvr_opp = base_cvr + delta_cvr_opp
        
        suggestion_opp = f"{opposite} segment is optimized for conversion vs. the {segment} segment. Consider a price-sensitivity test!"
        
        data.append({
            'SHOP_NAME': merchant_name,
            'TOP_DELIVERY_COUNTRY': 'US',
            'SEGMENT': opposite,
            'OPPOSITE_SEGMENT': segment,
            'CVR': cvr_opp,
            'OPPOSITE_CVR': cvr,
            'DELTA_CVR_ROUND': delta_cvr_opp,
            'SEGMENT_CHECKOUTS': segment_checkouts_opp,
            'CHECKOUT_PERCENTAGE_ROUND': checkout_pct_opp,
            'AOV_SEGMENT': aov * 1.1,  # slightly higher
            'ASR_SEGMENT': asr * 0.9,  # slightly lower
            'DAILY_POTENTIAL_CHECKOUTS': 0, # no potential for price sensitivity
            'Revenue Potential (Annual)': 0, # no potential for price sensitivity
            'OPTIMIZATION_SUGGESTION': suggestion_opp
        })
    
    return pd.DataFrame(data)

# Generate shipping demo data
def generate_shipping_data(merchant_name):
    """Generate realistic shipping promise data"""
    np.random.seed(hash(merchant_name) % 100)  # For reproducible results
    
    shipping_methods = [
        "Standard Shipping (3-5 business days)",
        "Express Shipping (1-2 business days)",
        "Free Shipping",
        "Economy Shipping",
        "Priority Mail",
        "Next Day Air"
    ]
    
    data = []
    
    for method in shipping_methods:
        # Customize based on shipping method
        if "Express" in method or "Priority" in method or "Next Day" in method:
            # Premium shipping - usually accurate
            tp80 = round(np.random.uniform(-0.5, 0.5), 1)
            median = round(np.random.uniform(-0.3, 0.3), 1)
            records = int(np.random.uniform(100, 500))
        elif "Free" in method or "Economy" in method:
            # Free/Economy shipping - usually too conservative
            tp80 = round(np.random.uniform(0.5, 2.0), 1)
            median = round(np.random.uniform(0.3, 1.0), 1)
            records = int(np.random.uniform(1000, 3000))
        else:
            # Standard shipping - slightly conservative
            tp80 = round(np.random.uniform(0.2, 1.2), 1)
            median = round(np.random.uniform(0.1, 0.8), 1)
            records = int(np.random.uniform(800, 2000))
            
        promises_val = int(np.random.choice([3, 4, 5, 7]))
        
        data.append({
            'S_SHOP_NAME': merchant_name,
            'S_SHOP_ID': f"shop_{np.random.randint(10000, 99999)}",
            'O_SHIPPING_METHOD_TITLE': method,
            'CALCULATED_PROMISES_VAL': promises_val,
            'TP80_DIFF': tp80,
            'MEDIAN_DIFF': median,
            'RECORD_COUNT': records
        })
    
    # Add some methods without promises
    for method in ["Standard Shipping", "Free Standard Shipping", "Shipping"]:
        data.append({
            'S_SHOP_NAME': merchant_name,
            'S_SHOP_ID': f"shop_{np.random.randint(10000, 99999)}",
            'O_SHIPPING_METHOD_TITLE': method,
            'CALCULATED_PROMISES_VAL': None,
            'TP80_DIFF': None,
            'MEDIAN_DIFF': None,
            'RECORD_COUNT': int(np.random.uniform(500, 2500))
        })
    
    return pd.DataFrame(data)

# Generate test history data
def generate_test_history(merchant_name, segment_type=None):
    """Generate realistic test history data"""
    np.random.seed(hash(merchant_name) % 100)  # Use merchant name as seed for consistency
    
    # Base segments for tests
    test_segments = [
        "First Time User Below Threshold",
        "Without Coupon",
        "Below Threshold without Coupon"
    ]
    
    # Filter based on segment type if provided
    if segment_type:
        if segment_type == "coupon":
            test_segments = [s for s in test_segments if "Coupon" in s]
        elif segment_type == "shipping":
            test_segments = ["Express Shipping Test", "Free Shipping Test"]
        elif segment_type == "user":
            test_segments = [s for s in test_segments if "User" in s]
        elif segment_type == "threshold":
            test_segments = [s for s in test_segments if "Threshold" in s]
    
    # Calculate dates relative to today
    today = datetime.now()
    
    data = []
    for segment in test_segments:
        test_start = today - timedelta(days=np.random.randint(30, 90))
        test_end = test_start + timedelta(days=np.random.randint(10, 25))
        test_cvr = round(0.65 + np.random.uniform(0.02, 0.08), 2)
        control_cvr = round(0.65, 2)
        lift_pct = round((test_cvr / control_cvr - 1) * 100, 1)
        segment_size = round(np.random.uniform(25, 45))
        
        data.append({
            'Segment': segment,
            'Test Start': test_start.strftime('%Y-%m-%d'),
            'Test End': test_end.strftime('%Y-%m-%d'),
            'Test CVR': test_cvr,
            'Control CVR': control_cvr,
            'Lift': f"+{lift_pct}%",
            'Segment Size': f"{segment_size}%",
            'Status': "Completed"
        })
    
    return pd.DataFrame(data)

# Replace Snowflake query functions with data generation ones
def fetch_recipe_segments(merchant, threshold_pct=0.15, significance=0.02, country=None, goal=None):
    """Generate and filter recipe segments data based on parameters"""
    # Generate base data
    df = generate_segments_data(merchant)
    
    # Apply filters
    df = df[df['CHECKOUT_PERCENTAGE_ROUND'] >= threshold_pct]
    
    if significance > 0:
        df = df[abs(df['DELTA_CVR_ROUND']) >= significance]
    
    if country and country != "All":
        df = df[df['TOP_DELIVERY_COUNTRY'] == country]
    
    # Apply goal filters
    if goal:
        if goal == "top-line":
            df = df[df['OPTIMIZATION_SUGGESTION'].str.contains('Improving the conversion rate')]
        elif goal == "margin":
            df = df[(df['SEGMENT'].str.contains('with Coupon')) & (df['DELTA_CVR_ROUND'] < 0)]
        elif goal == "no-discount":
            df = df[(df['SEGMENT'].str.contains('without Coupon')) & (df['DELTA_CVR_ROUND'] < 0)]
        elif goal == "fast-delivery":
            df = df[((df['SEGMENT'].str.contains('Below Threshold')) | 
                   (df['SEGMENT'].str.contains('First Time User'))) & 
                  (df['DELTA_CVR_ROUND'] < 0)]
    
    # Order by revenue potential
    df = df.sort_values(by="Revenue Potential (Annual)", ascending=False)
    
    return df

def fetch_shipping_promises(merchant):
    """Generate shipping promise data"""
    return generate_shipping_data(merchant)

# Function to create actionable recommendations based on segments
def generate_recommendations(segments_df, goal):
    """Generate personalized, actionable recommendations"""
    if segments_df.empty:
        return []
    
    recommendations = []
    
    # Sort by revenue potential and get top opportunities
    segments_df = segments_df.sort_values(by="Revenue Potential (Annual)", ascending=False)
    top_segments = segments_df.head(3)
    
    for _, row in top_segments.iterrows():
        segment = row['SEGMENT']
        opposite = row['OPPOSITE_SEGMENT']
        delta_cvr = row['DELTA_CVR_ROUND']
        revenue = row['Revenue Potential (Annual)']
        checkout_pct = row['CHECKOUT_PERCENTAGE_ROUND']
        
        # Skip positive conversion segments (price sensitivity tests)
        if delta_cvr >= 0 or revenue <= 0:
            continue
            
        # Create recommendation
        rec = {
            'segment': segment,
            'revenue': revenue,
            'delta_cvr': delta_cvr,
            'checkout_pct': checkout_pct,
            'opposite': opposite,
            'explanation': f"The {segment} segment has a {abs(delta_cvr*100):.1f}% lower conversion rate than the {opposite} segment and represents {checkout_pct*100:.1f}% of your checkout traffic."
        }
        
        # Determine specific action based on segment
        if "Coupon" in segment:
            if "without Coupon" in segment:
                rec['specific_action'] = f"Add targeted discount options for {segment} customers who abandon checkout"
            else:
                rec['specific_action'] = f"Test different discount levels for {segment} customers"
        elif "Threshold" in segment:
            if "Below Threshold" in segment:
                rec['specific_action'] = f"Add upsell prompts showing benefits of reaching free shipping threshold"
            else:
                rec['specific_action'] = f"Highlight shipping savings for {segment} customers"
        elif "First Time User" in segment:
            rec['specific_action'] = f"Add trust signals and simplified checkout for {segment}"
        elif "Returning User" in segment:
            rec['specific_action'] = f"Implement one-click checkout for {segment}"
        else:
            rec['specific_action'] = f"Optimize the checkout experience for {segment}"
        
        # Personalization based on merchant goal
        if goal == "top-line":
            rec['personalization'] = "This recipe directly increases top-line revenue by improving conversion in a high-volume segment."
        elif goal == "margin":
            rec['personalization'] = "This recipe balances conversion optimization with margin preservation, avoiding unnecessary discounting."
        elif goal == "no-discount":
            rec['personalization'] = "This recipe improves conversion through UX improvements instead of relying on discounts."
        elif goal == "fast-delivery":
            rec['personalization'] = "This recipe enhances delivery experience perception to increase checkout conversion."
        else:
            rec['personalization'] = "This recipe provides a balanced approach to improving checkout conversion."
            
        # Create seasonality explanation
        monthly_distribution = [0.07, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.09, 0.09, 0.10, 0.09]
        rec['seasonality'] = {
            'Q1': f"${revenue * (monthly_distribution[0] + monthly_distribution[1] + monthly_distribution[2]):.0f}",
            'Q2': f"${revenue * (monthly_distribution[3] + monthly_distribution[4] + monthly_distribution[5]):.0f}",
            'Q3': f"${revenue * (monthly_distribution[6] + monthly_distribution[7] + monthly_distribution[8]):.0f}",
            'Q4': f"${revenue * (monthly_distribution[9] + monthly_distribution[10] + monthly_distribution[11]):.0f}",
        }
        
        # Craft a ready-to-copy message with specific action steps
        rec['message'] = f"Based on your checkout data, we recommend testing a recipe for the {segment} segment, which could drive ${revenue:,.0f} in annual uplift by improving conversion by {abs(delta_cvr*100):.1f}%. ACTION: {rec['specific_action']}."
        
        recommendations.append(rec)
        
    return recommendations

# Function to analyze shipping data and generate recommendations
def generate_shipping_recommendations(shipping_df):
    """Generate shipping recommendations based on shipping data"""
    if shipping_df.empty:
        return []
    
    recommendations = []
    
    # Handle methods with promises
    methods_with_promises = shipping_df[shipping_df['CALCULATED_PROMISES_VAL'].notna()]
    for _, row in methods_with_promises.iterrows():
        method = row['O_SHIPPING_METHOD_TITLE']
        tp80 = row.get('TP80_DIFF', 0)
        median = row.get('MEDIAN_DIFF', 0)
        count = row.get('RECORD_COUNT', 0)
        promise = row.get('CALCULATED_PROMISES_VAL')
        
        # Determine specific action based on metrics
        if tp80 >= 1:
            action = f"Reduce delivery promise from {promise} days to {max(1, int(promise - 1))} days"
            explanation = f"Shipments using '{method}' are delivered {tp80:.1f} days faster than promised (80th percentile)."
            status = "opportunity"
        elif tp80 > 0:
            action = f"Consider tightening promise by 0.5 days"
            explanation = f"Shipments using '{method}' are delivered slightly faster ({tp80:.1f} days) than promised."
            status = "good"
        elif tp80 < -1:
            action = f"Extend delivery promise from {promise} days to {int(promise + 1)} days"
            explanation = f"Shipments using '{method}' are delivered {abs(tp80):.1f} days slower than promised (80th percentile)."
            status = "warning"
        else:
            action = "Keep current promise"
            explanation = f"The current promise for '{method}' is accurate."
            status = "accurate"
            
        recommendations.append({
            'method': method,
            'tp80_diff': tp80,
            'median_diff': median,
            'record_count': count,
            'calculated_promise': promise,
            'action': action,
            'explanation': explanation,
            'status': status,
            'has_promise': True
        })
    
    # Handle methods without promises
    methods_without_promises = shipping_df[shipping_df['CALCULATED_PROMISES_VAL'].isna()]
    for _, row in methods_without_promises.iterrows():
        method = row['O_SHIPPING_METHOD_TITLE']
        count = row.get('RECORD_COUNT', 0)
        
        # Suggest adding promise based on method name
        suggested_days = 0
        if "Express" in method or "Priority" in method or "Next Day" in method:
            suggested_days = 2
        elif "Economy" in method:
            suggested_days = 5
        else:
            suggested_days = 3
            
        recommendations.append({
            'method': method,
            'record_count': count,
            'action': f"Add a {suggested_days}-day delivery promise",
            'explanation': f"'{method}' has no delivery promise. Adding one could improve conversion.",
            'status': "missing",
            'has_promise': False
        })
    
    return sorted(recommendations, key=lambda x: 0 if not x.get('has_promise', True) else (-1 if x.get('status') == 'opportunity' else 1))

# Create a helper function for tooltips
def tooltip(text, help_text):
    return f"""
    <div class="tooltip">
        {text}
        <span class="tooltiptext">{help_text}</span>
    </div>
    """

# Create a section header with tooltip
def section_header(title, tooltip_text):
    return f"""
    <div class="header-with-tooltip">
        <h3 style="margin: 0;">{title}</h3>
        <span class="tooltip" style="margin-left: 8px; color: #6c757d; cursor: help;">
            ⓘ
            <span class="tooltiptext">{tooltip_text}</span>
        </span>
    </div>
    """

# Get merchant list (use static list for local version)
def get_merchants():
    return [
        "fashionboutique.myshopify.com",
        "electronics-hub.myshopify.com",
        "homesupplies.myshopify.com",
        "beautystore.myshopify.com",
        "outdoorgear.myshopify.com"
    ]

# Get countries list
def get_countries():
    return ["US", "CA", "UK", "AU", "DE", "FR"]

# Sidebar with PDQ branding
st.sidebar.markdown("""
<div style="text-align: center;">
    <h2 style="color: white;">PDQ</h2>
    <p style="color: #884dff; font-weight: 500;">CS Recipe Dashboard</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# Sidebar filters
st.sidebar.header("dashboard settings")

# Add time period information
analysis_start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
analysis_end = datetime.now().strftime("%Y-%m-%d")
st.sidebar.markdown(f"""
    <div class="time-period" style="color: white;">
        <strong>analysis period:</strong> {analysis_start} to {analysis_end}
    </div>
""", unsafe_allow_html=True)

# Merchant selector
merchants = get_merchants()
selected_merchant = st.sidebar.selectbox(
    "merchant name",
    merchants
)

# Country selector with "All" option
countries = ["All"] + get_countries()
selected_country = st.sidebar.selectbox(
    "delivery country",
    countries
)

# Checkout threshold filter with tooltip
threshold_help = "minimum percentage of checkouts a segment must have to be considered significant. higher values focus on more common customer segments."
st.sidebar.markdown(f"""<div style="color: white;">{tooltip("% checkout threshold (min)", threshold_help)}</div>""", unsafe_allow_html=True)
threshold_percent = st.sidebar.slider(
    "checkout_threshold",
    min_value=0.0,
    max_value=1.0,
    value=0.15,
    step=0.01,
    format="%.2f",
    label_visibility="collapsed"
)

# Significance toggle with tooltip
significance_help = "when enabled, only shows segments with statistically significant conversion differences (≥2% absolute difference)."
st.sidebar.markdown(f"""<div style="color: white;">{tooltip("only show significant opportunities", significance_help)}</div>""", unsafe_allow_html=True)
show_significant = st.sidebar.toggle(
    "significant_toggle",
    value=True,
    label_visibility="collapsed"
)
significance_threshold = 0.02 if show_significant else 0.0

# Goal alignment with tooltip
goal_help = "filter recommendations based on the merchant's primary business goal. each goal uses different criteria to prioritize opportunities."
st.sidebar.markdown(f"""<div style="color: white;">{tooltip("goal alignment", goal_help)}</div>""", unsafe_allow_html=True)
goal_options = {
    "all": "all opportunities",
    "top-line": "increase top-line revenue",
    "margin": "protect contribution margin",
    "no-discount": "minimize discount usage",
    "fast-delivery": "optimize delivery expectations"
}
selected_goal = st.sidebar.selectbox(
    "goal_selector",
    list(goal_options.keys()),
    format_func=lambda x: goal_options[x],
    label_visibility="collapsed"
)

# Similar merchants feature
st.sidebar.markdown("""<h4 style="color: white;">similar merchants</h4>""", unsafe_allow_html=True)
st.sidebar.markdown("""<p style="color: white; font-size: 12px;">merchants with similar patterns</p>""", unsafe_allow_html=True)

similar_merchants = ['similar-store.myshopify.com', 'alike-shop.myshopify.com', 'familiar-brand.myshopify.com']
for i, merchant in enumerate(similar_merchants):
    similarity = round(90 - i*10)
    st.sidebar.markdown(f"""<div style="color: white;">{merchant} <span style="color: #884dff; font-weight: 500;">({similarity}% similar)</span></div>""", unsafe_allow_html=True)

# Feedback section in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""<h4 style="color: white;">feedback</h4>""", unsafe_allow_html=True)
if st.sidebar.button("share feedback", use_container_width=True):
    st.sidebar.success("Thank you for your feedback!")

# Main content as tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Recipe Opportunities 🚀", 
    "Shipping Promise Analysis 📦", 
    "Tested vs. Untested Recipes 🧪",
    "Pitch-Ready Recipes 💼"
])

# Tab 1: Recipe Opportunities
with tab1:
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    
    # Fetch segment data using our data generation function
    segments_df = fetch_recipe_segments(
        selected_merchant, 
        threshold_percent, 
        significance_threshold, 
        selected_country,
        selected_goal if selected_goal != "all" else None
    )
    
    # Summary metrics
    st.markdown('<h3 class="section-header">opportunity summary</h3>', unsafe_allow_html=True)
    
    # Count opportunities by type
    conversion_opps = len(segments_df[segments_df['DELTA_CVR_ROUND'] < 0])
    sensitivity_opps = len(segments_df[segments_df['DELTA_CVR_ROUND'] > 0])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-container">
                <p class="kpi-number">{len(segments_df)}</p>
                <p class="kpi-label">total opportunities</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-container">
                <p class="kpi-number" style="color: #28a745;">{conversion_opps}</p>
                <p class="kpi-label">conversion optimization</p>
                <p style="color: #28a745; margin: 0; font-size: 0.8rem;">↑ increase revenue</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-container">
                <p class="kpi-number" style="color: #884dff;">{sensitivity_opps}</p>
                <p class="kpi-label">price sensitivity tests</p>
                <p style="color: #884dff; margin: 0; font-size: 0.8rem;">↑ test pricing</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display the segments table
    st.markdown('<h3 class="section-header">recipe opportunities</h3>', unsafe_allow_html=True)
    
    # Prepare display columns
    display_df = segments_df.copy()
    display_df = display_df.rename(columns={
        'SEGMENT': 'segment',
        'OPPOSITE_SEGMENT': 'opposite segment',
        'DELTA_CVR_ROUND': 'cvr vs opposite',
        'CHECKOUT_PERCENTAGE_ROUND': '% of checkouts',
        'Revenue Potential (Annual)': 'potential lift',
        'OPTIMIZATION_SUGGESTION': 'optimization suggestion'
    })
    
    # Format values for display
    display_df['cvr vs opposite'] = display_df['cvr vs opposite'].apply(lambda x: f"{x*100:.1f}%")
    display_df['% of checkouts'] = display_df['% of checkouts'].apply(lambda x: f"{x*100:.1f}%")
    display_df['potential lift'] = display_df['potential lift'].apply(lambda x: f"${x:,.0f}")
    
    # Select and order columns for display
    display_cols = [
        'segment', 
        'opposite segment', 
        'cvr vs opposite', 
        '% of checkouts', 
        'potential lift', 
        'optimization suggestion'
    ]
    
    # Show data table
    st.dataframe(display_df[display_cols], use_container_width=True)
    
    # Show detailed cards for top opportunities
    st.markdown('<h3 class="section-header">top 3 opportunities</h3>', unsafe_allow_html=True)
    
    # Get top 3 segments with negative delta_cvr (real opportunities)
    segments_df_neg = segments_df[segments_df['DELTA_CVR_ROUND'] < 0]
    top_3_df = segments_df_neg.nlargest(3, 'Revenue Potential (Annual)')
    
    for i, (_, row) in enumerate(top_3_df.iterrows()):
        segment = row['SEGMENT']
        opposite = row['OPPOSITE_SEGMENT']
        delta_cvr = row['DELTA_CVR_ROUND']
        revenue = row['Revenue Potential (Annual)']
        checkout_pct = row['CHECKOUT_PERCENTAGE_ROUND']
        
        # Determine specific action based on segment
        specific_action = "optimize checkout experience"
        if "Coupon" in segment:
            if "without Coupon" in segment:
                specific_action = "add targeted discount options for this segment"
            else:
                specific_action = "test different discount levels"
        elif "Threshold" in segment:
            if "Below Threshold" in segment:
                specific_action = "add upsell prompts showing free shipping benefits"
            else:
                specific_action = "highlight shipping savings"
        elif "First Time User" in segment:
            specific_action = "add trust signals and simplified checkout"
        elif "Returning User" in segment:
            specific_action = "implement one-click checkout"
        
        st.markdown(f"""
        <div class="recipe-card">
            <h4>{segment}</h4>
            <p><strong>issue:</strong> {abs(delta_cvr*100):.1f}% lower conversion vs {opposite}</p>
            <p><strong>segment size:</strong> {checkout_pct*100:.1f}% of checkouts</p>
            <p><strong>revenue impact:</strong> ${revenue:,.0f} annually</p>
            <p><strong>recommended action:</strong> {specific_action}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Segment filtering options
    st.markdown('<h3 class="section-header">filter by segment type</h3>', unsafe_allow_html=True)
    
    # Initialize session state for segment filter if it doesn't exist
    if 'segment_filter' not in st.session_state:
        st.session_state.segment_filter = None
    
    # Create buttons for segment filtering
    filter_col1, filter_col2, filter_col3, filter_col4, filter_col5 = st.columns(5)
    
    with filter_col1:
        if st.button("coupon-related", key="filter_coupon", use_container_width=True):
            st.session_state.segment_filter = 'coupon'
            st.rerun()
    
    with filter_col2:
        if st.button("shipping-related", key="filter_shipping", use_container_width=True):
            st.session_state.segment_filter = 'shipping'
            st.rerun()
    
    with filter_col3:
        if st.button("user type", key="filter_user", use_container_width=True):
            st.session_state.segment_filter = 'user'
            st.rerun()
    
    with filter_col4:
        if st.button("threshold", key="filter_threshold", use_container_width=True):
            st.session_state.segment_filter = 'threshold'
            st.rerun()
            
    with filter_col5:
        if st.button("clear filter", key="filter_clear", use_container_width=True):
            st.session_state.segment_filter = None
            st.rerun()
    
    # Apply filter if set
    if st.session_state.segment_filter:
        filter_type = st.session_state.segment_filter
        
        # Filter the dataframe
        if filter_type == 'coupon':
            filtered_df = display_df[display_df['segment'].str.contains('Coupon')]
            st.markdown(f"<p>Showing {len(filtered_df)} coupon-related segments</p>", unsafe_allow_html=True)
            st.dataframe(filtered_df, use_container_width=True)
        elif filter_type == 'shipping':
            filtered_df = display_df[display_df['segment'].str.contains('Threshold')]
            st.markdown(f"<p>Showing {len(filtered_df)} shipping-related segments</p>", unsafe_allow_html=True)
            st.dataframe(filtered_df, use_container_width=True)
        elif filter_type == 'user':
            filtered_df = display_df[display_df['segment'].str.contains('User')]
            st.markdown(f"<p>Showing {len(filtered_df)} user type segments</p>", unsafe_allow_html=True)
            st.dataframe(filtered_df, use_container_width=True)
        elif filter_type == 'threshold':
            filtered_df = display_df[display_df['segment'].str.contains('Threshold')]
            st.markdown(f"<p>Showing {len(filtered_df)} threshold segments</p>", unsafe_allow_html=True)
            st.dataframe(filtered_df, use_container_width=True)
    
    # Machine Learning Insights section (from the older version)
    st.markdown('<h3 class="section-header">machine learning insights</h3>', unsafe_allow_html=True)
    ml_col1, ml_col2 = st.columns(2)

    with ml_col1:
        st.markdown("""
        <div class="metric-card">
            <h4>merchant similarity analysis</h4>
            <p>this merchant shares patterns with:</p>
            <ol>
                <li>similar-store.myshopify.com (90% similar)</li>
                <li>alike-shop.myshopify.com (80% similar)</li>
                <li>familiar-brand.myshopify.com (70% similar)</li>
            </ol>
            <p>these merchants have successfully implemented similar recipes.</p>
        </div>
        """, unsafe_allow_html=True)

    with ml_col2:
        st.markdown("""
        <div class="metric-card">
            <h4>revenue forecast</h4>
            <p>implementing all recommended recipes could result in:</p>
            <ul>
                <li><strong>estimated annual lift:</strong> $1.2M - $1.5M</li>
                <li><strong>conversion rate improvement:</strong> 8-12%</li>
                <li><strong>implementation time:</strong> 2-3 weeks</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
# Tab 4: Pitch-Ready Recipes
with tab4:
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    
    # Get segments data
    segments_df = fetch_recipe_segments(
        selected_merchant, 
        threshold_percent, 
        significance_threshold, 
        selected_country,
        selected_goal if selected_goal != "all" else None
    )
    
    # Generate recommendations
    recommendations = generate_recommendations(segments_df, selected_goal)
    
    if not recommendations:
        st.info("no significant recommendations available with current filters. try adjusting the filters.")
    else:
        st.markdown('<h3 class="section-header">top recommendations for this merchant</h3>', unsafe_allow_html=True)
        
        # Add time period information
        analysis_start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        analysis_end = datetime.now().strftime("%Y-%m-%d")
        st.markdown(f"""
        <div class="time-period" style="margin-bottom: 20px;">
            based on analysis of checkout data from {analysis_start} to {analysis_end}
        </div>
        """, unsafe_allow_html=True)
        
        # Display each recommendation as a card
        for i, rec in enumerate(recommendations):
            segment = rec['segment']
            revenue = rec['revenue']
            delta_cvr = rec['delta_cvr']
            explanation = rec['explanation']
            personalization = rec['personalization']
            message = rec['message']
            specific_action = rec['specific_action']
            
            st.markdown(f"### recipe {i+1}: {segment}")
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"""
                <div class="recipe-card {'top-recipe' if i==0 else 'medium-recipe' if i==1 else 'low-recipe'}">
                    <h4>explanation</h4>
                    <p>{explanation}</p>
                    
                    <h4>estimated annual impact</h4>
                    <p class="highlight">${revenue:,.0f}</p>
                    
                    <h4>personalization</h4>
                    <p>{personalization}</p>
                    
                    <h4>recommended action</h4>
                    <p class="positive">{specific_action}</p>
                    
                    <div class="recommendation-text">
                        <h4>copyable message</h4>
                        <p>{message}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.metric(
                    "conversion gap", 
                    f"{abs(delta_cvr*100):.1f}%",
                    delta=f"${revenue/1000:.0f}K opportunity"
                )
                
                if st.button(f"copy message {i+1}", key=f"copy_message_{i}", use_container_width=True):
                    st.session_state[f'copy_message_clicked_{i}'] = True
                
                if st.button(f"download pdf {i+1}", key=f"download_{i}", use_container_width=True):
                    st.session_state[f'download_clicked_{i}'] = True
                
                # Show success messages
                if st.session_state.get(f'copy_message_clicked_{i}', False):
                    st.markdown("""
                    <div class="success-alert">
                        message copied to clipboard!
                    </div>
                    """, unsafe_allow_html=True)
                
                if st.session_state.get(f'download_clicked_{i}', False):
                    st.markdown("""
                    <div class="success-alert">
                        pdf report downloaded!
                    </div>
                    """, unsafe_allow_html=True)
    
        # Visualization of impact
        st.markdown('<h3 class="section-header">impact visualization</h3>', unsafe_allow_html=True)
        
        # Create data for bar chart
        chart_data = pd.DataFrame({
            'Segment': [rec['segment'] for rec in recommendations],
            'Revenue Impact': [rec['revenue'] for rec in recommendations]
        })
        
        # Display bar chart
        st.bar_chart(chart_data.set_index('Segment'))
        
        # Feedback section
        st.markdown('<h3 class="section-header">was this recommendation helpful?</h3>', unsafe_allow_html=True)
        
        feedback_col1, feedback_col2, feedback_col3 = st.columns(3)
        
        with feedback_col1:
            if st.button("👍 yes", key="feedback_yes", use_container_width=True):
                st.session_state['feedback'] = 'positive'
        
        with feedback_col2:
            if st.button("👎 no", key="feedback_no", use_container_width=True):
                st.session_state['feedback'] = 'negative'
        
        with feedback_col3:
            if st.button("💬 need more info", key="feedback_more", use_container_width=True):
                st.session_state['feedback'] = 'more_info'
        
        # Show feedback confirmation
        if 'feedback' in st.session_state:
            if st.session_state['feedback'] == 'positive':
                st.markdown("""
                <div class="success-alert">
                    thanks for your feedback! we'll continue to refine these recommendations.
                </div>
                """, unsafe_allow_html=True)
            elif st.session_state['feedback'] == 'negative':
                st.markdown("""
                <div class="success-alert">
                    thanks for your feedback. what could we improve?
                </div>
                """, unsafe_allow_html=True)
                st.text_area("what could we improve?", key="feedback_improvement")
            elif st.session_state['feedback'] == 'more_info':
                st.markdown("""
                <div class="success-alert">
                    we'll reach out with more detailed information about these recommendations.
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Additional Resources 
st.markdown('<div class="tab-container" style="margin-top: 20px;">', unsafe_allow_html=True)
st.markdown('<h3 class="section-header">additional resources</h3>', unsafe_allow_html=True)

resource_col1, resource_col2, resource_col3 = st.columns(3)

with resource_col1:
    st.markdown("""
    <div class="metric-card">
        <h4>implementation guides</h4>
        <ul>
            <li><a href="#">recipe implementation playbook</a></li>
            <li><a href="#">technical integration guide</a></li>
            <li><a href="#">a/b testing best practices</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with resource_col2:
    st.markdown("""
    <div class="metric-card">
        <h4>case studies</h4>
        <ul>
            <li><a href="#">fashion brand: +15% cvr</a></li>
            <li><a href="#">electronics store: +$800k revenue</a></li>
            <li><a href="#">home goods: +22% aov</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with resource_col3:
    st.markdown("""
    <div class="metric-card">
        <h4>support</h4>
        <ul>
            <li><a href="#">schedule merchant review</a></li>
            <li><a href="#">request custom analysis</a></li>
            <li><a href="#">contact recipe support</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Add tooltips
if "init_tooltips" not in st.session_state:
    st.session_state.init_tooltips = True

# Tab 3: Tested vs. Untested Recipes
with tab3:
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    
    # Initialize test segment filter in session state if it doesn't exist
    if 'test_segment_filter' not in st.session_state:
        st.session_state.test_segment_filter = None
    
    # Get tested recipes
    test_history = generate_test_history(selected_merchant, st.session_state.test_segment_filter)
    
    # Get all recipe segments for comparison
    all_segments_df = fetch_recipe_segments(
        selected_merchant, 
        0.05,  # lower threshold to include more segments 
        0.0,   # include all segments regardless of significance
        None,  # all countries
        None   # all goals
    )
    
    # Add time period information
    st.markdown(f"""
    <div class="time-period">
        analysis shows recipe tests from the last 90 days and identifies untested opportunities.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="section-header">tested recipes</h3>', unsafe_allow_html=True)
        
        if test_history.empty:
            st.info("no recipe tests found for this merchant.")
        else:
            # Add visual indicators for test results
            test_history['Result'] = test_history.apply(
                lambda row: f"✅ {row['Lift']}" if row['Status'] == 'Completed' else "⏳ in progress", 
                axis=1
            )
            
            # Format the dataframe for display
            display_cols = ['Segment', 'Test Start', 'Test End', 'Test CVR', 'Control CVR', 'Lift', 'Segment Size', 'Result']
            st.dataframe(test_history[display_cols], use_container_width=True)
            
            # Create a chart of test results
            st.markdown('<h4 style="margin-top: 20px;">test results by lift</h4>', unsafe_allow_html=True)
            
            # Extract lift values for chart
            lift_values = []
            for lift_str in test_history['Lift']:
                try:
                    lift_values.append(float(lift_str.strip('%').strip('+').strip('-')))
                except:
                    lift_values.append(0)
                    
            test_history['Lift Value'] = lift_values
            
            # Create chart data
            lift_chart_data = pd.DataFrame({
                'Segment': test_history['Segment'],
                'Lift (%)': test_history['Lift Value']
            })
            
            # Display chart
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.bar_chart(lift_chart_data.set_index('Segment'))
            st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h3 class="section-header">untested opportunities</h3>', unsafe_allow_html=True)
        
        if all_segments_df.empty:
            st.info("no untested opportunities found.")
        else:
            # Find untested segments (those not in test_history)
            tested_segments = test_history['Segment'].tolist() if not test_history.empty else []
            untested_df = all_segments_df[~all_segments_df['SEGMENT'].isin(tested_segments)]
            
            # Filter for actual opportunities (negative delta_cvr)
            untested_df = untested_df[untested_df['DELTA_CVR_ROUND'] < 0]
            
            # Sort by revenue potential
            untested_df = untested_df.sort_values('Revenue Potential (Annual)', ascending=False)
            
            if untested_df.empty:
                st.info("all significant opportunities have already been tested. good job!")
            else:
                # Prepare display dataframe
                untested_display = untested_df[['SEGMENT', 'DELTA_CVR_ROUND', 'CHECKOUT_PERCENTAGE_ROUND', 'Revenue Potential (Annual)']].copy()
                untested_display = untested_display.rename(columns={
                    'SEGMENT': 'segment',
                    'DELTA_CVR_ROUND': 'cvr opportunity',
                    'CHECKOUT_PERCENTAGE_ROUND': 'segment size',
                    'Revenue Potential (Annual)': 'revenue potential'
                })
                
                # Format values
                untested_display['cvr opportunity'] = untested_display['cvr opportunity'].apply(lambda x: f"{abs(x*100):.1f}%")
                untested_display['segment size'] = untested_display['segment size'].apply(lambda x: f"{x*100:.1f}%")
                untested_display['revenue potential'] = untested_display['revenue potential'].apply(lambda x: f"${x:,.0f}")
                
                st.dataframe(untested_display.head(10), use_container_width=True)
                
                # Show top untested opportunity
                if len(untested_df) > 0:
                    st.markdown('<h4 style="margin-top: 20px;">top untested opportunity</h4>', unsafe_allow_html=True)
                    
                    top_untested = untested_df.iloc[0]
                    segment = top_untested['SEGMENT']
                    delta_cvr = top_untested['DELTA_CVR_ROUND']
                    revenue = top_untested['Revenue Potential (Annual)']
                    
                    st.markdown(f"""
                    <div class="recipe-card">
                        <h4>{segment}</h4>
                        <p><strong>opportunity:</strong> {abs(delta_cvr*100):.1f}% cvr improvement potential</p>
                        <p><strong>revenue impact:</strong> ${revenue:,.0f} annual potential</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("set up test", key="setup_test", use_container_width=True):
                            st.session_state['setup_test_clicked'] = True
                    
                    with col2:
                        if st.button("schedule discussion", key="schedule_discussion", use_container_width=True):
                            st.session_state['schedule_discussion_clicked'] = True
                            
                    # Show success message if button was clicked
                    if st.session_state.get('setup_test_clicked', False):
                        st.markdown("""
                        <div class="success-alert">
                            test setup initiated! check your email for details.
                        </div>
                        """, unsafe_allow_html=True)
                        
                    if st.session_state.get('schedule_discussion_clicked', False):
                        st.markdown("""
                        <div class="success-alert">
                            discussion scheduled with merchant for next week.
                        </div>
                        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tab 2: Shipping Promise Analysis
with tab2:
    st.markdown('<div class="tab-container">', unsafe_allow_html=True)
    
    # Display shipping promise explanation
    st.markdown("""
    <div style="background-color: #f5f3ff; padding: 15px; border-radius: 5px; margin-bottom: 20px; border-left: 4px solid #6c2cef;">
        <h4 style="margin-top: 0; color: #6c2cef;">about shipping promises</h4>
        <p>this analysis compares actual delivery times with merchant-set promises to identify optimization opportunities. 
        adjusting delivery promises to match reality can improve conversion rates and customer satisfaction.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Fetch shipping data
    shipping_df = fetch_shipping_promises(selected_merchant)
    
    # Generate recommendations
    shipping_recs = generate_shipping_recommendations(shipping_df)
    
    # Count metrics
    opportunities = sum(1 for rec in shipping_recs if rec['status'] == 'opportunity')
    on_time = sum(1 for rec in shipping_recs if rec['status'] == 'accurate')
    missing_promises = sum(1 for rec in shipping_recs if rec['status'] == 'missing')
    warnings = sum(1 for rec in shipping_recs if rec['status'] == 'warning')
    
    # Display metrics
    st.markdown('<h3 class="section-header">shipping performance overview</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-container">
                <p class="kpi-number" style="color: #28a745;">{opportunities}</p>
                <p class="kpi-label">opportunity methods</p>
                <p style="font-size: 0.8rem;">methods where delivery is faster than promised</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-container">
                <p class="kpi-number">{on_time}</p>
                <p class="kpi-label">accurate promises</p>
                <p style="font-size: 0.8rem;">methods with well-calibrated promises</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-container">
                <p class="kpi-number" style="color: #884dff;">{missing_promises}</p>
                <p class="kpi-label">methods needing promises</p>
                <p style="font-size: 0.8rem; color: #884dff;">add delivery promises</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="kpi-container">
                <p class="kpi-number" style="color: #ff7b54;">{warnings}</p>
                <p class="kpi-label">promise warnings</p>
                <p style="font-size: 0.8rem;">methods with too aggressive promises</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Show detailed recommendation cards
    st.markdown('<h3 class="section-header">shipping recommendations</h3>', unsafe_allow_html=True)
    
    if shipping_recs:
        opportunity_recs = [rec for rec in shipping_recs if rec['status'] == 'opportunity']
        missing_recs = [rec for rec in shipping_recs if rec['status'] == 'missing']
        warning_recs = [rec for rec in shipping_recs if rec['status'] == 'warning']
        
        # First show opportunities
        if opportunity_recs:
            st.markdown("""<h4 style="color: #28a745;">🚀 opportunities to tighten promises</h4>""", unsafe_allow_html=True)
            
            for i, rec in enumerate(opportunity_recs[:3]):
                method = rec['method']
                tp80 = rec.get('tp80_diff', 0)
                action = rec['action']
                explanation = rec['explanation']
                
                st.markdown(f"""
                <div class="shipping-card" style="border-left-color: #28a745;">
                    <h4>{method}</h4>
                    <p><strong>opportunity:</strong> {explanation}</p>
                    <p><strong>metrics:</strong> arriving {tp80:.1f} days faster than promised (80th percentile)</p>
                    <p><strong>recommendation:</strong> {action}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Then show missing promises
        if missing_recs:
            st.markdown("""<h4 style="color: #884dff;">📦 methods needing delivery promises</h4>""", unsafe_allow_html=True)
            
            for i, rec in enumerate(missing_recs[:3]):
                method = rec['method']
                action = rec['action']
                explanation = rec['explanation']
                
                st.markdown(f"""
                <div class="shipping-card" style="border-left-color: #884dff;">
                    <h4>{method}</h4>
                    <p><strong>issue:</strong> {explanation}</p>
                    <p><strong>recommendation:</strong> {action}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Finally show warnings
        if warning_recs:
            st.markdown("""<h4 style="color: #ff7b54;">⚠️ promises that need adjustment</h4>""", unsafe_allow_html=True)
            
            for i, rec in enumerate(warning_recs[:3]):
                method = rec['method']
                tp80 = rec.get('tp80_diff', 0)
                action = rec['action']
                explanation = rec['explanation']
                
                st.markdown(f"""
                <div class="shipping-card" style="border-left-color: #ff7b54;">
                    <h4>{method}</h4>
                    <p><strong>issue:</strong> {explanation}</p>
                    <p><strong>recommendation:</strong> {action}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("no shipping optimization opportunities found.")
    
    # Add a section for the shipping methods table
    st.markdown('<h3 class="section-header">all shipping methods</h3>', unsafe_allow_html=True)
    
    # Create a display dataframe
    shipping_display = shipping_df.copy()
    
    # Calculate percentages
    total_records = shipping_display['RECORD_COUNT'].sum()
    shipping_display['PERCENTAGE'] = (shipping_display['RECORD_COUNT'] / total_records) * 100 if total_records > 0 else 0
    
    # Rename columns for display
    shipping_display = shipping_display.rename(columns={
        'O_SHIPPING_METHOD_TITLE': 'shipping method',
        'TP80_DIFF': 'tp80 diff',
        'MEDIAN_DIFF': 'median diff',
        'RECORD_COUNT': 'records',
        'PERCENTAGE': '%total',
        'CALCULATED_PROMISES_VAL': 'promise (days)'
    })
    
    # Format values
    shipping_display['%total'] = shipping_display['%total'].apply(lambda x: f"{x:.1f}%")
    
    # Select columns for display
    display_cols = [
        'shipping method', 
        'promise (days)',
        'tp80 diff', 
        'median diff', 
        'records', 
        '%total'
    ]
    
    # Show the table
    st.dataframe(shipping_display[display_cols], use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)