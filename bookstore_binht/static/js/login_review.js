class ReviewModalHandler {
    constructor() {
        this.reviewLoginTitle = document.getElementById('reviewLoginTitle');
        this.checkoutCloseButtonLogin = document.getElementById('checkoutCloseButtonLogin');
        this.checkoutMessage4 = document.getElementById('checkoutMessage4');
        this.loginTitle = document.getElementById('loginTitle');
        this.closeButtonLogin = document.getElementById('closeButtonLogin');
        this.modalHeader = document.getElementById('loginModalHeader');

        this.bindEvents();
    }

    bindEvents() {
        this.loginReviewButtons = document.querySelectorAll('#loginReview1, #loginReview2');

        this.loginReviewButtons.forEach(button => {
            button.addEventListener('click', () => this.handleReviewButtonClick());
        });

        $('#login').on('hidden.bs.modal', () => {
            this.handleModalClose();
        });
    }

    handleReviewButtonClick() {
        this.reviewLoginTitle.classList.remove('d-none');
        this.checkoutCloseButtonLogin.classList.remove('d-none');
        this.checkoutMessage4.classList.remove('d-none');
        this.modalHeader.classList.add('review-login-header');


        this.loginTitle.classList.add('d-none');
        this.closeButtonLogin.classList.add('d-none');
    }

    handleModalClose() {
        this.loginTitle.classList.remove('d-none');
        this.closeButtonLogin.classList.remove('d-none');

        this.reviewLoginTitle.classList.add('d-none');
        this.checkoutCloseButtonLogin.classList.add('d-none');
        this.checkoutMessage4.classList.add('d-none');
        this.modalHeader.classList.remove('review-login-header');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new ReviewModalHandler();
});
