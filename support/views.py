from rest_framework import viewsets, status #type: ignore
from rest_framework.decorators import action #type: ignore
from rest_framework.response import Response #type: ignore
from .models import SupportMessage
from .serializers import SupportMessageSerializer
from rest_framework.permissions import IsAuthenticated #type: ignore


class SupportMessageViewSet(viewsets.ModelViewSet):
    queryset = SupportMessage.objects.all()
    serializer_class = SupportMessageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        """
        This view should return a list of all the support messages
        for the currently authenticated user.
        """
        user = self.request.user
        return SupportMessage.objects.filter(user=user).order_by('-created_at')
    
    @action(detail=True, methods=['delete'], url_path='delete_message')
    def delete_message(self, request, pk=None):
        """
        Custom action to delete a specific support message using DELETE request to `/support/{id}/delete_message/`.
        """
        try:
            support_message = SupportMessage.objects.get(pk=pk, user=request.user)
            support_message.delete()
            return Response({'message': 'Support message deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except SupportMessage.DoesNotExist:
            return Response({'error': 'Support message not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'], url_path='clear_messages')
    def clear_messages(self, request):
        """
        Custom action to delete all support messages for the authenticated user using DELETE request to `/support/clear_messages/`.
        """
        user = request.user
        deleted_count, _ = SupportMessage.objects.filter(user=user).delete()
        return Response({'message': f'{deleted_count} support messages deleted successfully'}, status=status.HTTP_204_NO_CONTENT)