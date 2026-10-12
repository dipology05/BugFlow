
from pathlib import Path

import joblib

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import BugReport


# Load the trained ML model
MODEL_PATH = Path(settings.BASE_DIR) / "severity_model.joblib"
model = joblib.load(MODEL_PATH)


# Predict bug category using keywords
def predict_category(text):
    text = text.lower()

    security_words = [
        "security", "unauthorized", "authentication",
        "permission", "vulnerability", "sql injection",
        "xss", "password", "access denied"
    ]

    database_words = [
        "database", "sql", "query", "mysql", "postgres",
        "sqlite", "table", "column", "migration",
        "deadlock", "transaction"
    ]

    api_words = [
        "api", "endpoint", "http", "request", "response",
        "json", "rest", "timeout", "status code",
        "server error"
    ]

    ui_words = [
        "button", "page", "screen", "layout", "css",
        "html", "frontend", "display", "font",
        "click", "visual", "form"
    ]

    if any(word in text for word in security_words):
        return "Security"

    if any(word in text for word in database_words):
        return "Database"

    if any(word in text for word in api_words):
        return "API"

    if any(word in text for word in ui_words):
        return "UI"

    return ""


# Home page: submit a new bug report
def home(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        stack_trace = request.POST.get("stack_trace", "").strip()

        if title and description:
            text = title + " " + description

            predicted_severity = model.predict([text])[0]
            predicted_category = predict_category(text)

            bug = BugReport.objects.create(
                title=title,
                description=description,
                stack_trace=stack_trace,
                severity_label=predicted_severity,
                component_label=predicted_category,
            )

            return redirect("bug_detail", bug_id=bug.id)

    return render(request, "bugs/home.html")


# Display details of a particular bug
def bug_detail(request, bug_id):
    bug = get_object_or_404(BugReport, id=bug_id)

    return render(
        request,
        "bugs/bug_detail.html",
        {"bug": bug}
    )


# Dashboard with category and severity filters
def dashboard(request):
    bugs = BugReport.objects.all().order_by("-created_at")

    category = request.GET.get("category", "")
    severity = request.GET.get("severity", "")

    if category:
        bugs = bugs.filter(component_label=category)

    if severity:
        bugs = bugs.filter(severity_label=severity)

    context = {
        "bugs": bugs,
        "selected_category": category,
        "selected_severity": severity,
        "categories": BugReport.CATEGORY_CHOICES,
        "severities": BugReport.SEVERITY_CHOICES,

        "total_bugs": BugReport.objects.count(),
        "critical_bugs": BugReport.objects.filter(
            severity_label="Critical"
        ).count(),
        "ui_bugs": BugReport.objects.filter(
            component_label="UI"
        ).count(),
        "unclassified_bugs": BugReport.objects.filter(
            component_label=""
        ).count(),

        # Available status options for the dashboard dropdown
        "statuses": BugReport.STATUS_CHOICES,
    }

    return render(request, "bugs/dashboard.html", context)


# Update bug status from the dashboard


@require_POST
def update_bug_status(request, bug_id):
    bug = get_object_or_404(BugReport, id=bug_id)

    new_status = request.POST.get("status")

    if new_status in dict(BugReport.STATUS_CHOICES):
        bug.status = new_status
        bug.save(update_fields=["status"])

    return redirect("dashboard")


