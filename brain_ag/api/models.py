from decimal import Decimal

from api.validators import validate_areas, validate_doc_number
from django.core.validators import MinValueValidator
from django.db import models


class RuralProducer(models.Model):
    CPF = "CPF"
    CNPJ = "CNPJ"
    DOCUMENT_TYPE_CHOICES = [
        (CPF, "CPF"),
        (CNPJ, "CNPJ"),
    ]

    doc_type = models.CharField(
        max_length=4,
        choices=DOCUMENT_TYPE_CHOICES,
        default=CPF,
    )
    doc_number = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CPF or CNPJ",
        validators=[validate_doc_number],
    )
    producer_name = models.CharField(max_length=255, verbose_name="Producer Name")
    farm_name = models.CharField(max_length=255, verbose_name="Farm Name")
    city = models.CharField(max_length=100, verbose_name="City")
    state = models.CharField(max_length=2, verbose_name="State")
    total_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Total Area (ha)",
        validators=[MinValueValidator(Decimal("0"))],
    )
    arable_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Arable Area (ha)",
        validators=[MinValueValidator(Decimal("0"))],
    )
    vegetation_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Vegetation Area (ha)",
        validators=[MinValueValidator(Decimal("0"))],
    )

    planted_crops = models.ManyToManyField("Crop", verbose_name="Planted Crops")

    def clean(self):
        validate_areas(self.arable_area, self.vegetation_area, self.total_area)

    def __str__(self):
        return self.producer_name


class Crop(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
