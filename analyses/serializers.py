from rest_framework import serializers
from analyses.models import Analysis


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = "__all__"

    status = serializers.ReadOnlyField()
    started_at = serializers.DateTimeField(required=False)
    ended_at = serializers.DateTimeField(required=False)
