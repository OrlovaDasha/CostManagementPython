$(document).ready(function() {
    $("#load").hide();
        $.ajax({
             url: '/auto_categorization',
             data: $('form#main').serialize(),
             type: 'POST',
             beforeSend: function( xhr){
                 console.log("before")
                 $("#load").show();
                 $('#load').addClass('loader');
                 $("#mainDiv").hide();
                 $("#buttons").hide();
                },
             success: function(response) {
                 console.log(response);
                  $.each(response, function(key, value) {
                      var optionExists = $('select[name*=' + key + '] option[value="' + value["category"] + '"]').length > 0;

                    if(!optionExists)
                    {
                        $('select[name*=' + key + ']').append($("<option></option>").attr("value",value["category"]).text(value["category"]));
                    }
                      $('select[name*=' + key + '] option[value*= "'+  value["category"] + '"]').attr('selected','selected');
                     $('input[name=word' + key + ']').val(value["word"])
                    $('#load').removeClass('loader');
                    $("#mainDiv").show();
                    $("#buttons").show();
                    $("#load").hide();

                 });

             }
        //     error: function(error) {
        //         console.log(error);
        //     }
         });
    });


$(function() {
    $('a#add_category').click(function() {
        // var user = $('#txtUsername').val();
        // var pass = $('#txtPassword').val();
        $.ajax({
             url: '/add_category',
             data: $( '#new_category' ).serialize(),
             type: 'POST',
             success: function(response) {
                 console.log(response);
                 if ("Name" in response) {
                     $('select').append($("<option></option>").attr("value", response["Name"]).text(response["Name"]));
                 }
             }
        //     error: function(error) {
        //         console.log(error);
        //     }
         });
    });
});