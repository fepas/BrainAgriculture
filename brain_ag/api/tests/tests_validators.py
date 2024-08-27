from decimal import Decimal

from api.validators import validate_areas, validate_doc_number
from django.core.exceptions import ValidationError
from django.test import TestCase
from validate_docbr import CNPJ, CPF

cpf_validator = CPF()
cnpj_validator = CNPJ()


class ValidatorsTestCase(TestCase):

    def test_validate_doc_number_valid_cpf(self):
        """Test valid CPF number."""
        valid_cpf = cpf_validator.generate()
        try:
            validate_doc_number(valid_cpf)
        except ValidationError:
            self.fail(
                f"validate_doc_number raised ValidationError for valid CPF: {valid_cpf}"
            )

    def test_validate_doc_number_valid_cnpj(self):
        """Test valid CNPJ number."""
        valid_cnpj = cnpj_validator.generate()
        try:
            validate_doc_number(valid_cnpj)
        except ValidationError:
            self.fail(
                f"validate_doc_number raised ValidationError for valid CNPJ: {valid_cnpj}"
            )

    def test_validate_doc_number_invalid_cpf(self):
        """Test invalid CPF number."""
        invalid_cpf = "12345678900"  # Example of an invalid CPF
        with self.assertRaises(ValidationError):
            validate_doc_number(invalid_cpf)

    def test_validate_doc_number_invalid_cnpj(self):
        """Test invalid CNPJ number."""
        invalid_cnpj = "12345678000196"  # Example of an invalid CNPJ
        with self.assertRaises(ValidationError):
            validate_doc_number(invalid_cnpj)

    def test_validate_doc_number_empty_value(self):
        """Test empty document number."""
        with self.assertRaises(ValidationError):
            validate_doc_number("")

    def test_validate_doc_number_invalid_length(self):
        """Test document number with invalid length."""
        invalid_length = "123456789"  # Invalid length
        with self.assertRaises(ValidationError):
            validate_doc_number(invalid_length)

    def test_validate_areas_valid(self):
        """Test valid area values where sum of arable and vegetation areas does not exceed total area."""
        try:
            validate_areas(Decimal("50.00"), Decimal("25.00"), Decimal("80.00"))
        except ValidationError:
            self.fail("validate_areas raised ValidationError for valid area values")

    def test_validate_areas_invalid(self):
        """Test invalid area values where sum of arable and vegetation areas exceeds total area."""
        with self.assertRaises(ValidationError):
            validate_areas(Decimal("60.00"), Decimal("30.00"), Decimal("80.00"))

    def test_validate_areas_zero_values(self):
        """Test area values where arable and vegetation areas are zero, which is valid."""
        try:
            validate_areas(Decimal("0.00"), Decimal("0.00"), Decimal("0.00"))
        except ValidationError:
            self.fail("validate_areas raised ValidationError for zero values")

    def test_validate_areas_large_numbers(self):
        """Test area values with large numbers to ensure the function handles them properly."""
        try:
            validate_areas(
                Decimal("1000000.00"), Decimal("500000.00"), Decimal("1500000.00")
            )
        except ValidationError:
            self.fail("validate_areas raised ValidationError for large numbers")
