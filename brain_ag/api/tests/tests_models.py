from api.models import Crop, RuralProducer
from django.core.exceptions import ValidationError
from django.test import TestCase
from validate_docbr import CNPJ, CPF

cpf_validator = CPF()
cnpj_validator = CNPJ()


class CropModelTest(TestCase):

    def setUp(self):
        self.crop = Crop.objects.create(name="Soja")

    def test_crop_creation(self):
        self.assertEqual(str(self.crop), "Soja")


class RuralProducerModelTest(TestCase):

    def setUp(self):
        self.crop_soja = Crop.objects.create(name="Soja")
        self.producer = RuralProducer.objects.create(
            doc_type=RuralProducer.CPF,
            doc_number=cpf_validator.generate(),
            producer_name="João da Silva",
            farm_name="Fazenda Boa Esperança",
            city="Goiânia",
            state="GO",
            total_area=100,
            arable_area=60,
            vegetation_area=40,
        )
        self.producer.planted_crops.add(self.crop_soja)

    def test_producer_creation(self):
        self.assertEqual(str(self.producer), "João da Silva")

    def test_area_validation(self):
        """Test that ValidationError is raised when arable and vegetation areas exceed total area."""
        self.producer.arable_area = 70
        self.producer.vegetation_area = 40
        with self.assertRaises(ValidationError):
            self.producer.clean()

    def test_valid_doc_number(self):
        """Test that a valid CPF or CNPJ passes validation."""
        valid_cpf = cpf_validator.generate()
        self.producer.doc_number = valid_cpf
        try:
            self.producer.full_clean()  # Should not raise ValidationError
        except ValidationError:
            self.fail(f"Valid CPF {valid_cpf} raised ValidationError unexpectedly")

    def test_invalid_cpf(self):
        """Test that an invalid CPF raises ValidationError."""
        self.producer.doc_type = RuralProducer.CPF
        self.producer.doc_number = "12345678901"  # Invalid CPF
        with self.assertRaises(Exception):
            self.producer.full_clean()  # Should raise ValidationError

    def test_invalid_cnpj(self):
        """Test that an invalid CNPJ raises ValidationError."""
        self.producer.doc_type = RuralProducer.CNPJ
        self.producer.doc_number = "12345678000196"  # Invalid CNPJ
        with self.assertRaises(Exception):
            self.producer.full_clean()  # Should raise ValidationError
