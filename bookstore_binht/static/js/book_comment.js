class CommentToggle {
    constructor() {
        this.comments = document.querySelectorAll('.comment-content');
        this.icons = document.querySelectorAll('.comment-icon');
        this.readMores = document.querySelectorAll('.read-more');

        this.bindEvents();
    }

    bindEvents() {
        this.icons.forEach(icon => {
            icon.addEventListener('click', (event) => {
                const commentId = event.target.dataset.commentId;
                this.toggleComment(commentId);
            });
        });

        this.readMores.forEach(readMore => {
            readMore.addEventListener('click', (event) => {
                const commentId = event.target.dataset.commentId;
                this.toggleComment(commentId);
            });
        });
    }

    toggleComment(commentId) {
        const comment = document.querySelector(`.comment-content[data-comment-id="${commentId}"]`);
        const icon = document.querySelector(`.comment-icon[data-comment-id="${commentId}"]`);
        const readMore = document.querySelector(`.read-more[data-comment-id="${commentId}"]`);

        if (comment.classList.contains('line-clamp-3')) {
            comment.classList.remove('line-clamp-3');
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-up');
            readMore.textContent = 'read less...';
        } else {
            comment.classList.add('line-clamp-3');
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
            readMore.textContent = 'read more...';
        }
    }
}
