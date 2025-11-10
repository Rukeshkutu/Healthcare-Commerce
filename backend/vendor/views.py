from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Vendor, BusinessDocument
from .serializers import VendorDocumentSerializer, VendorRegistrationSerializer, VendorSerializer

@api_view(['POST'])
def vendor_registration(request):
    if request.method == 'POST':
        serializer = VendorRegistrationSerializer(data = request.data)
        if serializer.is_valid():
            vendor = serializer.save()
            return Response({
                'message': 'Vendor registered Successfully.',
                'vendor_id': vendor.id

            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def vendor_profile(request):
    try:
        vendor = Vendor.objects.get(user = request.user)
    except Vendor.DoesNotExist:
        return Response(
            {'error': 'Vendor profile not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
    if request.method == 'GET':
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def vendor_documents(request):
    vendor = get_object_or_404(Vendor, user = request.user)

    if request.method == 'GET':
        documents = vendor.documents.all()
        serializer = VendorDocumentSerializer(documents, many = True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = VendorDocumentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(vendor = vendor)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    