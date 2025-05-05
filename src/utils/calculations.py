def calculate_variance(actual, expected):
    """Calculate the variance between actual and expected values."""
    return actual - expected

def calculate_cumulative_balance(initial_balance, annual_costs):
    """Calculate the cumulative balance over the years."""
    cumulative_balance = initial_balance
    balances = []
    for cost in annual_costs:
        cumulative_balance += cost
        balances.append(cumulative_balance)
    return balances

def compare_financing_methods(method_a, method_b):
    """Compare two financing methods based on their cumulative balances."""
    comparison = {
        'method_a': {
            'cumulative_balance': sum(method_a),
            'annual_costs': method_a
        },
        'method_b': {
            'cumulative_balance': sum(method_b),
            'annual_costs': method_b
        }
    }
    return comparison