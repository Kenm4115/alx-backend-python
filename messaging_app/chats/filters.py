import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # filter messages by a time range
    sent_after = django_filters.IsoDateTimeFilter(field_name="sent_at", lookup_expr='gte')
    sent_before = django_filters.IsoDateTimeFilter(field_name="sent_at", lookup_expr='lte')

    # filter by participant (conversation contains this user)
    participant = django_filters.NumberFilter(method='filter_by_participant')

    class Meta:
        model = Message
        fields = ['sent_after', 'sent_before', 'participant']

    def filter_by_participant(self, queryset, name, value):
        # value is a user_id
        return queryset.filter(conversation__participants__id=value)
