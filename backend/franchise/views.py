from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Count
from .models import Franchise, FranchisePerformance
from .serializers import FranchiseSerializer, FranchisePerformanceSerializer, FranchiseRegistrationSerializer

@api_view(['POST'])
def franchise_registration(request):
    if request.method == 'POST':
        serializer = FranchiseRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            franchise = serializer.save()
            return Response({
                'message': 'Franchise registered successfully',
                'franchise_id': franchise.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def franchise_profile(request):
    try:
        franchise = Franchise.objects.get(owner=request.user)
    except Franchise.DoesNotExist:
        return Response(
            {'error': 'Franchise profile not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = FranchiseSerializer(franchise)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = FranchiseSerializer(franchise, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

