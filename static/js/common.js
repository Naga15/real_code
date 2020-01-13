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

// This slot is use to hide sidebar when sidebar toggle is click.
$('#sidebarToggle').click(function(){
  $('#text-vehc').hide();
});
$('#vinfo').on('hidden.bs.collapse', function () {
    // do something…
})
$('#vinfo').on('shown.bs.collapse', function () {
    $('#text-vehc').show();
    // do something…
})

//  This function is use to download PDF.
function downloadPDF(filter_search){
    var HTML_Width = $("#data-test").width();
    var HTML_Height = $("#data-test").height();
    var top_left_margin = 15;
    var PDF_Width = HTML_Width+(top_left_margin*2);
    var PDF_Height = (PDF_Width*1.5)+(top_left_margin*2);
    var canvas_image_width = HTML_Width;
    var canvas_image_height = HTML_Height;
    var totalPDFPages = Math.ceil(HTML_Height/PDF_Height)-1;
    html2canvas($("#data-test")[0],{allowTaint:true}).then(function(canvas){
          canvas.getContext('2d');
          //console.log(canvas.height+"  "+canvas.width);
          var imgData = canvas.toDataURL("image/jpeg", 1.0);
          var pdf = new jsPDF('p', 'pt',  [PDF_Width, PDF_Height]);
          pdf.addImage(imgData, 'JPG', top_left_margin, top_left_margin,canvas_image_width,canvas_image_height);
          for (var i = 1; i <= totalPDFPages; i++)
          {
            pdf.addPage(PDF_Width, PDF_Height);
            pdf.addImage(imgData, 'JPG', top_left_margin, -(PDF_Height*i)+(top_left_margin*4),canvas_image_width,canvas_image_height);
          }
          pdf.save(filter_search + "-Chassis-History.pdf");
          });
}
