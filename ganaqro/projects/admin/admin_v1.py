from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget

from projects.models import (
    Product,
    ProductCategory,
    Media,
    Partner,
    About,
    Contact,
    AppealContact,
    Motto,
    Statistic,
    Blog,
)

admin.site.site_header = 'Ganaqro Admin'
admin.site.site_title = 'Ganaqro'
admin.site.index_title = 'İdarəetmə paneli'


class AdminImageCompressMixin:
    """Browser-side image compression for admin forms that upload images."""

    class Media:
        js = ('assets/js/admin_image_compress.js',)


# ---------------------------------------------------------------------------
# Admin forms (CKEditor for rich-text description fields)
# ---------------------------------------------------------------------------

class AboutAdminForm(forms.ModelForm):
    class Meta:
        model = About
        fields = '__all__'
        widgets = {
            'description_az': CKEditorWidget(),
            'description_en': CKEditorWidget(),
            'description_ru': CKEditorWidget(),
        }


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'description_az': CKEditorWidget(),
            'description_en': CKEditorWidget(),
            'description_ru': CKEditorWidget(),
        }


class BlogAdminForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'
        widgets = {
            'description_az': CKEditorWidget(),
            'description_en': CKEditorWidget(),
            'description_ru': CKEditorWidget(),
        }


class MediaAdminForm(forms.ModelForm):
    """Background images only; content images belong on related model inlines."""

    class Meta:
        model = Media
        fields = (
            'image',
            'is_home_page_background_image',
            'is_about_page_background_image',
            'is_contact_page_background_image',
            'is_product_page_background_image',
        )


# ---------------------------------------------------------------------------
# Content inlines (no background-image flags)
# ---------------------------------------------------------------------------

class ContentMediaInline(admin.TabularInline):
    model = Media
    extra = 1
    fields = ('image_preview', 'image', 'video')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return '—'

    image_preview.short_description = _('Önizləmə')


class ProductMediaInline(ContentMediaInline):
    fk_name = 'product'
    verbose_name = 'Şəkil / Video'
    verbose_name_plural = 'Şəkillər / Videolar'


class PartnerMediaInline(ContentMediaInline):
    fk_name = 'partner'
    verbose_name = 'Logo'
    verbose_name_plural = 'Logolar'
    fields = ('image_preview', 'image')
    readonly_fields = ('image_preview',)


class AboutMediaInline(ContentMediaInline):
    fk_name = 'about'
    verbose_name = 'Media'
    verbose_name_plural = 'Media'
    fields = ('image_preview', 'image', 'video', 'name', 'short_description')
    readonly_fields = ('image_preview',)


# ---------------------------------------------------------------------------
# ProductCategory
# ---------------------------------------------------------------------------

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_az', 'name_en', 'name_ru', 'slug')
    search_fields = ('name_az', 'name_en', 'name_ru')
    prepopulated_fields = {'slug': ('name_az',)}
    ordering = ('id',)


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------

