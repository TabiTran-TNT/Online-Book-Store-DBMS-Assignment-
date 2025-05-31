class PasswordReset {
    constructor() {
        this.form = $('#resetPass form');
        this.resetPassModal = $('#resetPass');
        this.resetPassDoneModal = $('#resetPassDoneModal');

        this.bindEvents();
    }

    bindEvents() {
        this.form.on('submit', (e) => {
            e.preventDefault();
            this.submitForm();
        });
    }

    submitForm() {
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
                this.resetPassModal.modal('hide');
                this.resetPassDoneModal.modal('show');
            },
            error: (xhr, status, error) => {
                form.find("#reset-error").removeClass('d-none');
            }
        });
    }
}

$(document).ready(function() {
    new PasswordReset();
});
