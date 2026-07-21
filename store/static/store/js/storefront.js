$('#slider1, #slider2, #slider3, #slider4').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        },
    },
});

function updateTotals(data) {
    $('#amount').text(data.amount);
    $('#totalamount').text(data.totalamount);
}

$('.positive').click(function () {
    const button = $(this);
    const quantity = button.closest('.cart-item').find('.item-quantity');

    $.ajax({
        type: 'GET',
        url: '/pluscart/',
        data: {
            prod_id: button.attr('pid'),
        },
        success: function (data) {
            quantity.text(data.quantity);
            updateTotals(data);
        },
    });
});

$('.negative').click(function () {
    const button = $(this);
    const quantity = button.closest('.cart-item').find('.item-quantity');

    $.ajax({
        type: 'GET',
        url: '/minuscart/',
        data: {
            prod_id: button.attr('pid'),
        },
        success: function (data) {
            quantity.text(data.quantity);
            updateTotals(data);
        },
    });
});

$('.remove').click(function () {
    const button = $(this);

    $.ajax({
        type: 'GET',
        url: '/removecart/',
        data: {
            prod_id: button.attr('pid'),
        },
        success: function (data) {
            updateTotals(data);
            button.closest('.cart-row').remove();

            if (data.empty_cart) {
                $('#cart-items').html('<p>Your cart is empty.</p>');
                $('.d-grid a[href="/checkout/"]').replaceWith(
                    '<button class="btn btn-primary" disabled>Place Order</button>'
                );
            }
        },
    });
});
