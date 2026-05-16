"""Emit locale/*/LC_MESSAGES/django.po from in-script triples (dev helper). Run: python scripts/generate_frontend_locale.py"""
from __future__ import annotations

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def escape_po(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


HEADER_AZ = (
    'msgid ""\n'
    'msgstr ""\n'
    '"Project-Id-Version: Ganaqro\\n"\n'
    '"Language: az\\n"\n'
    '"MIME-Version: 1.0\\n"\n'
    '"Content-Type: text/plain; charset=UTF-8\\n"\n'
    '"Content-Transfer-Encoding: 8bit\\n"\n'
    '"Plural-Forms: nplurals=2; plural=(n != 1);\\n"\n'
    "\n"
)
HEADER_EN = HEADER_AZ.replace("Language: az", "Language: en")
HEADER_RU = HEADER_AZ.replace("Language: az", "Language: ru").replace(
    "plural=(n != 1)", "plural=(n%10==1 && n%100!=11 ? 0 : n%10>=2 && n%10<=4 && (n%100<10 || n%100>=20) ? 1 : 2)"
)

TRIPLES = [
    ("About us", "Haqqımızda", "About us", "О нас"),
    ("Address", "Ünvan", "Address", "Адрес"),
    ("All blog posts", "Bütün bloq yazıları", "All blog posts", "Все записи блога"),
    ("All rights reserved.", "Bütün hüquqlar qorunur.", "All rights reserved.", "Все права защищены."),
    ("Azerbaijani", "Azərbaycan", "Azerbaijani", "Азербайджанский"),
    ("Back to blog", "Bloqa qayıt", "Back to blog", "Назад к блогу"),
    ("Blog", "Bloq", "Blog", "Блог"),
    ("Blog pagination", "Bloq səhifələməsi", "Blog pagination", "Пагинация блога"),
    ("Blog post not found", "Bloq yazısı tapılmadı", "Blog post not found", "Запись блога не найдена"),
    ("Browse our photo collection", "Foto kolleksiyamıza nəzər salın", "Browse our photo collection", "Просмотрите нашу фотоколлекцию"),
    ("Call us", "Zəng et", "Call us", "Позвонить"),
    ("Categories", "Kateqoriyalar", "Categories", "Категории"),
    ("Clients", "Müştərilər", "Clients", "Клиенты"),
    ("Close", "Bağla", "Close", "Закрыть"),
    ("Contact", "Əlaqə", "Contact", "Контакт"),
    ("Contact information is not available.", "Əlaqə məlumatı mövcud deyil.", "Contact information is not available.", "Контактная информация недоступна."),
    ("Contact us", "Bizimlə əlaqə saxlayın", "Contact us", "Связаться с нами"),
    ("Contact us about any question", "Hər hansı sual üçün bizimlə əlaqə saxlayın", "Contact us about any question", "Свяжитесь с нами по любым вопросам"),
    ("Email address", "E-poçt ünvanı", "Email address", "Электронная почта"),
    ("Email", "E-poçt", "Email", "Эл. почта"),
    ("English", "English", "English", "Английский"),
    ("Explore %(category)s", "%(category)s üzrə bax", "Explore %(category)s", "Смотреть: %(category)s"),
    ("Follow us on social media", "Sosial şəbəkələrdə izləyin", "Follow us on social media", "Мы в соцсетях"),
    ("Full name", "Ad Soyad", "Full name", "ФИО"),
    ("Get in touch", "Bizimlə əlaqə", "Get in touch", "Свяжитесь с нами"),
    ("Get in touch with us", "Bizimlə əlaqə saxlayın", "Get in touch with us", "Свяжитесь с нами"),
    ("Home", "Ana Səhifə", "Home", "Главная"),
    ("Image viewer", "Şəkil baxışı", "Image viewer", "Просмотр изображений"),
    ("Interested? Get in touch!", "Maraqlandınız? Bizimlə əlaqə saxlayın!", "Interested? Get in touch!", "Интересует? Свяжитесь!"),
    ("Learn more", "Ətraflı", "Learn more", "Подробнее"),
    ("Main navigation", "Əsas naviqasiya", "Main navigation", "Основная навигация"),
    ("Map is not configured", "Xəritə təyin edilməyib", "Map is not configured", "Карта не настроена"),
    ("Map", "Xəritə", "Map", "Карта"),
    ("Menu", "Menyu", "Menu", "Меню"),
    ("Mobile number", "Mobil nömrə", "Mobile number", "Мобильный телефон"),
    ("News and articles from our team", "Komandamızdan xəbər və məqalələr", "News and articles from our team", "Новости и статьи нашей команды"),
    ("Next image", "Növbəti şəkil", "Next image", "Следующее изображение"),
    ("No blog posts yet", "Hələ bloq yazısı yoxdur", "No blog posts yet", "Записей в блоге пока нет"),
    ("No other posts.", "Başqa yazı yoxdur.", "No other posts.", "Других записей нет."),
    ("No products found", "Məhsul tapılmadı", "No products found", "Продукты не найдены"),
    ("Open image", "Şəkili aç", "Open image", "Открыть изображение"),
    ("Other posts", "Digər yazılar", "Other posts", "Другие записи"),
    ("Our blog posts", "Bloq yazılarımız", "Our blog posts", "Наш блог"),
    ("Our gallery", "Qaleriyamız", "Our gallery", "Наша галерея"),
    ("Partners", "Tərəfdaşlar", "Partners", "Партнёры"),
    ("Phone", "Telefon", "Phone", "Телефон"),
    ("Play video", "Videonu işə sal", "Play video", "Воспроизвести видео"),
    ("Please correct the errors in the form.", "Formdakı xətaları düzəldin.", "Please correct the errors in the form.", "Исправьте ошибки в форме."),
    ("Previous image", "Əvvəlki şəkil", "Previous image", "Предыдущее изображение"),
    ("Products pagination", "Məhsul səhifələməsi", "Products pagination", "Пагинация продуктов"),
    ("Products", "Məhsullar", "Products", "Продукты"),
    ("Projects", "Layihələr", "Projects", "Проекты"),
    ("Quick actions", "Tez keçidlər", "Quick actions", "Быстрые действия"),
    ("Quick links", "Keçidlər", "Quick links", "Ссылки"),
    ("Read more", "Ətraflı oxu", "Read more", "Читать далее"),
    ("Russian", "Русский", "Russian", "Русский"),
    ("Send message", "Göndər", "Send message", "Отправить"),
    ("Something went wrong. Please try again.", "Xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.", "Something went wrong. Please try again.", "Произошла ошибка. Попробуйте снова."),
    ("Subject", "Mövzu", "Subject", "Тема"),
    ("Views", "Baxış", "Views", "Просмотры"),
    ("View all products", "Bütün məhsullara bax", "View all products", "Все продукты"),
    ("views", "baxış", "views", "просмотров"),
    ("Your full name", "Adınız və soyadınız", "Your full name", "Ваше полное имя"),
    ("Your message has been sent successfully.", "Mesajınız uğurla göndərildi.", "Your message has been sent successfully.", "Ваше сообщение успешно отправлено."),
    ("Your message", "Mesajınız", "Your message", "Ваше сообщение"),
]


def write_catalog(lang_code: str, header: str) -> None:
    out = BASE_DIR / "locale" / lang_code / "LC_MESSAGES" / "django.po"
    out.parent.mkdir(parents=True, exist_ok=True)
    seen: set[str] = set()
    lines = [header.rstrip("\n"), ""]
    for mid, az, en, ru in TRIPLES:
        if mid in seen:
            continue
        seen.add(mid)
        if lang_code == "az":
            mstr = az
        elif lang_code == "ru":
            mstr = ru
        else:
            mstr = en
        lines.append(f'msgid "{escape_po(mid)}"')
        lines.append(f'msgstr "{escape_po(mstr)}"')
        lines.append("")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    os.chdir(BASE_DIR)
    write_catalog("az", HEADER_AZ)
    write_catalog("en", HEADER_EN)
    write_catalog("ru", HEADER_RU)
    print("Wrote django.po under locale/{az,en,ru}/LC_MESSAGES/")
    try:
        from babel.messages.mofile import write_mo
        from babel.messages.pofile import read_po
    except ImportError:
        print("(Optional) pip install Babel — then rerun to generate django.mo from django.po.")
        return
    for lang in ("az", "en", "ru"):
        po_path = BASE_DIR / "locale" / lang / "LC_MESSAGES" / "django.po"
        mo_path = BASE_DIR / "locale" / lang / "LC_MESSAGES" / "django.mo"
        catalog = read_po(po_path.open(encoding="utf-8"))
        write_mo(mo_path.open("wb"), catalog)
    print("Compiled django.mo (Babel)")


if __name__ == "__main__":
    main()
