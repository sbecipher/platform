from dataclasses import dataclass
from typing import Any

# Auto-generated FIX DTOs ported from Sbecipher_Source/PortLib/Messaging


@dataclass
class AAAClientDTO:
    pass


@dataclass
class AAATokenDTO:
    pass


@dataclass
class AccountAllocationDTO:
    pass


@dataclass
class AesRequestDTO:
    reply_to_user: str = ""


@dataclass
class AesResponseDTO:
    pass


@dataclass
class AllocationACKDTO:
    pass


@dataclass
class AllocationsDTO:
    pass


@dataclass
class AllocTemplateRequestDTO:
    pass


@dataclass
class BlotterOrderDTO:
    pass


@dataclass
class BlotterOrderListDTO:
    pass


@dataclass
class BlotterRequestDTO:
    pass


@dataclass
class CalculateSharesRequestDTO:
    pass


@dataclass
class CalculateSharesResponseDTO:
    pass


@dataclass
class CancelRejectDTO:
    pass


@dataclass
class CreateSecurityDTO:
    pass


@dataclass
class CreateSecurityRequestDTO:
    pass


@dataclass
class DashboardSelectionPageRequestDTO:
    pass


@dataclass
class DashboardSelectionPageResponseDTO:
    pass


@dataclass
class DataFeedAuthenticationDTO:
    pass


@dataclass
class DatafeedLookupDTO:
    pass


@dataclass
class DeleteSecurityRequestDTO:
    pass


@dataclass
class ExchangeLookupDTO:
    pass


@dataclass
class ExecReportDTO:
    symbol: str = ""
    side: Any = None
    currency: str = ""
    quantity: float = 0.0
    filled_quantity: float = 0.0
    settle_date_int: int = 0
    last_price: float = 0.0
    leg_security_type: Any = None
    leg_product: Any = None
    trade_legs: Any = None


@dataclass
class ExecTemplateRequestDTO:
    pass


@dataclass
class ImportTradesRequestDTO:
    pass


@dataclass
class IOIDTO:
    pass


@dataclass
class LocateMessageDTO:
    pass


@dataclass
class LocateRequestDTO:
    pass


@dataclass
class ModifyAllocationsRequestDTO:
    pass


@dataclass
class OrderDTO:
    pass


@dataclass
class OrderRejectDTO:
    pass


@dataclass
class PortfolioDTO:
    pass


@dataclass
class PortfolioListDTO:
    pass


@dataclass
class PositionDTO:
    pass


@dataclass
class PositionListDTO:
    pass


@dataclass
class PositionListRequestDTO:
    pass


@dataclass
class PositionListResponseDTO:
    pass


@dataclass
class RunReportRequestDTO:
    pass


@dataclass
class RunReportResponseDTO:
    pass


@dataclass
class SecurityDTO:
    pass


@dataclass
class SecurityListDTO:
    pass


@dataclass
class SecurityLookupDTO:
    pass


@dataclass
class SecuritySearchRequestDTO:
    pass


@dataclass
class ShowDashboardRequestDTO:
    pass


@dataclass
class ShowDashboardResponseDTO:
    pass


@dataclass
class ShowDashboardsByPortfolioResponseDTO:
    pass


@dataclass
class SubmitOrdersRequestDTO:
    pass


@dataclass
class TargetAllocationsDTO:
    pass


@dataclass
class TargetOrderDropdownsLookupDTO:
    pass


@dataclass
class UpdateSecurityRequestDTO:
    pass


@dataclass
class WebMessageBaseDTO:
    pass


@dataclass
class WorkingOrderDTO:
    pass


@dataclass
class WorkingOrderDropdownsLookupDTO:
    pass
