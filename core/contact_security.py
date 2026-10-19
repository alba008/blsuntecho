import hashlib
import hmac
import ipaddress

from django.conf import settings
from django.core.cache import caches

cache = caches['security']


WINDOW_SECONDS = 600
MAX_SUBMISSIONS = 3


def client_identifier(request):
    """
    Use the direct peer address.

    Production proxy configuration must be reviewed separately.
    Do not trust arbitrary X-Forwarded-For headers.
    """
    address = request.META.get("REMOTE_ADDR", "")

    try:
        return str(ipaddress.ip_address(address))
    except ValueError:
        return "unknown"


def rate_limit_key(request):
    identifier = client_identifier(request)

    digest = hmac.new(
        settings.SECRET_KEY.encode(),
        identifier.encode(),
        hashlib.sha256,
    ).hexdigest()

    return f"blsuntech:contact:v2:{digest}"


def submission_allowed(request):
    """
    Atomically reserve one submission slot where the cache backend
    supports atomic add/incr operations.

    This is a fixed-window limit, not a distributed security guarantee.
    """
    key = rate_limit_key(request)

    if cache.add(key, 1, timeout=WINDOW_SECONDS):
        return True

    try:
        count = cache.incr(key)
    except (ValueError, NotImplementedError):
        # Fail closed when an existing counter cannot be updated.
        return False

    return count <= MAX_SUBMISSIONS


# BLSUNTECH_CONTACT_REQUEST_LIMIT_V1
REQUEST_WINDOW_SECONDS = 600
MAX_REQUESTS = 20


def contact_request_allowed(request):
    """
    Count all contact POST attempts, including invalid submissions.

    Uses the existing security cache and its atomic add/incr operations.
    """
    identifier = client_identifier(request)

    digest = hmac.new(
        settings.SECRET_KEY.encode(),
        ("request:" + identifier).encode(),
        hashlib.sha256,
    ).hexdigest()

    key = f"blsuntech:contact:requests:v1:{digest}"

    if cache.add(key, 1, timeout=REQUEST_WINDOW_SECONDS):
        return True

    try:
        count = cache.incr(key)
    except (ValueError, NotImplementedError):
        return False

    return count <= MAX_REQUESTS
