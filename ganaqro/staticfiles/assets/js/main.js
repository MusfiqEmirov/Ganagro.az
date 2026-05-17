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

  const navmenuEl = document.querySelector('#navmenu');
  if (navmenuEl) {
    navmenuEl.addEventListener('click', function(e) {
      if (e.target !== navmenuEl) return;
      if (document.body.classList.contains('mobile-nav-active')) {
        mobileNavToogle();
      }
    });
  }

  /**
   * Mobil menyunu yalnız real keçiddə bağla (href="#" olan Məhsullar/Dil açıcıları menyunu dərhal bağlamasın).
   */
  document.querySelectorAll('#navmenu a').forEach((anchor) => {
    anchor.addEventListener('click', () => {
      if (!document.body.classList.contains('mobile-nav-active')) return;
      const href = anchor.getAttribute('href');
      if (!href || href === '#') return;
      mobileNavToogle();
    });
  });

  /**
   * Toggle mobile nav dropdowns
   */
  document.querySelectorAll('.navmenu .toggle-dropdown').forEach(navmenu => {
    navmenu.addEventListener('click', function(e) {
      e.preventDefault();
      const parent = this.parentNode;
      const panel = parent && parent.nextElementSibling;
      if (!panel) return;
      parent.classList.toggle('active');
      panel.classList.toggle('dropdown-active');
      e.stopImmediatePropagation();
      e.stopPropagation();
    });
  });

  /** Dropdown triggers with href="#" */
  document.querySelectorAll('.navmenu .dropdown--products > a[href="#"], .navmenu .dropdown--lang > a[href="#"]').forEach(a => {
    a.addEventListener('click', function(e) {
      e.preventDefault();
    });
  });

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

  /** DOM hazır olanda karruselləri işə salır (tam səh.fə yüklənməsini gözləmir). */
  function bootSwiperAndAos() {
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

})();