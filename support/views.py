from rest_framework import viewsets, status # type: ignore
from rest_framework.decorators import action # type: ignore
from rest_framework.response import Response # type: ignore
from .models import SupportMessage
from .serializers import SupportMessageSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny # type: ignore

class SupportMessageViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling support messages, including creation,
    retrieval, updating, and deletion of support messages.

    The viewset is restricted to authenticated users, and actions are
    scoped to the current user's messages.
    """
    queryset = SupportMessage.objects.all()
    serializer_class = SupportMessageSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """
        Save the support message instance with the current user as the author.

        Args:
            serializer (SupportMessageSerializer): The serializer instance with validated data.
        """
        serializer.save(user=self.request.user)
    
    def get_queryset(self):
        """
        Retrieve a list of all support messages for the currently authenticated user,
        ordered by creation date in descending order.

        Returns:
            QuerySet: A queryset of support messages for the current user.
        """
        user = self.request.user
        return SupportMessage.objects.filter(user=user).order_by('-created_at')
    
    @action(detail=True, methods=['delete'], url_path='delete_message')
    def delete_message(self, request, pk=None):
        """
        Custom action to delete a specific support message for the authenticated user
        using a DELETE request to `/support/{id}/delete_message/`.

        Args:
            request (Request): The request object containing the user and URL parameters.
            pk (int, optional): The primary key of the support message to delete.

        Returns:
            Response: A response indicating whether the deletion was successful or not.
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
        Custom action to delete all support messages for the authenticated user
        using a DELETE request to `/support/clear_messages/`.

        Args:
            request (Request): The request object containing the user.

        Returns:
            Response: A response indicating the number of messages deleted.
        """
        user = request.user
        deleted_count, _ = SupportMessage.objects.filter(user=user).delete()
        return Response({'message': f'{deleted_count} support messages deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
