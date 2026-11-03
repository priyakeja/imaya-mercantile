from django.db import models
import re
from urllib.parse import quote, quote_plus
from django.core.validators import MaxValueValidator, RegexValidator
from django.utils.html import escape
from django.utils.safestring import mark_safe

class HeroSettings(models.Model):
    autoplay = models.BooleanField(default=True)
    slide_duration = models.PositiveIntegerField(default=6, help_text="Ovvoru slide um ethana seconds irukkanum")
    zoom_scale = models.FloatField(default=1.12, help_text="Zoom-in alavu (1.05 = konjam, 1.2 = adhigam)")
    overlay_opacity = models.PositiveIntegerField(default=90, help_text="Dark overlay 0-100")
    show_dots = models.BooleanField(default=True)
    show_arrows = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Hero Settings"
        verbose_name_plural = "Hero Settings"

    def __str__(self):
        return "Hero Settings"


class HeroSlide(models.Model):
    eyebrow = models.CharField(max_length=100, help_text="Example: GLOBAL TRADE")
    title_line_1 = models.CharField(max_length=100, help_text="White colour line")
    title_line_2 = models.CharField(max_length=100, help_text="Gold colour line")
    description = models.TextField()
    background_image = models.ImageField(upload_to="hero/")

    primary_button_text = models.CharField(max_length=60)
    primary_button_url = models.CharField(max_length=255, default="#")
    primary_button_icon = models.CharField(
        max_length=60, blank=True, default="fa-solid fa-arrow-right-long",
        help_text="Font Awesome class. Venam na empty ah vidunga"
    )

    secondary_button_text = models.CharField(max_length=60, blank=True, default="Email Us")
    secondary_button_url = models.CharField(
        max_length=255, blank=True, help_text="Empty na Site Settings email ku mailto aagum"
    )
    secondary_button_icon = models.CharField(
        max_length=60, blank=True, default="fa-regular fa-envelope",
        help_text="Font Awesome class"
    )

    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title_line_1}"

    

