from .interfaces import ISecurityType, ISecurity
from typing import List, Dict, Any


class GeneralSecurityType(ISecurityType):
    """
    Auto-ported from GeneralSecurityPlugin
    """

    @property
    def type_id(self) -> int:
        return 33

    @property
    def type_name(self) -> str:
        return "GeneralSecurity"

    @property
    def description(self) -> str:
        return "Auto-ported GeneralSecurityPlugin"

    @property
    def build_version(self) -> str:
        return "1.0"

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

    def get_new_security(self) -> ISecurity:
        raise NotImplementedError("To be implemented")
