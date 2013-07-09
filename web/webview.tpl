<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">

<head>
	<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
	<title>SpicyMango</title>
	
	<link rel="stylesheet" href="./css/screen.css" type="text/css" media="screen" title="no title" charset="utf-8" />
	<link rel="stylesheet" href="./css/plugin.css" type="text/css" media="screen" title="no title" charset="utf-8" />
	<link rel="stylesheet" href="./css/custom.css" type="text/css" media="screen" title="no title" charset="utf-8" />
	
	<style type="text/css" media="screen">
		
	</style>

</head>

<body>
	
%include header_nav

	<div id="content" class="xfluid">
		
		<div class="portlet x3" style="min-height: 300px;">
			
			<div class="portlet-header">
				<h4>Event Totals</h4>
			</div> <!-- .portlet-header -->
			
			<div class="portlet-content">
				<table cellspacing="0" class="info_table">
					<tbody>
						<tr>
							<td class="value">{{eventcount}}</td>
							<td class="full">Events</td>
						</tr>
						<tr>
							<td class="value">{{highs}}</td>
							<td class="full">High</td>
						</tr>
						<tr>
							<td class="value">{{mediums}}</td>
							<td class="full">Medium</td>
						</tr>
						<tr>
							<td class="value">{{lows}}</td>
							<td class="full">Low</td>
						</tr>
					</tbody>
				</table>
			</div> <!-- .portlet-content -->
		</div> <!-- .portlet -->
		
		<div id="dash_chart" class="portlet x9">
			
			<div class="portlet-header">
				<h4>Current Alert Trends</h4>
			</div> <!-- .portlet-header -->
			<div class="portlet-content">
				<table class="stats" title="area" width="100%" cellpadding="0" cellspacing="0">
					<caption>Last 12 Hours</caption>
					<thead>
						<tr>
							<td>&nbsp;</td>
							{{!chart_hours}}
						</tr>
					</thead>
					
					<tbody>
						<tr>
							<th>High</th>
							{{!chart_highs}}
						</tr>
						
						<tr>
							<th>Medium</th>
							{{!chart_mediums}}
						</tr>
						
						<tr>
							<th>Low</th>
							{{!chart_lows}}
						</tr>
					</tbody>
				</table>
			</div> <!-- .portlet-content -->
		</div> <!-- .portlet -->
		
		<div class="xbreak"></div> <!-- .xbreak -->
		
		<div class="portlet x6">
			<div class="portlet-header">
				<h4>Most Recent Alerts</h4>
				
				<ul class="portlet-tab-nav">
					<li class="portlet-tab-nav-active"><a href="#allalerts">All</a></li>
					<li class=""><a href="#highalerts">High</a></li>
					<li class=""><a href="#medalerts">Medium</a></li>
					<li class=""><a href="#lowalerts">Low</a></li>
				</ul>
			</div> <!-- .portlet-header -->
			
			<div id="recent-alerts" class="portlet-content">
				<div id="allalerts" class="portlet-tab-content">
					<table class="support_table" cellspacing="0">
						<tbody>
						{{!recent_all}}
						</tbody>
					</table>
				</div> <!-- .portlet-tab-content -->
				<div id="highalerts" class="portlet-tab-content">
					<table class="support_table" cellspacing="0">
						<tbody>
						{{!recent_highs}}
						</tbody>
					</table>
				</div> <!-- .portlet-tab-content -->
				<div id="medalerts" class="portlet-tab-content">
					<table class="support_table" cellspacing="0">
						<tbody>
						{{!recent_mediums}}
						</tbody>
					</table>
				</div> <!-- .portlet-tab-content -->
				<div id="lowalerts" class="portlet-tab-content">
					<table class="support_table" cellspacing="0">
						<tbody>
						{{!recent_lows}}
						</tbody>
					</table>
				</div> <!-- .portlet-tab-content -->
			</div> <!-- .portlet-content -->			
		</div>  <!-- .portlet -->
		
		<div class="portlet x6">
			<div class="portlet-header">
				<h4>Top Indices</h4>
				<ul class="portlet-tab-nav">
					<li class="portlet-tab-nav-active"><a href="#topusers">Users</a></li>
					<li class=""><a href="#topalerts">Alerts</a></li>
					<li class=""><a href="#topkeywords">Keywords</a></li>
				</ul>
			</div> <!-- .portlet-header -->
			<div class="portlet-content">
				<div id="topusers" class="portlet-tab-content">
					<table cellspacing="0" class="inbox_table">
						<tbody>
							<tr><td></td><td><b>Username</b></td><td><b># of Alerts</b></td></tr>
							% for user in topusers:
							<tr>
								<td></td>
								<td class="full"><a href="javascript:void(0)">{{user[0]}}</a></td>
								<td rel="tooltip" title="Number of alerts by this user.">{{user[1]}}</td>
							</tr>
							% end
						</tbody>
					</table>
				</div> <!-- .portlet-tab-content -->
				<div id="topalerts" class="portlet-tab-content">
					<table cellspacing="0" class="inbox_table">
						<tbody>
							<tr><td></td><td><b>Alert</b></td><td><b>Weight</b></td></tr>
							% for alert in topalerts:
							<tr>
								<td></td>
								<td class="full"><a id="{{alert[2]}}" href="javascript:void(0)">{{alert[0]}}</a></td>
								<td rel="tooltip" title="Weighted value.">{{alert[1]}}</td>
							</tr>
							% end
						</tbody>
					</table>
				</div> <!-- .portlet-tab-content -->
				<div id="topkeywords" class="portlet-tab-content">
					<table cellspacing="0" class="inbox_table">
						<tbody>
							<tr><td></td><td><b>Keyword</b></td><td><b>Count</b></td></tr>
							% for keyword in topkeywords:
							<tr>
								<td></td>
								<td class="full">{{keyword[0]}}</td>
								<td rel="tooltip" title="Number of occurances.">{{keyword[1]}}</td>
							</tr>
							% end
						</tbody>
					</table>
				</div> <!-- .portlet-tab-content -->
			</div> <!-- .portlet-content -->			
		</div> <!-- .portlet -->
	</div> <!-- #content -->
	<!-- Dialogs for Dashboard -->
	<div id="dialog-recent" title="Details">
		<table cellpadding="0" cellspacing="0" border="0" class="display">
			<thead>
				<th>Module</th>
				<th>TimeStamp</th>
				<th>Weight</th>
				<th>Username</th>
				<th>Hostname</th>
				<th>IRC Chan</th>
				<th>Message</th>
			</thead>
			<tbody>
			</tbody>
		</table>
	</div>
	<div id="dialog-user" title="">
		<table cellpadding="0" cellspacing="0" border="0" class="display">
			<thead>
				<th>Module</th>
				<th>TimeStamp</th>
				<th>Weight</th>
				<th>Hostname</th>
				<th>IRC Chan</th>
				<th>Message</th>
			</thead>
			<tbody>
			</tbody>
		</table>
	</div>

