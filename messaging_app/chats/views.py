from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .permissions import IsParticipantOrReadOnly, IsSenderOrReadOnly, IsParticipantOfConversation
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter  # ✅ import your filter class
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.decorators import action

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


# ---------------------------------
# Conversation ViewSet with filters
# ---------------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related('participants', 'messages')
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [IsParticipantOrReadOnly]
    permission_classes = [IsParticipantOfConversation]

    # ✅ enable search and ordering
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__username', 'participants__first_name', 'participants__last_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])
        if not participant_ids or not isinstance(participant_ids, list):
            return Response({"detail": "participants list is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response({"detail": "One or more participants not found."},
                            status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def get_queryset(self):
        # filter to conversations where current user is a participant
        return Conversation.objects.filter(participants=self.request.user)

# ---------------------------------
# Message ViewSet with filters
# --------------------------------
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [IsSenderOrReadOnly]
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]

    # ✅ enable filtering
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter

    def get_queryset(self):
        queryset = Message.objects.all().select_related('conversation', 'sender')
        conversation_id = self.kwargs.get('conversation_pk')  # from nested router
        if conversation_id:
            queryset = queryset.filter(conversation__conversation_id=conversation_id)
        return queryset

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        if self.request.user not in conversation.participants.all():
            raise serializer.ValidationError("You are not part of this conversation.")
        serializer.save(conversation=conversation, sender=self.request.user)

    def get_queryset(self):
        # filter to messages in conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)
    
       
    @action(detail=False, methods=['post'])
    def send_custom(self, request):
        conversation_id = request.data.get('conversation')
        message_body = request.data.get('message_body')

        # Check if user is participant
        from .models import Conversation
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({'detail': 'Conversation not found.'}, status=status.HTTP_404_NOT_FOUND)

        if request.user not in conversation.participants.all():
            # ✅ Forbidden response
            return Response({'detail': 'You are not a participant of this conversation.'},
                            status=HTTP_403_FORBIDDEN)

        # Otherwise, proceed to create the message
        from .models import Message
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=message_body
        )
        from .serializers import MessageSerializer
        return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)