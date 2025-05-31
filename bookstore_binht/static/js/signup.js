class SignUp {
    constructor() {
        this.form = $('#signUp form');

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
            success: function(response) {
                const responseData = JSON.parse(response.html);
                if (responseData.status === 'success') {
                    $('#signUp').modal('hide');

                    $('#accountActivateModal .modal-body').html(`
                        Hi ${responseData.username},
                        Thanks for joining us. Please go to your email to activate your account.
                    `);
                    $('#accountActivateModal').modal('show');
                }
                if (responseData.status === 'error'){
                    form.find('#email-used').removeClass('d-none');
                }
            },
            error: function(xhr, status, error) {
                const rsp = JSON.parse(xhr.responseText);
                Object.entries(rsp.form.fields).forEach(([key, value]) => {
                    if (value.errors && value.errors.length > 0) {
                        if (value.errors[0] === 'A user is already registered with this email address.') {
                            form.find('#email-used').removeClass('d-none');
                        } else {
                            form.find(`#${key}`).removeClass('d-none');
                        }
                    }
                });

            }
        });
    }

}
