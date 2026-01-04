"""
Unit Tests for ABHA Exact Matching

Tests the ABHA exact matching algorithm with various scenarios.
"""

import pytest
from app.matching.abha_match import abha_exact_match


class TestABHAExactMatch:
    """Test suite for ABHA exact matching"""
    
    def test_exact_match_with_same_format(self):
        """Test ABHA numbers that match with same format"""
        patient_a = {"abha_number": "12-3456-7890-1234"}
        patient_b = {"abha_number": "12-3456-7890-1234"}
        
        result = abha_exact_match(patient_a, patient_b)
        
        assert result["matched"] is True
        assert result["score"] == 100.0
        assert result["method"] == "ABHA_EXACT"
    
    def test_exact_match_with_different_formats(self):
        """Test ABHA numbers that match but have different formats"""
        patient_a = {"abha_number": "12-3456-7890-1234"}
        patient_b = {"abha_number": "12 3456 7890 1234"}
        
        result = abha_exact_match(patient_a, patient_b)
        
        assert result["matched"] is True
        assert result["score"] == 100.0
    
    def test_no_match_different_numbers(self):
        """Test ABHA numbers that don't match"""
        patient_a = {"abha_number": "12-3456-7890-1234"}
        patient_b = {"abha_number": "12-3456-7890-5678"}
        
        result = abha_exact_match(patient_a, patient_b)
        
        assert result["matched"] is False
        assert result["score"] == 0.0
    
    def test_missing_abha_patient_a(self):
        """Test when patient A has no ABHA number"""
        patient_a = {"abha_number": None}
        patient_b = {"abha_number": "12-3456-7890-1234"}
        
        result = abha_exact_match(patient_a, patient_b)
        
        assert result["matched"] is False
        assert result["score"] == 0.0
        assert "missing" in result["details"].lower()
    
    def test_missing_abha_both_patients(self):
        """Test when both patients have no ABHA number"""
        patient_a = {}
        patient_b = {}
        
        result = abha_exact_match(patient_a, patient_b)
        
        assert result["matched"] is False
        assert result["score"] == 0.0
