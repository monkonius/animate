const toggleButton = document.getElementById('review-toggle');
const cancelButton = document.getElementById('cancel');

if (toggleButton && cancelButton) {
  const buttons = [];
  buttons.push(toggleButton, cancelButton);
  buttons.forEach(elem => {
    elem.addEventListener('click', () => {
      const reviewForm = document.querySelector('.review-form');
      reviewForm.classList.toggle('show');

      toggleButton.classList.toggle('hide');
    })
  })
}

const sort = document.getElementById('sort-by');
if (sort) {
  sort.addEventListener('change', (elem) => {
    const select = elem.target;
    select.form.submit();
  })
}