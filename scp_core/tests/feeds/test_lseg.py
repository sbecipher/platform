import pytest
from unittest.mock import patch, MagicMock
from scp_core.feeds.lseg_fundamentals import LSEGFundamentalsEngine

@patch('scp_core.feeds.lseg_fundamentals.get_settings')
def test_lseg_fundamentals_engine_init_missing_credentials(mock_get_settings):
    # Mock settings with missing credentials
    mock_settings = MagicMock()
    mock_settings.lseg_app_key = None
    mock_get_settings.return_value = mock_settings

    engine = LSEGFundamentalsEngine()
    assert not engine.session_active

@patch('scp_core.feeds.lseg_fundamentals.get_settings')
def test_lseg_fundamentals_engine_fallback_data(mock_get_settings):
    # Mock settings missing
    mock_settings = MagicMock()
    mock_settings.lseg_app_key = None
    mock_get_settings.return_value = mock_settings

    engine = LSEGFundamentalsEngine()
    results = engine.fetch_fundamentals(['AAPL', 'MP'])
    
    assert 'AAPL' in results
    assert 'MP' in results
    
    # Check AAPL calculations (Positive NOPAT)
    assert results['AAPL']['operating_income'] == 1000000.0
    assert results['AAPL']['tax_rate'] == 0.21
    assert results['AAPL']['nopat'] == 790000.0 # 1000000 * (1 - 0.21)
    assert not results['AAPL']['is_negative_nopat']
    
    # Check MP calculations (Negative NOPAT)
    assert results['MP']['operating_income'] == -500000.0
    assert results['MP']['nopat'] == -395000.0
    assert results['MP']['is_negative_nopat']

@patch('scp_core.feeds.lseg_fundamentals.get_settings')
def test_lseg_fundamentals_engine_update_ledger(mock_get_settings):
    mock_settings = MagicMock()
    mock_settings.lseg_app_key = None
    mock_get_settings.return_value = mock_settings

    engine = LSEGFundamentalsEngine()
    
    # Mock DB Session and query chain
    mock_db = MagicMock()
    mock_query = mock_db.query.return_value
    mock_filter = mock_query.filter_by.return_value
    
    # Mock the TargetAllocation object returned
    mock_allocation = MagicMock()
    mock_filter.first.return_value = mock_allocation
    
    engine.update_target_ledger(mock_db, ['MP'])
    
    # Assert DB commit was called
    mock_db.commit.assert_called_once()
    
    # Assert that is_negative_nopat was set to True since MP is negative
    assert mock_allocation.is_negative_nopat is True
