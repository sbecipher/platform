import lseg.data as ld
import pandas as pd
from typing import List, Dict, Set, Optional
from datetime import date


class RefinitivFeed:
    """
    Modern lseg-lib-python implementation replacing the legacy C# COM/DLL based feed adaptors
    (EikonFeedAdaptor / ReutersDatascopeFeedAdaptor).
    """

    # Legacy field mappings ported from C# implementations
    MNA_FIELDS = [
        "TR.MnAAcquirorPermId",
        "TR.MnATargetPermId",
        "TR.MnASynopsis",
        "TR.MnAEffectiveDate",
        "TR.MnAExpectedEffectiveDate",
    ]

    SPINOFF_FIELDS = ["TR.CACorpActDesc", "TR.CAEffectiveDate", "TR.CATermsNewShares", "TR.CATermsOldShares"]

    DIVIDEND_FIELDS = ["TR.DivUnadjustedGross", "TR.DivPayDate", "TR.DivExDate"]

    RIC_FIELD = "TR.RIC"
    PERM_ID_FIELD = "TR.OrganizationID"

    def __init__(self, session_name: Optional[str] = None):
        """
        Initialize the feed and open the session using modern lseg-lib-python.
        """
        try:
            if session_name:
                ld.open_session(name=session_name)
            else:
                ld.open_session()
            self.is_connected = True
        except Exception as e:
            self.is_connected = False
            print(f"Failed to connect to LSEG session: {e}")

    def get_corporate_actions(self, tickers: Set[str], start_date: date, end_date: date) -> Dict[str, pd.DataFrame]:
        """
        Consolidated method translating `GetCorporateActions` logic.
        Fetches M&A and SpinOff data using lseg.data.get_data.
        """
        results = {}

        # M&A Request
        mna_params = {"SDate": start_date.strftime("%Y%m%d"), "EDate": end_date.strftime("%Y%m%d")}
        try:
            mna_df = ld.get_data(universe=list(tickers), fields=self.MNA_FIELDS, parameters=mna_params)
            results["MNA"] = mna_df
        except Exception as e:
            print(f"Error fetching Mergers: {e}")

        # SpinOff Request
        spinoff_params = {
            "SDate": start_date.strftime("%Y%m%d"),
            "EDate": end_date.strftime("%Y%m%d"),
            "DateType": "ED",
            "CAEventType": "DEM:RIS",
        }
        try:
            spinoff_df = ld.get_data(universe=list(tickers), fields=self.SPINOFF_FIELDS, parameters=spinoff_params)
            results["SPINOFF"] = spinoff_df
        except Exception as e:
            print(f"Error fetching Spinoffs: {e}")

        return results

    def get_time_series_data(self, tickers: Set[str], field: str) -> pd.DataFrame:
        """
        Translates `GetTimeSeriesData` logic, mapping specific parameters (e.g., TR.FIIndexRatio).
        """
        parameters = {}
        if field.lower() == "tr.fiindexratio":
            parameters = {"SDate": "2M", "EDate": "-1M"}

        try:
            return ld.get_data(universe=list(tickers), fields=[field], parameters=parameters)
        except Exception as e:
            print(f"Error fetching Time Series Data for {field}: {e}")
            return pd.DataFrame()

    def subscribe_pricing(self, tickers: List[str], fields: List[str], on_update_callback=None):
        """
        Translates AdxRtList / streaming pricing data handling into lseg.data StreamingPrices.
        """

        def default_on_update(streaming_item, update):
            print(f"Update received for {streaming_item.name}: {update}")

        callback = on_update_callback if on_update_callback else default_on_update

        try:
            stream = ld.StreamingPrices(universe=tickers, fields=fields, on_update=callback)
            stream.open()
            return stream
        except Exception as e:
            print(f"Error starting streaming subscription: {e}")
            return None

    def close(self):
        """
        Close the active LSEG session.
        """
        ld.close_session()
        self.is_connected = False
