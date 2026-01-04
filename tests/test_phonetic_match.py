"""
Unit Tests for Phonetic Matching (Indian Names)

Tests the phonetic matching algorithm optimized for Indian names.
This is the WOW FACTOR of PRAISA!
"""

from app.matching.phonetic_match import (
    phonetic_match_indian,
    normalize_indian_name
)


class TestNormalizeIndianName:
    """Test suite for Indian name normalization"""

    def test_v_to_w_transliteration(self):
        """Test v→w transliteration"""
        assert normalize_indian_name("Vijay") == normalize_indian_name("Wijay")

    def test_s_to_sh_transliteration(self):
        """Test s→sh transliteration"""
        assert normalize_indian_name("Suresh") == normalize_indian_name("Shuresh")

    def test_vowel_elongation_aa(self):
        """Test a→aa vowel variation"""
        assert normalize_indian_name("Ram") == normalize_indian_name("Raam")

    def test_vowel_elongation_ee(self):
        """Test i→ee vowel variation"""
        assert normalize_indian_name("Sunita") == normalize_indian_name("Suneeta")


class TestPhoneticMatchIndian:
    """Test suite for phonetic matching"""

    def test_ramesh_ramehs_typo(self):
        """Test: Ramesh vs Ramehs (typo)"""
        result = phonetic_match_indian("Ramesh Singh", "Ramehs Singh")

        assert result["matched"] is True
        assert result["score"] == 90.0
        assert result["method"] == "PHONETIC_INDIAN"

    def test_priya_prya_dropped_vowel(self):
        """Test: Priya vs Prya (dropped vowel)"""
        result = phonetic_match_indian("Priya Sharma", "Prya Sharma")

        assert result["matched"] is True
        assert result["score"] == 90.0

    def test_vijay_wijay_transliteration(self):
        """Test: Vijay vs Wijay (v→w)"""
        result = phonetic_match_indian("Vijay Kumar", "Wijay Kumar")

        assert result["matched"] is True
        assert result["score"] == 90.0

    def test_sunita_suneeta_vowel_variation(self):
        """Test: Sunita vs Suneeta (i→ee)"""
        result = phonetic_match_indian("Sunita Gupta", "Suneeta Gupta")

        assert result["matched"] is True
        assert result["score"] == 90.0

    def test_amit_kumarr_extra_letter(self):
        """Test: Amit Kumar vs Amit Kumarr (extra r)"""
        result = phonetic_match_indian("Amit Kumar", "Amit Kumarr")

        assert result["matched"] is True
        assert result["score"] == 90.0

    def test_different_names_no_match(self):
        """Test: Different names should not match"""
        result = phonetic_match_indian("Amit Kumar", "Sumit Kumar")

        assert result["matched"] is False
        assert result["score"] == 0.0

    def test_empty_names(self):
        """Test: Empty names should not match"""
        result = phonetic_match_indian("", "Ramesh")

        assert result["matched"] is False
        assert result["score"] == 0.0
