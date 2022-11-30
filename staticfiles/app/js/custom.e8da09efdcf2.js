$(document).ready(function () {

    $('.increment-btn').click(function (e) { 
        e.preventDefault();
        
        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(inc_value,10);
        value = isNaN(value) ? 0 : value;
        if(value < 5)
        {
            value++;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });

    $('.decrement-btn').click(function (e) { 
        e.preventDefault();
        
        var dec_value = $(this).closest('.product_data').find('.qty-input').val();
        var value = parseInt(dec_value,10);
        value = isNaN(value) ? 0 : value;
        if(value > 1)
        {
            value--;
            $(this).closest('.product_data').find('.qty-input').val(value);
        }
    });


    $('.addToCartBtn').click(function (e) {
        e.preventDefault();

        /* estas variables las toma del input en la vista de librodetalle */
        var product_id = $(this).closest('.product_data').find('.prod_id').val(); 
        var producto_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
 
        $.ajax({
            method: "POST",
            url: "/add-to-cart",
            data: {
                'product_id':product_id,
                'producto_qty':producto_qty,
                csrfmiddlewaretoken: token
            },
            
            success: function (response) {
                console.log(response)
                alertify.success(response.status)
                
            }
        });
    });
    

    $('.changeQuantity').click(function (e) {
        e.preventDefault();

        var product_id = $(this).closest('.product_data').find('.prod_id').val(); 
        var producto_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
 
        $.ajax({
            method: "POST",
            url: "/update-cart",
            data: {
                'product_id':product_id,
                'producto_qty':producto_qty,
                csrfmiddlewaretoken: token
            },
            
            success: function (response) {
                console.log(response)
                alertify.success(response.status)
                
            }
        });
    });
    


    $(document).on('click', '.delete-cart-item', function (e) { 
        e.preventDefault();
        
        var product_id = $(this).closest('.product_data').find('.prod_id').val(); 
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "delete-cart-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status) 
                $('.cartdata').load(location.href + " .cartdata");
                
            }
        });
    });
    $('.reservarBtn').click(function (e) {
        e.preventDefault();

        /* estas variables las toma del input en la vista de librodetalle */
        var product_id = $(this).closest('.product_data').find('.prod_id').val(); 
        var producto_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
 
        $.ajax({
            method: "POST",
            url: "/reservar-libro",
            data: {
                'product_id':product_id,
                'producto_qty':producto_qty,
                csrfmiddlewaretoken: token
            },
            
            success: function (response) {
                console.log(response)
                alertify.success(response.status)
                
            }
        });
    });
    $('.addToCartBtnReserva').click(function (e) {
        e.preventDefault();

        /* estas variables las toma del input en la vista de librodetalle */
        var product_id = $(this).closest('.product_data').find('.prod_id').val(); 
        var producto_qty = $(this).closest('.product_data').find('.qty-input').val();
        var token = $('input[name=csrfmiddlewaretoken]').val();
 
        $.ajax({
            method: "POST",
            url: "/add-to-cart-reserva",
            data: {
                'product_id':product_id,
                'producto_qty':producto_qty,
                csrfmiddlewaretoken: token
            },
            
            success: function (response) {
                console.log(response)
                alertify.success(response.status)
                
            }
        });
    });
    $(document).on('click', '.delete-reserva-item', function (e) { 
        e.preventDefault();
        
        var product_id = $(this).closest('.product_data').find('.prod_id').val(); 
        var token = $('input[name=csrfmiddlewaretoken]').val();

        $.ajax({
            method: "POST",
            url: "delete-reserva-item",
            data: {
                'product_id': product_id,
                csrfmiddlewaretoken: token
            },
            success: function (response) {
                alertify.success(response.status) 
                $('.reservadata').load(location.href + " .reservadata");
                
            }
        });
    });
   
});