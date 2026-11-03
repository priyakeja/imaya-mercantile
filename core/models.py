from django.db import models


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=150, default="Imaya Mercantile")
    logo = models.ImageField(upload_to="logo/")
    favicon = models.ImageField(upload_to="logo/", blank=True, null=True)

    primary_color = models.CharField(
        max_length=7, default="#0B2A4A", help_text="Navy colour (hex). Header button, overlay"
    )
    accent_color = models.CharField(
        max_length=7, default="#C98A2B", help_text="Gold colour (hex). Active menu, highlights, buttons"
    )

    email = models.EmailField(blank=True, help_text="'Email Us' button inga irundhu mailto aagum")
    phone = models.CharField(max_length=30, blank=True)

    header_button_text = models.CharField(max_length=60, default="Request a Quote ↗", blank=True)
    header_button_url = models.CharField(max_length=255, default="#contact", blank=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name


class MenuItem(models.Model):
    title = models.CharField(max_length=60)
    url = models.CharField(max_length=255, help_text="Example: /  or  /about/  or  #products")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    open_in_new_tab = models.BooleanField(default=False)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title