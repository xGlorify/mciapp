$(document).ready(function () {
	$("#hoursSaveBtn").click(function (e) {
		$.ajax({
			type : "POST",
			dataType : "json",
			url : "/api/edit_hours",
			data: {

				hour_id : $("#hour_id").val(),
				date : $("#date").val(),
				employee_name : $("#employee_name").val(),
				regular_hours : $("#regular_hours").val(),
				ot_onehalf : $("#ot_onehalf").val(),
				ot_double : $("#ot_double").val(),
			},
			success: function (data) {
				if (data.error) {
				$("#errorAlert").text(data.error).show();
                $("#successAlert").hide();
				}
			else {
				$("#returnBtn").show();
				$("#successAlert").text(data.employee_name + " hour entry successfully edited for day of " + data.date +".").show();
                $("#errorAlert").hide();
			 }
			}
		});
	});
});