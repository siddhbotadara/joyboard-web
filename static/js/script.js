document.addEventListener("DOMContentLoaded", () => {
  const slider = document.getElementById("slider");
  const prevbtn = document.getElementById("prevbtn");
  const nextbtn = document.getElementById("nextbtn");
  const autoplayIntervalTime = 4250;

  let currentIndex = 0;
  const totalSlides = slider.children.length;
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

  nextbtn.addEventListener("click", () => {
    currentIndex = (currentIndex + 1) % totalSlides;
    updateSlider();
    resetAutoplay();
  });

  prevbtn.addEventListener("click", () => {
    currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
    updateSlider();
    resetAutoplay();
  });

  startAutoplay();
});

function togglepassword(inputId, iconId) {
  const pswd = document.getElementById(inputId);
  const btn = document.getElementById(iconId);

  const isHidden = pswd.type === 'password';
  pswd.type = isHidden ? 'text' : 'password';
  btn.textContent = isHidden ? '🙈' : '👁️';
}

function togglePassword() {
  const pswd = document.getElementById('password');
  const btn = document.getElementById('toggleIcon');

  const isHidden = pswd.type === 'password';
  pswd.type = isHidden ? 'text' : 'password';
  btn.textContent = isHidden ? '🙈' : '👁️';
}

