from datetime import datetime
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers
from analyses.models import Analysis


class AnalysesList(APIView):
    """
    List all analyses, or create a new analysis.
    """

    serializer_class = serializers.AnalysisSerializer

    def get(self, request, format=None):
        analyses = Analysis.objects.all()
        serializer = self.serializer_class(analyses, many=True)

        return Response(data=serializer.data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(status=Analysis.Status.PENDING)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
        )


class AnalysisDetail(APIView):
    """
    Retrieve, update or delete an analysis instance.
    """

    serializer_class = serializers.AnalysisSerializer

    def get_object(self, id):
        try:
            return Analysis.objects.get(pk=id)
        except Analysis.DoesNotExist:
            raise NotFound()

    def get(self, request, id, format=None):
        analysis = self.get_object(id)
        serializer = self.serializer_class(analysis)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, id, format=None):
        analysis = self.get_object(id)
        serializer = self.serializer_class(analysis, data=request.data)

        if not serializer.is_valid():
            return Response(
                data={
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id, format=None):
        analysis = self.get_object(id)
        deleted_rows = analysis.delete()

        if len(deleted_rows) <= 0:
            return Response(
                data={
                    "errors": {"global": "Nepodarilo sa vymazať analýzu"},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(status=status.HTTP_204_NO_CONTENT)


class AnalysisStart(APIView):
    """
    Analysis start
    """

    serializer_class = serializers.AnalysisSerializer

    def get_object(self, id):
        try:
            return Analysis.objects.get(pk=id)
        except Analysis.DoesNotExist:
            raise NotFound()

    def post(self, request, id, format=None):
        analysis = self.get_object(id)
        serializer = self.serializer_class(analysis, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(
                data={
                    "errors": {"global": "Nepodarilo sa aktualizovať stav analýzy."},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(status=Analysis.Status.IN_PROGRESS, started_at=datetime.now())
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AnalysisFinish(APIView):
    """
    Analysis finish
    """

    serializer_class = serializers.AnalysisSerializer

    def get_object(self, id):
        try:
            return Analysis.objects.get(pk=id)
        except Analysis.DoesNotExist:
            raise NotFound()

    def post(self, request, id, format=None):
        analysis = self.get_object(id)
        serializer = self.serializer_class(analysis, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(
                data={
                    "errors": {"global": "Nepodarilo sa aktualizovať stav analýzy."},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save(status=Analysis.Status.FINISHED, ended_at=datetime.now())
        return Response(data=serializer.data, status=status.HTTP_200_OK)
