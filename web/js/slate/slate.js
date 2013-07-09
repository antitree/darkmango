var slate = {};

slate = function ()
{
	var pub = {};
	var self = {};
	var chartColors = ['#BC4848','#FF9900','#555','#777','#999','#bbb','#ccc','#eee'];

	pub.init = function ()
	{		
		$('#search').find ('input').live ('click' , function () { $(this).val ('') });
		$("form.form select, form.form input:checkbox, form.form input:radio, form.form input:file").uniform();
				
		$('*[rel=datatable]').dataTable ();
		
		$("*[rel=tooltip]").tipsy ({ gravity: 's' });
		$("*[rel=facebox]").facebox ();
		
		$('table.stats').each(function() 
		{		
			var chartType = '';
			
			if ( $(this).attr('title') ) 
			{ 
				chartType = $(this).attr('title'); 				
			}
			else 
			{ 
				chartType = 'area'; 
			}
			
			var chart_width = $(this).parents ('.portlet').width () * .85;
					
			$(this).hide ().visualize({		
				type: chartType,	// 'bar', 'area', 'pie', 'line'
				width: chart_width,
				height: '240px',
				colors: chartColors
			});				
		});
	}
	
	return pub;
	
}();
