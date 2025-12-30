from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Token
from .serializers import TokenSerializer
from clinics.models import Session

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_token(request):
    token = Token.objects.filter(user=request.user)
    if not token:
        return Response({'error':'you dont have a valid token'},status=status.HTTP_404_NOT_FOUND)
    serializer=TokenSerializer(token,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_token(request):
    try:
        session = Session.objects.get(id=request.data.get('session'))
    except Session.DoesNotExist:
        return Response({'error': 'Session not found'}, status=404)

    # ❌ Stop if booking is closed
    if session.booking_status == 'CLOSE':
        return Response({'error': 'Booking closed'}, status=400)

    # ✅ Increment token number
    session.last_token_number += 1
    session.save()

    data = {
        'session': session.id,
        'user': request.user.id,
        'token_number': session.last_token_number
    }

    serializer = TokenSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


#only clinic can update token status
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_token_status(request, token_id):
    try:
        token = Token.objects.get(id=token_id)
    except Token.DoesNotExist:
        return Response({'error': 'Token not found'}, status=404)

    # 🔐 PERMISSION CHECK
    if token.session.clinic.owner != request.user:
        return Response(
            {'error': 'You are not allowed to update this token'},
            status=403
        )

    status_value = request.data.get('status')

    if status_value not in ['DONE', 'SKIPPED']:
        return Response({'error': 'Invalid status'}, status=400)

    token.status = status_value
    token.save()

    # Sync logic
    token.delete()

    return Response(
        {'message': f'Token {status_value} and removed'},
        status=200
    )
