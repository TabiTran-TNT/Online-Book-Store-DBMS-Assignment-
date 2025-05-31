class CommentAlert {
    constructor() {
      this.init();
    }

    init() {
      document.addEventListener('DOMContentLoaded', () => {
        this.checkMessages();
      });
    }

    checkMessages() {
      const messageElements = document.querySelectorAll('.django-message');
      messageElements.forEach((element) => this.handleMessage(element));
    }

    handleMessage(element) {
      const messageText = element.textContent.trim();
      if (messageText === 'You can only comment once on each book.') {
        const commentModal = new bootstrap.Modal(document.getElementById('commentModal'));
        commentModal.show();
      }
    }
  }
