from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def prompt(request):
    pass