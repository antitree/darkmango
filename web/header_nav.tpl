%import sys
%from src.bottle import request
%user = request.get_cookie("loggedin", secret='sm2345-45634')

<div id="wrapper" class="clearfix">
	
	<div id="top">
		<div id="header">
			<h1><a href="/">SpicyMango</a></h1>
			
			<div id="info">
				<p>
					Logged in as {{user}}
					<br />
					<a href="/login?action=logout">Logout</a>
				</p>
				
				<img src="./images/avatar.jpg" alt="avatar" />
			</div> <!-- #info -->
					
		</div> <!-- #header -->	
		
		
		<div id="nav">	
	
			<ul class="mega-container mega-grey">
	
				<li class="mega">
					<a href="/" class="mega-link">Dashboard</a>	
				</li>
		
				<li class="mega">
					<a href="/alerts" class="mega-link">Alerts</a>	
				</li>

				<li class="mega">
					<a href="/events" class="mega-link">Raw Events</a>	
				</li>

				<li class="mega mega-current">				
					<a href="javascript:;" class="mega-tab"><font style="color: orange;">Settings</font></a>
					<div class="mega-content mega-menu ">
						<ul>
							<li><a href="/set-password">Change Password</a></li>
							<li><a href="/set-keywords">Keywords</a></li>			
						</ul>
					</div>						
				</li>
				
			</ul>
		</div> <!-- #nav -->
	</div> <!-- #top -->
