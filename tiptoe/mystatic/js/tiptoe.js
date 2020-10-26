$(document).ready(function () {
    //Adding of Auto Search
    var searchForm = $(".search-form");
    var searchInput = searchForm.find("[name='q']");
    var typingTimer;
    var typingInterval = 1000;
    var searchBtn = searchForm.find("[type='submit']");

    searchInput.keyup(function (evt) {
        clearTimeout(typingTimer);
        typingTimer = setInterval(performSearch, typingInterval);
    });

    //key pressed
    searchInput.keydown(function (event) {
        clearTimeout(typingTimer);
    });

    function displaySearching() {
        searchBtn.addClass("disabled");
        searchBtn.html('<i class="fa fa-spin fa-spinner"></i>');
    }

    function performSearch() {
        displaySearching();
        var query = searchInput.val();
        setTimeout(function () {
            window.location.href = "/search/?q=" + query;
        }, 500);

    }

    //End of Auto search

    //Adding and Removing Products in Carts Ajaxily
    var addtoCart = $(".addtoCart");
    addtoCart.submit(function (e) {
        e.preventDefault();
        var thisForm = $(this);
        //var actionEndpoint = thisForm.attr("action");
        var actionEndpoint = thisForm.attr("data-endpoint");
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        $.ajax({
            url: actionEndpoint,
            method: httpMethod,
            data: formData,
            success: function (data) {
                //We looking for submit span in out dom
                var submitspan = thisForm.find(".submit-span");
                if (data.added) {
                    submitspan.html(
                        "<button class='btn btn-md  btn-outline-danger' type='submit'>× Remove</button>"
                    );
                } else {
                    submitspan.html(
                        "<button class='btn btn-md  btn-outline-primary' type='submit'> <i class='fas fa-shopping-cart'></i> </button>"
                    );
                }
                //Changing the cart number
                var navcartcount = $(".navcartcount");
                navcartcount.text(data.cartItemcount);

                var currentPath = window.location.href;

                if (currentPath.indexOf("cart") != -1) {
                    refreshcart();
                }
            },
            error: function (errorData) {
                $.alert({
                    title: 'Sorry',
                    content: 'An Error Occured',
                    theme: 'material'
                })
            }
        }); //End of ajax
    }); //End of addtocartsubmit

    //Refreshing cart after removing a product
    function refreshcart() {
        var cartTable = $(".cart-table");
        var cartBody = $(".cart-body");
        var cartTotal = $(".cart-total");
        var productRow = cartBody.find(".cart-product");
        var currentUrl = window.location.href;

        //Creating our ajax for cart refresh
        var refreshCartUrl = "/api/cart";
        var refreshCartMethod = "GET";
        var data = {};

        $.ajax({
            url: refreshCartUrl,
            method: refreshCartMethod,
            data: data,
            success: function (data) {
                var hiddenCartItemRemoveForm = $(".cart-item-remove-form");
                if (data.products.length > 0) {
                    productRow.html("");
                    i = data.products.length;
                    $.each(data.products, function (index, value) {
                        var newCartItemRemove = hiddenCartItemRemoveForm.clone();
                        newCartItemRemove.css("display", "block");
                        newCartItemRemove.find(".cart-item-product-id").val(value.id);

                        cartBody.prepend(
                            "<tr class='cart-product'><td><a href='" +
                            value.url +
                            "'><figure class='media'><div class='img-wrap'><img src='" +
                            value.image +
                            "' class='img-thumbnail img-sm'/></div><figcaption class='media-body'> <h6 class='title text-truncate'> <a href='" +
                            value.url +
                            "'>" +
                            value.name +
                            "</a></h6></figcaption> </figure></a></td><td><div class='price-wrap'><var class='price'>GHC" +
                            value.price +
                            "</var></div></td><td class='text-right'>" +
                            newCartItemRemove.html() +
                            "</td> </tr>"
                        );
                        i--;
                    });
                    //End f looping through products

                    cartTotal.text(data.total);
                } else {
                    window.location.href = currentUrl;
                }
            },
            error: function (errorData) {
                $.alert({
                    title: 'Sorry',
                    content: 'An Error Occured',
                    theme: 'dark'
                })
            }
        }); //End of ajax for refresh cart
    } //end of refresh cart function
}); //end of document ready