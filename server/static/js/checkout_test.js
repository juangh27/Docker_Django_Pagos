function showForm(value) {
    const form = document.getElementById("form");
    form.style.display = "none";
    setTimeout(() => {
        form.style.display = "block";
    }, 600);
    console.log("Passed value: " + value);
    form.reset();

}

//   }
function function1(value_passed) {
    $('.card').removeClass('bg-secondary text-white');
    const card = $(event.target).closest('.card');
    card.toggleClass('bg-secondary text-white');

}
const ite = document.getElementById("payment_type");

document.addEventListener("DOMContentLoaded", function () {

    const stripe = Stripe("");
    let elements;

    initialize();
    checkStatus();

    document
        .querySelector("#form")
        .addEventListener("submit", handleSubmit);

    let emailAddress = '';
    // Fetches a payment intent and captures the client secret
    async function initialize() {
        const response = await fetch("create-payment-intent", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ items }),
        });
        const { clientSecret } = await response.json();
        // console.log(response);
        const appearance = {
            theme: 'stripe',
        };
        elements = stripe.elements({ appearance, clientSecret });

        const linkAuthenticationElement = elements.create("linkAuthentication");
        linkAuthenticationElement.mount("#link-authentication-element");

        linkAuthenticationElement.on('change', (event) => {
            emailAddress = event.value.email;
        });

        const paymentElementOptions = {
            layout: "tabs",
        };

        const paymentElement = elements.create("payment", paymentElementOptions);
        paymentElement.mount("#payment-element");
    }

    async function handleSubmit(e) {
        e.preventDefault();
        setLoading(true);

        const { error } = await stripe.confirmPayment({
            elements,
            confirmParams: {
                // Make sure to change this to your payment completion page
                return_url: "http://localhost:80/nido/checkout",
                receipt_email: emailAddress,
            },
        });

        if (error.type === "card_error" || error.type === "validation_error") {
            showMessage(error.message);
        } else {
            showMessage("An unexpected error occurred.");
        }

        setLoading(false);
    }

    // Fetches the payment intent status after payment submission
    async function checkStatus() {
        const clientSecret = new URLSearchParams(window.location.search).get(
            "payment_intent_client_secret"
        );

        if (!clientSecret) {
            return;
        }

        const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

        switch (paymentIntent.status) {
            case "succeeded":
                showMessage("Payment succeeded!");
                break;
            case "processing":
                showMessage("Your payment is processing.");
                break;
            case "requires_payment_method":
                showMessage("Your payment was not successful, please try again.");
                break;
            default:
                showMessage("Something went wrong.");
                break;
        }
    }

    // ------- UI helpers -------

    function showMessage(messageText) {
        const messageContainer = document.querySelector("#payment-message");

        messageContainer.classList.remove("hidden");
        messageContainer.textContent = messageText;

        setTimeout(function () {
            messageContainer.classList.add("hidden");
            messageText.textContent = "";
        }, 4000);
    }

    // Show a spinner on payment submission
    function setLoading(isLoading) {
        if (isLoading) {
            // Disable the button and show a spinner
            document.querySelector("#submit").disabled = true;
            document.querySelector("#spinner").classList.remove("hidden");
            document.querySelector("#button-text").classList.add("hidden");
        } else {
            document.querySelector("#submit").disabled = false;
            document.querySelector("#spinner").classList.add("hidden");
            document.querySelector("#button-text").classList.remove("hidden");
        }
    }

});