
function getChart(xaxis,yaxis)
{
    var search 		= $("#search" ).val();
    var formData = {
        'x-axis': xaxis,
        'y-axis': yaxis,
        'search': search,
        'csrfmiddlewaretoken': jQuery("input[name='csrfmiddlewaretoken']").val()
    };
    $.ajax({
    type: 'POST',
    url: "/chart",
    data: formData,
    contentType: 'application/x-www-form-urlencoded; charset=UTF-8',
    success:
    function(data)
    {
        $("#chart-section").html(data);
    },
    })
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


    