from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from apps.contact.models import ContactMessage, ContactInformation
from apps.contact.serializers import ContactMessageSerializer, ContactInformationSerializer


class ContactMessageViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Your message has been sent successfully!"},
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ContactInformationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ContactInformation.objects.filter(show_on_website=True)
    serializer_class = ContactInformationSerializer
    permission_classes = [AllowAny]
    
    def list(self, request, *args, **kwargs):
        # Get the first active contact information
        contact_info = self.get_queryset().first()
        if contact_info:
            serializer = self.get_serializer(contact_info)
            return Response(serializer.data)
        return Response({}, status=status.HTTP_404_NOT_FOUND)
