/**
* Template Name: AgriCulture
* Template URL: https://bootstrapmade.com/agriculture-bootstrap-website-template/
* Updated: Aug 07 2024 with Bootstrap v5.3.3
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/

(function() {
  "use strict";

  /**
   * Apply .scrolled class to the body as the page is scrolled down
   */
  function toggleScrolled() {
    const selectBody = document.querySelector('body');
    const selectHeader = document.querySelector('#header');
    if (!selectHeader || !selectBody) return;
    if (!selectHeader.classList.contains('scroll-up-sticky') && !selectHeader.classList.contains('sticky-top') && !selectHeader.classList.contains('fixed-top')) return;
    window.scrollY > 100 ? selectBody.classList.add('scrolled') : selectBody.classList.remove('scrolled');
  }

  document.addEventListener('scroll', toggleScrolled);
  window.addEventListener('load', toggleScrolled);

  /**
   * Scroll up sticky header to headers with .scroll-up-sticky class
   */
  let lastScrollTop = 0;
  window.addEventListener('scroll', function() {
    const selectHeader = document.querySelector('#header');
    if (!selectHeader || !selectHeader.classList.contains('scroll-up-sticky')) return;

    let scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    if (scrollTop > lastScrollTop && scrollTop > selectHeader.offsetHeight) {
      selectHeader.style.setProperty('position', 'sticky', 'important');
      selectHeader.style.top = `-${selectHeader.offsetHeight + 50}px`;
    } else if (scrollTop > selectHeader.offsetHeight) {
      selectHeader.style.setProperty('position', 'sticky', 'important');
      selectHeader.style.top = "0";
    } else {
      selectHeader.style.removeProperty('top');
      selectHeader.style.removeProperty('position');
    }
    lastScrollTop = scrollTop;
  });

  /**
   * Mobile nav toggle
   */
  const mobileNavToggleBtn = document.querySelector('.mobile-nav-toggle');

  function mobileNavToogle() {
    document.querySelector('body').classList.toggle('mobile-nav-active');
    const open = document.body.classList.contains('mobile-nav-active');
    if (mobileNavToggleBtn) {
      mobileNavToggleBtn.classList.toggle('bi-list');
      mobileNavToggleBtn.classList.toggle('bi-x');
      mobileNavToggleBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    }
  }

  if (mobileNavToggleBtn) {
    mobileNavToggleBtn.addEventListener('click', mobileNavToogle);
    mobileNavToggleBtn.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        mobileNavToogle();
      }
    });
  }

  function isMobileNavView() {
    return window.matchMedia('(max-width: 1199px)').matches;
  }

  function toggleMobileNavDropdown(anchor) {
    const panel = anchor && anchor.nextElementSibling;
    if (!panel) return;
    anchor.classList.toggle('active');
    panel.classList.toggle('dropdown-active');
    if (anchor.classList.contains('lang-dropdown-toggle')) {
      anchor.setAttribute('aria-expanded', anchor.classList.contains('active') ? 'true' : 'false');
    }
  }

  const navmenuEl = document.querySelector('#navmenu');
  if (navmenuEl) {
    navmenuEl.addEventListener('click', function(e) {
      if (e.target === navmenuEl) {
        if (document.body.classList.contains('mobile-nav-active')) {
          mobileNavToogle();
        }
        return;
      }

      const dropdownAnchor = e.target.closest(
        'a.products-dropdown-toggle, a.lang-dropdown-toggle'
      );
      if (dropdownAnchor && dropdownAnchor.getAttribute('href') === '#') {
        e.preventDefault();
        if (isMobileNavView() && document.body.classList.contains('mobile-nav-active')) {
          if (!e.target.closest('.dropdown-menu-panel')) {
            toggleMobileNavDropdown(dropdownAnchor);
          }
        }
        return;
      }

      if (!document.body.classList.contains('mobile-nav-active')) return;
      const navLink = e.target.closest('#navmenu a[href]');
      if (!navLink) return;
      const href = navLink.getAttribute('href');
      if (!href || href === '#') return;
      mobileNavToogle();
    });
  }

  /**
   * Preloader — çıxarılması DOM hazır olan kimi (bütün şəkillərin load-u gözləmir).
   */
  const preloader = document.querySelector('#preloader');
  if (preloader) {
    const removePreloader = function() {
      preloader.remove();
    };
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', removePreloader);
    } else {
      removePreloader();
    }
    window.addEventListener('load', function preloaderSafetyRemove() {
      const el = document.getElementById('preloader');
      if (el) el.remove();
    }, { once: true });
  }

  /**
   * Scroll top button
   */
  const scrollTop = document.querySelector('#scroll-top');

  function toggleScrollTop() {
    if (scrollTop) {
      window.scrollY > 100 ? scrollTop.classList.add('active') : scrollTop.classList.remove('active');
    }
  }

  if (scrollTop) {
    scrollTop.addEventListener('click', (e) => {
      e.preventDefault();
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
    window.addEventListener('load', toggleScrollTop);
    document.addEventListener('scroll', toggleScrollTop);
  }

  function whenDomReady(fn) {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', fn);
    } else {
      fn();
    }
  }

  /**
   * Animation on scroll function and init
   */
  function aosInit() {
    AOS.init({
      duration: 600,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    });
  }

  /**
   * Auto generate the carousel indicators
   */
  document.querySelectorAll('.carousel-indicators').forEach((carouselIndicator) => {
    const carousel = carouselIndicator.closest('.carousel');
    if (!carousel || !carousel.id) return;
    const targetId = carousel.id;
    carousel.querySelectorAll('.carousel-item').forEach((carouselItem, index) => {
      if (index === 0) {
        carouselIndicator.innerHTML += `<li data-bs-target="#${targetId}" data-bs-slide-to="${index}" class="active"></li>`;
      } else {
        carouselIndicator.innerHTML += `<li data-bs-target="#${targetId}" data-bs-slide-to="${index}"></li>`;
      }
    });
  });

  /**
   * Init swiper sliders
   */
  function initSwiper() {
    document.querySelectorAll(".init-swiper").forEach(function(swiperElement) {
      const configEl = swiperElement.querySelector(".swiper-config");
      if (!configEl) return;
      let config;
      try {
        config = JSON.parse(configEl.innerHTML.trim());
      } catch (err) {
        console.warn("Swiper config JSON parse failed:", err);
        return;
      }

      try {
        if (swiperElement.classList.contains("swiper-tab")) {
          initSwiperWithCustomPagination(swiperElement, config);
        } else {
          new Swiper(swiperElement, config);
        }
      } catch (err2) {
        console.warn("Swiper init failed:", err2);
      }
    });
  }

  /**
   * Bloq və məhsul siyahılarında mobil görünüşdə səhifə başına 6 element.
   */
  function syncListPerPage() {
    const isListPage = document.body.classList.contains('blog-page')
      || document.body.classList.contains('services-page');
    if (!isListPage) {
      return;
    }

    const perPage = window.matchMedia('(max-width: 767px)').matches ? '6' : '9';
    const cookieName = 'ganaqro_list_per_page';
    const cookieMatch = document.cookie.match(new RegExp('(?:^|; )' + cookieName + '=([^;]*)'));
    const currentCookie = cookieMatch ? cookieMatch[1] : null;

    if (currentCookie !== perPage) {
      document.cookie = cookieName + '=' + perPage + ';path=/;max-age=86400;SameSite=Lax';
    }

    const url = new URL(window.location.href);
    const urlPerPage = url.searchParams.get('per_page');
    const expectedUrlPerPage = perPage === '9' ? null : perPage;

    if ((urlPerPage || null) !== expectedUrlPerPage) {
      if (expectedUrlPerPage) {
        url.searchParams.set('per_page', expectedUrlPerPage);
      } else {
        url.searchParams.delete('per_page');
      }
      window.location.replace(url.toString());
    }
  }

  /** DOM hazır olanda karruselləri işə salır (tam səh.fə yüklənməsini gözləmir). */
  function bootSwiperAndAos() {
    syncListPerPage();
    initSwiper();
    aosInit();
  }
  whenDomReady(bootSwiperAndAos);

  /** Şəkillər axını bitəndə swiper ölçülərini yeniləmək üçün (hero və s.). */
  window.addEventListener('load', function swiperPostLoadLayout() {
    requestAnimationFrame(function() {
      window.dispatchEvent(new Event('resize'));
    });
  }, { once: true });

  /**
   * Initiate glightbox
   */
  if (typeof GLightbox !== 'undefined') {
    GLightbox({
      selector: '.glightbox'
    });
  }

  function resetTurnstileIfPresent(form) {
    try {
      if (typeof turnstile === 'undefined' || !turnstile || !turnstile.reset) return;
      var widget = form.querySelector('.cf-turnstile');
      if (!widget) return;
      turnstile.reset();
    } catch (e) {
      // ignore
    }
  }

  function onAjaxFormSubmit(e) {
    var form = e.target;
    if (!form.matches('form[data-ajax="1"]')) return;
    e.preventDefault();

    var fd = new FormData(form);
    fetch(form.action || window.location.href, {
      method: 'POST',
      body: fd,
      credentials: 'same-origin',
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (data.ok) {
          form.reset();
        }
      })
      .finally(function () {
        resetTurnstileIfPresent(form);
      });
  }

  document.addEventListener('submit', onAjaxFormSubmit, true);

})();