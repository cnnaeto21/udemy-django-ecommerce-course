
$(document).ready(function(){
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndpoint = contactForm.attr("action")
    


    function displaySubmitting(submitBtn, defaultText, doSubmit){
        if (doSubmit) {
            submitBtn.addClass("disabled")
            submitBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching....")
        } else {
            submitBtn.removeClass("disabled")
            submitBtn.html(defaultText)
        }
        
    }
    
    contactForm.submit(function(event){
        event.preventDefault()
        var contactFormSubmitBtn = contactForm.find("[type='submit']")
        var contactFormSubmitBtnTxt = contactFormSubmitBtn.text()



        var contactFormData = contactForm.serialize()
        var thisForm = $(this)
        displaySubmitting(contactFormSubmitBtn, "", true)
        $.ajax({
            method: contactFormMethod,
            url: contactFormEndpoint,
            data: contactFormData,
            success: function(data){
                thisForm[0].reset()
                $.alert({
                    title: 'Success!',
                    content: 'Thank you for your submission!',
                    theme: "modern",
                })
                setTimeout(function(){
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 500)
            },
            error: function(error){
                console.log(error)
                var jsonData = error.responseJSON
                var msg = ""

                $.each(jsonData, function(key, value){
                    msg += key + ": " + value[0].message + "</br>"
                })
                $.alert({
                    title: 'Oops',
                    content: msg,
                    theme: "modern",
                })
                setTimeout(function(){
                    displaySubmitting(contactFormSubmitBtn, contactFormSubmitBtnTxt, false)
                }, 500)
            }
        })
    })



    var searchForm = $('.search-form')
    var searchInput = searchForm.find("[name='q']")
    var typingTimer;
    var typingInterval = 500
    var searchBtn = searchForm.find("[type='submit']")


    searchInput.keyup(function(event){
        clearTimeout(typingTimer)
        typingTimer = setTimeout(performSearch, typingInterval)
    })

    searchInput.keydown(function(event){
        clearTimeout(typingTimer)
    })

    function displaySearching(){
        searchBtn.addClass("disabled")
        searchBtn.html("<i class='fa fa-spin fa-spinner'></i> Searching....")
    }

    function performSearch(){
        displaySearching()
        var query = searchInput.val()
        setTimeout(function(){
            window.location.href='/search/?q=' + query
        }, 1000)
    }

    var productForm = $(".form-add-ajax")
    productForm.submit(function(event){
        event.preventDefault();
        //console.log("Form is not sending");
        var thisForm = $(this)
        var actionEndPoint = thisForm.attr("action");
        //var actionEndPoint = thisForm.attr("data-endpoint")
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();
    
        $.ajax({
            url: actionEndPoint,
            method: httpMethod,
            data: formData,
            success: function(data){
                var submitSpan = thisForm.find(".submit-span")
                if (data.added){
                    submitSpan.html("In Cart <button type = 'submit' class='btn btn-link'>Remove?</button>")
                } else{
                    submitSpan.html("<button type = 'submit' class='btn btn-success'>Add to Cart</button>")
                }
                var navBarCount = $('.navbar-cart-count')
                navBarCount.text(data.cartItemCount)
                var currentPath = window.location.href
                if (currentPath.indexOf("cart") != -1) {
                    updateCart()
                }

            },
            error: function(errorData){
                $.alert({
                    title: 'Oops',
                    content: 'An error occured!',
                    theme: "modern",
                });
                console.log("error")
                console.log(errorData)
            }
        })
    })

    function updateCart(){
        console.log("in current cart")
        var cartTable = $(".cart-table")
        var cartBody = cartTable.find(".cart-body")
        //cartBody.html("<h1>Changed</h1>")
        var productRows = cartBody.find(".cart-product")
        currentUrl = window.location.href


        var refreshCartUrl = '/api/cart'
        var refreshCartMethod = "GET";
        var data = {};

        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function(data){
                var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                if (data.products.length > 0){
                    productRows.html(" ")
                    i = data.products.length
                    $.each(data.products, function(index, value){
                        console.log(value)
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                        newCartItemRemove.css("display", "block")
                        newCartItemRemove.find(".cart-item-product-id").val(value.id)
                        cartBody.prepend("<tr><th scope=\"row\">"+ i +"</th><td><a href='"+ value.url + "'>"+ value.name + "</a>" + newCartItemRemove.html() + "<td></td>" + value.price + "</td></tr>")
                        i --
                    })
                    cartBody.find(".cart-subtotal").text(data.subtotal)
                    cartBody.find(".cart-total").text(data.total)
                } else {
                    window.location.href = currentUrl
                }
            },
            error: function(errorData){
                $.alert({
                    title: 'Oops',
                    content: 'An error occured!',
                    theme: "modern",
                });
                console.log("error")
                console.log(errorData)

            }
        })
    }
})