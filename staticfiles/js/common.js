function getBrandInfo(name)
{
    jQuery('#brand-btn-txt').text(name)
    jQuery("#branch-chart").html('');
    jQuery("#branch-chart").html('<div style="margin-left: 42%;margin-top: 35% "><div class="loader"></div></div>');
    jQuery.ajax({
        url:"/brand/info/"+name,
        type: "GET",
        success: function(data)
        {
            jQuery("#branch-chart").html(data);
        }
    });
}
function QuestionType(id)
{
    if(id == 1 || id == 2 || id == 4)
    {
        jQuery("#mcq-file").show();
        jQuery("#otn-file").hide();
        jQuery("#ott-file").hide();
        jQuery("#slider-file").hide();
    }
    else if(id == 5)
    {
        jQuery("#mcq-file").hide();
        jQuery("#otn-file").show();
        jQuery("#ott-file").hide();
        jQuery("#slider-file").hide();
    }
    else if(id == 6)
    {
        jQuery("#mcq-file").hide();
        jQuery("#otn-file").hide();
        jQuery("#ott-file").show();
        jQuery("#slider-file").hide();
    }
    else
    {
        jQuery("#mcq-file").hide();
        jQuery("#otn-file").hide();
        jQuery("#ott-file").hide();
        jQuery("#slider-file").show();
    }
    //create validation
    Validation(id)
}

function Validation(id)
{
    var Opt =  jQuery('#id_NoOfOpt').val()
    if(Opt == '')
    {
        Opt = 1
    }
    
    if(id == 1 || id == 2 || id == 4)
    {
        for (i = 1; i <= Opt; i++) 
        { 
            jQuery('#ans_val_'+i).attr("required", true);
            jQuery('#ans_lbl_'+i).attr("required", true);
        }

         //removed
         jQuery('#MinVal').attr("required", false);
         jQuery('#MaxVal').attr("required", false);
         jQuery('#Step').attr("required", false);
         jQuery('#int_MinVal').attr("required", false);
         jQuery('#int_MaxVal').attr("required", false);
         jQuery('#MaxLength').attr("required", false);
    }
    else if(id == 5)
    {
        //add
        jQuery('#int_MinVal').attr("required", true);
        jQuery('#int_MaxVal').attr("required", true);

        //removed
        jQuery('#MinVal').attr("required", false);
        jQuery('#MaxVal').attr("required", false);
        jQuery('#Step').attr("required", false);
        jQuery('#MaxLength').attr("required", false);
        for (i = 1; i <= Opt; i++) 
         { 
            jQuery('#ans_val_'+i).attr("required", false);
            jQuery('#ans_lbl_'+i).attr("required", false);
         }

    }
    else if(id == 6)
    {
         //add
         jQuery('#MaxLength').attr("required", true);
         
         //removed
         jQuery('#MinVal').attr("required", false);
         jQuery('#MaxVal').attr("required", false);
         jQuery('#Step').attr("required", false);
         jQuery('#int_MinVal').attr("required", false);
         jQuery('#int_MaxVal').attr("required", false);
         for (i = 1; i <= Opt; i++) 
         { 
            jQuery('#ans_val_'+i).attr("required", false);
            jQuery('#ans_lbl_'+i).attr("required", false);
         }
    }
    else
    {
         //add
         jQuery('#MinVal').attr("required", true);
         jQuery('#MaxVal').attr("required", true);
         jQuery('#Step').attr("required", true);
 
         //removed
         jQuery('#int_MinVal').attr("required", false);
         jQuery('#int_MaxVal').attr("required", false);
         jQuery('#MaxLength').attr("required", false);
         for (i = 1; i <= Opt; i++) 
         { 
            jQuery('#ans_val_'+i).attr("required", false);
            jQuery('#ans_lbl_'+i).attr("required", false);
         }
    }
}

