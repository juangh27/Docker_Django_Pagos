// function showForm(value) {
//     // const form = document.getElementById("form");
//     // form.style.display = "none";
//     // setTimeout(() => {
//         // }, 600);
        
//         // do something with the passed value
//     console.log("Passed value: " + value);
//     // var card = document.querySelector('.card');
//     // $('.card').toggleClass('bg-primary bg-success');
//     // var hiddenInput = document.getElementById("myHiddenInput");
//     // var val = hiddenInput.value;
//     // alert("The hidden value is: " + val)
//     // alert("The hidden value is: " + card)
//     // form.reset();

// }

// function showForm(value) {
//     const form = document.getElementById("form");
//     form.style.display = "block";
// }


// function function1(value_passed) {
//     // alert("This is function 1.");
//     var hiddenInput = document.getElementById("myHiddenInput");
//     var val = hiddenInput.value;
//     // alert("The hidden value is: " + value_passed);
//     const card = $(event.target).closest('.card');

//     // $('.card').toggleClass('bg-secondary bg-light text-black');
//     //  $('.card').removeClass('bg-secondary bg-light text-black');
//     // card.toggleClass('bg-light bg-secondary text-white');
//     // $('.card').toggleClass('bg-light bg-secondary text-white');
//     // $('.card').toggleClass('bg-light bg-secondary text-white');
//   }
function showform(value_passed) {
    form.style.display = "block";
    $('.card').removeClass('bg-secondary text-white');
    const card = $(event.target).closest('.card');
    card.toggleClass('bg-secondary text-white');
    stripeform(value_passed);

}

// function getValue() {
    //     var hiddenInput = document.getElementById("myHiddenInput");
//     var val = hiddenInput.value;
//     alert("The hidden value is: " + val);
//   }



// your code here
function stripeform(item_id) {
    // This is your test publishable API key.
    const stripe = Stripe("pk_test_51MnTwYH4JG7lr5M7xBE6bAxWHUletv7z48idp9NITuOplGCxJm3bkAZIbmWWtI2lXPcSDJQNTu2ceVFTzrsgxi1300l9LWJNMZ");

    // The items the customer wants to buy
    // const hiddenInput = document.getElementById("payment_type");
    const items = [{ id: item_id }];

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

        // This point will only be reached if there is an immediate error when
        // confirming the payment. Otherwise, your customer will be redirected to
        // your `return_url`. For some payment methods like iDEAL, your customer will
        // be redirected to an intermediate site first to authorize the payment, then
        // redirected to the `return_url`.
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

}