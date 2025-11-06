from django.shortcuts import get_list_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Vendor, BusinessDocument
from .serializers import VendorDocumentSerializer, VendorRegistrationSerializer, VendorSerializer

@api_view(['POST'])
