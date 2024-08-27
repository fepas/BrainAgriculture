from django.db.models import Count, Sum
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import RuralProducer
from .serializers import RuralProducerSerializer


class RuralProducerViewSet(viewsets.ModelViewSet):
    queryset = RuralProducer.objects.all()
    serializer_class = RuralProducerSerializer


@api_view(["GET"])
def general_statistics(request):
    # Total count of farms
    total_count = RuralProducer.objects.count()

    # Total area of all farms
    total_area = RuralProducer.objects.aggregate(Sum("total_area"))["total_area__sum"]

    # Number of farms by state
    farms_by_state = RuralProducer.objects.values("state").annotate(count=Count("id"))

    # Number of farms by crop
    farms_by_crop = RuralProducer.objects.values("planted_crops__name").annotate(
        count=Count("id")
    )

    # Land use distribution (arable vs vegetation area)
    land_use = RuralProducer.objects.aggregate(
        arable_sum=Sum("arable_area"), vegetation_sum=Sum("vegetation_area")
    )

    response_data = {
        "total_farms": total_count,
        "total_area": total_area,
        "farms_by_state": list(farms_by_state),
        "farms_by_crop": list(farms_by_crop),
        "land_use_distribution": {
            "arable_area": land_use["arable_sum"],
            "vegetation_area": land_use["vegetation_sum"],
        },
    }

    return Response(response_data)
