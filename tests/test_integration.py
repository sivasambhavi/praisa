"""
Integration Tests for PRAISA

Tests end-to-end functionality including database and API integration.
"""

import pytest
from app.database.db import get_patient
from app.matching.simple_matcher import match_patients


class TestGoldenPairsIntegration:
    """Integration tests using golden pairs from database"""

    # Golden pairs with expected match results
    GOLDEN_PAIRS = [
        ("HA001", "HB001", "Ramesh Singh", "Ramehs Singh"),
        ("HA002", "HB002", "Priya Sharma", "Prya Sharma"),
        ("HA003", "HB003", "Vijay Kumar", "Wijay Kumar"),
        ("HA004", "HB004", "Amit Kumar", "Amit Kumarr"),
        ("HA005", "HB005", "Sunita Gupta", "Suneeta Gupta"),
    ]

    @pytest.mark.parametrize("ha_id,hb_id,name_a,name_b", GOLDEN_PAIRS)
    def test_golden_pair_matches(self, ha_id, hb_id, name_a, name_b):
        """Test that all golden pairs match correctly"""
        # Get patients from database
        patient_a = get_patient(ha_id)
        patient_b = get_patient(hb_id)

        # Skip if database not set up
        if not patient_a or not patient_b:
            pytest.skip(
                f"Database not initialized or patients {ha_id}/{hb_id} not found"
            )

        # Match patients
        result = match_patients(patient_a, patient_b)

        # All golden pairs should match with high confidence
        assert (
            result["match_score"] >= 90.0
        ), f"Expected >= 90% match for {ha_id} and {hb_id}"
        assert result["recommendation"] == "MATCH"
        assert result["confidence"] == "high"

    def test_all_golden_pairs_have_same_abha(self):
        """Verify all golden pairs share the same ABHA number"""
        for ha_id, hb_id, _, _ in self.GOLDEN_PAIRS:
            patient_a = get_patient(ha_id)
            patient_b = get_patient(hb_id)

            if not patient_a or not patient_b:
                pytest.skip("Database not initialized")

            # Normalize ABHA numbers for comparison
            abha_a = (
                str(patient_a.get("abha_number", "")).replace(" ", "").replace("-", "")
            )
            abha_b = (
                str(patient_b.get("abha_number", "")).replace(" ", "").replace("-", "")
            )

            assert abha_a == abha_b, f"ABHA mismatch for {ha_id} and {hb_id}"


class TestDatabaseIntegration:
    """Integration tests for database operations"""

    def test_get_patient_exists(self):
        """Test retrieving an existing patient"""
        patient = get_patient("HA001")

        if not patient:
            pytest.skip("Database not initialized")

        assert patient["patient_id"] == "HA001"
        assert "name" in patient
        assert "abha_number" in patient

    def test_get_patient_not_exists(self):
        """Test retrieving a non-existent patient"""
        patient = get_patient("INVALID_ID")

        assert patient is None


class TestEndToEndMatching:
    """End-to-end matching tests"""

    def test_complete_matching_workflow(self):
        """Test complete workflow: fetch patients -> match -> verify result"""
        # Fetch two patients
        patient_a = get_patient("HA001")
        patient_b = get_patient("HB001")

        if not patient_a or not patient_b:
            pytest.skip("Database not initialized")

        # Match them
        result = match_patients(patient_a, patient_b)

        # Verify comprehensive result structure
        assert "match_score" in result
        assert "confidence" in result
        assert "method" in result
        assert "recommendation" in result
        assert "patient_a_id" in result
        assert "patient_b_id" in result
        assert "details" in result

        # Verify details contain all strategy results
        assert "ml_result" in result["details"]
        assert result["details"]["is_ml_driven"] is True
