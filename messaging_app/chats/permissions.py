# messaging_app/chats/permissions.py
from rest_framework.permissions import BasePermission

class IsParticipantOrReadOnly(BasePermission):
    """
    Only participants of the conversation can access it.
    """
    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()

class IsSenderOrReadOnly(BasePermission):
    """
    Only the sender can modify their message, others can read.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return obj.sender == request.user


