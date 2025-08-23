function showModelSelector(id) {
    document.querySelectorAll('[id^="model-selector-"]').forEach(el => {
      el.classList.add('d-none');
    });

    const wrapper = document.getElementById(`model-selector-${id}`);
    wrapper.classList.remove('d-none');

    setTimeout(() => {
      document.addEventListener('click', window[`outsideClick_${id}`] = function(e) {
        if (!wrapper.contains(e.target)) {
          wrapper.classList.add('d-none');
          document.removeEventListener('click', window[`outsideClick_${id}`]);
        }
      });
    }, 0);
  }

  function redirectToTranscribe(id) {
    const model = document.getElementById(`model-select-${id}`).value;
    window.location.href = `/transcribe/${id}?model=${encodeURIComponent(model)}`;
  }