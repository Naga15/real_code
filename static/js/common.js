function getChart(xaxis,yaxis)
{
    var search 		= $("#search" ).val();
    if(search != '')
    {
       $('#search-form').submit()
    }
    else
    {
        $("#chart-section").html('<div class="alert alert-info">Search by Chassis ID / ESN</div>');
    }
}
function ClearForm()
{
	$('#search').val('')
	$('#search-form').submit()
}
$(document).ready(function()
{
    $("input[name='x-axis']").click(function(){
        getChart($(this).attr('value'),$("input[name='y-axis']:checked").val())
     })

    $("input[name='y-axis']").click(function(){
        getChart($("input[name='x-axis']:checked").val(),$(this).attr('value'))
    })
});

function callbackCEPDATA()
{
    alert('called')
}