@admin.register(Product)
class ProductAdmin(AdminImageCompressMixin, admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name_az', 'category', 'is_active', 'on_main_page', 'created_at')
    list_filter = ('category', 'is_active', 'on_main_page')
    search_fields = ('name_az', 'name_en', 'name_ru')
    prepopulated_fields = {'slug': ('name_az',)}
    list_editable = ('is_active', 'on_main_page')
    ordering = ('-created_at',)
    inlines = [ProductMediaInline]
    fieldsets = (
        (_('Azərbaycan'), {'fields': ('name_az', 'description_az')}),
        (_('English'), {'fields': ('name_en', 'description_en'), 'classes': ('collapse',)}),
        (_('Русский'), {'fields': ('name_ru', 'description_ru'), 'classes': ('collapse',)}),
        (_('Parametrlər'), {'fields': ('category', 'slug', 'is_active', 'on_main_page')}),
    )


# ---------------------------------------------------------------------------
# Partner
# ---------------------------------------------------------------------------

@admin.register(Partner)
class PartnerAdmin(AdminImageCompressMixin, admin.ModelAdmin):
    list_display = ('name_az', 'is_active', 'instagram', 'facebook', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name_az', 'name_en', 'name_ru')
    list_editable = ('is_active',)
    ordering = ('-created_at',)
    inlines = [PartnerMediaInline]
    fieldsets = (
        (_('Azərbaycan'), {'fields': ('name_az',)}),
        (_('English'), {'fields': ('name_en',), 'classes': ('collapse',)}),
        (_('Русский'), {'fields': ('name_ru',), 'classes': ('collapse',)}),
        (_('Sosial şəbəkələr'), {'fields': ('instagram', 'facebook', 'linkedn')}),
        (_('Parametrlər'), {'fields': ('is_active',)}),
    )


# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------

@admin.register(About)
class AboutAdmin(AdminImageCompressMixin, admin.ModelAdmin):
    form = AboutAdminForm
    list_display = ('main_title_az',)
    search_fields = ('main_title_az',)
    inlines = [AboutMediaInline]
    fieldsets = (
        (_('Azərbaycan'), {'fields': ('main_title_az', 'second_title_az', 'description_az')}),
        (_('English'), {'fields': ('main_title_en', 'second_title_en', 'description_en'), 'classes': ('collapse',)}),
        (_('Русский'), {'fields': ('main_title_ru', 'second_title_ru', 'description_ru'), 'classes': ('collapse',)}),
        (_('Video'), {'fields': ('video', 'video_poster')}),
    )


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('address_az', 'phone', 'email', 'instagram', 'facebook')
    search_fields = ('address_az', 'phone', 'email')
    fieldsets = (
        (_('Ünvan'), {'fields': ('address_az', 'address_en', 'address_ru')}),
        (_('Əlaqə nömrələri'), {'fields': ('phone', 'whatsapp_number')}),
        (_('Sosial şəbəkələr'), {'fields': ('email', 'email_two', 'instagram', 'facebook', 'youtube', 'linkedn', 'tiktok')}),
    )


# ---------------------------------------------------------------------------
# AppealContact
# ---------------------------------------------------------------------------

def mark_as_read(modeladmin, request, queryset):
    queryset.update(is_read=True)


mark_as_read.short_description = _('Seçilmişləri oxunmuş kimi işarələ')


def mark_as_unread(modeladmin, request, queryset):
    queryset.update(is_read=False)


mark_as_unread.short_description = _('Seçilmişləri oxunmamış kimi işarələ')


@admin.register(AppealContact)
class AppealContactAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('full_name', 'email', 'subject')
    ordering = ('-created_at',)
    readonly_fields = ('full_name', 'email', 'subject', 'info', 'created_at')
    actions = [mark_as_read, mark_as_unread]

    def has_add_permission(self, request):
        return False


# ---------------------------------------------------------------------------
# Motto
# ---------------------------------------------------------------------------

@admin.register(Motto)
class MottoAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    fieldsets = (
        (_('Azərbaycan'), {'fields': ('text_az',)}),
        (_('English'), {'fields': ('text_en',), 'classes': ('collapse',)}),
        (_('Русский'), {'fields': ('text_ru',), 'classes': ('collapse',)}),
    )


# ---------------------------------------------------------------------------
# Statistic
# ---------------------------------------------------------------------------

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'value_one', 'value_two', 'value_three', 'value_four')


# ---------------------------------------------------------------------------
# Media (page background images only)
# ---------------------------------------------------------------------------

@admin.register(Media)
class MediaAdmin(AdminImageCompressMixin, admin.ModelAdmin):
    form = MediaAdminForm
    list_display = (
        'image_preview',
        'is_home_page_background_image',
        'is_about_page_background_image',
        'is_contact_page_background_image',
        'is_product_page_background_image',
        'created_at',
    )
    list_filter = (
        'is_home_page_background_image',
        'is_about_page_background_image',
        'is_contact_page_background_image',
        'is_product_page_background_image',
    )
    ordering = ('-created_at',)
    readonly_fields = ('image_preview', 'created_at')

    fieldsets = (
        (_('Şəkil'), {'fields': ('image_preview', 'image')}),
        (_('Hansı səhifənin fonudur'), {'fields': (
            'is_home_page_background_image',
            'is_about_page_background_image',
            'is_contact_page_background_image',
            'is_product_page_background_image',
        )}),
        (_('Metadata'), {'fields': ('created_at',)}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return '—'

    image_preview.short_description = _('Önizləmə')

    def save_model(self, request, obj, form, change):
        obj.about = None
        obj.product = None
        obj.partner = None
        obj.video = None
        super().save_model(request, obj, form, change)


# ---------------------------------------------------------------------------
# Blog
# ---------------------------------------------------------------------------

@admin.register(Blog)
class BlogAdmin(AdminImageCompressMixin, admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ('image_preview', 'name_az', 'date', 'view_count', 'created_at')
    search_fields = ('name_az', 'name_en', 'name_ru')
    ordering = ('-date', '-created_at')
    readonly_fields = ('image_preview', 'view_count', 'created_at')
    fieldsets = (
        (_('Azərbaycan'), {'fields': ('name_az', 'description_az')}),
        (_('English'), {'fields': ('name_en', 'description_en'), 'classes': ('collapse',)}),
        (_('Русский'), {'fields': ('name_ru', 'description_ru'), 'classes': ('collapse',)}),
        (_('Media'), {'fields': ('image_preview', 'image')}),
        (_('Parametrlər'), {'fields': ('date', 'view_count', 'created_at')}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return '—'

    image_preview.short_description = _('Önizləmə')
