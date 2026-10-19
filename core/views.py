from django.shortcuts import render


def home(request):
    return render(request, "core/home.html")


# BLSUNTECH_PHASE2_VIEWS
def services(request):
    return render(request, "core/services.html")


def about(request):
    return render(request, "core/about.html")


# BLSUNTECH_PHASE3_PROJECTS_VIEW
def projects(request):
    return render(request, "core/projects.html")


# BLSUNTECH_V2_PUBLIC_CASE_STUDIES
from django.http import Http404

PROJECT_CASE_STUDIES = {
    "kira-edu": {
        "name": "Kira Edu",
        "category": "Education Technology",
        "image": "images/projects/kira-edu.webp",
        "website": "https://" + "kira.ithewatcher.com/",
        "overview": (
            "A digital learning platform designed to bring training "
            "programs, enrollment, and learning administration into "
            "one accessible experience."
        ),
        "challenge": (
            "Coordinating courses, schedules, student registration, "
            "and communication across separate processes can make "
            "training administration difficult and time-consuming."
        ),
        "solution": (
            "Kira Edu brings essential learning and enrollment "
            "activities into a unified platform, helping students "
            "explore programs while supporting more organized "
            "training administration."
        ),
    },
    "sockcs": {
        "name": "Sockcs",
        "category": "E-Commerce",
        "image": "images/projects/sockcs.webp",
        "website": "https://" + "sockcs.com/",
        "overview": (
            "An online shopping platform built to present products "
            "and create a clear digital storefront."
        ),
        "challenge": (
            "A business needs an accessible online presence where "
            "customers can discover its products without unnecessary "
            "complexity."
        ),
        "solution": (
            "Sockcs provides a structured shopping experience with "
            "product presentation and navigation designed around "
            "customer discovery."
        ),
    },
    "dafara": {
        "name": "DAFARA",
        "category": "Social Impact",
        "image": "images/projects/dafara.webp",
        "website": "https://" + "dafara.org/",
        "overview": (
            "A nonprofit digital platform presenting the organization's "
            "mission, programs, initiatives, and ways to contribute."
        ),
        "challenge": (
            "Community-focused organizations need a clear way to "
            "communicate their work, build awareness, and connect "
            "supporters with their initiatives."
        ),
        "solution": (
            "DAFARA provides a central online presence where visitors "
            "can learn about programs and find donation pathways."
        ),
    },
    "makutanoni": {
        "name": "Makutanoni",
        "category": "Digital Marketplace",
        "image": "images/projects/makutanoni.webp",
        "website": "https://" + "makutanoni.com/",
        "overview": (
            "A digital marketplace focused on presenting listings, "
            "supporting discovery, and connecting people with "
            "commercial opportunities."
        ),
        "challenge": (
            "Products and opportunities can be difficult to discover "
            "when information is scattered across disconnected "
            "channels."
        ),
        "solution": (
            "Makutanoni brings marketplace listings into a structured "
            "digital experience designed to help visitors explore "
            "available opportunities."
        ),
    },
}


def project_detail(request, slug):
    project = PROJECT_CASE_STUDIES.get(slug)

    if project is None:
        raise Http404("Project not found")

    return render(
        request,
        "core/project_detail.html",
        {"project": project},
    )


# BLSUNTECH_CONTACT_V1
from django.shortcuts import redirect
from django.core.cache import cache
from django.views.decorators.http import require_http_methods
from .forms import BusinessInquiryForm


@require_http_methods(["GET", "POST"])
def contact(request):
    from django.http import HttpResponse
    from .contact_security import (
        submission_allowed,
        contact_request_allowed,
    )

    if request.method == "POST":
        if not contact_request_allowed(request):
            return HttpResponse(
                "Too many requests. Please try again later.",
                status=429,
                headers={"Retry-After": "600"},
            )

        form = BusinessInquiryForm(request.POST)

        if form.is_valid():
            if not submission_allowed(request):
                form.add_error(
                    None,
                    "Too many inquiries have been submitted. "
                    "Please try again later."
                )
            else:
                form.save()
                request.session["contact_submitted"] = True
                return redirect("core:contact_success")
    else:
        form = BusinessInquiryForm()

    return render(
        request,
        "core/contact.html",
        {"form": form},
    )


def contact_success(request):
    if not request.session.pop("contact_submitted", False):
        return redirect("core:contact")

    return render(request, "core/contact_success.html")
