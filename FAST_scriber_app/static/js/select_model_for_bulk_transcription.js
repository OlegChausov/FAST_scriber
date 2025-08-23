  function showBulkModelSelector() {
    const wrapper = document.getElementById("bulk-model-selector");
    wrapper.classList.remove("d-none");

    setTimeout(() => {
      document.addEventListener('click', window.bulkOutsideClick = function(e) {
        if (!wrapper.contains(e.target)) {
          wrapper.classList.add('d-none');
          document.removeEventListener('click', window.bulkOutsideClick);
        }
      });
    }, 0);
  }

  function setBulkModel() {
    const model = document.getElementById("bulk-model-select").value;

    // Добавляем скрытое поле в форму
    const input = document.createElement("input");
    input.type = "hidden";
    input.name = "selected_model";
    input.value = model;
    document.querySelector("form").appendChild(input);
  }