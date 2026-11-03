from .models import SiteSettings, MenuItem


def site_data(request):
    from sections.models import FooterSection, ContactSection

    footer = FooterSection.objects.filter(is_active=True).first()
    links = list(footer.links.filter(is_active=True)) if footer else []

    return {
        "site": SiteSettings.objects.first(),
        "menu_items": MenuItem.objects.filter(is_active=True),
        "footer": footer,
        "footer_explore": [l for l in links if l.column == "explore"],
        "footer_quick": [l for l in links if l.column == "quick"],
        "footer_contact": ContactSection.objects.filter(is_active=True).first(),
    }