$(document).ready(function(){

    $.ajax({
        method:"post",
        url:"/showall_contacts",
        data:{},
        success:function(res){
            $("#place_for_contacts").html(res);
        }
    })


    $.ajax({
        method:"post",
        url:"/showall_notifications",
        data:{},
        success:function(res){
            $("#place_for_notifications").html(res);
        }
    })

    var callStarted = false;
    var calling_id;


    var profile_shown = false;
    $('body').on("click",".profile_show", function () {

        
        if (profile_shown === true){
                $('#profile_change').fadeOut(250, function(){
                    $('.profile_show').text('⮞')
                    $('#profile_change').hide();
                    $('.profile_hide').fadeIn(250);
                })
                profile_shown = false;
            } else {
                $('.profile_hide').fadeOut(250, function(){
                    $('.profile_show').text('⮜')
                    $('.profile_hide').hide();
                    $('#profile_change').fadeIn(250);
                })
                profile_shown = true;
            }
    });

    $('body').on("click","#save_changes", function () {
        var username = $('#change_username').val()
        if (username !== ''){
            $.ajax({
                method:"post",
                url:"/edit_profile",
                data:{username:username},
                success:function(data){
                    $("#username_display").text(data.username);
                    $('#change_username').attr("placeholder", data.username)
                    $('#change_username').val('')
                }
            })
        }
    })

    $('body').on("click",".notifyButton", function () {
        contact_id = $(this).attr('contact_id');
        var timestamp = $('#timestamp'+contact_id).children("option:selected").val();
        $('#timestamp'+contact_id).prop('selectedIndex',0);
        $.ajax({
            method:"post",
            url:"/createNotification",
            data:{contact_id:contact_id, timestamp:timestamp},
            success:function(res){
                $("#place_for_notifications").html(res);
            }
        })
    });

    $('body').on("click",".deleteNotification", function () {
        notification_id = $(this).attr('notification_id');
        $('#notificationSearch').val('');
        $.ajax({
            method:"post",
            url:"/deleteNotification",
            data:{notification_id:notification_id},
            success:function(res){
                $("#place_for_notifications").html(res);
            }
        })
    });

    $('body').on("click",".confirmNotification", function () {
        notification_id = $(this).attr('notification_id');
        $('#notificationSearch').val('');
        $.ajax({
            method:"post",
            url:"/confirmNotification",
            data:{notification_id:notification_id},
            success:function(res){
                $("#place_for_notifications").html(res);
            }
        })
    });

    $('body').on("click",".addContact", function () {
        contact_id = $(this).attr('contact_id');
        $('#contactSearch').val('')
        $.ajax({
            method:"post",
            url:"/addContact",
            data:{contact_id:contact_id},
            success:function(res){
                $("#place_for_contacts").html(res);
            }
        })
    });

    $('body').on("click",".deleteContact", function () {
        contact_id = $(this).attr('contact_id');
        $('#contactSearch').val('')
        $.ajax({
            method:"post",
            url:"/deleteContact",
            data:{contact_id:contact_id},
            success:function(res){
                $("#place_for_contacts").html(res);
            }
        })
    });

    var muted = false
    $('body').on("click",".muteCall", function () {
        contact_id = $(this).attr('contact_id');
        if (muted === true){
            $('#mutecall'+contact_id).css('opacity', '0.3') 
            muted = false
        } else{
            $('#mutecall'+contact_id).css('opacity', '1') 
            muted = true;
        }
    });

    $('body').on("click",".startCall", function () {

        contact_id = $(this).attr('contact_id');
        if(callStarted === true){
            if(contact_id === calling_id){
                $('#callSection'+calling_id).fadeOut(200 , function(){
                    $('#call'+calling_id).attr("src","/static/call.png");
                    $('#call'+calling_id).css("margin-right", "10px");
                    $('#contactRow'+contact_id).css("background-color","rgb(116, 103, 128)");
                    callStarted = false;
                    $('#stopwatch'+calling_id).hide()
                    $('#mutecall'+calling_id).hide();
                    muted = false
                    $('#notify'+calling_id).show();
                    $('#delete'+calling_id).show();
                    $('#timestamp'+contact_id).show()
                    stopTimer();
                });
                $('#callSection'+calling_id).fadeIn(200);
                $('#contactSearch').prop('disabled', false)
            }
        } else {
            calling_id = $(this).attr('contact_id');
            $('#callSection'+calling_id).fadeOut(200, function(){
                callStarted = true;
                startTimer()
                $('#call'+calling_id).attr("src","/static/endcall.png");
                $('#call'+calling_id).css("margin-right", "40px")
                $('#contactRow'+contact_id).css("background-color","rgb(160, 150, 170)");
                $('#mutecall'+calling_id).show();
                $('#stopwatch'+calling_id).show();
                $('#mutecall'+contact_id).css('opacity', '0.3');
                $('#notify'+calling_id).hide();
                $('#timestamp'+contact_id).hide()
                $('#delete'+calling_id).hide();
            });
            $('#callSection'+calling_id).fadeIn(200);
            $('#contactSearch').prop('disabled', true)
           
        }
        });

        $('#contactSearch').on('input',function(e){
            var searchboxcontactText = $('#contactSearch').val()
            if(searchboxcontactText !== ""){
                $.ajax({
                    method:"post",
                    url:"/filter_contacts",
                    data:{text:searchboxcontactText},
                    success:function(res){
                        $("#place_for_contacts").html(res);
                    }
                })
            } else{
                $.ajax({
                    method:"post",
                    url:"/showall_contacts",
                    data:{},
                    success:function(res){
                        $("#place_for_contacts").html(res);
                    }
                })
            }
        })


        $('#notificationSearch').on('input',function(e){
            var searchboxcontactText = $('#notificationSearch').val()
            if(searchboxcontactText !== ""){
                $.ajax({
                    method:"post",
                    url:"/filter_notifications",
                    data:{text:searchboxcontactText},
                    success:function(res){
                        $("#place_for_notifications").html(res);
                    }
                })
            } else{
                $.ajax({
                    method:"post",
                    url:"/showall_notifications",
                    data:{},
                    success:function(res){
                        $("#place_for_notifications").html(res);
                    }
                })
            }
        })

window.seconds = 0;
window.minutes = 0;
window.hours = 0;

function startTimer() {
	window.action = setInterval(increment,1000);
}

function stopTimer() {
    clearInterval(action);  
    seconds = -1;
    minutes = 0;
    hours = 0; 
    increment();  
}
function zeroPad(time) {
  var numZeropad = time + '';
  while(numZeropad.length < 2) {
      numZeropad = "0" + numZeropad;
  }
  return numZeropad;
}
function increment() {
	seconds++;
  if (seconds === 60) {
       minutes++;
       seconds = 0;
  }
  if (minutes === 60){
    hours++;
    minutes = 0;
  }

  document.getElementById("stopwatch"+calling_id).innerHTML = zeroPad(hours) + ":" + zeroPad(minutes) + ":" + zeroPad(seconds);
}

});