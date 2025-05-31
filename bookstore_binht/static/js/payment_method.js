class PaymentMethodToggle {
    constructor() {
        this.paymentSelect = $('#paymentSelect');
        this.creditCardForm = $('#payment-form');
        this.cashForm = $('#cash-form');
        this.checkboxes = $('.checkbox-container .form-check-input');

        this.bindEvents();
        this.toggleForm();
    }

    bindEvents() {
        this.paymentSelect.on('change', () => {
            this.toggleForm();
        });

        this.checkboxes.on('change', () => {
            this.uncheckOthers(event.target);
            this.toggleForm();
        });
    }

    uncheckOthers(selectedCheckbox) {
        this.checkboxes.each(function() {
            if (this !== selectedCheckbox) {
                $(this).prop('checked', false);
            }
        });
    }

    toggleForm() {
        const selectedMethod = this.paymentSelect.is(':visible')
            ? this.paymentSelect.val()
            : this.checkboxes.filter(':checked').val();

        if (selectedMethod === 'creditCard') {
            this.creditCardForm.removeClass('d-none');
            this.cashForm.addClass('d-none');
        } else if (selectedMethod === 'cash') {
            this.creditCardForm.addClass('d-none');
            this.cashForm.removeClass('d-none');
        }
    }
}

$(document).ready(() => {
    new PaymentMethodToggle();
});
