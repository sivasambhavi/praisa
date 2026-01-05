def calculate_data_quality(patient: dict) -> tuple[int, list[str]]:
    """
    Calculate data quality score (0-100) for a patient record.

    Scoring Logic:
    - ABHA Number: +40 points (Gold Standard ID)
    - Mobile Number: +20 points (Verifiable Contact)
    - Date of Birth: +10 points (Clinical Critical)
    - Address: +10 points (Demographic Critical)
    - Gender: +10 points (Demographic Critical)
    - Name: +10 points (Basic Identity - always present essentially)

    Total Possible: 100

    Args:
        patient: Patient dictionary or object

    Returns:
        tuple: (score: int, missing_fields: list[str])
    """
    score = 0
    missing_fields = []

    # helper to check if field exists and is not empty
    def has_value(key):
        val = patient.get(key)
        return val is not None and str(val).strip() != ""

    # 1. Name (+10)
    if has_value("name"):
        score += 10
    else:
        missing_fields.append("Name")

    # 2. ABHA Number (+40) - The most critical identifier
    if has_value("abha_number"):
        score += 40
    else:
        missing_fields.append("ABHA Number")

    # 3. Mobile (+20)
    if has_value("mobile"):
        score += 20
    else:
        missing_fields.append("Mobile Number")

    # 4. Date of Birth (+10)
    if has_value("dob"):
        score += 10
    else:
        missing_fields.append("Date of Birth")

    # 5. Gender (+10)
    if has_value("gender"):
        score += 10
    else:
        missing_fields.append("Gender")

    # 6. Address (+10)
    if has_value("address"):
        score += 10
    else:
        missing_fields.append("Address")

    return score, missing_fields