class AboutSection(models.Model):
    heading = models.CharField(max_length=200, default="Rooted in quality, built on partnership.")
    description = models.TextField(
        default="We connect quality agricultural produce with buyers worldwide — through responsible sourcing, careful handling and open, reliable communication."
    )
    main_image = models.ImageField(upload_to="about/", help_text="Left side periya image")
    small_image = models.ImageField(
        upload_to="about/", blank=True, null=True, help_text="Keela overlap aagura chinna square image"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "About Section"
        verbose_name_plural = "About Section"

    def __str__(self):
        return "About Section"


class AboutTab(models.Model):
    section = models.ForeignKey(AboutSection, on_delete=models.CASCADE, related_name="tabs")
    title = models.CharField(max_length=60, help_text="Example: Sourcing")
    content = models.TextField(help_text="Tab click panna keela varum text")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title



class ProductsSection(models.Model):
    eyebrow = models.CharField(max_length=100, default="Our Products")
    heading = models.CharField(max_length=200, default="From the field, with care")
    subtitle = models.CharField(
        max_length=255, blank=True, default="Contact us for specifications and availability."
    )
    button_text = models.CharField(
        max_length=60, default="Enquire About Product ↗", help_text="Card keela irukkura link text"
    )

    # popup texts
    modal_eyebrow = models.CharField(max_length=100, default="Product Overview")
    overview_label = models.CharField(max_length=60, default="Overview")
    range_label = models.CharField(
        max_length=60, default="Product Range", help_text="Product name pinnaadi varum: TURMERIC PRODUCT RANGE"
    )
    journey_eyebrow = models.CharField(max_length=100, default="Visual Processing Journey")
    journey_heading = models.CharField(max_length=150, default="From product to shipment")
    spec_eyebrow = models.CharField(max_length=100, default="Specifications")
    spec_heading = models.CharField(max_length=150, default="Product information")
    packaging_label = models.CharField(max_length=60, default="Packaging")
    modal_footer_note = models.CharField(
        max_length=200, default="Product details are confirmed per enquiry."
    )
    modal_button_prefix = models.CharField(
        max_length=60, default="Enquire About", help_text="Button: Enquire About + Product name ↗"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Products Section"
        verbose_name_plural = "Products Section"

    def __str__(self):
        return "Products Section"


class JourneyStep(models.Model):
    title = models.CharField(max_length=60, help_text="Example: Origin")
    description = models.CharField(max_length=120, blank=True, default="Supplier details to confirm")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
        verbose_name = "Journey Step"

    def __str__(self):
        return self.title


class Product(models.Model):
    # card
    name = models.CharField(max_length=100)
    short_description = models.TextField()
    image = models.ImageField(upload_to="products/")
    order = models.PositiveIntegerField(default=0, help_text="01, 02 number automatic ah order padi varum")
    is_active = models.BooleanField(default=True)

    # popup
    category = models.CharField(
        max_length=60, blank=True, default="Spice", help_text="Spice / Agricultural Produce"
    )
    overview = models.TextField(blank=True, default="")
    range_items = models.TextField(
        blank=True, default="", help_text="Product range list. Ovvoru line um oru bullet"
    )
    packaging_text = models.TextField(
        blank=True, default="Packaging and product specifications are confirmed per enquiry."
    )
    button_url = models.CharField(
        max_length=255, default="#contact", help_text="Popup la irukkura Enquire button link"
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

    @property
    def range_list(self):
        return [line.strip() for line in self.range_items.splitlines() if line.strip()]


class ProductSpec(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specs")
    label = models.CharField(max_length=100, help_text="Example: Curcumin")
    value = models.CharField(max_length=255, help_text="Example: From 1% to 6%")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.product.name} - {self.label}"



class WhySection(models.Model):
    eyebrow = models.CharField(max_length=100, default="Why Choose Us")
    heading = models.CharField(max_length=200, default="Principles that guide every shipment.")
    image = models.ImageField(upload_to="why/")

    badge_icon = models.CharField(
        max_length=60, blank=True, default="bi bi-leaf", help_text="Image mela navy card icon class"
    )
    badge_text = models.CharField(max_length=150, default="Indian produce, handled with care.")

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Why Choose Us Section"
        verbose_name_plural = "Why Choose Us Section"

    def __str__(self):
        return "Why Choose Us Section"


class WhyFeature(models.Model):
    section = models.ForeignKey(WhySection, on_delete=models.CASCADE, related_name="features")
    icon = models.CharField(
        max_length=60,
        default="bi bi-shield-check",
        help_text="Bootstrap Icons: 'bi bi-shield-check' | Font Awesome: 'fa-regular fa-handshake'",
    )
    title = models.CharField(max_length=120)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

class ProcessSection(models.Model):
    eyebrow = models.CharField(max_length=100, default="Our Export Process")
    heading = models.CharField(max_length=200, default="From source to shipment")
    step_prefix = models.CharField(
        max_length=30, blank=True, default="Step",
        help_text="Card la 'Step 01' nu varum. Prefix inga maathalaam",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Process Section"
        verbose_name_plural = "Process Section"

    def __str__(self):
        return "Process Section"


class ProcessStep(models.Model):
    section = models.ForeignKey(ProcessSection, on_delete=models.CASCADE, related_name="steps")
    icon = models.CharField(
        max_length=60,
        default="bi bi-box",
        help_text="Bootstrap: 'bi bi-box' | Boxicons: 'bx bx-ship' | Font Awesome: 'fa-solid fa-seedling'",
    )
    image = models.ImageField(upload_to="process/")
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0, help_text="Step 01, 02 number order padi automatic ah varum")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

class CommitmentSection(models.Model):
    eyebrow = models.CharField(max_length=100, default="Export Commitment")
    heading = models.CharField(max_length=200, default="From Indian Origins to International Opportunities.")
    description = models.TextField(
        default="We are committed to connecting the richness of Indian agriculture with buyers seeking dependable quality."
    )
    background_image = models.ImageField(upload_to="commitment/")

    overlay_start = models.PositiveIntegerField(
        default=90, help_text="Left side navy overlay darkness (0-100)"
    )
    overlay_end = models.PositiveIntegerField(
        default=25, help_text="Right side navy overlay darkness (0-100)"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Export Commitment Section"
        verbose_name_plural = "Export Commitment Section"

    def __str__(self):
        return "Export Commitment Section"

class CertificationSection(models.Model):
    eyebrow = models.CharField(max_length=100, default="Certifications & Quality")
    heading = models.CharField(max_length=200, default="Certification gallery")
    valid_label = models.CharField(
        max_length=40, default="Valid until:",
        help_text="Card la 'Valid until: ...' nu varum. Label inga maathalaam",
    )
    placeholder_text = models.CharField(
        max_length=80, default="Certificate image placeholder",
        help_text="Image upload pannala na kaattura text",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Certification Section"
        verbose_name_plural = "Certification Section"

    def __str__(self):
        return "Certification Section"


class Certificate(models.Model):
    section = models.ForeignKey(
        CertificationSection, on_delete=models.CASCADE, related_name="certificates"
    )
    name = models.CharField(max_length=150, help_text="Example: FSSAI License")
    issued_by = models.CharField(
        max_length=150, blank=True, default="To be Added",
        help_text="Name keela small text (issuer / registration number)",
    )
    valid_until = models.CharField(
        max_length=100, blank=True, default="To be Added",
        help_text="Example: 31 Mar 2028 (text, so 'To be Added' um podalaam)",
    )
    image = models.ImageField(
        upload_to="certificates/", blank=True, null=True,
        help_text="Empty na placeholder kaattum",
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

class ContactSection(models.Model):
    # heading
    eyebrow = models.CharField(max_length=100, default="Contact")
    heading = models.CharField(max_length=200, default="Let’s talk trade.")
    form_title = models.CharField(max_length=100, default="Enquiry form")
    is_active = models.BooleanField(default=True)

    # contact details
    email_title = models.CharField(max_length=40, default="Email")
    email = models.EmailField(default="info@imayamercantile.in")
    email_icon = models.CharField(max_length=60, default="bi bi-envelope",
                                  help_text="Bootstrap icon class. Example: bi bi-envelope")

    address_title = models.CharField(max_length=40, default="Address")
    address = models.CharField(max_length=255, default="Namakkal, India")
    address_icon = models.CharField(max_length=60, default="bi bi-geo-alt")
    map_url = models.URLField(blank=True, help_text="Optional. Empty na address la irundhu Google Maps link auto aagum")

    phone_title = models.CharField(max_length=40, default="Phone")
    phone = models.CharField(max_length=30, default="70106 17086")
    phone_icon = models.CharField(max_length=60, default="bi bi-telephone")

    # form labels
    label_name = models.CharField(max_length=60, default="Name")
    label_company = models.CharField(max_length=60, default="Company")
    label_country = models.CharField(max_length=60, default="Country")
    label_email = models.CharField(max_length=60, default="Email")
    label_products = models.CharField(max_length=60, default="Product of interest")
    products_placeholder = models.CharField(max_length=60, default="Select products")
    label_quantity = models.CharField(max_length=60, default="Required quantity")
    label_phone = models.CharField(max_length=60, default="Phone number")
    label_message = models.CharField(max_length=60, default="Message")
    submit_text = models.CharField(max_length=60, default="Submit Enquiry")
    submit_icon = models.CharField(max_length=60, default="bi bi-arrow-up-right")

    # mail
    recipient_email = models.EmailField(help_text="Enquiry mail inga varum")
    success_message = models.TextField(
        default="Thank you! Your enquiry has been sent. We will get back to you shortly."
    )

    # whatsapp
    whatsapp_enabled = models.BooleanField(default=True)
    whatsapp_number = models.CharField(
        max_length=20, default="917010617086",
        help_text="Country code oda, + illama. Example: 917010617086",
    )
    whatsapp_message = models.TextField(
        default="Hello Imaya Mercantile, I would like to enquire about your products."
    )
    product_whatsapp_message = models.TextField(
        default="Hello Imaya Mercantile, I would like to enquire about {product}.",
        help_text="Product popup button message. {product} nu irundha andha idathula product name varum",
    )

    class Meta:
        verbose_name = "Contact Section"
        verbose_name_plural = "Contact Section"

    def __str__(self):
        return "Contact Section"

    @property
    def email_link(self):
        return f"https://mail.google.com/mail/?view=cm&fs=1&to={quote(self.email, safe='@')}"

    @property
    def mailto_link(self):
        return f"mailto:{self.email}"

    @property
    def phone_link(self):
        return "tel:" + re.sub(r"[^\d+]", "", self.phone)

    @property
    def map_link(self):
        return self.map_url or f"https://www.google.com/maps/search/?api=1&query={quote_plus(self.address)}"

    @property
    def whatsapp_link(self):
        number = re.sub(r"\D", "", self.whatsapp_number)
        return f"https://wa.me/{number}?text={quote(self.whatsapp_message)}"
    
    def product_whatsapp_link(self, product_name):
        number = re.sub(r"\D", "", self.whatsapp_number)
        text = self.product_whatsapp_message.replace("{product}", product_name)
        return f"https://wa.me/{number}?text={quote(text)}"

class ContactImage(models.Model):
    section = models.ForeignKey(ContactSection, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="contact/")
    alt_text = models.CharField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.alt_text or f"Contact image {self.pk}"


class ContactEnquiry(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=80)
    email = models.EmailField()
    products = models.CharField(max_length=500, blank=True)
    quantity = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    mail_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Enquiry"
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.name} ({self.country})"
    
class FAQSection(models.Model):
    eyebrow = models.CharField(max_length=100, default="Buyer Information")
    heading = models.CharField(max_length=200, default="Questions, answered.")
    description = models.TextField(
        blank=True,
        default="Share your requirements with us for details on products, orders and export enquiries.",
    )
    one_at_a_time = models.BooleanField(
        default=True, help_text="Tick na oru question open aana matha question close aagum"
    )
    open_first = models.BooleanField(
        default=False, help_text="Page load la 1st question open ah irukkanum na tick pannunga"
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "FAQ Section"
        verbose_name_plural = "FAQ Section"

    def __str__(self):
        return "FAQ Section"


class FAQItem(models.Model):
    section = models.ForeignKey(FAQSection, on_delete=models.CASCADE, related_name="items")
    question = models.CharField(max_length=255)
    answer = models.TextField(help_text="Enter pottu pudhu line / paragraph podalaam")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question
    
class BusinessEnquirySection(models.Model):
    eyebrow = models.CharField(max_length=100, default="Business Enquiry")
    heading = models.CharField(max_length=200, default="Looking for an Agricultural Export Partner?")
    description = models.TextField(
        blank=True,
        default="Share your requirements and we’ll get back to you with next steps.",
    )

    button_text = models.CharField(max_length=60, default="Send an Enquiry")
    button_link = models.CharField(
        max_length=255, default="#contact",
        help_text="Section na #contact, page link na full URL (https://...)",
    )
    button_icon = models.CharField(
        max_length=60, blank=True, default="bi bi-arrow-right",
        help_text="Bootstrap icon class. Icon vendam na empty ah vidunga",
    )
    open_in_new_tab = models.BooleanField(default=False)

    background_image = models.ImageField(upload_to="business_enquiry/", blank=True)
    overlay_color = models.CharField(
        max_length=7, default="#ffffff",
        validators=[RegexValidator(r"^#[0-9a-fA-F]{6}$", "Hex color kudunga. Example: #ffffff")],
        help_text="Image mela varura overlay color. Example: #ffffff",
    )
    overlay_start = models.PositiveIntegerField(
        default=75, validators=[MaxValueValidator(100)],
        help_text="Left side overlay (0-100). Athigam na image mangum",
    )
    overlay_end = models.PositiveIntegerField(
        default=70, validators=[MaxValueValidator(100)],
        help_text="Right side overlay (0-100)",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Business Enquiry Section"
        verbose_name_plural = "Business Enquiry Section"

    def __str__(self):
        return "Business Enquiry Section"
    
HEX_VALIDATOR = RegexValidator(r"^#[0-9a-fA-F]{6}$", "Hex color kudunga. Example: #041b35")


class FooterSection(models.Model):
    # top call-to-action band
    cta_eyebrow = models.CharField(max_length=100, default="Let’s Work Together")
    cta_heading = models.CharField(
        max_length=200, default="Let’s bring the finest {Indian produce} to you.",
        help_text="{ } kulla irukkura text gold color la varum. Example: Let’s bring the finest {Indian produce} to you.",
    )
    cta_description = models.TextField(
        blank=True,
        default="Connect with IMAYA MERCANTILE for product information and export enquiries.",
    )
    cta_button_text = models.CharField(max_length=60, default="Send an Enquiry")
    cta_button_link = models.CharField(max_length=255, default="#contact")
    cta_button_icon = models.CharField(
        max_length=60, blank=True, default="bi bi-arrow-up-right",
        help_text="Bootstrap icon class. Vendam na empty",
    )
    cta_new_tab = models.BooleanField(default=False)

    # brand column
    logo = models.ImageField(
        upload_to="footer/", blank=True,
        help_text="Empty na Site Settings la irukkura logo use aagum",
    )
    tagline = models.CharField(max_length=150, default="Quality Agriculture. Global Possibilities.")
    badge_text = models.CharField(max_length=80, blank=True, default="Quality · Trust · Export")

    # column titles (links Footer links la add pannunga)
    explore_title = models.CharField(max_length=40, default="Explore")
    quick_title = models.CharField(max_length=40, default="Quick Links")
    contact_title = models.CharField(max_length=40, default="Get in Touch")
    quote_text = models.CharField(max_length=60, default="Request a Quote")
    quote_link = models.CharField(max_length=255, default="#contact")
    quote_icon = models.CharField(max_length=60, blank=True, default="bi bi-arrow-up-right")

    # bottom bar
    copyright_text = models.CharField(max_length=200, default="© IMAYA MERCANTILE. All rights reserved.")
    credit_prefix = models.CharField(max_length=80, blank=True, default="Designed & Developed by")
    credit_name = models.CharField(max_length=120, blank=True, default="Vetri IT Systems Private Limited")
    credit_url = models.URLField(blank=True, help_text="Company website link. Empty na link illama text mattum varum")
    show_back_to_top = models.BooleanField(default=True)

    # colours
    bg_start = models.CharField(max_length=7, default="#041b35", validators=[HEX_VALIDATOR],
                                help_text="Background gradient left/top color")
    bg_end = models.CharField(max_length=7, default="#07355d", validators=[HEX_VALIDATOR],
                              help_text="Background gradient right/bottom color")
    highlight_color = models.CharField(max_length=7, default="#e3b36a", validators=[HEX_VALIDATOR],
                                       help_text="Gold text color (eyebrow, heading highlight, icons)")
    button_color = models.CharField(max_length=7, default="#d5a14c", validators=[HEX_VALIDATOR],
                                    help_text="Send an Enquiry button color")

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Footer"
        verbose_name_plural = "Footer"

    def __str__(self):
        return "Footer"

    @property
    def cta_heading_html(self):
        parts = re.split(r"\{(.+?)\}", self.cta_heading)
        out = []
        for i, part in enumerate(parts):
            if i % 2:
                out.append(f'<span class="ft-hl">{escape(part)}</span>')
            else:
                out.append(escape(part))
        return mark_safe("".join(out))


class FooterLink(models.Model):
    COLUMN_CHOICES = [("explore", "Explore column"), ("quick", "Quick Links column")]

    section = models.ForeignKey(FooterSection, on_delete=models.CASCADE, related_name="links")
    column = models.CharField(max_length=10, choices=COLUMN_CHOICES, default="explore")
    title = models.CharField(max_length=60)
    url = models.CharField(max_length=255, help_text="Example: /  or  #about  or  #products")
    order = models.PositiveIntegerField(default=0)
    open_in_new_tab = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title
    
class FeedbackSection(models.Model):
    THEME_CHOICES = [("dark", "Dark (navy background)"), ("light", "Light (white background)")]

    eyebrow = models.CharField(max_length=100, default="Client Feedback")
    heading = models.CharField(max_length=200, default="Trusted by buyers across the world")
    description = models.TextField(
        blank=True,
        default="Hear from the importers and partners we have supplied with quality Indian agricultural products.",
    )
    theme = models.CharField(max_length=5, choices=THEME_CHOICES, default="dark")
    show_rating = models.BooleanField(default=True, help_text="Star rating kaattanum na tick")
    show_arrows = models.BooleanField(default=True)
    show_dots = models.BooleanField(default=True)
    autoplay = models.BooleanField(default=True, help_text="Thaanaa slide aagum")
    autoplay_seconds = models.PositiveIntegerField(
        default=5, validators=[MaxValueValidator(60)],
        help_text="Ovvoru slide um ethana seconds (1-60)",
    )
    is_active = models.BooleanField(default=True, help_text="Untick pannina section website la theriyaadhu")

    class Meta:
        verbose_name = "Feedback Section"
        verbose_name_plural = "Feedback Section"

    def __str__(self):
        return "Feedback Section"


class Feedback(models.Model):
    RATING_CHOICES = [(i, f"{i} star{'s' if i > 1 else ''}") for i in range(5, 0, -1)]

    section = models.ForeignKey(FeedbackSection, on_delete=models.CASCADE, related_name="feedbacks")
    name = models.CharField(max_length=100, help_text="Customer name")
    role = models.CharField(max_length=100, blank=True, help_text="Example: Purchase Manager")
    company = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=80, blank=True, help_text="Example: United Arab Emirates")
    photo = models.ImageField(
        upload_to="feedback/", blank=True, null=True,
        help_text="Optional. Empty na name oda first letter kaattum",
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=5)
    message = models.TextField(help_text="Customer feedback text")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    def __str__(self):
        return f"{self.name} ({self.rating}\u2605)"

    @property
    def initial(self):
        return (self.name or "?").strip()[:1].upper()

    @property
    def filled_stars(self):
        return range(self.rating)

    @property
    def empty_stars(self):
        return range(5 - self.rating)

    @property
    def subtitle(self):
        return ", ".join(x for x in (self.role, self.company) if x)