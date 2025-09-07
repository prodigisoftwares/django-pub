// Custom utility for animation-delay classes
document.addEventListener('DOMContentLoaded', function () {
  const style = document.createElement('style');
  style.innerHTML = `
    .animate-delay-2000 {
      animation-delay: 2s !important;
    }
    .animate-delay-200 {
      animation-delay: 0.2s !important;
    }
    .animate-delay-400 {
      animation-delay: 0.4s !important;
    }
  `;
  document.head.appendChild(style);
});