function AddTXT()
{
    var counterPlus  = jQuery("#id_NoOfOpt").val();
    if(counterPlus == "")
    {
        counterPlus = 2
    }
    else
    {
        counterPlus++;
    }   
    var newTextBoxDiv = jQuery(document.createElement('div')).attr("id", 'OptionDiv' + counterPlus);
    newTextBoxDiv.after().html('<div class="row"><div class="col-lg-2"><div class="form-group"><label class="form-label">Answer '+counterPlus+' <span class="form-required">*</span> &nbsp;&nbsp;<i class="fe fe-help-circle" data-toggle="tooltip" title="These are answer options from prior questions that may be of help to you in creating an appropriate answer for this question"></i></label></div></div><div class="col-lg-3"><div class="form-group "><input type="text" name="ans_lbl_'+counterPlus+'" id="ans_lbl_'+counterPlus+'" placeholder="Enter Answer Key" class="form-control" required></div></div><div class="col-lg-3"><div class="form-group "><input type="text" name="ans_val_'+counterPlus+'" id="ans_val_'+counterPlus+'" placeholder="Enter Answer Value" class="form-control" required></div></div><div class="col-lg-1"><div class="form-group "><button type="button" onclick="removeTXT('+counterPlus+')" class="btn btn-icon btn-primary btn-danger"><i class="fe fe-trash"></i></button></div></div></div>');
    newTextBoxDiv.appendTo("#mcq-options");
    jQuery("#id_NoOfOpt").val(counterPlus);
}

function removeTXT(id)
{
    var NoOfOpt = jQuery("#id_NoOfOpt").val();
    jQuery('#OptionDiv' + id).remove();
    NoOfOpt--;
    jQuery("#id_NoOfOpt").val(NoOfOpt); 
}


function getMedia()
{
    if (jQuery("#id_QuestionIsMedia").prop('checked') == true)
    {
        jQuery(".field-QuestionMediaType").show();
        jQuery('.field-QuestionMediaType input[type="radio"]').each(function (index) 
        {
            var qmTypeId = jQuery(this).attr("id"); 
            jQuery('#'+qmTypeId).attr("required", true);
        });
    }
    else
    {
        jQuery(".field-QuestionMediaType").hide();
        jQuery(".field-QuestionMedia").hide();
        jQuery(".field-QuestionMediaAudio").hide();
        jQuery(".field-QuestionMediaVideo").hide();
        jQuery('.field-QuestionMediaType input[type="radio"]').each(function (index) 
        {
            var qmTypeId = jQuery(this).attr("id"); 
            jQuery('#'+qmTypeId).attr("required", false);
        });
        jQuery('#id_QuestionMedia').attr("required", false);
        jQuery('#id_QuestionMediaVideo').attr("required", false);
        jQuery('#id_QuestionMediaAudio').attr("required", false);
    }
}

function getMediaType(mtype,flag)
{
    if (flag == 'True' && mtype == 'Image') 
    {
        jQuery(".field-QuestionMedia").show();
        jQuery(".field-QuestionMediaAudio").hide();
        jQuery(".field-QuestionMediaVideo").hide();
        //jQuery('#id_QuestionMedia').attr("required", true);
        jQuery('#id_QuestionMediaVideo').attr("required", false);
        jQuery('#id_QuestionMediaAudio').attr("required", false); 
    }
    else if(flag == 'True' && mtype == 'Video')
    {
        jQuery(".field-QuestionMedia").hide();
        jQuery(".field-QuestionMediaAudio").hide();
        jQuery(".field-QuestionMediaVideo").show();
        jQuery('#id_QuestionMedia').attr("required", false);
        jQuery('#id_QuestionMediaVideo').attr("required", true);
        jQuery('#id_QuestionMediaAudio').attr("required", false);  
    }
    else if(flag == 'True' && mtype == 'Audio')
    {
        jQuery(".field-QuestionMedia").hide();
        jQuery(".field-QuestionMediaAudio").show();
        jQuery(".field-QuestionMediaVideo").hide();
        jQuery('#id_QuestionMedia').attr("required", false);
        jQuery('#id_QuestionMediaVideo').attr("required", false);
        //jQuery('#id_QuestionMediaAudio').attr("required", true);
    }
    else
    {
        jQuery(".field-QuestionMedia").hide();
        jQuery(".field-QuestionMediaAudio").hide();
        jQuery(".field-QuestionMediaVideo").hide();
        jQuery('#id_QuestionMedia').attr("required", false);
        jQuery('#id_QuestionMediaVideo').attr("required", false);
        jQuery('#id_QuestionMediaAudio').attr("required", false);
    }
}   

