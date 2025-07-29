document.addEventListener("DOMContentLoaded", () => {
  const slider = document.getElementById("slider");
  const prevbtn = document.getElementById("prevbtn");
  const nextbtn = document.getElementById("nextbtn");
  const autoplayIntervalTime = 4250;

  let currentIndex = 0;
  const totalSlides = slider ? slider.children.length : 0;
  let autoplayInterval;

  function updateSlider() {
    slider.style.transition = "transform 2s ease-in-out";
    slider.style.transform = `translateX(-${currentIndex * 100}%)`;
  }

  function startAutoplay() {
    autoplayInterval = setInterval(() => {
      currentIndex = (currentIndex + 1) % totalSlides;
      updateSlider();
    }, autoplayIntervalTime);
  }

  function resetAutoplay() {
    clearInterval(autoplayInterval);
    startAutoplay();
  }

  if (nextbtn) {
    nextbtn.addEventListener("click", () => {
      currentIndex = (currentIndex + 1) % totalSlides;
      updateSlider();
      resetAutoplay();
    });
  }

  if (prevbtn) {
    prevbtn.addEventListener("click", () => {
      currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
      updateSlider();
      resetAutoplay();
    });
  }

  if (slider && prevbtn && nextbtn) {
    startAutoplay();
  }
});

// Toggle function for password
function togglePassword(inputId, iconId) {
  const pswd = document.getElementById(inputId);
  const btn = document.getElementById(iconId);

  if (!pswd || !btn) return;

  const isHidden = pswd.type === "password";
  pswd.type = isHidden ? "text" : "password";

  btn.innerHTML = isHidden ? "🙈" : "👁️";
}
