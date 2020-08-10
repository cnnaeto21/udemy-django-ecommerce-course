$(document).ready(function(){
    var stripeFormModule = $(".stripe-payment-form")
    var stripeModuleToken = stripeFormModule.attr("data-token")
    var stripeModuleNextUrl = stripeFormModule.attr("data-next-url")
    var stripeModuleBtnTitle = stripeFormModule.attr("data-btn-title") || "Add Card"
    var stripeTemplate = $.templates("#stripeTemplate")
    var stripeTemplateDataContext = {
        publish_key: stripeModuleToken,
        next_url: stripeModuleNextUrl,
        btn_title: stripeModuleBtnTitle
    }
    var stripeTemplateHtml = stripeTemplate.render(stripeTemplateDataContext)
    stripeFormModule.html(stripeTemplateHtml)


    // https secure site when live 
    var paymentForm = $(".payment-form")
    if (paymentForm > 1){
        alert("Only one payment form is allowed per page")
        paymentForm.css('display', 'none')
    }

    else if (paymentForm.length == 1){
    var pubKey = paymentForm.attr('data-token')
    var nextUrl = paymentForm.attr('data-next-url')
    // Create a Stripe client.
    var stripe = Stripe(pubKey);

    // Create an instance of Elements.
    var elements = stripe.elements();

    // Custom styling can be passed to options when creating an Element.
    // (Note that this demo uses a wider set of styles than the guide below.)
    var style = {
    base: {
        color: '#32325d',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
        color: '#aab7c4'
        }
    },
    invalid: {
        color: '#fa755a',
        iconColor: '#fa755a'
    }
    };

    // Create an instance of the card Element.
    var card = elements.create('card', {style: style});

    // Add an instance of the card Element into the `card-element` <div>.
    card.mount('#card-element');

    // Handle real-time validation errors from the card Element.
    card.addEventListener('change', function(event) {
    var displayError = document.getElementById('card-errors');
    if (event.error) {
        displayError.textContent = event.error.message;
    } else {
        displayError.textContent = '';
    }
    });

    // // Handle form submission.
    // var form = document.getElementById('payment-form');
    // form.addEventListener('submit', function(event) {
    // event.preventDefault();
    // // get btn
    // // displaye new btn UI

    // var loadTime = 1500
    // var errorHtml = "<i class='fa fa-warning'></i> An error occured "
    // var errorClasses = "btn btn-danger disabled my-3"
    // var loadingHtml = "<i class='fa fa-spin fa-spinner'></i>Loading..."
    // var loadingClasses = "btn btn-success disabled my-3"
    // stripe.createToken(card).then(function(result) {
    //     if (result.error) {
    //     // Inform the user if there was an error.
    //     var errorElement = document.getElementById('card-errors');
    //     errorElement.textContent = result.error.message;
    //     } else {
    //     // Send the token to your server.
    //     stripeTokenHandler(nextUrl, result.token);

    //     }
    // });
    // });

    var form = $('#payment-form');
    var btnLoad = from.find(".btn-load")
    var btnLoadDefualtHtml = btnLoad.html()
    var btnLoadDefualtClasses = btnLoad.attr("class")


    form.on('submit', function(event) {
        event.preventDefault();
        // get btn
        // displaye new btn UI
        var $this = $(this)
        var btnLoad = $this.find('.btn-load')
        //var loadTime = 1500
        btnLoad.blur()
        var currentTimeOut;
        var errorHtml = "<i class='fa fa-warning'></i> An error occured "
        var errorClasses = "btn btn-danger disabled my-3"
        var loadingHtml = "<i class='fa fa-spin fa-spinner'></i> Loading..."
        var loadingClasses = "btn btn-success disabled my-3"
        stripe.createToken(card).then(function(result) {
            if (result.error) {
            // Inform the user if there was an error.
            var errorElement = $('#card-errors');
            errorElement.textContent = result.error.message;
            currentTimeOut = displaybtnStatus(btnLoad, errorHtml, errorClasses, 1000, currentTimeOut)
            } else {
            // Send the token to your server.
            currentTimeOut = displaybtnStatus(btnLoad, loadingHtml, loadingClasses, 1000, currentTimeOut)
            stripeTokenHandler(nextUrl, result.token);

            }
        });
    })


    function displaybtnStatus(element, newHtml, newClasses, loadTime, timeout){
        if (!loadTime){
            loadTime = 1500
        }
        // var defaultHtml = element.html()
        // var defaultClasses=element.attr("class")
        element.html(newHtml)
        element.removeClass(btnLoadDefualtClasses)
        element.addClass(newClasses)
        return setTimeout(function(){
            element.html(btnLoadDefualtHtml)
            element.removeClass(newClasses)
            element.addClass(btnLoadDefualtClasses)
        }, loadTime)
    }


    function redirectToNext(nextPath, timeOffset) {
        if (nextPath) {
            setTimeout(function(){
                window.location.href = nextPath
            }, timeOffset)
        }
    }

    // Submit the form with the token ID.
    function stripeTokenHandler(nextUrl, token) {
        console.log(token.id)
        var paymentMethodEndpint = '/billing/payment-method/create/'
        var data = {
            'token': token.id
        }
        console.log("Hello WOrld")
        $.ajax({
            data: data,
            url: paymentMethodEndpint,
            method: "POST",
            success: function(data){
                var successMsg = data.message || "Success! Your card was added."
                card.clear()
                if (nextUrl){
                    successMsg = successMsg + "<br/><br/><i class='fa fa-spin fa-spinner'></i> Redirecting..."
                }
                if ($.alert){
                    $.alert(successMsg)
                } else {
                    alert(successMsg)
                }
                btnLoad.html(btnLoadDefualtHtml)
                btnLoad.attr('class', btnLoadDefualtClasses)
                redirectToNext(nextUrl, 1800)
            },
            error: function(error){
                console.log(error)
                $.alert({title: "An error occured", content:"Please try adding your card again."})
                btnLoad.html(btnLoadDefualtHtml)
                btnLoad.attr('class', btnLoadDefualtClasses)
            }
        })
    }
}
})
