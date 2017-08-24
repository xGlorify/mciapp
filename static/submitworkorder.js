    $(document).ready(function () {
        $("#materialsForm").hide();
        $("#hoursForm").hide();
        $("#createWorkorderButton").click(function (e) {    
        $.ajax({
            type : "POST",
            dataType : "json",
            url : "/api/submitworkorder",
            data : $("#createWorkorder").serialize(),
            success: function (data) {
               if (data.error) {
                $("#errorAlert").text(data.error).show();
                $("#successAlert").hide();
                $("#materialsForm").hide();
               }
               else {
                $("#successAlert").text(data.company + ' PO# ' + data.customer_po + ' successfully created with a work order number of MCI' + data.workorder_id + '. Submit your materials below.').fadeIn("slow");
                $("#materialPanelHeading").text('Workorder MCI ' + data.workorder_id + ' Materials Information - ' + data.company)
                $("#errorAlert").hide();
                $("#workorderPanel").hide();
                $("#materialsForm").fadeIn("slow");
                $('#materialsButton').click(function (e) {
                    var form_data = new FormData($('#actualMatForm'));
                    form_data.append('workorder_id', data.workorder_id);
                    form_data.append('description', $('#description').val());
                    form_data.append('cost', $('#cost').val());
                    form_data.append('quantity', $('#quantity').val());
                    form_data.append('used', $('#used').val());
                    form_data.append('supplier', $('#supplier').val());
                    form_data.append('attachment', $('#attachment')[0].files[0]);
                    $.ajax({
                        type : "POST",
                        dataType :"json",
                        url : "/api/submit_materials",
                        data : form_data,
                        contentType : false,
                        cache : false,
                        processData : false,
                        success: function (data) {
                            if (data.error) {
                            $("#errorAlert").text(data.error).show();
                            $("#successAlert").hide();
                            }
                         else {
                            $("#successAlert").text(data.quantity + ' of ' + data.materials + ' successfully added to workorder MCI' + data.workorder_id + '. You may submit additional materials or hours below.').show();
                            $("#errorAlert").hide();
                            $("#materialsForm").trigger("reset");
                            $("#hoursForm").fadeIn("slow");
                         }
                        }
                    });
                    e.preventDefault();
               });
            $("#hoursButton").click(function (e) {
                $.ajax({
                    type : "POST",
                    dataType : "json",
                    url : "/api/submit_hours",
                    data : {
                        workorder_id : data.workorder_id,
                        employee_name : $('#employee_name').val(),
                        date : $('#date').val(),
                        regular_hours : $('#regular_hours').val(),
                        ot_onehalf : $('#ot_onehalf').val(),
                        ot_double : $('#ot_double').val()
                    },
                    success: function (data) {
                        if (data.error) {
                        $("#errorAlert").text(data.error).show();
                        $("#successAlert").hide();
                    }
                     else {
                        $("#successAlert").text(data.employee_name + ' successfully added hours.').show();
                        $("#errorAlert").hide();
                    }
                    }
                });
            e.preventDefault();
            });
            };
        }
        });
    e.preventDefault();
    });
});
