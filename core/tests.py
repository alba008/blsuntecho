from django.core.cache import caches
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from .models import BusinessInquiry


@override_settings(
    CACHES={
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "blsuntech-contact-tests",
        },
        "security": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "blsuntech-security-tests",
        },
    }
)
class ContactSecurityTests(TestCase):

    def setUp(self):
        caches["security"].clear()
        self.url = reverse("core:contact")
        self.payload = {
            "name": "Security Test",
            "email": "security@example.com",
            "company": "BlsunTech QA",
            "service": "software",
            "message": (
                "This is a legitimate inquiry for testing "
                "the contact security workflow."
            ),
            "website": "",
        }

    def test_concurrent_rate_limit(self):
        from concurrent.futures import ThreadPoolExecutor
        from django.test import RequestFactory
        from .contact_security import submission_allowed

        factory = RequestFactory()

        def attempt(_):
            request = factory.post(
                "/contact/",
                REMOTE_ADDR="192.0.2.99",
            )
            return submission_allowed(request)

        with ThreadPoolExecutor(max_workers=10) as executor:
            results = list(executor.map(attempt, range(20)))

        self.assertEqual(sum(results), 3)

    def test_contact_page_loads(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_valid_inquiry_is_saved(self):
        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(BusinessInquiry.objects.count(), 1)

    def test_honeypot_rejected(self):
        payload = {
            **self.payload,
            "website": "https://spam.example",
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(BusinessInquiry.objects.count(), 0)

    def test_short_message_rejected(self):
        payload = {
            **self.payload,
            "message": "Too short",
        }

        response = self.client.post(self.url, payload)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(BusinessInquiry.objects.count(), 0)

    def test_rate_limit_across_sessions(self):
        for _ in range(3):
            client = Client(REMOTE_ADDR="192.0.2.25")
            response = client.post(self.url, self.payload)
            self.assertEqual(response.status_code, 302)

        fourth_client = Client(REMOTE_ADDR="192.0.2.25")
        response = fourth_client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Too many inquiries have been submitted."
        )
        self.assertEqual(BusinessInquiry.objects.count(), 3)

    def test_csrf_protection(self):
        client = Client(enforce_csrf_checks=True)

        response = client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(BusinessInquiry.objects.count(), 0)

    def test_forwarded_header_cannot_bypass_limit(self):
        for i in range(4):
            client = Client(
                REMOTE_ADDR="192.0.2.50",
                HTTP_X_FORWARDED_FOR=f"198.51.100.{i + 1}",
            )
            response = client.post(self.url, self.payload)

            if i < 3:
                self.assertEqual(response.status_code, 302)
            else:
                self.assertEqual(response.status_code, 200)

        self.assertEqual(BusinessInquiry.objects.count(), 3)
