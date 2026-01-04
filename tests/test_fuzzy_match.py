"""
Unit Tests for Fuzzy Matching

Tests the fuzzy string matching algorithm using RapidFuzz.
"""

import pytest
from app.matching.fuzzy_match import fuzzy_match


class TestFuzzyMatch:
    """Test suite for fuzzy matching"""
    
    def test_exact_match(self):
        """Test exact name match"""
        result = fuzzy_match("Ramesh Singh", "Ramesh Singh")
        
        assert result["matched"] is True
        assert result["score"] == 100.0
        assert result["method"] == "FUZZY"
    
    def test_high_similarity_match(self):
        """Test high similarity (>= 80%)"""
        result = fuzzy_match("Ramesh Kumar Singh", "Ramesh K Singh")
        
        assert result["matched"] is True
        assert result["score"] >= 80.0
    
    def test_low_similarity_no_match(self):
        """Test low similarity (< 80%)"""
        result = fuzzy_match("Ramesh Singh", "Completely Different")
        
        assert result["matched"] is False
        assert result["score"] < 80.0
    
    def test_case_insensitive(self):
        """Test case insensitivity"""
        result = fuzzy_match("RAMESH SINGH", "ramesh singh")
        
        assert result["matched"] is True
        assert result["score"] == 100.0
    
    def test_empty_names(self):
        """Test empty names"""
        result = fuzzy_match("", "Ramesh")
        
        assert result["matched"] is False
        assert result["score"] == 0.0
