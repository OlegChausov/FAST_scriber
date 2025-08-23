document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".transcript-status").forEach(div => {
    const status = div.dataset.status;
    const id = div.dataset.id;

    if (["In process", "None", "Failed", "Done", "Missing"].includes(status)) {
      startPolling(id, div);
    }
  });
});

function startPolling(audioId, container) {
  const interval = setInterval(() => {
    fetch(`/status/${audioId}`)
      .then(res => res.json())
      .then(data => {
        const newStatus = data.status;
        container.dataset.status = newStatus;
        container.innerHTML = renderStatusHTML(newStatus, audioId);

        if (["Failed"].includes(newStatus)) {
          clearInterval(interval);
        }
      })
      .catch(err => {
        console.error(`Ошибка при polling для ${audioId}:`, err);
        clearInterval(interval);
      });
  }, 3000); // каждые 3 секунды
}

function renderStatusHTML(status, audioId) {
  switch (status) {
    case "Done":
      return `<a href="/go_transcribation/${audioId}" class="btn btn-outline-success">Читать</a>`;
    case "In process":
      return `<span class="text-muted">Выполняется</span>`;
    case "Failed":
      return `<span class="text-danger">Ошибка</span>`;
    case "Missing":
      return `<span class="text-warning">Файл не найден</span>`;
    default:
      return `<span class="text-secondary">Не обработан</span>`;
  }
}
