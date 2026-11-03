from django.contrib import admin
from django.utils.html import format_html
from .models import (
    HeroSettings, HeroSlide, AboutSection, AboutTab,
    ProductsSection, Product, ProductSpec, JourneyStep,
    WhySection, WhyFeature,ProcessSection, ProcessStep,
    CommitmentSection,CertificationSection, Certificate,
    ContactSection, ContactImage, ContactEnquiry,
    FAQSection, FAQItem, BusinessEnquirySection,
    FooterSection, FooterLink, 
    FeedbackSection, Feedback,
)


@admin.register(HeroSettings)
class HeroSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not HeroSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("preview", "title_line_1", "title_line_2", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)

    def preview(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;">', obj.background_image.url)
        return "-"


class AboutTabInline(admin.TabularInline):
    model = AboutTab
    extra = 3
    fields = ("title", "order", "is_active")


@admin.register(AboutSection)
class AboutSectionAdmin(admin.ModelAdmin):
    inlines = [AboutTabInline]

    def has_add_permission(self, request):
        return not AboutSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ProductsSection)
class ProductsSectionAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Section heading", {"fields": ("eyebrow", "heading", "subtitle", "button_text", "is_active")}),
        ("Popup texts", {"fields": (
            "modal_eyebrow", "overview_label", "range_label",
            "journey_eyebrow", "journey_heading",
            "spec_eyebrow", "spec_heading", "packaging_label",
            "modal_footer_note", "modal_button_prefix",
        )}),
    )

    def has_add_permission(self, request):
        return not ProductsSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(JourneyStep)
class JourneyStepAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)


class ProductSpecInline(admin.TabularInline):
    model = ProductSpec
    extra = 4
    fields = ("label", "value", "order")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("preview", "name", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)
    inlines = [ProductSpecInline]
    fieldsets = (
        ("Card", {"fields": ("name", "short_description", "image", "order", "is_active")}),
        ("Popup", {"fields": ("category", "overview", "range_items", "packaging_text", "button_url")}),
    )

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;border-radius:4px;">', obj.image.url)
        return "-"



class WhyFeatureInline(admin.StackedInline):
    model = WhyFeature
    extra = 4
    fields = ("icon", "title", "description", "order", "is_active")


@admin.register(WhySection)
class WhySectionAdmin(admin.ModelAdmin):
    inlines = [WhyFeatureInline]

    def has_add_permission(self, request):
        return not WhySection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

class ProcessStepInline(admin.StackedInline):
    model = ProcessStep
    extra = 4
    fields = ("icon", "image", "title", "description", "order", "is_active")


@admin.register(ProcessSection)
class ProcessSectionAdmin(admin.ModelAdmin):
    inlines = [ProcessStepInline]

    def has_add_permission(self, request):
        return not ProcessSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(CommitmentSection)
class CommitmentSectionAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Content", {"fields": ("eyebrow", "heading", "description", "background_image", "is_active")}),
        ("Overlay", {"fields": ("overlay_start", "overlay_end")}),
    )

    def has_add_permission(self, request):
        return not CommitmentSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

class CertificateInline(admin.StackedInline):
    model = Certificate
    extra = 4
    fields = ("name", "issued_by", "valid_until", "image", "order", "is_active")


@admin.register(CertificationSection)
class CertificationSectionAdmin(admin.ModelAdmin):
    inlines = [CertificateInline]

    def has_add_permission(self, request):
        return not CertificationSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

class ContactImageInline(admin.TabularInline):
    model = ContactImage
    extra = 3


@admin.register(ContactSection)
class ContactSectionAdmin(admin.ModelAdmin):
    inlines = [ContactImageInline]
    fieldsets = (
        ("Heading", {"fields": ("eyebrow", "heading", "form_title", "is_active")}),
        ("Contact details", {"fields": (
            ("email_title", "email", "email_icon"),
            ("address_title", "address", "address_icon"),
            "map_url",
            ("phone_title", "phone", "phone_icon"),
        )}),
        ("Form labels", {"fields": (
            "label_name", "label_company", "label_country", "label_email",
            "label_products", "products_placeholder", "label_quantity",
            "label_phone", "label_message", ("submit_text", "submit_icon"),
        )}),
        ("Mail", {"fields": ("recipient_email", "success_message")}),
                ("WhatsApp", {"fields": ("whatsapp_enabled", "whatsapp_number", "whatsapp_message", "product_whatsapp_message")}),
    )

    def has_add_permission(self, request):
        return not ContactSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactEnquiry)
class ContactEnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "country", "phone", "mail_sent", "created_at")
    list_filter = ("mail_sent", "created_at")
    search_fields = ("name", "email", "company", "country", "message")
    readonly_fields = [f.name for f in ContactEnquiry._meta.fields]

    def has_add_permission(self, request):
        return False
    
class FAQItemInline(admin.StackedInline):
    model = FAQItem
    extra = 1
    fields = ("question", "answer", ("order", "is_active"))


@admin.register(FAQSection)
class FAQSectionAdmin(admin.ModelAdmin):
    inlines = [FAQItemInline]
    fieldsets = (
        ("Heading", {"fields": ("eyebrow", "heading", "description", "is_active")}),
        ("Behaviour", {"fields": ("one_at_a_time", "open_first")}),
    )

    def has_add_permission(self, request):
        return not FAQSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
    
@admin.register(BusinessEnquirySection)
class BusinessEnquirySectionAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Content", {"fields": ("eyebrow", "heading", "description", "is_active")}),
        ("Button", {"fields": ("button_text", "button_link", "button_icon", "open_in_new_tab")}),
        ("Background", {"fields": ("background_image", "overlay_color", ("overlay_start", "overlay_end"))}),
    )

    def has_add_permission(self, request):
        return not BusinessEnquirySection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
    
class FooterLinkInline(admin.TabularInline):
    model = FooterLink
    extra = 6
    fields = ("column", "title", "url", "order", "open_in_new_tab", "is_active")


@admin.register(FooterSection)
class FooterSectionAdmin(admin.ModelAdmin):
    inlines = [FooterLinkInline]
    fieldsets = (
        ("Top band", {"fields": (
            "cta_eyebrow", "cta_heading", "cta_description",
            "cta_button_text", "cta_button_link", "cta_button_icon", "cta_new_tab",
        )}),
        ("Brand column", {"fields": ("logo", "tagline", "badge_text")}),
        ("Columns", {"fields": (
            "explore_title", "quick_title", "contact_title",
            "quote_text", "quote_link", "quote_icon",
        )}),
        ("Bottom bar", {"fields": (
            "copyright_text", "credit_prefix", "credit_name", "credit_url", "show_back_to_top",
        )}),
        ("Colours", {"fields": ("bg_start", "bg_end", "highlight_color", "button_color")}),
        ("Status", {"fields": ("is_active",)}),
    )

    def has_add_permission(self, request):
        return not FooterSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
    
class FeedbackInline(admin.StackedInline):
    model = Feedback
    extra = 1
    fields = (("name", "rating"), ("role", "company", "country"), "photo", "message", ("order", "is_active"))


@admin.register(FeedbackSection)
class FeedbackSectionAdmin(admin.ModelAdmin):
    inlines = [FeedbackInline]
    fieldsets = (
        ("Heading", {"fields": ("eyebrow", "heading", "description", "is_active")}),
        ("Look", {"fields": ("theme", "show_rating")}),
        ("Slider", {"fields": ("show_arrows", "show_dots", ("autoplay", "autoplay_seconds"))}),
    )

    def has_add_permission(self, request):
        return not FeedbackSection.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False