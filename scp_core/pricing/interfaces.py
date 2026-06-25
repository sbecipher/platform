from abc import ABC, abstractmethod
from typing import List, Dict, Any


class ISecurity(ABC):
    """
    Represents an individual financial security/instrument instance.
    """

    @property
    @abstractmethod
    def security_id(self) -> str:
        pass


class ISecurityType(ABC):
    """
    Defines the contract for a financial instrument plugin (e.g. Bond, Cash, Options).
    Ported from PluginInterface.ISecurityType
    """

    @property
    @abstractmethod
    def type_id(self) -> int:
        pass

    @property
    @abstractmethod
    def type_name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def build_version(self) -> str:
        pass

    @property
    @abstractmethod
    def default_pricing_model(self) -> str:
        pass

    @property
    @abstractmethod
    def contract_size(self) -> float:
        pass

    @property
    @abstractmethod
    def quote_size(self) -> float:
        pass

    @property
    @abstractmethod
    def is_fx_security(self) -> bool:
        pass

    @abstractmethod
    def get_column_info(self) -> List[Dict[str, Any]]:
        """Returns metadata about the columns required by this security."""

    @abstractmethod
    def get_market_data_ids(self) -> List[str]:
        """Returns the IDs required for market data feeds."""

    @abstractmethod
    def get_new_security(self) -> ISecurity:
        """Instantiates a new ISecurity object of this type."""
