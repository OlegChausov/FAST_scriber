document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector('#uploadModal form');
  if (form) {
    form.addEventListener('submit', () => {
      const spinner = document.getElementById("spinner");
      if (spinner) {
        spinner.style.display = "block";
      }
    });
  } else {
    console.warn("Форма загрузки не найдена");
  }
});
