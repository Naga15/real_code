// This function is use to display graph in dashboard.
function dashboard(filter_search, filter_Engine_Only, X_Array, Y_Array, hovertext, I_Array, Color_Array, filter_x_axis, filter_y_axis){
    var shortvin 					= filter_search
    var filter_Engine_Only 	= filter_Engine_Only
    var annotations 				= []
    var X_Array 						= X_Array
    var Y_Array 						= Y_Array
    var TEXTS 							= hovertext
    var DID 								= I_Array
    var Color_Array 				= Color_Array
    var i;

    for (i = 0; i < X_Array.length; i++){
        color_bg = getRandomColor()
        annotations.push({
                                        x: X_Array[i],
                                        y: Y_Array[i],
                                        align: "center",
                                        arrowcolor: color_bg,
                                        arrowhead: 20,
                                        arrowsize: 1,
                                        ax: -0,
                                        ay: -90,
                                        //bgcolor: color_bg,
                                        bordercolor: color_bg,
                                        borderpad: 3,
                                        borderwidth: 2,
                                        font: {size: 13},
                                        text: TEXTS[i],
                                        textangle: 0
                                        }
                                    );
    }

    var myPlot = document.getElementById('chart-section'),
    data = [ {
				x:X_Array,
				y:Y_Array,
				DID : I_Array,
				type:'scatter',
        mode:'lines+markers',
				text: hovertext,
				marker:{color:Color_Array,size:16},
				}
			],
    layout = {

			showlegend: false,
			/*annotations: annotations,*/


		hovermode:'closest',
		autosize: true,
		width:document.getElementById("data-test").offsetWidth-100,
		height: 600,
		margin: {
			l: 50,
			r: 10,
			b: 100,
			t: 50,
			pad: 1
		},
		title: {
			text: filter_search + ' Chassis History',
		},
		xaxis: {
			title: {
			text: filter_x_axis,
			},
		},
		yaxis: {
			title: {
			text: filter_y_axis,
			}
		}
    };

    Plotly.newPlot('chart-section', data, layout,{scrollZoom: false, displayModeBar: false, editable: false})

    myPlot.on('plotly_click', function(data){
      var eventid = '';
        for(var i=0; i < data.points.length; i++)
        {
            ClickIndex = data.points[i].pointIndex;
                    eventid = data.points[i].data.DID[ClickIndex];
        }
        if(eventid)
        {
            openFormPopup(eventid, shortvin, filter_Engine_Only)
        }
    });

}

// This function is use to open popup menu.
function openFormPopup(eventid, shortvin, filter_Engine_Only){

//	$("#loaderModal").modal();
	$.ajax({
		type: 'GET',
		url: "/service/"+shortvin+"/"+eventid+"/"+filter_Engine_Only,
		success:
		function(data)
		{
			// $("#loaderModal").modal('hide');
			$('#form-data').html('')
			$('#form-data').html(data)
			$("#myModal").modal();
		},
		})
}

// This function is use to get random color.
function getRandomColor(){
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

// This function is use to print graph.
function PrintPlot(){
	printDiv('data-test');
}

// This function is use to print div.
function printDiv(divName){
	var printContents = document.getElementById(divName).innerHTML;
	var originalContents = document.body.innerHTML;
	document.body.innerHTML = printContents;
	window.print();
	document.body.innerHTML = originalContents;
}

// This function is use to Export CSV.
function ExportCSV(filter_search, filter_Engine_Only, filter_x_axis, filter_y_axis){
	var filter_search = filter_search;
	var filter_x_axis = filter_x_axis;
	var filter_y_axis = filter_y_axis;
	var filter_Engine_Only = filter_Engine_Only;
	window.location = 'export-to-csv/'+filter_search+'/'+filter_x_axis+'/'+filter_y_axis+"/"+filter_Engine_Only;
}


