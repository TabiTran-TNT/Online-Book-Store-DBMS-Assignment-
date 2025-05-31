class ProfileEdit {
    constructor() {
        this.form = $('form');
        this.bindEvents();
    }

    bindEvents() {
        $('.edit-field').on('click', this.toggleField.bind(this));
        $('#cancel-edit').on('click', this.cancelEdit.bind(this));
    }

    toggleField(event) {
        const fieldId = $(event.target).data('field-id');
        const field = $(`#${fieldId}`);

        if (fieldId === 'id_current_password') {

            $('#id_current_password').removeClass('d-none').prop('readonly', false).addClass('edit-chosen-field');
            $('#id_password').removeClass('d-none').prop('readonly', false).addClass('edit-chosen-field');
            $('#id_confirm_password').removeClass('d-none').prop('readonly', false).addClass('edit-chosen-field');

            $('hr').eq(2).removeClass('d-none');
        } else {
            field.prop('readonly', false).addClass('edit-chosen-field');
        }
    }

    cancelEdit() {
        window.location.reload();
    }
}

$(document).ready(function() {
    new ProfileEdit();
});
