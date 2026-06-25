from dataclasses import dataclass, field
from typing import List


@dataclass
class AccountAllocation:
    account_id: int
    account_name: str
    pre_allocation: float = 0.0
    filled_allocation: float = 0.0
    todays_allocation: float = 0.0
    include: bool = True


@dataclass
class PortfolioAllocation:
    portfolio_id: int
    pre_allocation: float = 0.0
    filled_allocation: float = 0.0
    todays_allocation: float = 0.0
    include: bool = True
    account_allocations: List[AccountAllocation] = field(default_factory=list)
