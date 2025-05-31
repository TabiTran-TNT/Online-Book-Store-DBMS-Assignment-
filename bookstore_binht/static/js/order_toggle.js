class OrderToggle {
    constructor() {
        this.icons = document.querySelectorAll('[id^="order-icon-"]');
        this.bindEvents();
    }

    bindEvents() {
        this.icons.forEach(icon => {
            icon.addEventListener('click', () => {
                this.toggleDescription(icon);
            });
        });
    }

    toggleDescription(icon) {
        const orderId = icon.getAttribute('data-order-id');
        const description = document.getElementById(`descriptionCollapse-${orderId}`);
        const isCollapsed = description.classList.contains('d-none');

        if (isCollapsed) {
            description.classList.remove('d-none');
            icon.classList.remove('fa-chevron-down');
            icon.classList.add('fa-chevron-up');
        } else {
            description.classList.add('d-none');
            icon.classList.remove('fa-chevron-up');
            icon.classList.add('fa-chevron-down');
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new OrderToggle();
});
