from .interfaces import ISecurityType, ISecurity
from typing import List, Dict, Any


class AmortizingBondSecurity(ISecurity):
    """
    Auto-generated skeletal implementation for AmortizingBond positions.
    Deep math to be implemented manually.
    """

    def __init__(self, **kwargs):
        self._security_id = kwargs.get("security_id", "UNKNOWN")
        # TODO: Add dynamic parameters based on asset class

    @property
    def security_id(self) -> str:
        return self._security_id


class AmortizingBondType(ISecurityType):
    """
    Auto-generated skeletal type for AmortizingBondPlugin.
    """

    @property
    def type_id(self) -> int:
        return 0

    @property
    def type_name(self) -> str:
        return "AmortizingBond"

    @property
    def description(self) -> str:
        return "Auto-generated port of AmortizingBondPlugin"

    @property
    def build_version(self) -> str:
        return "1.0.0"

    @property
    def default_pricing_model(self) -> str:
        return "Default"

    @property
    def contract_size(self) -> float:
        return 1.0

    @property
    def quote_size(self) -> float:
        return 1.0

    @property
    def is_fx_security(self) -> bool:
        return False

    def get_column_info(self) -> List[Dict[str, Any]]:
        return []

    def get_market_data_ids(self) -> List[str]:
        return []

    def get_new_security(self, **kwargs) -> ISecurity:
        return AmortizingBondSecurity(**kwargs)
