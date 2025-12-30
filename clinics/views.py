from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Session,ClinicProfile
from .serializers import SessionSerializer, ClinicProfileSerializer

@api_view(['GET'])
def get_session(request,clinic_username):
    try:
        clinic=ClinicProfile.objects.get(username=clinic_username)
    except ClinicProfile.DoesNotExist:
        return Response({'error':'clinic does not exists'},status=status.HTTP_404_NOT_FOUND)
    try:
        session=Session.objects.get(clinic=clinic)
    except Session.DoesNotExist:
        return Response({'error':'session does not exists'},status=status.HTTP_404_NOT_FOUND)
    serializer=SessionSerializer(session)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_session(request):
    try:
        user=ClinicProfile.objects.get(user=request.user)
    except ClinicProfile.DoesNotExist:
        return Response({'error':'clinic profile does not exist'},status=status.HTTP_404_NOT_FOUND)
    serializer=SessionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_session(request,id):
    try:
        user=ClinicProfile.objects.get(user=request.user)
    except ClinicProfile.DoesNotExist:
        return Response({'error':'clinic profile does not exist'},status=status.HTTP_404_NOT_FOUND)
    try:
        session=Session.objects.get(id=id)
    except Session.DoesNotExist:
        return Response({'error':'session does not exist'},status=status.HTTP_404_NOT_FOUND)
    if session.clinic != user:
        return Response({'error':'you are not the owner of this session'},status=status.HTTP_401_UNAUTHORIZED)
    serializer=SessionSerializer(session,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_session(request,id):
    try:
        user=ClinicProfile.objects.get(user=request.user)
    except ClinicProfile.DoesNotExist:
        return Response({'error':'clinic profile does not exist'},status=status.HTTP_404_NOT_FOUND)
    try:
        session=Session.objects.get(id=id)
    except Session.DoesNotExist:
        return Response({'error':'session does not exist'},status=status.HTTP_404_NOT_FOUND)
    if session.clinic != user:
        return Response({'error':'you are not the owner of this session'},status=status.HTTP_401_UNAUTHORIZED)
    session.delete()
    return Response({'message':'Session deleted successfully'},status=status.HTTP_204_NO_CONTENT)
