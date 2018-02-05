$(document).ready(function() {
    $("#load").hide();
});

$(function() {
    $('a#auto_categorization').click(function() {
        // var user = $('#txtUsername').val();
        // var pass = $('#txtPassword').val();
        $.ajax({
             url: '/auto_categorization',
             data: $('form').serialize(),
             type: 'POST',
             beforeSend: function( xhr){
                 console.log("before")
                 $("#load").show();
                 $('#load').addClass('loader');
                 $("#main").hide();
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
                    $('#load').removeClass('loader');
                    $("#main").show();
                    $("#buttons").show();
                    $("#load").hide();

                 });

             }
        //     error: function(error) {
        //         console.log(error);
        //     }
         });
    });
});