from rest_framework import serializers
from .models import User, Conversation, Message


# 1️⃣ User Serializer with explicit CharFields
class UserSerializer(serializers.ModelSerializer):
    # Using CharField explicitly for demonstration
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at',
        ]


# 2️⃣ Message Serializer with computed field
class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()  # computed field

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',       # FK ID or nested if you adjust
            'sender_name',  # computed field
            'message_body',
            'sent_at',
        ]

    def get_sender_name(self, obj):
        # Compute a full name for display
        return f"{obj.sender.first_name} {obj.sender.last_name}".strip()


# 3️⃣ Conversation Serializer with validation
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    # Example of a writable CharField to pass participant IDs when creating
    participant_ids = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'participant_ids',  # write-only input
            'created_at',
            'messages',
        ]

    # Example custom validation using ValidationError
    def validate_participant_ids(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least two participants."
            )
        return value
