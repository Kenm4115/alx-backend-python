from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions

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


class IsParticipantOfConversation(BasePermission):
    """
    Allow only authenticated participants of a conversation
    to view, send, update, or delete messages.
    """

    def has_permission(self, request, view):
        # User must be authenticated to access any endpoint
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read-only methods are allowed only if user is a participant
        if request.method in SAFE_METHODS:
            # obj could be Conversation or Message
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
            if hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
            return False
        else:
            # For write operations, check similarly
            if hasattr(obj, 'participants'):
                return request.user in obj.participants.all()
            if hasattr(obj, 'conversation'):
                return request.user in obj.conversation.participants.all()
            return False
