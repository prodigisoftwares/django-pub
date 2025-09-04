document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname.includes('/change/')) {
        setTimeout(function() {
            const uploadLabel = document.querySelector('label[for="id_image"]');
            if (uploadLabel) {
                const copyBtn = document.createElement('span');
                copyBtn.className = 'cursor-pointer text-base-400 px-3 hover:text-base-700 dark:text-base-500 dark:hover:text-base-200 border-r border-base-200 dark:border-base-700 p-1';
                copyBtn.title = 'Copy image URL';
                copyBtn.innerHTML = '<span class="block material-symbols-outlined">content_copy</span>';
                copyBtn.onclick = function() {
                    const filePathInput = document.querySelector('input[type="text"][disabled]');
                    if (filePathInput && filePathInput.value) {
                        const url = filePathInput.value; // Just the path, no domain
                        navigator.clipboard.writeText(url).then(() => {
                            const icon = copyBtn.querySelector('span');
                            const originalIcon = icon.textContent;
                            icon.textContent = 'check';
                            setTimeout(() => { icon.textContent = originalIcon; }, 1500);
                        }).catch(err => {
                            console.error('Failed to copy: ', err);
                        });
                    }
                };
                uploadLabel.parentElement.insertAdjacentElement("afterend", copyBtn);
            }
        }, 500);
    }
});