function AddParentSub(mid,id)
{   
    jQuery(".sidebar-menu li a").removeClass("sub-ques-active");

    if(jQuery("#parent_" + id).length == 0) 
    {
        var ulHtml = '<ul id="parent_'+id+'"><li><a id="parent_sub_'+mid+'_'+id+'" class="text-inherit sub-ques-active">Sub Question</a></li></ul>';
        jQuery("#li_"+id).append(ulHtml);
    }
    else
    {
        if(jQuery('#parent_sub_'+mid+'_'+id).length == 0) 
        {
            var ulHtml = '<li><a id="parent_sub_'+mid+'_'+id+'" class="text-inherit sub-ques-active">Sub Question</a></li>';
            jQuery("#parent_"+id).append(ulHtml);
        }
        else
        {
            jQuery('#parent_sub_'+mid+'_'+id).addClass("sub-ques-active");
        }
    }
    
    jQuery.ajax({
        url:"/question/add-sub-qus/"+mid+"/"+id,
        type: "GET",
        success: function(data)
        {
            jQuery("#subqus").html(data);

            /* QuestionType click event*/
            jQuery('.field-QuestionType input[type="radio"]').click(function () 
            {
                if (this.checked == true) 
                {
                    QuestionType(jQuery(this).attr("value"))
                }
            });

            /* add ans for question type*/
            jQuery("#addmoreoptions").click(function()
            {
                AddTXT()
                
            })

            
            /* Display Flag click event*/
            jQuery('#id_DisplayFlag_0').click(function () 
            {
                jQuery('#DisplayFlag-section').hide()
                jQuery('#id_ConditionType').attr("required", false);
                jQuery('#id_ConditionTypeValue').attr("required", false);

            });

            /* Display click event*/
            jQuery('#id_DisplayFlag_1').click(function () 
            {
                jQuery('#DisplayFlag-section').show()
                jQuery('#id_ConditionType').attr("required", true);
                jQuery('#id_ConditionTypeValue').attr("required", true);
        
            });

            //Click Media
            jQuery('#id_QuestionIsMedia').click(function () 
            {
                getMedia()
            });
            /* click on media type*/
            jQuery('.chkmtype').click(function () 
            {
                if (this.checked == true)
                {
                    getMediaType(jQuery(this).attr("value"),'True')
                }
                else
                {
                    getMediaType(jQuery(this).attr("value"),'False')
                }
            });

        }
    });
}

