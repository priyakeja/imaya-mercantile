from django.shortcuts import render
from sections.models import (
    HeroSettings, HeroSlide, AboutSection, ProductsSection, Product, JourneyStep,
    WhySection, ProcessSection, CommitmentSection,CertificationSection , 
    ContactSection, ContactEnquiry, FAQSection, BusinessEnquirySection, 
    FeedbackSection,
)
import logging
import re
import unicodedata

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .countries import COUNTRIES, ALIASES, normalize_country

from .countries import COUNTRIES, ALIASES, normalize_country

logger = logging.getLogger(__name__)





def home(request):
    about = AboutSection.objects.filter(is_active=True).first()
    why = WhySection.objects.filter(is_active=True).first()
    process = ProcessSection.objects.filter(is_active=True).first()
    certs = CertificationSection.objects.filter(is_active=True).first()
    contact = ContactSection.objects.filter(is_active=True).first()
    products = list(Product.objects.filter(is_active=True).prefetch_related("specs"))
    if contact and contact.whatsapp_enabled and contact.whatsapp_number:
        for p in products:
            p.whatsapp_url = contact.product_whatsapp_link(p.name)
    faq = FAQSection.objects.filter(is_active=True).first()
    feedback = FeedbackSection.objects.filter(is_active=True).first()

    context = {
        "hero_settings": HeroSettings.objects.first() or HeroSettings(),
        "hero_slides": HeroSlide.objects.filter(is_active=True),
        "about": about,
        "about_tabs": about.tabs.filter(is_active=True) if about else [],
        "products_section": ProductsSection.objects.first() or ProductsSection(),
        "products": products,
        "journey_steps": JourneyStep.objects.filter(is_active=True),
        "why": why,
        "why_features": why.features.filter(is_active=True) if why else [],
        "process": process,
        "process_steps": process.steps.filter(is_active=True) if process else [],
        "commitment": CommitmentSection.objects.filter(is_active=True).first(),
        "certs": certs,
        "certificates": certs.certificates.filter(is_active=True) if certs else [],
        "contact": contact,
        "contact_images": contact.images.filter(is_active=True) if contact else [],
        "contact_products": list(
            Product.objects.filter(is_active=True).values_list("name", flat=True)
        ),
        "country_data": {"countries": COUNTRIES, "aliases": ALIASES},
        "feedback": feedback,
        "feedbacks": feedback.feedbacks.filter(is_active=True) if feedback else [],
        "faq": faq,
        "faq_items": faq.items.filter(is_active=True) if faq else [],
                "biz_cta": BusinessEnquirySection.objects.filter(is_active=True).first(),
        
    }
    return render(request, "home.html", context)


def _valid_name(value):
    if not unicodedata.category(value[0]).startswith("L"):
        return False
    return all(
        unicodedata.category(ch)[0] in ("L", "M") or ch in " .'’-" for ch in value
    )


def validate_enquiry(data):
    errors = {}

    name = data["name"]
    if not name:
        errors["name"] = "Please enter your name."
    elif len(name) < 3:
        errors["name"] = "Name must be at least 3 characters."
    elif len(name) > 100:
        errors["name"] = "Name is too long (maximum 100 characters)."
    elif not _valid_name(name):
        errors["name"] = "Name can contain only letters, spaces and . ' -"

    country = data["country"]
    if not country:
        errors["country"] = "Please enter your country."
    else:
        proper = normalize_country(country)
        if proper:
            data["country"] = proper
        else:
            errors["country"] = "Please enter a valid country name (for example: India)."

    email = data["email"]
    if not email:
        errors["email"] = "Please enter your email address."
    else:
        try:
            validate_email(email)
        except ValidationError:
            errors["email"] = "Please enter a valid email address (for example: name@example.com)."

    quantity = data["quantity"]
    if quantity:
        if not re.fullmatch(r"[0-9]+", quantity):
            errors["quantity"] = "Required quantity must be a number (digits only)."
        elif int(quantity) == 0:
            errors["quantity"] = "Required quantity must be greater than 0."
        elif len(quantity) > 9:
            errors["quantity"] = "Required quantity is too large."

    phone = data["phone"]
    if phone and not re.fullmatch(r"[0-9]{10}", phone):
        errors["phone"] = "Phone number must be exactly 10 digits."

    message = data["message"]
    if not message:
        errors["message"] = "Please enter your message."
    elif len(message) > 2000:
        errors["message"] = "Message is too long (maximum 2000 characters)."

    if len(data["company"]) > 150:
        errors["company"] = "Company name is too long (maximum 150 characters)."

    return errors


@require_POST
def contact_submit(request):
    section = ContactSection.objects.filter(is_active=True).first()
    if not section:
        return JsonResponse({"ok": False, "message": "The enquiry form is not available."}, status=404)

    # honeypot (bots fill this hidden field)
    if request.POST.get("website"):
        return JsonResponse({"ok": True, "message": section.success_message})

    data = {
        key: request.POST.get(key, "").strip()
        for key in ("name", "company", "country", "email", "quantity", "phone", "message")
    }
    errors = validate_enquiry(data)
    if errors:
        return JsonResponse(
            {"ok": False, "errors": errors, "message": "Please correct the highlighted fields."},
            status=400,
        )

    valid_products = set(Product.objects.filter(is_active=True).values_list("name", flat=True))
    products = [p for p in request.POST.getlist("products") if p in valid_products]

    enquiry = ContactEnquiry.objects.create(
        name=data["name"], company=data["company"], country=data["country"],
        email=data["email"], products=", ".join(products), quantity=data["quantity"],
        phone=data["phone"], message=data["message"],
    )

    body = "\n".join([
        "New enquiry from the website",
        "-" * 32,
        f"Name: {data['name']}",
        f"Company: {data['company'] or '-'}",
        f"Country: {data['country']}",
        f"Email: {data['email']}",
        f"Product of interest: {', '.join(products) or '-'}",
        f"Required quantity: {data['quantity'] or '-'}",
        f"Phone: {data['phone'] or '-'}",
        "",
        "Message:",
        data["message"],
    ])

    try:
        EmailMessage(
            subject=f"New enquiry from {data['name']} ({data['country']})",
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[section.recipient_email],
            reply_to=[data["email"]],
         ).send()
        enquiry.mail_sent = True
        enquiry.save(update_fields=["mail_sent"])
    except Exception:
        logger.exception("Enquiry mail failed")
        return JsonResponse({
            "ok": False,
            "message": "Sorry, we could not send your enquiry right now. "
                       "Please try again in a moment or contact us on WhatsApp.",
        }, status=500)

    return JsonResponse({"ok": True, "message": section.success_message})