import pandas as pd
import numpy as np


def calculate_cumulative_return(daily_returns: pd.Series) -> float:
    """
    Calculates the cumulative return over a series of daily returns via geometric linking.
    Replaces the legacy SQL approach of `exp(sum(ln(1+r)))`.
    """
    if daily_returns.empty:
        return 0.0
    return (1 + daily_returns).prod() - 1


def calculate_annualized_return(daily_returns: pd.Series, periods_per_year: int = 252) -> float:
    """
    Calculates the annualized return.
    """
    if daily_returns.empty:
        return 0.0
    cum_return = calculate_cumulative_return(daily_returns)
    num_periods = len(daily_returns)
    if num_periods == 0:
        return 0.0
    return (1 + cum_return) ** (periods_per_year / num_periods) - 1


def calculate_sharpe_ratio(daily_returns: pd.Series, risk_free_rate: float = 0.0, periods_per_year: int = 252) -> float:
    """
    Calculates the annualized Sharpe Ratio.
    """
    if daily_returns.empty:
        return 0.0
    excess_returns = daily_returns - (risk_free_rate / periods_per_year)
    mean_excess = excess_returns.mean()
    std_excess = excess_returns.std()

    if std_excess == 0.0 or pd.isna(std_excess):
        return 0.0

    return (mean_excess / std_excess) * np.sqrt(periods_per_year)


def calculate_sortino_ratio(
    daily_returns: pd.Series, risk_free_rate: float = 0.0, periods_per_year: int = 252
) -> float:
    """
    Calculates the annualized Sortino Ratio (only penalizing downside volatility).
    """
    if daily_returns.empty:
        return 0.0

    excess_returns = daily_returns - (risk_free_rate / periods_per_year)
    downside_returns = excess_returns[excess_returns < 0]

    mean_excess = excess_returns.mean()
    downside_std = downside_returns.std()

    if pd.isna(downside_std) or downside_std == 0.0:
        return 0.0

    return (mean_excess / downside_std) * np.sqrt(periods_per_year)


def calculate_beta(portfolio_returns: pd.Series, benchmark_returns: pd.Series) -> float:
    """
    Calculates the Beta of the portfolio relative to a benchmark.
    Both series must be aligned by date index.
    """
    aligned = pd.concat([portfolio_returns, benchmark_returns], axis=1).dropna()
    if aligned.empty or len(aligned) < 2:
        return 0.0

    cov_matrix = np.cov(aligned.iloc[:, 0], aligned.iloc[:, 1])
    cov_xy = cov_matrix[0, 1]
    var_y = cov_matrix[1, 1]

    if var_y == 0:
        return 0.0

    return cov_xy / var_y


def calculate_information_ratio(
    portfolio_returns: pd.Series, benchmark_returns: pd.Series, periods_per_year: int = 252
) -> float:
    """
    Calculates the Information Ratio of the portfolio relative to a benchmark.
    """
    aligned = pd.concat([portfolio_returns, benchmark_returns], axis=1).dropna()
    if aligned.empty:
        return 0.0

    active_returns = aligned.iloc[:, 0] - aligned.iloc[:, 1]
    mean_active = active_returns.mean()
    tracking_error = active_returns.std()

    if tracking_error == 0 or pd.isna(tracking_error):
        return 0.0

    return (mean_active / tracking_error) * np.sqrt(periods_per_year)


def calculate_return_after_fees(
    gross_returns: pd.Series, management_fee_bps: float, performance_fee_bps: float
) -> pd.Series:
    """
    Calculates net returns by deducting accrued management and performance fees.
    """
    if gross_returns.empty:
        return gross_returns

    # Simplified accrual: deduct daily fraction of annual management fee
    daily_mgmt_fee = (management_fee_bps / 10000) / 252

    # High watermark logic for performance fee is complex; this is a simplified daily proxy
    # In reality, perf fee is only charged on positive net profit above HWM.
    net_returns = []
    hwm = 1.0
    current_nav = 1.0

    for r in gross_returns:
        gross_nav = current_nav * (1 + r)
        # deduct mgmt fee
        gross_nav -= gross_nav * daily_mgmt_fee

        if gross_nav > hwm:
            perf_fee = (gross_nav - hwm) * (performance_fee_bps / 10000)
            gross_nav -= perf_fee
            hwm = gross_nav

        daily_net = (gross_nav / current_nav) - 1
        net_returns.append(daily_net)
        current_nav = gross_nav

    return pd.Series(net_returns, index=gross_returns.index)
