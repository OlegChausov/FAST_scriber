document.addEventListener("DOMContentLoaded", () => {
  const audio = document.getElementById("audioPlayer");
  const segments = document.querySelectorAll(".segment");

  let currentEndTime = null;
  let activeSegment = null;

  segments.forEach(segment => {
    segment.addEventListener("click", () => {
      const start = parseFloat(segment.dataset.start);
      const end = parseFloat(segment.dataset.end);

      if (isNaN(start) || isNaN(end)) {
        console.warn("Некорректные тайминги:", segment.dataset.start, segment.dataset.end);
        return;
      }

      currentEndTime = end;
      audio.currentTime = start;
      audio.play();

      // Сброс предыдущей подсветки
      if (activeSegment) {
        activeSegment.classList.remove("bg-warning", "border-start", "border-warning", "ps-3");
      }

      // Подсветка текущего сегмента
      segment.classList.add("bg-warning", "border-start", "border-warning", "ps-3");
      activeSegment = segment;
    });
  });

  audio.addEventListener("timeupdate", () => {
    if (currentEndTime !== null && audio.currentTime >= currentEndTime) {
      audio.pause();
      currentEndTime = null;

      // Убираем подсветку
      if (activeSegment) {
        activeSegment.classList.remove("bg-warning", "border-start", "border-warning", "ps-3");
        activeSegment = null;
      }
    }
  });
});