%include footer	

<script  type="text/javascript" src="js/jquery/jquery.1.4.2.min.js"></script>
<script  type="text/javascript" src="js/jquery-ui.js"></script>
<script  type="text/javascript" src="js/slate/slate.js"></script>
<script  type="text/javascript" src="js/slate/slate.portlet.js"></script>
<script  type="text/javascript" src="js/plugin.js"></script>

<script type="text/javascript" charset="utf-8">
$(function () 
{
        slate.init ();
        slate.portlet.init ();
		$("#dialog-recent").dialog({ autoOpen: false, width: 900 });
		$("#dialog-user").dialog({ autoOpen: false, width: 900 });
		$(".support_table a, #topalerts a").click(function() {
			var id = this.id
			$.ajax({
				url: 'dash-detail',
				type: 'GET',
				cache: false,
				data: { type : 'recent', eid : id },
				success: function(html) {
					$("#dialog-recent tbody").html(html);
					$("#dialog-recent").dialog( "open" );
				},
				error: function() {
					alert('Error');
				}
			});
		});
		$("#topusers a").click(function() {
			var user = this.innerHTML;
			$.ajax({
				url: 'dash-detail',
				type: 'GET',
				cache: false,
				data: { type : 'topuser', username : user },
				success: function(html) {
					$("#dialog-user").dialog({ title : "Last 10 Alerts from Username: " + user })
					$("#dialog-user tbody").html(html);
					$("#dialog-user").dialog( "open" );
				},
				error: function() {
					alert('Error');
				}
			});
		});
		setInterval("location.reload(true)", 300000);
});
</script>

</body>
</html>