function EditSub(mid,id)
{
    
    jQuery(".sidebar-menu li a").removeClass("sub-ques-active");
    
    jQuery('#a_'+id).addClass("sub-ques-active");

    jQuery.ajax({
        url:"/question/edit-sub-qus/"+mid+"/"+id,
        type: "GET",
        success: function(data)
        {
            jQuery("#subqus").html(data);

            /* QuestionType checked event*/
            jQuery('.field-QuestionType input[type="radio"]:checked').each(function (index) 
            {
                var qType = jQuery(this).attr("value"); 
                QuestionType(qType)
            });

            /* QuestionType click event*/
            jQuery('.field-QuestionType input[type="radio"]').click(function () 
            {
                if (this.checked == true) 
                {
                    QuestionType(jQuery(this).attr("value"))
                }
            });

            /* add ans for question type*/
            jQuery("#addmoreoptions").click(function()
            {
                AddTXT()
                
            })

            if(jQuery('#id_DisplayFlag_0').is(':checked'))
            {
                jQuery('#DisplayFlag-section').hide()
                jQuery('#id_ConditionType').attr("required", false);
                jQuery('#id_ConditionTypeValue').attr("required", false);
            }
            else
            {
                jQuery('#DisplayFlag-section').show()
                jQuery('#id_ConditionType').attr("required", true);
                jQuery('#id_ConditionTypeValue').attr("required", true);
            }
            /* Display Flag click event*/
            jQuery('#id_DisplayFlag_0').click(function () 
            {
                jQuery('#DisplayFlag-section').hide()
                jQuery('#id_ConditionType').attr("required", false);
                jQuery('#id_ConditionTypeValue').attr("required", false);

            });

            /* Display click event*/
            jQuery('#id_DisplayFlag_1').click(function () 
            {
                jQuery('#DisplayFlag-section').show()
                jQuery('#id_ConditionType').attr("required", true);
                jQuery('#id_ConditionTypeValue').attr("required", true);
        
            });

             /* Question Media*/
            if (jQuery("#id_QuestionIsMedia").is(":checked")) 
            {
                getMedia()
            }    
            jQuery('.field-QuestionMediaType input[type="radio"]:checked').each(function (index) 
            {
                getMediaType(jQuery(this).attr("value"),'True') 
            });

            //Click Media
            jQuery('#id_QuestionIsMedia').click(function () 
            {
                getMedia()
            });
            /* click on media type*/
            jQuery('.chkmtype').click(function () 
            {
                if (this.checked == true)
                {
                    getMediaType(jQuery(this).attr("value"),'True')
                }
                else
                {
                    getMediaType(jQuery(this).attr("value"),'False')
                }
            });

        }
    });
}

function split( val ) 
{
    return val.split( /,\s*/ );
}
    function extractLast( term ) 
{
    return split( term ).pop();
}

function getNotificationCount()
{
    $.ajax({
    url: "/client/notification/count?&id=" + (new Date()).getTime(),
    success:
    function(res)
    {
        if(res != '0')
        {
            jQuery('.nav-unread').show()
        }
    },
    })
}

function getNotificationList()
{
    jQuery('#notification').html('')
    $.ajax({
    url: "/client/notification/list?&id=" + (new Date()).getTime(),
    success:
    function(res)
    {
        if(res != 'fail')
        {
            jQuery('.nav-unread').hide()
            jQuery('#notification').html(res)
        }
    },
    })
}


jQuery(document).ready(function()
{
    var NoOfSubQus          = jQuery("#id_NoOfSubQus").val();
    
    /* QuestionType checked event*/
    jQuery('.field-QuestionType input[type="radio"]:checked').each(function (index) 
    {
        var qType = jQuery(this).attr("value"); 
        QuestionType(qType)
    });

    
    /* Question Media*/
    if (jQuery("#id_QuestionIsMedia").is(":checked")) 
    {
        getMedia()
    }    
    jQuery('.field-QuestionMediaType input[type="radio"]:checked').each(function (index) 
    {
        getMediaType(jQuery(this).attr("value"),'True') 
    });


     /* QuestionType click event*/
     jQuery('.field-QuestionType input[type="radio"]').click(function () 
     {
         if (this.checked == true) 
         {
             QuestionType(jQuery(this).attr("value"))
         }
     });

    /* add ans for question type*/
    jQuery("#addmoreoptions").click(function()
    {
        AddTXT()

    })

    //Click Media
    jQuery('#id_QuestionIsMedia').click(function () 
    {
        getMedia()
    });
    /* click on -media type*/
    jQuery('.chkmtype').click(function () 
    {
        if (this.checked == true)
        {
            getMediaType(jQuery(this).attr("value"),'True')
        }
        else
        {
            getMediaType(jQuery(this).attr("value"),'False')
        }
    });

    jQuery('.nav-link').click(function () 
    {
        getNotificationList()
    });

    /*setInterval(function (){ getNotificationCount();}, 15000);*/

});


    