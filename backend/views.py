from rest_framework import status
from rest_framework.generics import (
    ListAPIView,
    UpdateAPIView,
    CreateAPIView,
    get_object_or_404
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from backend.models import User, Job, Application
from backend.serializers import (
    UserSignupSerializer,
    LoginSerializers,
    JobSerializer,
    JobApplicationSerializer,
    JobApplicationSerializerNew,
)
from utils.constants import *


class UserSignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        """
        This method allows users to signup.
        """
        try:
            data = request.data
            user = User.objects.filter(email=data["email"]).first()
            if user:
                return Response(
                    {ERROR: "User already exists", SUCCESS: False},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    SUCCESS: True,
                    STATUS_CODE: status.HTTP_201_CREATED,
                    MESSAGE: "User created successfully",
                },
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e.args[0])},
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserLoginView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializers

    def create(self, request, *args, **kwargs):
        """
        This method allows users to login
        """
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            return Response(
                {
                    SUCCESS: True,
                    STATUS_CODE: status.HTTP_200_OK,
                    MESSAGE: "User login successfully",
                    DATA: serializer.validated_data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e.args[0])},
                status=status.HTTP_400_BAD_REQUEST,
            )


class JobView(CreateAPIView, UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        """
        This method allows admin to post a new job
        """
        try:
            data = request.data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    SUCCESS: True,
                    STATUS_CODE: status.HTTP_201_CREATED,
                    MESSAGE: "Job created successfully",
                    DATA: serializer.data,
                },
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    def update(self, request, *args, **kwargs):
        """
        This method allows admin to update a posted job.
        """
        try:
            data = request.data
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(
                {
                    SUCCESS: True,
                    STATUS_CODE: status.HTTP_200_OK,
                    MESSAGE: "Job updated successfully",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {SUCCESS: False, ERROR: str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


class UserJobListView(ListAPIView):
    queryset = Job.objects.filter(status="open")
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        job_title = self.request.query_params.get("job_title", None)
        job_location = self.request.query_params.get("job_location", None)
        company_name = self.request.query_params.get("company_name", None)

        queryset = super().get_queryset().order_by("-id")
        if job_title:
            queryset = queryset.filter(title__icontains=job_title)
        if job_location:
            queryset = queryset.filter(location__icontains=job_location)
        if company_name:
            queryset = queryset.filter(company_name=company_name)
        return queryset

    def list(self, request, *args, **kwargs):
        """
        This method allows users to view open jobs vacancies
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': "Job list",
                'data': serializer.data,
            }, status=status.HTTP_200_OK
        )


class UserJobApplicationView(CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        This method allows users to apply for a job
        """
        try:
            data = request.data
            data["user"] = request.user.id
            application_obj = self.queryset.filter(user=request.user, job=data["job"])
            job = get_object_or_404(Job, pk=data["job"])
            if job.status != "open":
                return Response(
                    {
                        SUCCESS: False,
                        ERROR: f"Job is already {job.status}",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if application_obj.exists():
                return Response(
                    {
                        SUCCESS: False,
                        ERROR: "You have already applied for this job",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = JobApplicationSerializerNew(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                {
                    SUCCESS: True,
                    STATUS_CODE: status.HTTP_200_OK,
                    MESSAGE: "Job applied successfully",
                    DATA: serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {
                    SUCCESS: False,
                    ERROR: str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
