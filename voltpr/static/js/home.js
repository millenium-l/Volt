const slides = document.querySelector('.slides');
const images = document.querySelectorAll('.slides img');
let index = 0;

function moveSlides() {
  index++;
  if (index >= images.length) {
    index = 0; // loop back to first image
  }
  slides.style.transform = `translateX(-${index * 500}px)`;
}

// change image every 3 seconds
setInterval(moveSlides, 1000);