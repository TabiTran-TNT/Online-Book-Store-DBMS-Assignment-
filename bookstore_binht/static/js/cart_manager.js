class CartManager {
    constructor() {
        this.addToCartButtons = $('.add-to-cart');
        this.decreaseFromCartButtons = $('.decrease-from-cart');
        this.addToCartUrl = '/cart/add/';
        this.decreaseFromCartUrl = '/cart/decrease/';
        this.csrfToken = $('input[name=csrfmiddlewaretoken]').val();

        this.initEventListeners();
    }

    initEventListeners() {
        this.addToCartButtons.each((index, button) => {
            $(button).on('click', this.handleAddToCart.bind(this));
        });

        this.decreaseFromCartButtons.each((index, button) => {
            $(button).on('click', this.handleDecreaseFromCart.bind(this));
        });
    }

    handleAddToCart(event) {
        const button = $(event.currentTarget);
        const bookId = button.data('book-id');

        $.ajax({
            url: this.addToCartUrl,
            type: 'POST',
            headers: {
                'X-CSRFToken': this.csrfToken
            },
            data: {
                'book_id': bookId
            },
            success: (response) => {
                this.updateCartCount(response.total_item,
                    response.total_price,
                    response.add_book_quantity,
                    response.add_book_id);
            },
            error: (error) => {
                console.error('Error adding to cart:', error);
            }
        });
    }

    handleDecreaseFromCart(event) {
        const button = $(event.currentTarget);
        const bookId = button.data('book-id');

        $.ajax({
            url: this.decreaseFromCartUrl,
            type: 'POST',
            headers: {
                'X-CSRFToken': this.csrfToken
            },
            data: {
                'book_id': bookId
            },
            success: (response) => {
                if (response.total_item == 0){
                    location.reload();
                }
                else{
                    this.updateCartCount(response.total_item,
                        response.total_price,
                        response.decrease_book_quantity,
                        response.decrease_book_id);
                }
            },
            error: (error) => {
                console.error('Error decreasing from cart:', error);
            }
        });
    }

    updateCartCount(total_item, total_price, book_quantity, book_id) {
        const cartIcon = $('.bi-cart2');
        const existingBadge = cartIcon.find('.badge');
        const existingTotalPrice = $('.total-cart-price');

        const bookQuantity = $(`#${book_id}`);

        if (existingBadge.length > 0) {
            existingBadge.text(total_item);
        } else {
            if (total_item > 0) {
                const badgeHtml = `<span class="position-absolute top-0 start-100 translate-middle-x rounded-circle badge bg-warning py-1 px-1">${total_item}</span>`;
                cartIcon.append(badgeHtml);
            }
        }

        if (existingTotalPrice.length > 0) {
            existingTotalPrice.text(`${total_price}`);
        }

        if (book_quantity != '0'){
            bookQuantity.text(book_quantity);
        }
        else{
            $(`.book-item#book-${book_id}`).remove();
        }

        const headerCart = $('[name="header-cart"]');
        if (headerCart.length > 0) {
            console.log('headerCart', headerCart);
            headerCart.text(`YOUR CART (${total_item})`);
        }

        const cartHeaderList = $('[name="cart-header-list"]');
        if (cartHeaderList.length > 0) {
            cartHeaderList.text(`YOUR CART (${total_item})`);
        }

        const cartLink = $('[name="cart-sidebar"]');
        if (cartLink.length > 0) {
            cartLink.text(`Cart (${total_item})`);
        }
    }
}

$(document).ready(() => {
    new CartManager();
});
