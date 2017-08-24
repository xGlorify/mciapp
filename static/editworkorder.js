$(document).ready(function () {
	$("#workorderEditPanel").hide();
	$("#notesEditPanel").hide();
	$("#informationPanelEditBtn").click(function (e) {
		$("#workorderInformationPanel").hide();
		$("#workorderNotesPanel").hide();
		$("#workorderEditPanel").show();
		$("#notesEditPanel").show();
		$("#informationPanelSaveBtn").click(function (a) {

			$.ajax({
				type : "POST",
				dataType : "json",
				url : "/api/update_workorder",
				data: {

					id : $("#id").val(),
					customer : $("#customer").val(),
					customer_po : $("#customer_po").val(),
					requested_by : $("#requested_by").val(),
					work_description : $("#work_description").val(),
					work_notes : $("#work_notes").val(),
					status : $("#status").val()

				},
				success: function (data) {
					if (data.error) {
					$("#errorAlert").text(data.error).show();
	                $("#successAlert").hide();
					}
				else {
					$("#successAlert").text("Workorder MCI" + data.workorder_id + " Edited Succesfully").show();
	                $("#errorAlert").hide();
				 }
				}
			});
		});
	});
	$("#addHoursBtn").click(function() {
		var form2_data = new FormData($('#addHoursForm'))
     	form2_data.append('workorder_id', $('#workorder_id').val());
        form2_data.append('date', $('#date').val());
        form2_data.append('employee_name', $('#employee_name').val());
        form2_data.append('regular_hours', $('#regular_hours').val());
        form2_data.append('ot_onehalf', $('#ot_onehalf').val());
        form2_data.append('ot_double', $('#ot_double').val());
		$.ajax({
			type : "POST",
			dataType : "json",
			url : "/api/submit_hours",
			data : form2_data,
			contentType : false,
            cache : false,
            processData : false,

				success: function (data) {
					if (data.error) {
					$("#errorAlert2").text(data.error).show();
	                $("#successAlert2").hide();
					}
				else {
					$("#successAlert2").text(data.employee_name + ' hours successfully added. You may enter additional hours or reload the page to view your entries.').show();
					$('#regular_hours').val("");
					$('#employee_name').val("");
					$('#date').val("");
					$('#ot_onehalf').val("");
					$('#ot_double').val("");
	                $("#errorAlert2").hide();
				 }
				}
		})
	});
    $('#addMatBtn').click(function (e) {
        var form_data = new FormData($('#addMatForm'));
        form_data.append('workorder_id', $('#workorder_id').val());
        form_data.append('description', $('#description').val());
        form_data.append('cost', $('#cost').val());
        form_data.append('quantity', $('#quantity').val());
        form_data.append('used', $('#used').val());
        form_data.append('supplier', $('#supplier').val());
        form_data.append('attachment', $('#attachment')[0].files[0]);
        $.ajax({
            type : "POST",
            dataType : "json",
            url : "/api/submit_materials",
            data : form_data,
            contentType : false,
            cache : false,
            processData : false,
            success: function (data) {
                if (data.error) {
                $("#errorAlert3").text(data.error).show();
                $("#successAlert3").hide();
                }
             else {
                $("#successAlert3").text(data.quantity + ' of ' + data.materials + ' successfully added to workorder MCI' + data.workorder_id + '. You may enter additional items or reload the page to view your submission(s).').show();
                $("#description").val("");
				$('#cost').val("");
				$('#quantity').val("");
				$('#used').val("");
				$('#supplier').val("");
				$('#attachment').val("");
				$("#errorAlert3").hide();
             }
            }
        });
        e.preventDefault();
   });
    $('#addAttachBtn').click(function (e) {
        var form_data = new FormData($('#addAttachForm'));
        form_data.append('workorder_id', $('#workorder_id').val());
        form_data.append('woa_description', $('#woa_description').val());
        form_data.append('woa_attachment', $('#woa_attachment')[0].files[0]);
        $.ajax({
            type : "POST",
            dataType : "json",
            url : "/api/submit_workorder_attachment",
            data : form_data,
            contentType : false,
            cache : false,
            processData : false,
            success: function (data) {
                if (data.error) {
                $("#errorAlert4").text(data.error).show();
                $("#successAlert4").hide();
                }
             else {
                $("#successAlert4").text(data.description + ' successfully uploaded to workorder MCI' + data.workorder_id + '. You may upload additional files or reload the page to view your submission(s).').show();
                $("#description").val("");
				$('#attachment').val("");
				$("#errorAlert4").hide();
             }
            }
        });
        e.preventDefault();
   });
});