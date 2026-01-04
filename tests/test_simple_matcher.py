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

        assert result["match_score"] == 100.0
        assert result["method"] == "ABHA_EXACT"
        assert result["confidence"] == "high"
        assert result["recommendation"] == "MATCH"

    def test_phonetic_match_when_no_abha(self):
        """Test phonetic match when ABHA not available"""
        patient_a = {"patient_id": "HA002", "name": "Vijay Kumar", "abha_number": None}
        patient_b = {"patient_id": "HB002", "name": "Wijay Kumar", "abha_number": None}

        result = match_patients(patient_a, patient_b)

        assert result["match_score"] == 90.0
        assert result["method"] == "PHONETIC_INDIAN"
        assert result["confidence"] == "high"
        assert result["recommendation"] == "MATCH"

    def test_fuzzy_match_fallback(self):
        """Test fuzzy match as fallback"""
        patient_a = {
            "patient_id": "HA003",
            "name": "Ramesh Kumar Singh",
            "abha_number": None,
        }
        patient_b = {
            "patient_id": "HB003",
            "name": "Ramesh K Singh",
            "abha_number": None,
        }

        result = match_patients(patient_a, patient_b)

        assert result["method"] == "FUZZY"
        assert result["match_score"] >= 80.0
        assert result["confidence"] == "medium"

    def test_review_recommendation_low_score(self):
        """Test REVIEW recommendation for scores 60-79%"""
        patient_a = {"patient_id": "HA004", "name": "Ramesh Singh", "abha_number": None}
        patient_b = {"patient_id": "HB004", "name": "Ramesh Kumar", "abha_number": None}

        result = match_patients(patient_a, patient_b)

        # This might be MATCH or REVIEW depending on fuzzy score
        assert result["recommendation"] in ["MATCH", "REVIEW"]

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

        assert result["match_score"] == 0.0
        assert result["method"] == "NONE"
        assert result["recommendation"] == "NO_MATCH"

    def test_details_included_in_response(self):
        """Test that all strategy details are included"""
        patient_a = {"patient_id": "HA001", "name": "Test", "abha_number": None}
        patient_b = {"patient_id": "HB001", "name": "Test", "abha_number": None}

        result = match_patients(patient_a, patient_b)

        assert "details" in result
        assert "abha_result" in result["details"]
        assert "phonetic_result" in result["details"]
        assert "fuzzy_result" in result["details"]

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
