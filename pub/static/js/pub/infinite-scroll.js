document.body.addEventListener('htmx:beforeRequest', function(evt) {
  document.getElementById('loading-indicator').classList.remove('hidden');
});

document.body.addEventListener('htmx:afterRequest', function(evt) {
  document.getElementById('loading-indicator').classList.add('hidden');
});

document.body.addEventListener('htmx:afterSwap', function(evt) {
  const newElements = evt.detail.target.querySelectorAll('.animate-fade-in-up');
  newElements.forEach((el, index) => {
    el.style.animationDelay = `${(index + 1) * 100}ms`;
    el.classList.remove('animate-fade-in-up');
    el.offsetHeight;
    el.classList.add('animate-fade-in-up');
  });
});
