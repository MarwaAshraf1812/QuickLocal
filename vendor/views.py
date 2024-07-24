from rest_framework import viewsets #type: ignore
from .models import Vendor
from .serializers import VendorSerializer
from .permissions import IsStaffUser

class VendorViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling vendors, including creation,
    retrieval, updating, and deletion of vendors.
    """
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    permission_classes = [IsStaffUser]

    def perform_create(self, serializer):
        """
        Save the vendor object with the current user as the owner.
        """
        serializer.save(user=self.request.user)
