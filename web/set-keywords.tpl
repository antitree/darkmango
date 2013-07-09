<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
	<title>SpicyMango</title>	
<!--	
    <style type="text/css" title="currentStyle">
            @import "./css/jquery-ui.css";
            @import "./css/jquery-ui-1.7.2.custom.css";
    </style>
-->
    <link rel="stylesheet" href="./css/screen.css" type="text/css" media="screen" title="no title" charset="utf-8" />	
	<link rel="stylesheet" href="./css/plugin.css" type="text/css" media="screen" title="no title" charset="utf-8" />	
	<link rel="stylesheet" href="./css/custom.css" type="text/css" media="screen" title="no title" charset="utf-8" />
</head>

<body>
	
%include header_nav
	
	<div id="content" class="xfluid">
		
		<div class="portlet x6">
			<div class="portlet-header"><h4>Keywords</h4></div>
			
			<div class="portlet-content">
                <!-- Place holder where add and delete buttons will be generated -->
                <!--<div class="add_delete_toolbar" /></div>-->
                <div>
                <button id="btnAddNewRow" class="btn btn-small">Add</button>
                <button id="btnDeleteRow" class="delete_row btn btn-small">Delete</button>
				<button id="btnAnalyze" type="button" class="btn btn-small btn-orange">Re-Analyze Data</button><span id="dataLoading" style="display: none; float: right;"><h3>Analyzing...</h3></span>
				</div>
                <br />
                <table cellpadding="0" cellspacing="0" border="0" class="display" id="keyword_table">
					<thead>
						<tr>
							<th>keyword</th>
							<th>weight</th>
						</tr>
					</thead>
					<tbody>
                        {{!dataRows}}
					</tbody>
				</table>
                
                <!-- Custom form for adding new records -->
                <form id="formAddNewRow" action="#" title="New Keyword">
                    <label for="keyword">Keyword</label><br />
                    <input type="text" name="keyword" id="keyword" class="required" rel="0" />
                    <br />
                    <label for="weight">Weight</label><br />
                    <input type="text" name="weight" id="weight" class="required" rel="1" />
                    <br />
                </form>

			</div>
		</div><!-- #portlet -->
		<div class="portlet x3">
			<div class="portlet-header"><h4>Thresholds</h4></div>
			<div class="portlet-content">
				<div id="slider"></div>
				<br />
				<form>
					<label for="lowrange">Low Range:</label>
					<span id="lowrange" style="border: 0px; font-weight: bold; color: #666;"></span>
					<br />
					<label for="medrange">Medium Range:</label>
					<span id="medrange" style="border: 0px; font-weight: bold; color: #F90;"></span>
					<br />
					<label for="highrange">High Range:</label>
					<span id="highrange" style="border: 0px; font-weight: bold; color: #BC4848;"></span>
					<button id="btnThreshold" type="button" class="btn btn-small btn-grey" style="float: right;" disabled="disabled">Save</button>
				</form>
			</div>
		</div> <!-- #portlet -->
	</div> <!-- #content -->

%include footer

<script  type="text/javascript" src="js/jquery/jquery.1.4.2.min.js"></script>
<script  type="text/javascript" src="js/slate/slate.js"></script>
<script  type="text/javascript" src="js/slate/slate.portlet.js"></script>
<script  type="text/javascript" src="js/jquery.dataTables.min.js"></script>
<script  type="text/javascript" src="js/jquery.dataTables.editable.js"></script>
<script  type="text/javascript" src="js/jquery.jeditable.js"></script>
<script  type="text/javascript" src="js/jquery-ui.js"></script>
<script  type="text/javascript" src="js/jquery.validate.js"></script>

<script type="text/javascript" charset="utf-8">
$(function () 
{
	//slate.init ();
	//slate.portlet.init ();
	var oTable = $('#keyword_table').dataTable({
		"aaSorting": [[ 1, "desc" ]],
        "oLanguage": {
                        "oPaginate": {
                                        "sNext": "",
                                        "sPrevious": ""
                                     }
                     }
	}).makeEditable({
                     sUpdateURL: "keyupdate",
                     sAddURL: "keyadd",
					 sDeleteURL: "keydelete",
					 "aoColumns": [
					                {
									cssclass:"required"
									},
									{
									cssclass:"required digits",
									oValidationOptions: {
										rules: {
											value: {
											  range: [-100, 100]
											}
										  }
										}
									}
						],
	});

	$('#btnAnalyze').click(function (){
			$(this).addClass( "btn-grey" ); 
			$(this).removeClass( "btn-orange" );
			$('#dataLoading').css({ 'display' : 'block', 'text-decoration' : 'blink' });
			$(this).attr("disabled", "disabled");
			$.ajax({
				url: "reAnalyze",
				type: "GET",
				cache: false,
				success: function (html) {     
					if (html==1) {
						$('#btnAnalyze').addClass( "btn-orange" ); 
						$('#btnAnalyze').removeClass( "btn-grey" );
						$('#dataLoading').css({ 'display' : 'none', 'text-decoration' : 'none' });
						$('#btnAnalyze').removeAttr("disabled");
					} else 
						alert('Sorry, unexpected error.');
					}
			});

	});
	$('#slider').slider({
		range: true,
		min: 1,
		max: 100,
		values: {{slider}} 
		slide: function( event, ui ) {
			$( "#lowrange" ).text( "1 - " + ui.values[ 0 ] );
			$( "#medrange" ).text( (ui.values[ 0 ] + 1) + " - " + (ui.values[ 1 ] - 1) );
			$( "#highrange" ).text( ui.values[ 1 ] + " - 100" );
			$('#btnThreshold').addClass( "btn-navy" ); 
			$('#btnThreshold').removeClass( "btn-grey" );
			$('#btnThreshold').removeAttr("disabled");
									 }
	});
	$( "#lowrange" ).text( "1 - " + $( "#slider" ).slider( "values", 0 ) );
	$( "#medrange" ).text( ( $( "#slider" ).slider( "values", 0 ) + 1) + " - " + ( $( "#slider" ).slider( "values", 1 ) - 1) );
	$( "#highrange" ).text( $( "#slider" ).slider( "values", 1 ) + " - 100" );
	$('#btnThreshold').click(function (){
			$.ajax({
				url: "thresholdsave",
				type: "GET",
				cache: false,
				data: { lmax : $("#slider").slider("values", 0) , mmin : ($("#slider").slider("values", 0) + 1) , mmax : ($("#slider").slider("values", 1) - 1) , hmin : $("#slider").slider("values", 1) },
				success: function (html) {     
					if (html==1) {
						$('#btnThreshold').addClass( "btn-grey" ); 
						$('#btnThreshold').removeClass( "btn-navy" );
						$('#btnThreshold').attr("disabled", "disabled");
					} else 
						alert('Sorry, unexpected error.');
					},
				error: function () {
					alert("Could not connect to Server");
				}
			});
	});
	$("#formAddNewRow").validate({
	  rules: {
		weight: {
		  range: [-100, 100]
		}
	  }
	});
});

</script>

</body>
</html>
