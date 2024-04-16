// Declare and initialize variables for academic level, service type, currency, number of pages, total price, and discount
var academicLevel, serviceType, currency = 'USD', numberOfPages;  
var totalPrice = 0;  
var discount = 0;  

// Function that runs when the window loads
window.onload = function () {
    // Add an event listener to the form that triggers when any input field changes
    document.getElementById('myform').addEventListener('change', function () {
        // Reset the discount
        discount = 0;
        // Clear the discount and final price fields
        document.getElementById('discount').innerText = '';
        document.getElementById('finalPrice').innerText = '';
        
        // Get the values of the academic level, service type, currency, and number of pages from the form
        academicLevel = document.getElementsByName('academic_level')[0].value;
        serviceType = document.getElementsByName('service_type')[0].value;
        currency = document.getElementsByName('currency')[0].value;
        numberOfPages = document.getElementsByName('number_of_pages_increment')[0].value;
        // Get the writer category from the Django form
        var writerCategory = "{{form.writer}}"; 
        // Display the selected options
        document.getElementById('selectedOptions').innerText = 'The academic level is: ' + academicLevel + ', \n the service type is: ' + serviceType + ', \n The currency is: ' + currency + ', \n The number of pages is: ' + numberOfPages + ', \n The writer category is: ' + writerCategory;

        // Calculate the total price based on the selected options
        totalPrice = calculatePrice(academicLevel, serviceType, currency, numberOfPages);
        // Display the total price
        document.getElementById('totalPrice').innerText = 'The total price is: ' + currency + ' ' + totalPrice;

        // Remove the old PayPal script tag if it exists
        var oldScript = document.getElementById('paypal-js');
        if (oldScript) {
            oldScript.remove();
        }

        // Create a new script tag for the PayPal SDK
        var script = document.createElement('script');
        script.id = 'paypal-js';
        script.src = 'https://www.paypal.com/sdk/js?client-id=AW7XnTz50r52rNBP5ZTnYQSv3_MLcYtP1n1UGmaAPXdKmioFSlTlfJIAo44COSLpVsvP2z-BCr93-8eV&currency=' + currency;
        // When the script loads, initialize the PayPal buttons
        script.onload = function () {
            paypal.Buttons({
                createOrder: function (data, actions) {
                    // Calculate the total price based on the selected options
                    totalPrice = calculatePrice(academicLevel, serviceType, currency, numberOfPages);
                    // This function sets up the details of the transaction, including the amount and line item details.
                    return actions.order.create({
                        purchase_units: [{
                            amount: {
                                value: totalPrice,
                                currency_code: currency 
                            }
                        }]
                    }).catch(error => console.error('Error creating order:', error));
                },
                onApprove: function (data, actions) {
                    // This function captures the funds from the transaction.
                    return actions.order.capture().then(function (details) {
                        // This function shows a transaction success message to your buyer.
                        alert('Transaction completed by ' + details.payer.name.given_name);
                    });
                }
            }).render('#paypal-button-container');  // Add an HTML element with this id to your page
        };
        // Add the new script tag to the body of the document
        document.body.appendChild(script);
    });
    // Add an event listener to the coupon code field that triggers when it changes
    document.getElementsByName('coupon_code')[0].addEventListener('change', applyCoupon);
}

// Function to calculate the price based on the academic level, service type, currency, and number of pages
function calculatePrice(academicLevel, serviceType, currency, numberOfPages) {
    // Define the base prices for each academic level
    var basePrices = { 'high_school': 10, 'undergraduate': 20, 'masters': 30, 'phd': 40 };
    // Define the multipliers for each service type
    var serviceMultipliers = { 'writing': 1, 'editing': 0.8, 'proofreading': 0.6 };
    // Define the exchange rates for each currency
    var currencyRates = { 'USD': 1, 'EUR': 0.85, 'GBP': 0.75, 'KES': 110.15 };
    // Get the base price, service multiplier, and currency rate based on the selected options
    var basePrice = basePrices[academicLevel];
    var serviceMultiplier = serviceMultipliers[serviceType];
    var currencyRate = currencyRates[currency];
    // Calculate the price
    var price = basePrice * serviceMultiplier * currencyRate * numberOfPages;
    // Return the price minus the discount
    return (price - price * discount).toFixed(2);
}

// Function to select a choice
function selectChoice(choice) {
    // Set the value of the selected choice field to the selected choice
    document.getElementById('selected_choice').value = choice;
}

// Function to apply a coupon
function applyCoupon() {
    // Get the coupon code from the form
    var couponCode = document.getElementsByName('coupon_code')[0].value;
    // Validate the coupon code and get the discount value
    validateCoupon(couponCode).then(discountValue => {
        if (discountValue) {
            // If the coupon code is valid, update the global discount variable
            discount = discountValue;  
            // Display the discount
            document.getElementById('discount').innerText = 'Discount: ' + discount;
            // Calculate the total price
            var totalPrice = calculatePrice(academicLevel, serviceType, currency, numberOfPages);
            // Display the final price
            document.getElementById('finalPrice').innerText = 'Final Price: ' + currency + ' ' + totalPrice;
        } else {
            // If the coupon code is invalid, display an error message
            document.getElementById('discount').innerText = 'Invalid coupon code';
            document.getElementById('finalPrice').innerText = '';
        }
    });
}

// Function to validate a coupon code
function validateCoupon(couponCode) {
    // If the coupon code is undefined, log an error and return null
    if (!couponCode) {
        console.error('Coupon code is undefined');
        return Promise.resolve(null);
    }

    // Fetch the coupon from the API
    return fetch('http://127.0.0.1:8000/api/coupons/' + couponCode)
        .then(response => {
            // If the response is not ok, throw an error
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Parse the response as JSON
            return response.json();
        })
        .then(coupon => {
            // If the coupon is active, return the discount value as a decimal
            if (coupon.active) {
                return coupon.discount / 100;  
            } else {
                // If the coupon is not active, return null
                return null;  
            }
        })
        .catch(error => {
            // If an error occurred, log the error and return null
            console.error('There has been a problem with your fetch operation:', error);
            return null;  
        });
}

// Function to pay now
function payNow(event) {
    // Prevent the form from submitting
    event.preventDefault();
    // Calculate the total price
    var totalPrice = calculatePrice(academicLevel, serviceType, currency, numberOfPages);
}
