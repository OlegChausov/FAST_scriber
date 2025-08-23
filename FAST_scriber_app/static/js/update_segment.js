document.querySelectorAll(".segment-text").forEach(span => {
  span.addEventListener("click", () => {
    const segment = span.closest(".segment");
    const transcriptId = segment.closest("[data-transcript]").dataset.transcript;
    const start = parseFloat(segment.dataset.start);

    const originalText = span.textContent;
    const input = document.createElement("input");
    input.type = "text";
    input.value = originalText;
    input.className = "form-control form-control-sm";
    input.style.minWidth = "200px";

    // Replace span with input
    span.replaceWith(input);
    input.focus();

    const save = () => {
      const newText = input.value.trim();
      if (newText && newText !== originalText) {
        // Update DOM
        const newSpan = document.createElement("span");
        newSpan.className = "segment-text";
        newSpan.textContent = newText;
        input.replaceWith(newSpan);

        // Reattach click handler
        newSpan.addEventListener("click", span.onclick);

        // Send to backend
        fetch("/update_segment", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            transcript_id: transcriptId,
            start: start,
            text: newText
          })
        }).catch(err => {
          console.error("Ошибка при отправке:", err);
        });
      } else {
        // Cancel edit
        span.textContent = originalText;
        input.replaceWith(span);
      }
    };

    input.addEventListener("blur", save);
    input.addEventListener("keydown", e => {
      if (e.key === "Enter") {
        input.blur();
      } else if (e.key === "Escape") {
        input.replaceWith(span);
      }
    });
  });
});

