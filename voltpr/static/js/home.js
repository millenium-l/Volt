// JavaScript for Home Page
const slides = document.querySelector(".slides");
const images = document.querySelectorAll(".slides img");
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




// Search functionality
document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".search");
  const input = form.querySelector("input[name='q']");
  const container = document.getElementById("product-container");

  // 🔁 Reusable fetch function
  function fetchProducts(url) {
  fetch(url)
    .then(res => res.json())
    .then(data => {
      document.getElementById("product-container").innerHTML = data.html;
    });
}

  // 🔍 Search
  form.addEventListener("submit", function (e) {
  e.preventDefault();

  const query = input.value;
  const category = form.dataset.category || "";

  fetchProducts(`/ajax_products/?q=${query}&category=${category}`);
});

  // 📄 Pagination (THIS IS NEW 🔥)
  document.addEventListener("click", function (e) {
  if (e.target.closest(".page-link")) {
    e.preventDefault();

    const link = e.target.closest(".page-link");
    const url = new URL(link.href);

    const page = url.searchParams.get("page");
    const query = input.value;
    const category = form.dataset.category || "";

    fetchProducts(`/ajax_products/?q=${query}&page=${page}&category=${category}`);
  }
});
});
