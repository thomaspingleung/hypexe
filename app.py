import streamlit as st
import numpy as np

# Discounted Cash Flow (DCF) function
def discounted_cash_flow(fcf, growth_rate, discount_rate, terminal_growth, years=5):
    fcf_values = [(fcf * (1 + growth_rate) ** t) / (1 + discount_rate) ** t for t in range(1, years + 1)]
    terminal_value = (fcf * (1 + growth_rate) ** years * (1 + terminal_growth)) / (discount_rate - terminal_growth)
    terminal_value /= (1 + discount_rate) ** years
    intrinsic_value = sum(fcf_values) + terminal_value
    return intrinsic_value

# Benjamin Graham's valuation function
def benjamin_graham_valuation(eps, growth_rate, expected_return=0.1):
    intrinsic_value = eps * (8.5 + 2 * growth_rate * 100) * 4.4 / expected_return
    return intrinsic_value

# Multiples valuation function
def multiples_valuation(peers_pe, stock_eps):
    intrinsic_value = peers_pe * stock_eps
    return intrinsic_value

# Aggregate Score function
def aggregate_score(current_price, dcf_value, graham_value, multiples_value, weights=(0.4, 0.3, 0.3)):
    dcf_score = min(max((dcf_value / current_price) * 100, 0), 100)
    graham_score = min(max((graham_value / current_price) * 100, 0), 100)
    multiples_score = min(max((multiples_value / current_price) * 100, 0), 100)
    aggregate = (weights[0] * dcf_score + weights[1] * graham_score + weights[2] * multiples_score)
    return round(aggregate, 2)

# Streamlit app
st.title("Stock Valuation Indicator")
st.write("This app calculates a stock's valuation score using Discounted Cash Flow, Benjamin Graham's formula, and Multiples valuation.")

# Input fields
current_price = st.number_input("Current stock price ($):", min_value=0.0, step=0.01)
fcf = st.number_input("Free Cash Flow (in millions):", min_value=0.0, step=0.01)
growth_rate = st.number_input("Expected annual growth rate (e.g., 0.05 for 5%):", min_value=0.0, step=0.01)
discount_rate = st.number_input("Discount rate (e.g., 0.1 for 10%):", min_value=0.0, step=0.01)
terminal_growth = st.number_input("Terminal growth rate (e.g., 0.02 for 2%):", min_value=0.0, step=0.01)
eps = st.number_input("Earnings Per Share (EPS):", min_value=0.0, step=0.01)
peers_pe = st.number_input("Average P/E ratio of peer companies:", min_value=0.0, step=0.01)

# Perform calculations when the user clicks the button
if st.button("Calculate Valuation"):
    # Calculate intrinsic values
    dcf_value = discounted_cash_flow(fcf, growth_rate, discount_rate, terminal_growth)
    graham_value = benjamin_graham_valuation(eps, growth_rate)
    multiples_value = multiples_valuation(peers_pe, eps)

    # Calculate aggregate score
    aggregate = aggregate_score(current_price, dcf_value, graham_value, multiples_value)

    # Display results
    st.subheader("Valuation Results")
    st.write(f"**Discounted Cash Flow (DCF) Intrinsic Value:** ${dcf_value:,.2f}")
    st.write(f"**Benjamin Graham Intrinsic Value:** ${graham_value:,.2f}")
    st.write(f"**Multiples Intrinsic Value:** ${multiples_value:,.2f}")
    st.write(f"**Aggregate Score:** {aggregate}%")

    # Recommendation
    if aggregate >= 75:
        st.success("Recommendation: Strong Buy")
    elif 50 <= aggregate < 75:
        st.info("Recommendation: Buy")
    elif 25 <= aggregate < 50:
        st.warning("Recommendation: Hold")
    else:
        st.error("Recommendation: Do Not Buy")
