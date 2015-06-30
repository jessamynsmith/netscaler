/**
 * Created by jeffrey.dambly on 6/29/15.
 */
// AJAX for posting
function create_post(form, mymodal, update) {
    $.ajax({
            url : form.attr('action'), // the endpoint
            type : "POST", // http method
            data : form.serialize(), // data sent with the post request
            // handle a successful response
            success : function(json) {
                form.val(''); // remove the value from the input
                mymodal.modal('hide');
                update.html(json);
            },
            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
}

function deletemodal(id, mymodal, url, update){
    console.log(id);
    console.log(mymodal);
    console.log(url);
    console.log(update);
    $.get(url, function(data){
        id.html(data);
    });
    mymodal.modal('toggle');

}