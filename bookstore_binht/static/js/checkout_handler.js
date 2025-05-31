class CheckoutHandler {
    constructor() {
      this.checkoutButton = document.getElementById('checkoutButton');
      this.loginModal = new bootstrap.Modal(document.getElementById('login'));
      this.loginTitle = document.getElementById('loginTitle');
      this.checkoutLoginTitle = document.getElementById('checkoutLoginTitle');
      this.closeButtonLogin = document.getElementById('closeButtonLogin');
      this.checkoutCloseButtonLogin = document.getElementById('checkoutCloseButtonLogin');
      this.checkoutMessage1 = document.getElementById('checkoutMessage1');
      this.checkoutMessage2 = document.getElementById('checkoutMessage2');
      this.modalHeader = document.getElementById('loginModalHeader');

      this.bindEvents();
    }

    bindEvents() {
      this.checkoutButton.addEventListener('click', (event) => this.handleCheckoutClick(event));
    }

    handleCheckoutClick = (event) => {
      event.preventDefault();
      const userAuthenticated = this.checkoutButton.getAttribute('data-authenticated');

      if (userAuthenticated === "false") {
        this.loginTitle.classList.add('d-none');
        this.checkoutLoginTitle.classList.remove('d-none');
        this.closeButtonLogin.classList.add('d-none');
        this.checkoutCloseButtonLogin.classList.remove('d-none');
        this.checkoutMessage1.classList.remove('d-none');
        this.checkoutMessage2.classList.remove('d-none');
        this.modalHeader.classList.add('checkout-login-header');

        this.loginModal.show();
      } else {
        window.location.href = this.checkoutButton.href;
      }
    }
  }

document.addEventListener('DOMContentLoaded', () => {
    new CheckoutHandler();
});
