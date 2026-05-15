from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from django.utils.translation import gettext as _

from projects.models import Blog
from projects.forms.forms_v1 import AppealContactForm
from projects.utils.queries import (
    get_language_from_request,
    get_home_page_data,
    get_product_list_data,
    get_product_by_slug,
    serialize_product,
    get_background_image,
    get_about,
    serialize_about,
    get_partners,
    serialize_partner,
    get_contact,
    serialize_contact,
    get_statistics,
    get_product_categories,
    serialize_product_category,
    get_blog_list_data,
    get_blog_by_id,
    serialize_blog,
)


class HomePageView(View):
    template_name = 'index.html'

    def get(self, request):
        lang = get_language_from_request(request)
        context = get_home_page_data(request, lang)
        context['footer_image'] = get_background_image('footer')
        context['language'] = lang
        return render(request, self.template_name, context)


class ProductPageView(View):
    template_name = 'products.html'

    def get(self, request, category_slug=None):
        lang = get_language_from_request(request)
        if category_slug:
            request.GET = request.GET.copy()
            request.GET['slug'] = category_slug
        context = get_product_list_data(request, lang)
        context['background_image'] = get_background_image('product')
        context['footer_image'] = get_background_image('footer')
        context['language'] = lang
        return render(request, self.template_name, context)


class ProductDetailPageView(View):
    template_name = 'product-detail.html'

    def get(self, request, slug):
        lang = get_language_from_request(request)

        product = get_product_by_slug(slug, lang)
        if product:
            categories = get_product_categories(lang)
            contact = get_contact(lang)
            context = {
                'product': serialize_product(product, lang),
                'categories': [serialize_product_category(c, lang) for c in categories],
                'contact': serialize_contact(contact, lang) if contact else None,
                'language': lang,
                'background_image': get_background_image('product'),
                'footer_image': get_background_image('footer'),
            }
            return render(request, self.template_name, context)

        from projects.models import ProductCategory
        try:
            category = ProductCategory.objects.get(slug=slug)
            request.GET = request.GET.copy()
            request.GET['slug'] = slug
            context = get_product_list_data(request, lang)
            context['background_image'] = get_background_image('product')
            context['footer_image'] = get_background_image('footer')
            context['language'] = lang
            return render(request, 'products.html', context)
        except ProductCategory.DoesNotExist:
            raise Http404(_("Məhsul tapılmadı"))


class AboutPageView(View):
    template_name = 'about.html'

    def get(self, request):
        lang = get_language_from_request(request)
        is_active = request.GET.get('is_active', 'true').lower() == 'true'
        about = get_about(lang)
        partners = get_partners(lang=lang, is_active=is_active)
        contact = get_contact(lang)
        statistics = get_statistics()
        categories = get_product_categories(lang)
        context = {
            'about': serialize_about(about, lang) if about else None,
            'partners': [serialize_partner(p, lang) for p in partners],
            'contact': serialize_contact(contact, lang) if contact else None,
            'categories': [serialize_product_category(c, lang) for c in categories],
            'statistics': statistics,
            'language': lang,
            'background_image': get_background_image('about'),
            'footer_image': get_background_image('footer'),
        }
        return render(request, self.template_name, context)


class ContactPageView(View):
    template_name = 'contact.html'

    def get(self, request):
        lang = get_language_from_request(request)
        contact = get_contact(lang)
        categories = get_product_categories(lang)
        form = AppealContactForm()
        context = {
            'contact': serialize_contact(contact, lang) if contact else None,
            'categories': [serialize_product_category(c, lang) for c in categories],
            'language': lang,
            'background_image': get_background_image('contact'),
            'footer_image': get_background_image('footer'),
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        lang = get_language_from_request(request)
        form = AppealContactForm(request.POST)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, _('Mesajınız uğurla göndərildi.'))
                return redirect('projects:contact-page')
            except Exception:
                messages.error(request, _('Xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.'))
        else:
            messages.error(request, _('Formda xəta var. Zəhmət olmasa düzəldin.'))

        contact = get_contact(lang)
        categories = get_product_categories(lang)
        context = {
            'contact': serialize_contact(contact, lang) if contact else None,
            'categories': [serialize_product_category(c, lang) for c in categories],
            'language': lang,
            'background_image': get_background_image('contact'),
            'footer_image': get_background_image('footer'),
            'form': form,
        }
        return render(request, self.template_name, context)


class BlogPageView(View):
    template_name = 'blog.html'

    def get(self, request):
        lang = get_language_from_request(request)
        context = get_blog_list_data(request, lang)
        context['language'] = lang
        categories = get_product_categories(lang)
        context['categories'] = [serialize_product_category(c, lang) for c in categories]
        return render(request, self.template_name, context)


class BlogDetailPageView(View):
    template_name = 'blog-detail.html'

    def get(self, request, blog_id):
        lang = get_language_from_request(request)
        blog = get_blog_by_id(blog_id)
        if not blog:
            raise Http404(_("Bloq tapılmadı"))

        Blog.objects.filter(pk=blog_id).update(view_count=blog.view_count + 1)

        contact = get_contact(lang)
        categories = get_product_categories(lang)
        context = {
            'blog': serialize_blog(blog, lang),
            'contact': serialize_contact(contact, lang) if contact else None,
            'categories': [serialize_product_category(c, lang) for c in categories],
            'language': lang,
            'footer_image': get_background_image('footer'),
        }
        return render(request, self.template_name, context)
