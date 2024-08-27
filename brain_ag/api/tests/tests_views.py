from decimal import Decimal

from api.models import Crop, RuralProducer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from validate_docbr import CNPJ, CPF

cpf_validator = CPF()
cnpj_validator = CNPJ()


class RuralProducerAPITest(APITestCase):

    def setUp(self):
        self.crop_soja = Crop.objects.create(name="Soja")
        self.crop_milho = Crop.objects.create(name="Milho")
        self.producer_1 = RuralProducer.objects.create(
            doc_type=RuralProducer.CPF,
            doc_number=cpf_validator.generate(),
            producer_name="Paulo Santos",
            farm_name="Fazenda São José",
            city="Campo Grande",
            state="MS",
            total_area=250,
            arable_area=150,
            vegetation_area=100,
        )
        self.producer_1.planted_crops.add(self.crop_soja)

        self.producer_2 = RuralProducer.objects.create(
            doc_type=RuralProducer.CNPJ,
            doc_number=cnpj_validator.generate(),
            producer_name="Ana Silva",
            farm_name="Fazenda Boa Vista",
            city="São Paulo",
            state="SP",
            total_area=500,
            arable_area=300,
            vegetation_area=150,
        )
        self.producer_2.planted_crops.add(self.crop_milho)

    def test_create_producer(self):
        """Test that a new producer can be created successfully via the API."""
        data = {
            "doc_type": "CNPJ",
            "doc_number": cnpj_validator.generate(),
            "producer_name": "Carlos Almeida",
            "farm_name": "Fazenda Nova",
            "city": "Brasília",
            "state": "DF",
            "total_area": 300,
            "arable_area": 200,
            "vegetation_area": 100,
            "planted_crops": [self.crop_soja.id],
        }
        response = self.client.post(reverse("ruralproducer-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RuralProducer.objects.count(), 3)

    def test_create_producer_invalid_data(self):
        """Test that creating a producer with invalid data returns an error."""
        data = {
            "doc_type": "CNPJ",
            "doc_number": "invalid_cnpj",
            "producer_name": "",
            "farm_name": "Fazenda Nova",
            "city": "Brasília",
            "state": "DF",
            "total_area": 300,
            "arable_area": 200,
            "vegetation_area": 150,
            "planted_crops": [self.crop_soja.id],
        }
        response = self.client.post(reverse("ruralproducer-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_producer(self):
        """Test that a producer can be updated successfully via the API."""
        data = {
            "doc_type": "CNPJ",
            "doc_number": self.producer_1.doc_number,
            "producer_name": "Paulo Santos Updated",
            "farm_name": "Fazenda São José Updated",
            "city": "Campo Grande",
            "state": "MS",
            "total_area": 260,
            "arable_area": 160,
            "vegetation_area": 100,
            "planted_crops": [self.crop_soja.id, self.crop_milho.id],
        }
        response = self.client.put(
            reverse("ruralproducer-detail", kwargs={"pk": self.producer_1.id}), data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["producer_name"], "Paulo Santos Updated")
        self.assertEqual(response.data["total_area"], "260.00")

    def test_delete_producer(self):
        """Test that a producer can be deleted successfully via the API."""
        response = self.client.delete(
            reverse("ruralproducer-detail", kwargs={"pk": self.producer_1.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RuralProducer.objects.count(), 1)

    def test_general_statistics(self):
        """Check that general statistics are correctly returned by the API."""
        response = self.client.get(reverse("general_statistics"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_farms"], 2)
        self.assertEqual(response.data["total_area"], Decimal("750.00"))
        self.assertEqual(
            response.data["farms_by_state"],
            [{"state": "MS", "count": 1}, {"state": "SP", "count": 1}],
        )
        self.assertEqual(
            response.data["farms_by_crop"],
            [
                {"planted_crops__name": "Milho", "count": 1},
                {"planted_crops__name": "Soja", "count": 1},
            ],
        )
        self.assertEqual(
            response.data["land_use_distribution"],
            {"arable_area": Decimal("450.00"), "vegetation_area": Decimal("250.00")},
        )
