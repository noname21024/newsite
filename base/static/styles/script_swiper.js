var swiper = new Swiper(".slide-content", {
    slidesPerView: 3,
    spaceBetween: 30,
    freeMode: true,
    loop: true,
    centerSlider: 'true',
    fade:'true',
    grabCursor: 'true',

    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
    },
    breakpoints: {
    640: {
      slidesPerView: 1,
    },
    768: {
      slidesPerView: 3,
    },
    1200: {
      slidesPerView: 5,
    },
  },

  autoplay: {
    delay: 2500,
    disableOnInteraction: false,
  },
    });