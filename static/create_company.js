    $(document).ready(function() {
        $('form').submit(function (e) {    
        $.ajax({
            type: "POST",
            dataType: "json",
            url : "/api/create_company",
            data : $('form').serialize(),
            success: function (data) {
               if (data.error) {
                $('#errorAlert').text(data.error).show();
                $('#successAlert').hide();
               }
              
               else {
                $('#successAlert').text(data.company + ' successfully created.').show();
                $('#errorAlert').hide();
               }
            }
        });
        e.preventDefault();
    });
});