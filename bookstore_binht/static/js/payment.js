document.addEventListener('DOMContentLoaded', function() {
    const stripePublishableKey = document.getElementById('payment-form').dataset.stripePublishableKey;
    const clientSecret = document.getElementById('payment-form').dataset.clientSecret;
    const paymentStatusUrl = document.getElementById('payment-form').dataset.paymentStatusUrl;
    const stripe = Stripe(stripePublishableKey);
    const appearance = {
        theme: 'stripe',
        variables: {
          colorBackground: '#C4E3EC',
          colorText: '#30313d',
          borderRadius: '0px',
          fontWeightBold: '700',
        },
        rules: {
            '.Label': {
                fontWeight: 'var(--fontWeightBold)',
            },
        },
      };
    const elements = stripe.elements({
        clientSecret: clientSecret,
        appearance: appearance,
    });
    const paymentElement = elements.create('payment');
    paymentElement.mount('#payment-element');

    const form = document.getElementById('payment-form');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const {error: submitError} = await elements.submit();

        if (submitError) {
            document.getElementById('error-message').textContent = submitError.message;
            return;
        }

        const {error: stripeError} = await stripe.confirmPayment({
            elements,
            confirmParams: {
                return_url: paymentStatusUrl,
            },
            clientSecret: clientSecret,
        });

        if (stripeError) {
            document.getElementById('error-message').textContent = stripeError.message;
            return;
        }

    });
});
