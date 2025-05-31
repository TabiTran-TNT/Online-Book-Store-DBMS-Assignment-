class StarRating {
  constructor() {
    this.stars = document.querySelectorAll('.star');
    this.ratingInput = document.querySelector('input[name="rating"]');

    this.bindEvents();
  }

  bindEvents() {
    this.stars.forEach(star => {
      star.addEventListener('click', this.handleStarClick.bind(this, star));
    });
  }

  handleStarClick(clickedStar) {
    const ratingValue = clickedStar.dataset.value;
    this.ratingInput.value = ratingValue;

    this.stars.forEach(star => {
      star.classList.toggle('fas', star.dataset.value <= ratingValue);
      star.classList.toggle('far', star.dataset.value > ratingValue);
    });
  }
}
