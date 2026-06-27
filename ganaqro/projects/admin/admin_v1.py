from django import forms
from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget

from projects.admin.admin_help import (
    AdminPageHelpMixin,
    ABOUT_HELP,
    APPEAL_HELP,
    BLOG_HELP,
    CATEGORY_HELP,
    CONTACT_HELP,
    FAQ_HELP,
    MEDIA_HELP,
    MOTTO_HELP,
    PARTNER_HELP,
    PRODUCT_HELP,
    STATISTIC_HELP,
    patch_admin_site_order,
)
from projects.admin.filters import (
    AppealContactMonthFilter,
    AppealContactPeriodFilter,
    AppealContactYearFilter,
)
from projects.admin.widgets import BootstrapIconSelect

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

admin.site.site_header = 'Ganaqro — Sayt idarəetməsi'
admin.site.site_title = 'Ganaqro Admin'
admin.site.index_title = 'Bölmə seçin — hər biri saytın müəyyən hissəsini idarə edir'
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


class StatisticAdminForm(forms.ModelForm):
    class Meta:
        model = Statistic
        fields = '__all__'
        widgets = {
            'icon_one': BootstrapIconSelect(),
            'icon_two': BootstrapIconSelect(),
            'icon_three': BootstrapIconSelect(),
            'icon_four': BootstrapIconSelect(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ('icon_one', 'icon_two', 'icon_three', 'icon_four'):
            self.fields[field_name].empty_label = _('İkon yoxdur')
            self.fields[field_name].required = False


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
            'is_faq_page_background_image',
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
    verbose_name = 'Şəkil'
    verbose_name_plural = 'Şəkillər'
    fields = ('image_preview', 'image')
    readonly_fields = ('image_preview',)


class PartnerMediaInline(ContentMediaInline):
    fk_name = 'partner'
    verbose_name = 'Logo'
    verbose_name_plural = 'Logo'
    max_num = 1
    extra = 1
    fields = ('image_preview', 'image')
    readonly_fields = ('image_preview',)


class AboutMediaInline(admin.StackedInline):
    """Haqqımızda qalereyası — yalnız şəkillər."""

    model = Media
    fk_name = 'about'
    extra = 1
    verbose_name = 'Qalereya şəkli'
    verbose_name_plural = 'Qalereya şəkilləri'
    classes = ('wide',)
    readonly_fields = ('image_preview',)

    fieldsets = (
        (_('Şəkil'), {'fields': ('image_preview', 'image')}),
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
class ProductCategoryAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    admin_page_help = CATEGORY_HELP
    list_display = ('name_az', 'name_en', 'name_ru', 'slug')
    search_fields = ('name_az', 'name_en', 'name_ru')
    prepopulated_fields = {'slug': ('name_az',)}
    ordering = ('id',)


# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------

@admin.register(Product)
class ProductAdmin(AdminImageCompressMixin, AdminPageHelpMixin, admin.ModelAdmin):
    admin_page_help = PRODUCT_HELP
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
        (_('Parametrlər'), {
            'fields': ('category', 'slug', 'is_active', 'on_main_page'),
            'description': _(
                'Kateqoriya — hansı qrupa aid olduğu. '
                '«Saytda göstərilsin?» söndürülərsə məhsul gizlənir. '
                '«Ana səhifədə göstərilsin?» — ana səhifə məhsul panellərində görünür (hər kateqoriyada max 6).'
            ),
        }),
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
class PartnerAdmin(AdminImageCompressMixin, AdminPageHelpMixin, admin.ModelAdmin):
    admin_page_help = PARTNER_HELP
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
        (_('Parametrlər'), {
            'fields': ('is_active',),
            'description': _('«Saytda göstərilsin?» söndürülərsə loqo karuseldə görünməz.'),
        }),
    )


# ---------------------------------------------------------------------------
# About
# ---------------------------------------------------------------------------

@admin.register(About)
class AboutAdmin(AdminImageCompressMixin, AdminPageHelpMixin, admin.ModelAdmin):
    admin_page_help = ABOUT_HELP
    form = AboutAdminForm
    list_display = ('main_title_az',)
    search_fields = ('main_title_az',)
    inlines = [AboutMediaInline]
    fieldsets = (
        (_('Azərbaycan'), {'fields': ('main_title_az', 'second_title_az', 'description_az'), 'classes': ('wide',)}),
        (_('English'), {'fields': ('main_title_en', 'second_title_en', 'description_en'), 'classes': ('wide', 'g-lang-en')}),
        (_('Русский'), {'fields': ('main_title_ru', 'second_title_ru', 'description_ru'), 'classes': ('wide', 'g-lang-ru')}),
        (_('Əsas tanıtım videosu (yalnız 1)'), {
            'fields': ('video', 'video_poster'),
            'description': _(
                'Haqqımızda və ana səhifədə mətnin yanında göstərilən yeganə video. '
                'Aşağıdakı «Qalereya şəkilləri» bölməsində yalnız şəkil əlavə edilir — video yox.'
            ),
        }),
    )

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for instance in instances:
            if isinstance(instance, Media) and instance.about_id:
                instance.video = None
            instance.save()
        formset.save_m2m()


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

@admin.register(Contact)
class ContactAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    admin_page_help = CONTACT_HELP
    list_display = ('address_az', 'phone', 'email', 'instagram', 'facebook')
    search_fields = ('address_az', 'phone', 'email')
    fieldsets = (
        (_('Ünvan (saytda və footer-də)'), {'fields': ('address_az', 'address_en', 'address_ru')}),
        (_('Xəritə'), {
            'fields': ('map_embed_url',),
            'description': _('Əlaqə səhifəsində Google Xəritə bloku.'),
        }),
        (_('Telefon və WhatsApp'), {'fields': ('phone', 'whatsapp_number')}),
        (_('E-poçt və sosial şəbəkələr'), {
            'fields': ('email', 'email_two', 'instagram', 'facebook', 'youtube', 'linkedn', 'tiktok'),
            'description': _('Footer və Əlaqə səhifəsində ikon/link kimi görünür.'),
        }),
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
class AppealContactAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    admin_page_help = APPEAL_HELP
    list_display = ('full_name', 'email', 'phone', 'is_read', 'created_at')
    list_filter = (
        'is_read',
        AppealContactPeriodFilter,
        AppealContactYearFilter,
        AppealContactMonthFilter,
    )
    search_fields = ('full_name', 'email', 'phone', 'info', 'subject')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('full_name', 'email', 'phone', 'subject', 'info', 'created_at')
    actions = [mark_as_read, mark_as_unread]
    list_per_page = 50

    def has_add_permission(self, request):
        return False


# ---------------------------------------------------------------------------
# Motto
# ---------------------------------------------------------------------------

@admin.register(Motto)
class MottoAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    admin_page_help = MOTTO_HELP
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
        (_('Harada göstərilsin?'), {
            'fields': (
                'show_on_home_hero',
                'is_about_page',
                'is_contact_page',
                'is_product_page',
                'is_blog_page',
            ),
            'description': _(
                'Ana səhifə karuseli — yuxarı slayder. '
                'Digər seçimlər — həmin səhifənin yuxarı banner fon şəklinin üstündə deviz mətni. '
                'Deviz yoxdursa banner boş qalır, amma fon şəkli görünür.'
            ),
        }),
    )


# ---------------------------------------------------------------------------
# Statistic
# ---------------------------------------------------------------------------

@admin.register(Statistic)
class StatisticAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    admin_page_help = STATISTIC_HELP
    form = StatisticAdminForm
    fieldsets = (
        (_('1-ci statistika kartı (soldan birinci)'), {
            'fields': (
                'value_one',
                'icon_one',
                'caption_one_az',
                'caption_one_en',
                'caption_one_ru',
            ),
            'description': _('Böyük rəqəm + istəyə görə ikon + altında qısa izah. Məs: 25 və ya 90+ — İllik təcrübə'),
        }),
        (_('2-ci statistika kartı'), {
            'fields': (
                'value_two',
                'icon_two',
                'caption_two_az',
                'caption_two_en',
                'caption_two_ru',
            ),
        }),
        (_('3-cü statistika kartı'), {
            'fields': (
                'value_three',
                'icon_three',
                'caption_three_az',
                'caption_three_en',
                'caption_three_ru',
            ),
        }),
        (_('4-cü statistika kartı (sağdan sonuncu)'), {
            'fields': (
                'value_four',
                'icon_four',
                'caption_four_az',
                'caption_four_en',
                'caption_four_ru',
            ),
        }),
    )
    list_display = (
        '__str__',
        'value_one',
        'caption_one_az',
        'value_two',
        'caption_two_az',
        'value_three',
        'caption_three_az',
        'value_four',
        'caption_four_az',
    )


# ---------------------------------------------------------------------------
# Media (page background images only)
# ---------------------------------------------------------------------------

@admin.register(Media)
class MediaAdmin(AdminImageCompressMixin, AdminPageHelpMixin, admin.ModelAdmin):
    admin_page_help = MEDIA_HELP
    """Yalnız səhifə fon şəkilləri: məhsul/partnyor/Haqqımızda inlaynlərində yaradılan media burada görünmür."""

    form = MediaAdminForm
    list_display = (
        'image_preview',
        'is_home_page_background_image',
        'is_about_page_background_image',
        'is_contact_page_background_image',
        'is_product_page_background_image',
        'is_blog_page_background_image',
        'is_faq_page_background_image',
        'created_at',
    )
    list_filter = (
        'is_home_page_background_image',
        'is_about_page_background_image',
        'is_contact_page_background_image',
        'is_product_page_background_image',
        'is_blog_page_background_image',
        'is_faq_page_background_image',
    )
    ordering = ('-created_at',)
    readonly_fields = ('image_preview', 'created_at')

    fieldsets = (
        (_('Şəkil'), {'fields': ('image_preview', 'image')}),
        (_('Hansı səhifənin yuxarı banner fonudur?'), {
            'fields': (
                'is_home_page_background_image',
                'is_about_page_background_image',
                'is_contact_page_background_image',
                'is_product_page_background_image',
                'is_blog_page_background_image',
                'is_faq_page_background_image',
            ),
            'description': _(
                'Yalnız bir səhifə seçin. Bu şəkil həmin səhifənin yuxarı geniş banner '
                'hissəsində arxa fonda görünür.'
            ),
        }),
        (_('Sistem məlumatı'), {'fields': ('created_at',)}),
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
class FAQAdmin(AdminPageHelpMixin, admin.ModelAdmin):
    admin_page_help = FAQ_HELP
    list_display = ('question_az', 'sort_order', 'is_active', 'created_at')
    list_editable = ('sort_order', 'is_active')
    search_fields = ('question_az', 'question_en', 'question_ru', 'answer_az')
    ordering = ('sort_order', 'id')
    fieldsets = (
        (_('Azərbaycan'), {'fields': ('question_az', 'answer_az'), 'classes': ('wide',)}),
        (_('English'), {'fields': ('question_en', 'answer_en'), 'classes': ('wide', 'g-lang-en')}),
        (_('Русский'), {'fields': ('question_ru', 'answer_ru'), 'classes': ('wide', 'g-lang-ru')}),
        (_('Parametrlər'), {
            'fields': ('sort_order', 'is_active'),
            'description': _('Sıra nömrəsi kiçik olanda sual yuxarıda görünür. «Saytda göstərilsin?» söndürülərsə gizlənir.'),
        }),
    )


# ---------------------------------------------------------------------------
# Blog
# ---------------------------------------------------------------------------

@admin.register(Blog)
class BlogAdmin(AdminImageCompressMixin, AdminPageHelpMixin, admin.ModelAdmin):
    admin_page_help = BLOG_HELP
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
        (_('Parametrlər'), {
            'fields': ('date', 'on_main_page', 'view_count', 'created_at'),
            'description': _(
                'Tarix — yazının dərc tarixi. '
                '«Ana səhifədə göstərilsin?» — ana səhifə bloq bölməsində (max 6). '
                'Baxış sayı avtomatik sayılır.'
            ),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;border-radius:4px;" />', obj.image.url)
        return '—'

    image_preview.short_description = _('Önizləmə')


patch_admin_site_order()
