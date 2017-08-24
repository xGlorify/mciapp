	$(document).ready(function () {
		$('#registerUserButton').click(function (e) {
			$.ajax({
				type : "POST",
				dataType : "json",
				url : "/api/register_user",
				data : $("#registerUser").serialize(),
				success: function (data) {
					if (data.error) {
					$("#errorAlert").text(data.error).show();
                	$("#successAlert").hide();
                	}
                	else {
                	$("#successAlert").text(data.first_name + ' ' + data.last_name + ' successfully registered.').fadeIn();
                	$("#errorAlert").hide();
                	}
				}
			});
			e.preventDefault();
		});
	});