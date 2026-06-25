from enum import Enum


class OrderTimeInForce(Enum):
    DAY = 1
    GTC = 2
    OPG = 3
    IOC = 4
    FOK = 5
    GTX = 6
    GTD = 7


class OrderAction(Enum):
    BUY = 1
    SELL = 2
    SHORT = 3
    COVER = 4


class CommissionCalcType(Enum):
    PER_SHARE = 1
    PERCENTAGE = 2
    FLAT = 3
    BASIS_POINTS = 4


class OrdersSettlementTypeEnum(Enum):
    REGULAR = 1
    CASH = 2
    NEXT_DAY = 3
    T_PLUS_1 = 4
    T_PLUS_2 = 5
    T_PLUS_3 = 6
    SELLERS_OPTION = 7
    WHEN_ISSUED = 8
