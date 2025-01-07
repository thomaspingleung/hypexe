import numpy as np

# Discounted Cash Flow (DCF) function
def discounted_cash_flow(fcf, growth_rate, discount_rate, terminal_growth, years=5):
    """
    Calculate intrinsic value using Discounted Cash Flow (DCF).
    """
    fcf_values = [(fcf * (1 + growth_rate) ** t) / (1 + discount_rate) ** t for t in range(1, years + 1)]
    terminal_value = (fcf * (1 + growth_rate) ** years * (1 + terminal_growth)) / (discount_rate - terminal_growth)
    terminal_value /= (1 + discount_rate) ** years
    intrinsic_value = sum(fcf_values) + terminal_value
    return intrinsic_value

# Benjamin Graham's valuation function
def benjamin_graham_valuation(eps, growth_rate, expected_return=0.1):
    """
    Calculate intrinsic value using Benjamin Graham's formula.
    """
    intrinsic_value = eps * (8.5 + 2 * growth_rate * 100) * 4.4 / expected_return
    return intrinsic_value

# Multiples valuation function
def multiples_valuation(peers_pe, stock_eps):
    """
    Calculate intrinsic value using multiples (e.g., PE ratio).
    """
    intrinsic_value = peers_pe * stock_eps
    return intrinsic_value

# Aggregate Score function
def aggregate_score(current_price, dcf_value, graham_value, multiples_value, weights=(0.4, 0.3, 0.3)):
    """
    Generate an aggregate score based on DCF, Graham, and Multiples valuations.
    """
    dcf_score = min(max((dcf_value / current_price) * 100, 0), 100)
    graham_score = min(max((graham_value / current_price) * 100, 0), 100)
    multiples_score = min(max((multiples_value / current_price) * 100, 0), 100)
    aggregate = (weights[0] * dcf_score + weights[1] * graham_score + weights[2] * multiples_score)
    return round(aggregate, 2)

# Main program
if __name__ == "__main__":
    print("Stock Valuation Indicator Score")

    # Input data
    current_price = float(input("Enter current stock price: "))
    fcf = float(input("Enter Free Cash Flow (in millions): "))
    growth_rate = float(input("Enter expected annual growth rate (e.g., 0.05 for 5%): "))
    discount_rate = float(input("Enter discount rate (e.g., 0.1 for 10%): "))
    terminal_growth = float(input("Enter terminal growth rate (e.g., 0.02 for 2%): "))
    eps = float(input("Enter Earnings Per Share (EPS): "))
    peers_pe = float(input("Enter average P/E ratio of peer companies: "))

    # Perform valuations
    dcf_value = discounted_cash_flow(fcf, growth_rate, discount_rate, terminal_growth)
    graham_value = benjamin_graham_valuation(eps, growth_rate)
    multiples_value = multiples_valuation(peers_pe, eps)

    # Calculate aggregate score
    aggregate = aggregate_score(current_price, dcf_value, graham_value, multiples_value)

    # Output results
    print("\nValuation Results:")
    print(f"  - DCF Intrinsic Value: ${dcf_value:.2f}")
    print(f"  - Graham Intrinsic Value: ${graham_value:.2f}")
    print(f"  - Multiples Intrinsic Value: ${multiples_value:.2f}")
    print(f"\nAggregate Score: {aggregate}%")

    # Recommendation
    if aggregate >= 75:
        print("Recommendation: Strong Buy")
    elif 50 <= aggregate < 75:
        print("Recommendation: Buy")
    elif 25 <= aggregate < 50:
        print("Recommendation: Hold")
    else:
        print("Recommendation: Do Not Buy")
