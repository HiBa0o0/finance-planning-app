class FinancePlan:
    def __init__(self, annual_costs, cumulative_balances):
        self.annual_costs = annual_costs
        self.cumulative_balances = cumulative_balances

    def calculate_variance(self):
        # Implement variance calculation logic here
        pass

    def add_annual_cost(self, cost):
        self.annual_costs.append(cost)

    def add_cumulative_balance(self, balance):
        self.cumulative_balances.append(balance)

    def get_summary(self):
        return {
            "annual_costs": self.annual_costs,
            "cumulative_balances": self.cumulative_balances
        }