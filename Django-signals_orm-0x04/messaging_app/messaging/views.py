from django.shortcuts import render, redirect
from .models import Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

@cache_page(60)  # Cache timeout in seconds
@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log them out before deleting
    user.delete()
    return HttpResponse("Your account and associated data have been deleted.", status=200)


def conversation_view(request, user_id):
    messages = (
        Message.objects
        .filter(receiver_id=user_id, parent_message__isnull=True)
        .select_related('sender', 'receiver', 'parent_message')
        .prefetch_related('replies')  # Prefetch replies for threading
        .order_by('-timestamp')
    )
    return render(request, 'messaging/conversation.html', {'messages': messages})


@login_required
def unread_messages_view(request):
    unread_messages = Message.unread.for_user(request.user)
    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})
