class DescriptionToggle {
    constructor() {
      this.description = document.getElementById('book-description');
      this.icon = document.getElementById('description-icon');
      this.readMore = document.getElementById('read-more');

      this.bindEvents();
    }

    bindEvents() {
      this.icon.addEventListener('click', () => {
        this.toggleDescription();
      });

      this.readMore.addEventListener('click', () => {
        this.toggleDescription();
      });
    }

    toggleDescription() {
      if (this.description.classList.contains('line-clamp-5')) {
        this.description.classList.remove('line-clamp-5');
        this.icon.classList.remove('fa-chevron-down');
        this.icon.classList.add('fa-chevron-up');
        this.readMore.textContent = 'read less...';
      } else {
        this.description.classList.add('line-clamp-5');
        this.icon.classList.remove('fa-chevron-up');
        this.icon.classList.add('fa-chevron-down');
        this.readMore.textContent = 'read more...';
      }
    }
  }
