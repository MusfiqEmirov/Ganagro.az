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
    FAQ,
)

admin.site.site_header = 'Ganaqro — Admin'
admin.site.site_title = 'Ganaqro Admin'
admin.site.index_title = 'İdarəetmə paneli'
admin.site.empty_value_display = '—'


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

    def clean(self):
        cleaned_data = super().clean()
        on_main_page = cleaned_data.get('on_main_page')
        category = cleaned_data.get('category')

        if on_main_page and category:
            qs = Product.objects.filter(
                category=category,
                on_main_page=True,
                is_active=True,
            )
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.count() >= 6:
                raise forms.ValidationError(
                    f'"{category}" kateqoriyasında artıq 6 ədəd "Ana səhifədə olsun" məhsul var. '
                    f'Yeni məhsul əlavə etmək üçün əvvəlcə mövcud məhsullardan birini ana səhifədən çıxarın.'
                )
        return cleaned_data


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
            'is_blog_page_background_image',
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
    verbose_name_plural = 'Logo'
    max_num = 1
    extra = 1
    fields = ('image_preview', 'image')
    readonly_fields = ('image_preview',)


class AboutMediaInline(admin.StackedInline):
    """Haqqımızda qalereyasında başlıq və qısa mətn üçün AZ / EN / RU."""

    model = Media
    fk_name = 'about'
    extra = 1
    verbose_name = 'Media'
    verbose_name_plural = 'Media'
    classes = ('wide',)
    readonly_fields = ('image_preview',)

    fieldsets = (
        (_('Media faylı'), {'fields': ('image_preview', 'image', 'video')}),
        (_('Azərbaycan'), {'fields': ('name_az', 'short_description_az'), 'classes': ('wide',)}),
        (_('English'), {'fields': ('name_en', 'short_description_en'), 'classes': ('wide', 'g-lang-en')}),
        (_('Русский'), {'fields': ('name_ru', 'short_description_ru'), 'classes': ('wide', 'g-lang-ru')}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'

    image_preview.short_description = _('Önizləmə')


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
    list_editable = ('is_active', 'on_main_page')
    ordering = ('-created_at',)
    inlines = [ProductMediaInline]
    fieldsets = (
        (_('Azərbaycan'), {'fields': ('name_az', 'description_az'), 'classes': ('wide',)}),
        (_('English'), {'fields': ('name_en', 'description_en'), 'classes': ('wide', 'g-lang-en')}),
        (_('Русский'), {'fields': ('name_ru', 'description_ru'), 'classes': ('wide', 'g-lang-ru')}),
        (_('Parametrlər'), {'fields': ('category', 'slug', 'is_active', 'on_main_page')}),
    )

    def get_prepopulated_fields(self, request, obj=None):
        return {}

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('slug',)
        return ()

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if obj is None:
            result = []
            for name, options in fieldsets:
                fields = tuple(f for f in options.get('fields', []) if f != 'slug')
                result.append((name, {**options, 'fields': fields}))
            return result
        return fieldsets



# ---------------------------------------------------------------------------
# Partner
# ---------------------------------------------------------------------------

@admin.register(Partner)
class PartnerAdmin(AdminImageCompressMixin, admin.ModelAdmin):
    list_display = ('name_az', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name_az', 'name_en', 'name_ru')
    list_editable = ('is_active',)
    ordering = ('-created_at',)
    inlines = [PartnerMediaInline]
    fieldsets = (
        (_('Azərbaycan'), {'fields': ('name_az',)}),
        (_('English'), {'fields': ('name_en',), 'classes': ('wide', 'g-lang-en')}),
        (_('Русский'), {'fields': ('name_ru',), 'classes': ('wide', 'g-lang-ru')}),
        # (_('Sosial şəbəkələr'), {'fields': ('instagram', 'facebook', 'linkedn')}),
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
        (_('Azərbaycan'), {'fields': ('main_title_az', 'second_title_az', 'description_az'), 'classes': ('wide',)}),
        (_('English'), {'fields': ('main_title_en', 'second_title_en', 'description_en'), 'classes': ('wide', 'g-lang-en')}),
        (_('Русский'), {'fields': ('main_title_ru', 'second_title_ru', 'description_ru'), 'classes': ('wide', 'g-lang-ru')}),
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
        (_('Xəritə'), {'fields': ('map_embed_url',)}),
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
    list_display = ('full_name', 'email', 'phone', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('full_name', 'email', 'phone', 'subject')
    ordering = ('-created_at',)
    readonly_fields = ('full_name', 'email', 'phone', 'subject', 'info', 'created_at')
    actions = [mark_as_read, mark_as_unread]

    def has_add_permission(self, request):
        return False


# ---------------------------------------------------------------------------
# Motto
# ---------------------------------------------------------------------------

@admin.register(Motto)
class MottoAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'show_on_home_hero',
        'is_about_page',
        'is_contact_page',
        'is_product_page',
        'is_blog_page',
    )
    list_filter = (
        'show_on_home_hero',
        'is_about_page',
        'is_contact_page',
        'is_product_page',
        'is_blog_page',
    )
    fieldsets = (
        (_('Azərbaycan'), {'fields': ('text_az',)}),
        (_('English'), {'fields': ('text_en',), 'classes': ('wide', 'g-lang-en')}),
        (_('Русский'), {'fields': ('text_ru',), 'classes': ('wide', 'g-lang-ru')}),
        (_('Harada göstərilsin'), {
            'fields': (
                'show_on_home_hero',
                'is_about_page',
                'is_contact_page',
                'is_product_page',
                'is_blog_page',
            ),
            'description': _(
                'Səhifə seçilsə, deviz həmin səhifənin başlıq bölməsində (h1 altında) görünəcək. '
                'Ana səhifə karuseli üçün "Ana səhifə karuselində göstər" işarələyin.'
            ),
        }),
    )


# ---------------------------------------------------------------------------
# Statistic
# ---------------------------------------------------------------------------

@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Göstərici 1'), {
            'fields': (
                'value_one',
                'caption_one_az',
                'caption_one_en',
                'caption_one_ru',
            ),
        }),
        (_('Göstərici 2'), {
            'fields': (
                'value_two',
                'caption_two_az',
                'caption_two_en',
                'caption_two_ru',
            ),
        }),
        (_('Göstərici 3'), {
            'fields': (
                'value_three',
                'caption_three_az',
                'caption_three_en',
                'caption_three_ru',
            ),
        }),
        (_('Göstərici 4'), {
            'fields': (
                'value_four',
                'caption_four_az',
                'caption_four_en',
                'caption_four_ru',
            ),
        }),
    )
    list_display = (
        '__str__',
        'value_one',
        'value_two',
        'value_three',
        'value_four',
    )


# ---------------------------------------------------------------------------
# Media (page background images only)
# ---------------------------------------------------------------------------

@admin.register(Media)
class MediaAdmin(AdminImageCompressMixin, admin.ModelAdmin):
    """Yalnız səhifə fon şəkilləri: məhsul/partnyor/Haqqımızda inlaynlərində yaradılan media burada görünmür."""

    form = MediaAdminForm
    list_display = (
        'image_preview',
        'is_home_page_background_image',
        'is_about_page_background_image',
        'is_contact_page_background_image',
        'is_product_page_background_image',
        'is_blog_page_background_image',
        'created_at',
    )
    list_filter = (
        'is_home_page_background_image',
        'is_about_page_background_image',
        'is_contact_page_background_image',
        'is_product_page_background_image',
        'is_blog_page_background_image',
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
            'is_blog_page_background_image',
        )}),
        (_('Metadata'), {'fields': ('created_at',)}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return '—'

    image_preview.short_description = _('Önizləmə')

    def get_queryset(self, request):
        """Inlayndan gələn kontent mediaya qarışmasın."""
        qs = super().get_queryset(request)
        return qs.filter(
            about__isnull=True,
            product__isnull=True,
            partner__isnull=True,
        )

    def save_model(self, request, obj, form, change):
        obj.about = None
        obj.product = None
        obj.partner = None
        obj.video = None
        super().save_model(request, obj, form, change)


# ---------------------------------------------------------------------------
# FAQ
# ---------------------------------------------------------------------------

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question_az', 'sort_order', 'is_active', 'created_at')
    list_editable = ('sort_order', 'is_active')
    search_fields = ('question_az', 'question_en', 'question_ru', 'answer_az')
    ordering = ('sort_order', 'id')
    fieldsets = (
        (_('Azərbaycan'), {'fields': ('question_az', 'answer_az'), 'classes': ('wide',)}),
        (_('English'), {'fields': ('question_en', 'answer_en'), 'classes': ('wide', 'g-lang-en')}),
        (_('Русский'), {'fields': ('question_ru', 'answer_ru'), 'classes': ('wide', 'g-lang-ru')}),
        (_('Parametrlər'), {'fields': ('sort_order', 'is_active')}),
    )


# ---------------------------------------------------------------------------
# Blog
# ---------------------------------------------------------------------------

@admin.register(Blog)
class BlogAdmin(AdminImageCompressMixin, admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ('image_preview', 'name_az', 'date', 'on_main_page', 'view_count', 'created_at')
    search_fields = ('name_az', 'name_en', 'name_ru')
    list_filter = ('on_main_page',)
    ordering = ('-date', '-created_at')
    readonly_fields = ('image_preview', 'view_count', 'created_at')
    fieldsets = (
        (_('Azərbaycan'), {'fields': ('name_az', 'description_az'), 'classes': ('wide',)}),
        (_('English'), {'fields': ('name_en', 'description_en'), 'classes': ('wide', 'g-lang-en')}),
        (_('Русский'), {'fields': ('name_ru', 'description_ru'), 'classes': ('wide', 'g-lang-ru')}),
        (_('Media'), {'fields': ('image_preview', 'image')}),
        (_('Parametrlər'), {'fields': ('date', 'on_main_page', 'view_count', 'created_at')}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return '—'

    image_preview.short_description = _('Önizləmə')
