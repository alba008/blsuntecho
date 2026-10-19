from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),

    # BLSUNTECH_PHASE2_ROUTES
    path("services/", views.services, name="services"),
    path("about/", views.about, name="about"),
    path("projects/", views.projects, name="projects"),
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),

]
