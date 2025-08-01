from .models import Message, Notification, MessageHistory
from django.test import TestCase
from django.contrib.auth.models import User


class MessageNotificationTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username='sender', password='pass')
        self.receiver = User.objects.create_user(
            username='receiver', password='pass')

    def test_notification_created_on_message(self):
        message = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content='Hello!'
        )
        notification_exists = Notification.objects.filter(
            user=self.receiver, message=message).exists()
        self.assertTrue(notification_exists)


class MessageEditHistoryTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(
            username='sender', password='pass')
        self.receiver = User.objects.create_user(
            username='receiver', password='pass')
        self.message = Message.objects.create(
            sender=self.sender, receiver=self.receiver, content='Original')

    def test_edit_logs_history(self):
        self.message.content = 'Updated content'
        self.message.save()

        history = MessageHistory.objects.filter(message=self.message)
        self.assertEqual(history.count(), 1)
        self.assertEqual(history.first().old_content, 'Original')
        self.assertTrue(self.message.edited)


class DeleteUserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='pass')
        self.other = User.objects.create_user(
            username='other', password='pass')
        self.message = Message.objects.create(
            sender=self.user, receiver=self.other, content="Hi")
        self.history = MessageHistory.objects.create(
            message=self.message, old_content="Old")
        self.notification = Notification.objects.create(
            user=self.other, message=self.message)

    def test_user_deletion_cleans_related_data(self):
        self.user.delete()

        self.assertFalse(Message.objects.filter(sender=self.user).exists())
        self.assertFalse(MessageHistory.objects.filter(
            message__sender=self.user).exists())
