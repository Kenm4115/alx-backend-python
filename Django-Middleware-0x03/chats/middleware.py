# messaging_app/chats/middleware.py
import time
from collections import defaultdict, deque
from django.http import JsonResponse
from django.http import HttpResponseForbidden
import logging
from datetime import datetime

# Configure a logger that writes to a file
logger = logging.getLogger("request_logger")
# file will be created in project root
handler = logging.FileHandler("requests.log")
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # One-time configuration and initialization
        self.get_response = get_response

    def __call__(self, request):
        # Log before view is called
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Continue processing the request
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time initialization (if needed)

    def __call__(self, request):
        # Get the current hour from server time
        current_hour = datetime.now().hour  # returns 0–23

        # ✅ Allow access only between 18 (6PM) and 21 (9PM)
        # i.e., deny if hour < 18 or hour >= 21
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden(
                "Access to the messaging app is restricted outside 6PM to 9PM."
            )

        # Continue processing normally
        response = self.get_response(request)
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware to limit number of POST requests (e.g., sending messages)
    from each IP address to 5 per minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Store a history of timestamps for each IP address
        self.requests_log = defaultdict(deque)  # {ip: deque[timestamps]}

        # Limit configuration
        self.limit = 5          # max messages
        self.time_window = 60   # seconds

    def __call__(self, request):
        # Only track POST requests to message endpoints
        if request.method == "POST" and request.path.startswith("/api/messages"):
            ip = self.get_client_ip(request)
            now = time.time()

            timestamps = self.requests_log[ip]

            # Remove timestamps outside the time window
            while timestamps and now - timestamps[0] > self.time_window:
                timestamps.popleft()

            # Check limit
            if len(timestamps) >= self.limit:
                return JsonResponse(
                    {
                        "detail": "Message rate limit exceeded. Please wait before sending more."
                    },
                    status=429  # Too Many Requests
                )

            # Record this request
            timestamps.append(now)

        # Continue with normal processing
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """
        Get the client IP address from request META.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolepermissionMiddleware:
    """
    Middleware that checks if the user has an 'admin' or 'moderator' role
    before allowing access to certain restricted actions.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Any one-time configuration can go here

    def __call__(self, request):
        # 👉 Decide which paths or actions need role checking
        # For example, we check all API endpoints under /api/admin-only/
        if request.path.startswith("/api/admin-only/"):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("You must be logged in.")

            # Assuming your custom User model has a 'role' field
            user_role = getattr(user, "role", None)
            if user_role not in ["admin", "moderator"]:
                return HttpResponseForbidden("You do not have permission to access this resource.")

        # ✅ If all good, continue
        response = self.get_response(request)
        return response
