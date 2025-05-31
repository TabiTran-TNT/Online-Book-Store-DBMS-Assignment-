class SessionExpiry {
    constructor(sessionExpiryTime, warningTime) {
        if (SessionExpiry.instance) {
            return SessionExpiry.instance;
        }

        this.sessionExpiryTime = sessionExpiryTime;
        this.warningTime = warningTime;
        this.showModalTime = this.sessionExpiryTime - this.warningTime;
        this.timeoutId = null;

        const storedExpiryTime = localStorage.getItem('sessionExpiryTime');
        if (storedExpiryTime) {
            this.sessionExpiryTime = new Date(storedExpiryTime).getTime() - Date.now();
            this.showModalTime = this.sessionExpiryTime - this.warningTime;
        } else {
            const expiryDate = new Date(Date.now() + this.sessionExpiryTime);
            localStorage.setItem('sessionExpiryTime', expiryDate.toISOString());
        }

        SessionExpiry.instance = this;
        return this;
    }

    start() {
        const modalShown = localStorage.getItem('modalShown');
        if (this.sessionExpiryTime > 0 && !modalShown) {
            this.timeoutId = setTimeout(() => {
                this.showModal();
            }, this.showModalTime);
        } else if (!modalShown) {
            this.showModal();
        }
    }

    showModal() {
        const modalShown = localStorage.getItem('modalShown');
        if (!modalShown) {
            this.updateModalForSessionExpiry();
            $('#login').modal('show');
            localStorage.setItem('modalShown', 'true');

            $('#login').on('hidden.bs.modal', () => {
                this.handleModalClose();
            });

            $(document).on('loginSuccess', () => {
                this.handleLoginSuccess();
                $('#login').modal('hide');
            });

            setTimeout(() => {
                this.resetSessionExpiry();
            }, this.warningTime);
        }
    }

    updateModalForSessionExpiry() {
        $('#loginTitle').addClass('d-none');
        $('#closeButtonLogin').addClass('d-none');

        $('#cartExpireTitle').removeClass('d-none');
        $('#checkoutCloseButtonLogin').removeClass('d-none');
        $('#checkoutMessage3').removeClass('d-none');

        $('#loginModalHeader').addClass('checkout-login-header');
    }

    revertModalToInitialState() {
        $('#loginTitle').removeClass('d-none');
        $('#closeButtonLogin').removeClass('d-none');

        $('#cartExpireTitle').addClass('d-none');
        $('#checkoutCloseButtonLogin').addClass('d-none');
        $('#checkoutMessage3').addClass('d-none');

        $('#loginModalHeader').removeClass('checkout-login-header');
    }

    resetSessionExpiry() {
        this.clearTimeout();
        localStorage.removeItem('modalShown');
        const expiryDate = new Date(Date.now() + this.sessionExpiryTime);
        localStorage.setItem('sessionExpiryTime', expiryDate.toISOString());
        this.start();
    }

    handleModalClose() {
        this.clearTimeout();
        this.revertModalToInitialState();
    }

    handleLoginSuccess() {
        this.clearTimeout();
        localStorage.removeItem('modalShown');
        localStorage.removeItem('sessionExpiryTime');
    }

    clearTimeout() {
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
            this.timeoutId = null;
        }
    }

}

class Login {
    constructor() {
        this.form = $('#login form');

        this.activationTitle = document.getElementById('accountActivateModalLabel');
        this.verificationLoginTitle = document.getElementById('verificationLoginTitle');
        this.closeButtonAccountActivate1 = document.getElementById('closeButtonAccountActivate1');
        this.closeButtonAccountActivate2 = document.getElementById('closeButtonAccountActivate2');
        this.modalHeader = document.getElementById('activateModalHeader');

        this.bindEvents();
    }

    bindEvents() {
        this.form.on('submit', (e) => {
            e.preventDefault();
            this.submitForm();
        });
    }

    submitForm = () => {
        const form = this.form;
        $.ajax({
            url: form.attr('action'),
            method: form.attr('method'),
            data: form.serialize(),
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val(),
                'X-Requested-With': 'XMLHttpRequest'
            },
            success: (response) => {
                const responseData = JSON.parse(response.html);
                if (responseData.status === 1) {
                    window.location.reload();
                } else if (responseData.status === 'unverified') {
                    $('#login').modal('hide');
                    $('#accountActivateModal .modal-body').html(`
                        You haven't activated your account yet. Please go to your email to activate.
                    `);
                    this.activationTitle.classList.add('d-none');
                    this.verificationLoginTitle.classList.remove('d-none');
                    this.closeButtonAccountActivate1.classList.add('d-none');
                    this.closeButtonAccountActivate2.classList.remove('d-none');
                    this.modalHeader.classList.add('verification-login-header');

                    $('#accountActivateModal').modal('show');
                }
            },
            error: function(xhr, status, error) {
                form.find("#login-error").removeClass('d-none');
                const responseData = JSON.parse(xhr.responseJSON.html);
                if (responseData.show_captcha) {

                    form.find("#login-error").text("Invalid credentials or captcha");
                    $('#captcha-container').removeClass('d-none');

                    const newCaptchaKey = responseData.new_cptch_key;
                    const newCaptchaImageUrl = responseData.new_cptch_image;

                    $('input[name="captcha_0"]').val(newCaptchaKey);
                    $('img.captcha').attr('src', newCaptchaImageUrl);
                }
            }
        });
    }
}

$(document).ready(function () {
    const sessionExpiryTime = 60 * 60 * 3 * 1000;
    const warningTime = 60 * 15 * 1000;

    const sessionExpiry = new SessionExpiry(sessionExpiryTime, warningTime);
    sessionExpiry.start();
    new Login();
});
