# Ganagro.az

Official website of **Ganagro** — a multilingual corporate platform for showcasing products and services, company information, news, and customer communication.

**Website:** [ganaqro.az](https://ganaqro.az)

---

## Purpose of the site

- Present the company and its areas of activity
- Display product categories and products
- Receive customer inquiries (contact form)
- Publish news and articles on the blog
- Answer frequently asked questions (FAQ)
- Serve visitors in Azerbaijani, English, and Russian

---

## Languages

The site is available in **3 languages**:

| Language | Code |
|----------|------|
| Azerbaijani | `az` (default) |
| English | `en` |
| Russian | `ru` |

Visitors switch language from the header menu and see content in their chosen language. Texts are entered separately for all three languages in the admin panel.

---

## Pages and features

### Home

- **Hero carousel** — company slogans and main visual presentation
- **Product panels** — selected products by category (items marked to appear on the home page)
- **Statistics** — key figures (e.g. years in business, projects, clients)
- **About preview** — video or image, short text, link to the full About page
- **Gallery** — company images (with fullscreen view)
- **Blog preview** — latest posts selected for the home page
- **Partners** — logos of partner organizations
- **FAQ** — short list of frequently asked questions
- **Contact button** — direct link to the contact page

### About us

- Full company presentation (title, subtitle, rich text)
- Video or image materials
- Additional media gallery

### Products

- **Category** selection from the menu
- Product cards in each category: image, name, short description
- **Pagination** when there are many products
- Direct link from a product card to that product on the page (anchor link)

### Blog

- List of posts (date, image, short excerpt)
- **Detail page** for each post — full text and image
- View count tracking (for statistics)

### FAQ (Frequently asked questions)

- Questions and answers in accordion format
- Selected questions can also appear on the home page

### Contact

**Left side — company details (managed in the admin panel):**

- Address
- Phone (tap to call)
- WhatsApp
- Email addresses
- Social networks (Instagram, Facebook, YouTube, LinkedIn, TikTok, etc.)
- Google Maps (embedded map)

**Right side — contact form:**

| Field | Required |
|-------|----------|
| Full name | Yes |
| Email | Yes |
| Mobile number | No |
| Subject | Yes |
| Message | Yes (max 500 characters) |

**After the form is submitted:**

1. The visitor sees a success message on the site
2. The inquiry is saved in the **admin panel**
3. Form details are sent automatically to the company email (name, email, phone, subject, message, date/time)

---

## General site features

- **Responsive design** — mobile, tablet, and desktop
- **Animations** — smooth scroll-in effects
- **Footer** — contact and social links, navigation
- **Category menu** — quick access to product categories

---

## Admin panel (content management)

Sign in via the private admin URL to update site content. Main sections:

| Section | What you manage |
|---------|-----------------|
| **Product categories** | Category names (3 languages), order |
| **Products** | Name, description, image/video, active status, show on home page |
| **About us** | Company text, video, gallery |
| **Contact** | Address, phone, email, social links, map |
| **Contact inquiries** | Messages from the form; read/unread status |
| **Blog** | Posts, date, image, show on home page |
| **FAQ** | Questions and answers |
| **Partners** | Logo and name |
| **Statistics** | Home page figures |
| **Mottos** | Page headings and hero carousel text |
| **Background images** | Top banner images for pages |

**Notes for content managers:**

- Up to **6 products** per category are shown on the home page
- Blog and FAQ entries must be filled in for each language separately
- Contact inquiries cannot be added manually in the panel — they only come from the website form

---

## Who it is for

| User | What they do on the site |
|------|--------------------------|
| **Visitor / customer** | Browse products, read the blog, submit the form, get in touch |
| **Company staff** | Update content in the admin panel, read inquiries |
| **Management** | Review statistics, partners, and corporate presentation |

---

## Contact flow (overview)

```
Visitor fills in the form
        ↓
“Thank you” message on the site
        ↓
    ┌───┴───┐
    ↓       ↓
 Admin    Email
 panel    notification
```

---

*Technical setup and server configuration are handled by the development team.*
 