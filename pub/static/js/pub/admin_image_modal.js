document.addEventListener("DOMContentLoaded", function () {
  // Image hover modal functionality
  let hoverModal = null;
  let hoverTimeout = null;

  function createModal() {
    const modal = document.createElement("div");
    modal.className = "image-hover-modal";
    document.body.appendChild(modal);

    return modal;
  }

  function showModal(imageUrl, event) {
    if (!hoverModal) {
      hoverModal = createModal();
    }

    clearTimeout(hoverTimeout);
    hoverModal.innerHTML = `<img src="${imageUrl}" alt="Image preview" />`;
    const rect = event.target.getBoundingClientRect();
    const modalLeft = Math.min(event.pageX + 15, window.innerWidth - 520);
    const modalTop = Math.max(event.pageY - 150, 10);
    hoverModal.style.left = modalLeft + "px";
    hoverModal.style.top = modalTop + "px";
    hoverModal.classList.add("show");
  }

  function hideModal() {
    if (hoverModal) {
      hoverTimeout = setTimeout(() => {
        hoverModal.classList.remove("show");
      }, 100);
    }
  }

  document.querySelectorAll(".image-title-hover").forEach((titleElement) => {
    const imageUrl = titleElement.getAttribute("data-image-url");

    if (imageUrl) {
      titleElement.addEventListener("mouseenter", (e) =>
        showModal(imageUrl, e),
      );
      titleElement.addEventListener("mouseleave", hideModal);
    }
  });
});
