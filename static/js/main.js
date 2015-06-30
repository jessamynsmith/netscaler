/**
 * Created by jeffrey.dambly on 6/29/15.
 */
// AJAX for posting
function create_post(form, mymodal) {

    console.log("create post is working!"); // sanity check
    console.log(form.serialize());
    $.ajax({
            url : form.attr('action'), // the endpoint
            type : "POST", // http method
            data : form.serialize(), // data sent with the post request
            // handle a successful response
            success : function(json) {
                form.val(''); // remove the value from the input
                mymodal.modal('hide');
                console.log(json); // log the returned json to the console
                console.log("success"); // another sanity check
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
}

var temp = $('.modal').on('show.bs.modal', function(){
        console.log('modal is shown');
        console.log(this.id);
        return $(this)
    });
// Submit post on submit
$('.form-inline').on('submit', function(event) {
    event.preventDefault();
    console.log("form submitted!");  // sanity check

    create_post($(this), temp);
});

$(".modal").on('hide.bs.modal', function(){
    console.log('Modal was hidden from the user');
});