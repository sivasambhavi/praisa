"""
Custom Exception Classes for PRAISA

Defines domain-specific exceptions for better error handling and debugging.
All custom exceptions inherit from base Exception class.
"""


class PraisaException(Exception):
    """Base exception for all PRAISA-specific errors"""

    pass


class PatientNotFoundException(PraisaException):
    """
    Raised when a patient is not found in the database.

    Example:
        >>> patient = get_patient("INVALID_ID")
        >>> if not patient:
        >>>     raise PatientNotFoundException(f"Patient INVALID_ID not found")
    """

    pass


class MatchingException(PraisaException):
    """
    Raised when matching algorithm encounters an error.

    Example:
        >>> try:
        >>>     result = match_patients(patient_a, patient_b)
        >>> except Exception as e:
        >>>     raise MatchingException(f"Matching failed: {str(e)}")
    """

    pass


class DatabaseException(PraisaException):
    """
    Raised when database operations fail.

    Example:
        >>> try:
        >>>     db.execute(query)
        >>> except SQLAlchemyError as e:
        >>>     raise DatabaseException(f"Database error: {str(e)}")
    """

    pass


class ValidationException(PraisaException):
    """
    Raised when input validation fails.

    Example:
        >>> if not patient_id:
        >>>     raise ValidationException("Patient ID is required")
    """

    pass


class ABHAValidationException(ValidationException):
    """
    Raised when ABHA number validation fails.

    Example:
        >>> if not is_valid_abha(abha_number):
        >>>     raise ABHAValidationException(f"Invalid ABHA format: {abha_number}")
    """

    pass
