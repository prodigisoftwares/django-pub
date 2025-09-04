document.addEventListener('DOMContentLoaded', function() {
  // Handle copy functionality for both change form and list view
  function setupCopyFunctionality(button) {
    button.onclick = function() {
      let url = '';
      
      // Check if this is a list view button (has data-url attribute)
      if (button.hasAttribute('data-url')) {
        url = button.getAttribute('data-url');
      } else {
        // This is the change form - get URL from the file path input
        const filePathInput = document.querySelector('input[type="text"][disabled]');
        if (filePathInput && filePathInput.value) {
          url = filePathInput.value;
        }
      }
      
      if (url) {
        navigator.clipboard.writeText(url).then(() => {
          const icon = button.querySelector('span');
          const originalIcon = icon.textContent;
          icon.textContent = 'check';
          setTimeout(() => { icon.textContent = originalIcon; }, 1500);
        }).catch(err => {
          console.error('Failed to copy: ', err);
        });
      }
    };
  }

  // Setup copy buttons in list view
  document.querySelectorAll('.copy-url-btn').forEach(setupCopyFunctionality);

  // Setup copy button in change form (existing functionality)
  if (window.location.pathname.includes('/change/')) {
    setTimeout(function() {
      const uploadLabel = document.querySelector('label[for="id_image"]');

      if (uploadLabel) {
        const copyBtn = document.createElement('span');
        
        copyBtn.className = 'cursor-pointer text-base-400 px-3 hover:text-base-700 dark:text-base-500 dark:hover:text-base-200 border-r border-base-200 dark:border-base-700 p-1';

        copyBtn.title = 'Copy image URL';
        copyBtn.innerHTML = '<span class="block material-symbols-outlined">content_copy</span>';
        
        setupCopyFunctionality(copyBtn);
        uploadLabel.parentElement.insertAdjacentElement("afterend", copyBtn);
      }
    }, 500);
  }
});
