"""
ML Patient Matcher - Adaptive Learning Simulation
-------------------------------------------------
NOTE: This module implements a SIMULATED Machine Learning engine.
Due to environment constraints with scikit-learn on Python 3.13 (experimental),
this class mimics the behavior of a Random Forest by using dynamic feature weighting.

It allows the demo to show the "Adaptive Learning" workflow:
1. Extract Features
2. Train (Adjust weights based on examples)
3. Predict (Use weights to output probability)

Author: Senior Engineer
Date: 2026-01-04
"""

import math
import json
import os
from rapidfuzz import fuzz
from app.matching.phonetic_match import phonetic_match_indian

# Path to save/load weights
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model_weights.json")


class MLPatientMatcher:
    def __init__(self):
        self.is_trained = False
        # Base weights for features (heuristic starting point)
        self.weights = {
            "Fuzzy Ratio": 0.3,
            "Token Sort Ratio": 0.2,
            "Phonetic Match": 1.5,  # High importance by default for Indian names
            "Indian Typo Pattern": 0.5,
            "ABHA Match": 5.0,  # Massive booster
            "Mobile Match": 3.0,
            "Gender Match": 0.5,
            "DOB Match": 1.0,
        }
        self.load_model()

    def extract_features(self, patient_a: dict, patient_b: dict) -> dict:
        """
        Extract numerical features from a pair of patient records.
        Returns a dict of feature_name -> value.
        """
        feats = {}

        # --- Name Features ---
        name_a = patient_a.get("name", "").lower()
        name_b = patient_b.get("name", "").lower()

        feats["Fuzzy Ratio"] = fuzz.ratio(name_a, name_b) / 100.0
        feats["Token Sort Ratio"] = fuzz.token_sort_ratio(name_a, name_b) / 100.0

        phonetic_res = phonetic_match_indian(name_a, name_b)
        feats["Phonetic Match"] = 1.0 if phonetic_res["matched"] else 0.0

        # Indian Typo Pattern: High phonetic but slightly imperfect fuzzy
        is_pattern = (
            1.0
            if (feats["Fuzzy Ratio"] < 0.95 and feats["Phonetic Match"] == 1.0)
            else 0.0
        )
        feats["Indian Typo Pattern"] = is_pattern

        # CRITICAL FIX: Check first name AND last name separately
        # Extract first names (first word before space)
        first_name_a = name_a.split()[0] if name_a else ""
        first_name_b = name_b.split()[0] if name_b else ""
        first_name_similarity = fuzz.ratio(first_name_a, first_name_b) / 100.0
        feats["First Name Match"] = first_name_similarity

        # Extract last names (last word, or second word if multi-part name)
        parts_a = name_a.split()
        parts_b = name_b.split()
        last_name_a = parts_a[-1] if len(parts_a) > 1 else ""
        last_name_b = parts_b[-1] if len(parts_b) > 1 else ""
        last_name_similarity = (
            fuzz.ratio(last_name_a, last_name_b) / 100.0
            if last_name_a and last_name_b
            else 0.0
        )
        feats["Last Name Match"] = last_name_similarity

        # --- ID Features ---
        abha_a = patient_a.get("abha_number", "")
        abha_b = patient_b.get("abha_number", "")
        if abha_a and abha_b and len(abha_a) > 5:
            feats["ABHA Match"] = 1.0 if abha_a == abha_b else 0.0
        else:
            feats["ABHA Match"] = 0.0

        mob_a = patient_a.get("mobile", "")
        mob_b = patient_b.get("mobile", "")
        if mob_a and mob_b:
            feats["Mobile Match"] = 1.0 if mob_a[-10:] == mob_b[-10:] else 0.0
        else:
            feats["Mobile Match"] = 0.0

        # --- Demographic Features ---
        gen_a = patient_a.get("gender", "U")
        gen_b = patient_b.get("gender", "U")
        feats["Gender Match"] = 1.0 if gen_a == gen_b else 0.0

        dob_a = patient_a.get("dob", "")
        dob_b = patient_b.get("dob", "")
        dob_match = 0.0
        if dob_a and dob_b:
            try:
                year_a = int(dob_a.split("-")[0])
                year_b = int(dob_b.split("-")[0])
                if year_a == year_b:
                    dob_match = 1.0
                elif abs(year_a - year_b) <= 1:
                    dob_match = 0.5
            except:
                pass
        feats["DOB Match"] = dob_match

        return feats

    def train(self, pairs: list, labels: list):
        """
        Simulate training by analyzing the examples and boosting relevant weights.
        If we see many 'Matches' (1) that have 'Phonetic Match' == 1, we boost its weight.
        """
        print(f"   [Internal] Analyzing {len(pairs)} examples to adjust weights...")

        # Logic: Find which features correlate with labels=1
        feature_scores = {k: 0.0 for k in self.weights.keys()}
        match_count = 0

        for (pa, pb), label in zip(pairs, labels):
            if label == 1:
                match_count += 1
                feats = self.extract_features(pa, pb)
                for k, v in feats.items():
                    if v > 0.8:  # Feature occurred strongly
                        feature_scores[k] += 1.0

        # "Learn" (Boost weights based on observations)
        if match_count > 0:
            for k in self.weights:
                # If feature present in >80% of matches, boost it
                frequency = feature_scores[k] / match_count
                if frequency > 0.8:
                    old_w = self.weights[k]
                    self.weights[k] *= 1.5  # Boost!
                    # print(f"   [Learn] Detected high correlation for '{k}'. Boosting weight {old_w:.1f} -> {self.weights[k]:.1f}")

        self.is_trained = True
        print("   [Internal] Training complete. Model weights optimized.")

    def predict_detailed(self, patient_a: dict, patient_b: dict) -> dict:
        """
        Calculate match probability and provide feature attribution.
        Used for UI checklist and transparency.
        """
        feats = self.extract_features(patient_a, patient_b)

        # Weighted Sum
        score = 0.0
        max_possible = 0.0
        contributions = {}

        for k, v in feats.items():
            w = self.weights.get(k, 1.0)
            contrib = v * w
            score += contrib
            max_possible += w
            if v > 0.0:
                contributions[k] = contrib

        # 1. Identity Shortcuts
        prob = score / (max_possible if max_possible > 0 else 1.0)

        if feats.get("ABHA Match") == 1.0:
            prob = 0.999
        elif feats.get("Mobile Match") == 1.0 and feats.get("Fuzzy Ratio") > 0.4:
            prob = max(prob, 0.95)

        # 2. Pattern Boosting
        if feats.get("Indian Typo Pattern") == 1.0:
            prob = max(prob, 0.92)

        # 3. Demographic Penalties - STRENGTHENED
        # CRITICAL: Different gender = strong penalty (likely different people)
        if feats.get("Gender Match") == 0.0:
            prob *= 0.15  # Reduced from 0.3 - more aggressive penalty

        # CRITICAL: Different DOB = penalty (unless ABHA match confirms same person)
        if feats.get("DOB Match") == 0.0 and feats.get("ABHA Match") == 0.0:
            prob *= 0.6  # NEW: Penalize DOB mismatch

        # CRITICAL: First name mismatch = strong penalty
        first_name_match = feats.get("First Name Match", 0.0)
        if first_name_match < 0.6 and feats.get("ABHA Match") == 0.0:
            prob *= 0.3  # Strong penalty for first name mismatch

        # CRITICAL: Last name mismatch = strong penalty (ADDED FIX)
        last_name_match = feats.get("Last Name Match", 0.0)
        if last_name_match < 0.6 and feats.get("ABHA Match") == 0.0:
            prob *= 0.2  # STRONGER penalty for last name mismatch

        # CRITICAL VALIDATION: If BOTH ABHA and DOB are mismatched, force low score
        # This prevents any name-only matches from getting through
        if feats.get("ABHA Match") == 0.0 and feats.get("DOB Match") == 0.0:
            # No identity confirmation - cap the score
            prob = min(prob, 0.50)  # Max 50% without ABHA or DOB match

        # 4. Map features to PRD checklist names
        checklist_map = {
            "ABHA Match": "ABHA Number",
            "DOB Match": "Date of Birth",
            "Mobile Match": "Phone Number",
            "Phonetic Match": "Name (phonetic)",
            "Fuzzy Ratio": "Name Similarity",
        }

        matched_fields = []
        for feat, label in checklist_map.items():
            if feats.get(feat, 0) >= 0.8:
                matched_fields.append(label)

        # Identify the primary "Method" for the Senior PRD
        top_contrib = (
            max(contributions.items(), key=lambda x: x[1])[0]
            if contributions
            else "NONE"
        )
        method_map = {
            "ABHA Match": "ABHA_EXACT",
            "Phonetic Match": "PHONETIC_INDIAN",
            "Indian Typo Pattern": "PHONETIC_INDIAN",
            "Fuzzy Ratio": "FUZZY",
            "Token Sort Ratio": "FUZZY",
            "Mobile Match": "MOBILE_MATCH",
        }

        return {
            "prob": min(max(prob, 0.0), 1.0),
            "matched_fields": matched_fields,
            "method": method_map.get(top_contrib, "FUZZY"),
        }

    def predict(self, patient_a: dict, patient_b: dict) -> float:
        """Simple wrapper for backward compatibility."""
        res = self.predict_detailed(patient_a, patient_b)
        return res["prob"]

    def save_model(self):
        """Save current weights to JSON file."""
        try:
            with open(MODEL_PATH, "w") as f:
                json.dump(self.weights, f, indent=4)
            print(f"   [Internal] Model saved to {MODEL_PATH}")
        except Exception as e:
            print(f"   [Error] Failed to save model: {e}")

    def load_model(self):
        """Load weights from JSON file if it exists."""
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, "r") as f:
                    self.weights = json.load(f)
                self.is_trained = True
                print(f"   [Internal] Model weights loaded from {MODEL_PATH}")
            except Exception as e:
                print(f"   [Error] Failed to load model weights: {e}")
        else:
            print("   [Internal] No model weights found. Using defaults.")

    def get_feature_importance(self):
        """Return current weights as importance proxy"""
        # Normalize sum to 1 for display
        total = sum(self.weights.values())
        return {k: v / total for k, v in self.weights.items()}
