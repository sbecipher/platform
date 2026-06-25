from .interfaces import ISecurityType, ISecurity
from typing import List, Dict, Any


class CDSSecurity(ISecurity):
    """
    Auto-generated skeletal implementation for CDS positions.
    Deep math to be implemented manually.
    """

    def __init__(self, **kwargs):
        self._security_id = kwargs.get("security_id", "UNKNOWN")
        # TODO: Add dynamic parameters based on asset class

    @property
    def security_id(self) -> str:
        return self._security_id


class CDSType(ISecurityType):
    """
    Auto-generated skeletal type for CDSPlugin.
    """

    @property
    def type_id(self) -> int:
        return 0

    @property
    def type_name(self) -> str:
        return "CDS"

    @property
    def description(self) -> str:
        return "Auto-generated port of CDSPlugin"

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
        return CDSSecurity(**kwargs)
