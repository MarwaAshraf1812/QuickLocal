from rest_framework import viewsets  # type: ignore
from .models import Vendor
from .serializers import VendorSerializer
from .permissions import IsStaffUser
from rest_framework.decorators import action  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore

class VendorViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling vendor-related operations, including
    listing, creating, updating, and deleting vendors.

    Attributes:
        queryset (QuerySet): A queryset of all vendor objects.
        serializer_class (Serializer): The serializer class used for vendor data.
        permission_classes (list): List of permission classes for controlling access.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsStaffUser]

    def perform_create(self, serializer):
        """
        Save the vendor object with the current user as the owner.

        Args:
            serializer (Serializer): The serializer instance used to save the vendor.
        """
        serializer.save(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of all vendors.

        Args:
            request (Request): The request object containing query parameters.

        Returns:
            Response: A response object containing the list of vendors.
        """
        response = super().list(request, *args, **kwargs)
        print("Response data:", response.data)  # Debugging line
        return response
    
    @action(detail=False, methods=['post'], url_path='create_vendor')
    def create_vendor(self, request):
        """
        Create a new vendor using a POST request.

        Args:
            request (Request): The request object containing the vendor data.

        Returns:
            Response: A response object containing the created vendor's data, or error messages.
        """
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['put'], url_path='update_vendor')
    def update_vendor(self, request, pk=None):
        """
        Update an existing vendor using a PUT request.

        Args:
            request (Request): The request object containing the updated vendor data.
            pk (int): The primary key of the vendor to be updated.

        Returns:
            Response: A response object containing the updated vendor's data, or error messages.
        """
        try:
            vendor = Vendor.objects.get(pk=pk)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorSerializer(vendor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['delete'], url_path='delete_vendor')
    def delete_vendor(self, request, pk=None):
        """
        Delete a vendor using a DELETE request.

        Args:
            request (Request): The request object.
            pk (int): The primary key of the vendor to be deleted.

        Returns:
            Response: A response object indicating success or failure of the deletion.
        """
        try:
            vendor = Vendor.objects.get(pk=pk)
            vendor.delete()
            return Response({'message': 'Vendor deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)
