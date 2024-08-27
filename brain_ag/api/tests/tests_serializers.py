from api.models import Crop
from api.serializers import RuralProducerSerializer
from django.test import TestCase
from validate_docbr import CPF

cpf_validator = CPF()


class RuralProducerSerializerTest(TestCase):

    def setUp(self):
        self.crop_soja = Crop.objects.create(name="Soja")

    def test_valid_data(self):
        data = {
            "doc_type": "CPF",
            "doc_number": cpf_validator.generate(),
            "producer_name": "Maria da Silva",
            "farm_name": "Fazenda Primavera",
            "city": "Ribeirão Preto",
            "state": "SP",
            "total_area": 200,
            "arable_area": 120,
            "vegetation_area": 80,
            "planted_crops": [self.crop_soja.id],
        }
        serializer = RuralProducerSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_area(self):
        data = {
            "doc_type": "CPF",
            "doc_number": cpf_validator.generate(),
            "producer_name": "José Pereira",
            "farm_name": "Fazenda Bela Vista",
            "city": "Uberlândia",
            "state": "MG",
            "total_area": 150,
            "arable_area": 100,
            "vegetation_area": 60,
            "planted_crops": [self.crop_soja.id],
        }
        serializer = RuralProducerSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn(
            "The sum of arable and vegetation areas cannot exceed the total area.",
            serializer.errors["non_field_errors"],
        )
