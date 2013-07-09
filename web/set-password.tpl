<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
	<title>SpicyMango</title>	
	
	<link rel="stylesheet" href="./css/screen.css" type="text/css" media="screen" title="no title" charset="utf-8" />	
	<link rel="stylesheet" href="./css/plugin.css" type="text/css" media="screen" title="no title" charset="utf-8" />	
	<link rel="stylesheet" href="./css/custom.css" type="text/css" media="screen" title="no title" charset="utf-8" />	
	<style type="text/css">
		label { float: left; display: block; width: 120px; }
		label.error { float: none; color: red; padding-left: .5em; vertical-align: top; }
	</style>
</head>

<body>
	
%include header_nav
	
	<div id="content" class="xfluid">
		
		<div class="portlet x3">
			<div class="portlet-header"><h4>Change Password</h4></div>
			
			<div class="portlet-content">
				
				<form id="chngpass" method="GET" action="#">
					<label id="lcurrentpass" for="currentpass">Current Password:</label>
					<input id="currentpass" name="currentpass" type="password" value="" /> 
					<br />
					<label id="lnewpass" for="newpass">New Password:</label>
					<input id="newpass" name="newpass" type="password" value="" />
					<br />
					<label id="lconfirmpass" for="confirmpass">Confirm Password:</label>
					<input id="confirmpass" name="confirmpass" type="password" value="" />
					<br /><br />
					<input id="submitpass" name="submitpass" type="submit" value="Save" class="btn btn-small" />
				</form>
				
			</div>
		</div>
		
	</div> <!-- #content -->

%include footer

<script  type="text/javascript" src="js/jquery/jquery.1.4.2.min.js"></script>
<script  type="text/javascript" src="js/jquery.validate.js"></script>
<!--<script  type="text/javascript" src="js/slate/slate.js"></script>
<script  type="text/javascript" src="js/slate/slate.portlet.js"></script>
<script  type="text/javascript" src="js/plugin.js"></script>-->

<script type="text/javascript" charset="utf-8">
$(function () 
{
	//slate.init ();
	//slate.portlet.init ();
	
	$("#chngpass").validate({
			rules: {
				currentpass: "required",
				newpass: {
					required: true,
					minlength: 6
				},
				confirmpass: {
					required: true,
					equalTo: "#newpass",
					minlength: 6
				}
			},
			submitHandler: function() {
				$.ajax({
					url: "setpass",
					type: "POST",
					cache: false,
					data: $("#chngpass").serialize(),
					success: function(html) {
						if (html==1) {
							alert("Password Changed\nPlease login again.");
							window.location.href = "/login";
						}
						else if (html==2) {
							alert("Current Password Incorrect");
							$("#currentpass").val('');
						}
						else {
							alert("Server Error");
							$("#currentpass").val('');
							$("#newpass").val('');
							$("#confirmpass").val('');
						}
					},
					failure: function() {
						alert("Failure");
					}
				});
			}
	});

});
</script>

</body>
</html>
