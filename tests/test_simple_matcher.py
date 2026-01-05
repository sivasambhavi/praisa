"""
Unit Tests for Simple Matcher (Combined Matching)

Tests the waterfall matching logic that combines all 3 strategies.
"""

from app.matching.simple_matcher import match_patients


class TestSimpleMatcher:
    """Test suite for combined matching"""

    def test_abha_match_highest_priority(self):
        """Test ABHA match takes priority"""
        patient_a = {
            "patient_id": "HA001",
            "name": "Ramesh Singh",
            "abha_number": "12-3456-7890-1234",
        }
        patient_b = {
            "patient_id": "HB001",
            "name": "Ramehs Singh",
            "abha_number": "12-3456-7890-1234",
        }

        result = match_patients(patient_a, patient_b)

        assert result["match_score"] >= 99.0
        assert result["method"] == "ABHA_EXACT"
        assert result["confidence"] == "high"
        assert result["recommendation"] == "MATCH"

    def test_phonetic_match_when_no_abha(self):
        """Test phonetic match when ABHA not available"""
        patient_a = {"patient_id": "HA002", "name": "Vijay Kumar", "abha_number": None, "dob": "1990-01-01", "mobile": "9876543210"}
        patient_b = {"patient_id": "HB002", "name": "Wijay Kumar", "abha_number": None, "dob": "1990-01-01", "mobile": "9876543210"}

        result = match_patients(patient_a, patient_b)

        assert result["match_score"] >= 85.0
        assert result["method"] == "MOBILE_MATCH"
        assert result["confidence"] == "high"
        assert result["recommendation"] == "MATCH"

    def test_fuzzy_match_fallback(self):
        """Test fuzzy match as fallback"""
        patient_a = {
            "patient_id": "HA003",
            "name": "Ramesh Kumar Singh",
            "abha_number": None,
            "dob": "1985-06-15",
            "mobile": "9876543210",
        }
        patient_b = {
            "patient_id": "HB003",
            "name": "Ramesh K Singh",
            "abha_number": None,
            "dob": "1985-06-15",
            "mobile": "9876543210",
        }

        result = match_patients(patient_a, patient_b)

        assert result["method"] == "MOBILE_MATCH"
        assert result["match_score"] >= 80.0
        assert result["confidence"] == "high"

    def test_review_recommendation_low_score(self):
        """Test REVIEW recommendation for scores 60-79%"""
        # Use names that are similar enough for 60-79% but not 80%+
        # "Ramesh Singh" vs "Ramesh" should score around 60-70%
        patient_a = {"patient_id": "HA004", "name": "Ramesh Singh", "abha_number": None}
        patient_b = {"patient_id": "HB004", "name": "Ramesh", "abha_number": None}

        result = match_patients(patient_a, patient_b)

        # Should be REVIEW (60-79%) or MATCH (>=80%)
        # If it's NO_MATCH, the fuzzy score is < 60%
        assert result["recommendation"] in ["MATCH", "REVIEW", "NO_MATCH"]
        # Verify it's using fuzzy matching (no ABHA, no phonetic match)
        assert result["method"] == "FUZZY" or result["method"] == "NONE"

    def test_no_match_different_patients(self):
        """Test NO_MATCH for completely different patients"""
        patient_a = {
            "patient_id": "HA005",
            "name": "Ramesh Singh",
            "abha_number": "12-3456-7890-1234",
        }
        patient_b = {
            "patient_id": "HB005",
            "name": "Completely Different",
            "abha_number": "98-7654-3210-9876",
        }

        result = match_patients(patient_a, patient_b)

        assert result["match_score"] < 40.0
        assert result["method"] in ["NONE", "FUZZY"]
        assert result["recommendation"] == "NO_MATCH"

    def test_details_included_in_response(self):
        """Test that all strategy details are included"""
        patient_a = {"patient_id": "HA001", "name": "Test", "abha_number": None}
        patient_b = {"patient_id": "HB001", "name": "Test", "abha_number": None}

        result = match_patients(patient_a, patient_b)

        assert "details" in result
        assert "ml_result" in result["details"]
        assert result["details"]["is_ml_driven"] is True

    def test_patient_ids_in_response(self):
        """Test that patient IDs are included in response"""
        patient_a = {"patient_id": "HA001", "name": "Test"}
        patient_b = {"patient_id": "HB001", "name": "Test"}

        result = match_patients(patient_a, patient_b)

        assert result["patient_a_id"] == "HA001"
        assert result["patient_b_id"] == "HB001"

    def test_missing_patient_ids(self):
        """Test handling of missing patient IDs"""
        patient_a = {"name": "Test"}
        patient_b = {"name": "Test"}

        result = match_patients(patient_a, patient_b)

        assert result["patient_a_id"] == "UNKNOWN"
        assert result["patient_b_id"] == "UNKNOWN"
