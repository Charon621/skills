'use strict';
const dialog = document.querySelector('#lightbox');
let previousFocus;
document.addEventListener('click', (event) => {
  const button = event.target.closest('.zoom');
  if (!button) return;
  const image = button.querySelector('img');
  previousFocus = document.activeElement;
  document.querySelector('#modal-title').textContent = button.dataset.title;
  document.querySelector('#modal-caption').textContent = button.dataset.caption;
  const enlarged = document.querySelector('#modal-image');
  enlarged.src = image.src;
  enlarged.alt = image.alt;
  dialog.showModal();
  dialog.scrollTop = 0;
});
document.querySelector('#close-modal').addEventListener('click', () => dialog.close());
dialog.addEventListener('close', () => previousFocus?.focus());
dialog.addEventListener('click', (event) => {
  if (event.target !== dialog) return;
  const bounds = dialog.getBoundingClientRect();
  if (event.clientX < bounds.left || event.clientX > bounds.right ||
      event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
});
document.querySelector('#print').addEventListener('click', () => window.print());
