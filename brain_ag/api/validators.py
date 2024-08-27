from django.forms import ValidationError
from validate_docbr import CNPJ, CPF

cpf_validator = CPF()
cnpj_validator = CNPJ()


def validate_doc_number(value):
    """
    Validate CPF or CNPJ using the pycpfcnpj library.

    :param value: The document number to validate.
    :raises ValidationError: If the document number is invalid.
    """
    # Determine if value should be validated as CPF or CNPJ
    if not value:
        raise ValidationError("This field cannot be empty.")

    # Check if it's a CPF or CNPJ based on length and format
    if len(value) == 11:  # CPF has 11 digits
        if not cpf_validator.validate(value):
            raise ValidationError("Invalid CPF number.")
    elif len(value) == 14:  # CNPJ has 14 digits
        if not cnpj_validator.validate(value):
            raise ValidationError("Invalid CNPJ number.")
    else:
        raise ValidationError(
            "Document number must be either CPF (11 digits) or CNPJ (14 digits)."
        )


def validate_areas(arable_area, vegetation_area, total_area):
    """
    Check that the sum of arable and vegetation areas does not exceed the total area.

    Ensures that the combined area of arable land and vegetation is less than or equal
    to the total farm area. Raises a `ValidationError` if this condition is not met.

    Args:
        arable_area (Decimal): The area used for farming, in hectares.
        vegetation_area (Decimal): The area covered by vegetation, in hectares.
        total_area (Decimal): The total farm area, in hectares.

    Raises:
        ValidationError: If the sum of `arable_area` and `vegetation_area` is greater than `total_area`.
    """
    if arable_area + vegetation_area > total_area:
        raise ValidationError(
            "The sum of arable and vegetation areas cannot exceed the total area."
        )
