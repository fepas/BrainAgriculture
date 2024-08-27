from rest_framework import serializers

from .models import RuralProducer


class RuralProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RuralProducer
        fields = "__all__"

    def validate(self, data):
        arable_area = data.get("arable_area")
        vegetation_area = data.get("vegetation_area")
        total_area = data.get("total_area")

        if arable_area + vegetation_area > total_area:
            raise serializers.ValidationError(
                "The sum of arable and vegetation areas cannot exceed the total area."
            )

        return data
