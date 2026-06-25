import numpy as np
import pandas as pd


class RiskAnalytics:
    """
    High-performance risk analytics engine utilizing pandas and numpy.
    Replaces C# loop-based calculations with vectorized operations.
    """

    def __init__(self, confidence_interval: float = 0.99):
        self.ci = confidence_interval

    def calculate_historical_var(self, returns_df: pd.DataFrame, portfolio_weights: np.ndarray) -> float:
        """
        Calculates Value at Risk (VaR) using historical simulation.

        :param returns_df: DataFrame of historical daily returns for assets.
        :param portfolio_weights: Numpy array of asset weights.
        :return: VaR at the given confidence interval.
        """
        # Vectorized portfolio returns
        portfolio_returns = returns_df.dot(portfolio_weights)

        # Calculate VaR using percentile
        var = np.percentile(portfolio_returns, (1 - self.ci) * 100)
        return var

    def run_monte_carlo_stress_test(
        self, current_prices: np.ndarray, cov_matrix: np.ndarray, num_simulations: int = 10000
    ) -> np.ndarray:
        """
        Runs Monte Carlo simulations using Cholesky decomposition for correlated random walks.

        :param current_prices: Array of current asset prices.
        :param cov_matrix: Covariance matrix of asset returns.
        :param num_simulations: Number of paths to simulate.
        :return: Array of simulated portfolio values.
        """
        num_assets = len(current_prices)

        # Cholesky decomposition of covariance matrix
        L = np.linalg.cholesky(cov_matrix)

        # Generate correlated random shocks
        uncorrelated_shocks = np.random.normal(0, 1, (num_assets, num_simulations))
        correlated_shocks = L.dot(uncorrelated_shocks)

        # Apply shocks to current prices (assuming 1-day step, zero drift for simplicity)
        simulated_prices = current_prices[:, np.newaxis] * (1 + correlated_shocks)

        return simulated_prices
