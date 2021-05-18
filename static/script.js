// Gets Bot response and generate new div.

// $( "#buttonInput" ).removeClass( "send_btn_enabled" );

function formatAMPM(date) {
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var ampm = hours >= 12 ? 'pm' : 'am';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  var strTime = 'Today, '+ hours + ':' + minutes + ' ' + ampm;
  return strTime;
}

$( document ).ready(function() {
    var date_time = formatAMPM(new Date);
    var src = "{{ url_for('static', filename='robot2.jpeg')}}";
    var botHtml = '<div class="d-flex justify-content-start mb-4"> <div class="msg_cotainer"> Hello! I am your weather assistant. <span class="msg_time">'+ date_time +'</span> </div> </div>';
    $("#chatbox").append(botHtml);
});


function getBotResponse(){
    var rawText = $("#textInput").val();
    if (rawText){
        var date_time = formatAMPM(new Date);
        // $( "#buttonInput" ).addClass( "send_btn_enabled" );
        var userHtml = '<div class="d-flex justify-content-end mb-4"> <div class="msg_cotainer_send">' +rawText+ '<span class="msg_time_send">'+ date_time +'</span> </div> </div>';
        $("#textInput").val("");
        $("#chatbox").append(userHtml);
        // document.getElementById('userInput').scrollHeight;
        $.get("/get", {msg:rawText }).done(function(data) {
            var botHtml = '<div class="d-flex justify-content-start mb-4"> <div class="msg_cotainer">' + data +' <span class="msg_time">8:40 AM, Today</span> </div> </div>';
            $("#chatbox").append(botHtml);
            scrollBottom();
        });
    }
}

function scrollBottom(){
    var element = $("#chatbox")[0];
    var element_height = ($("#chatbox")[0].scrollHeight);
    element.scrollTo(0, element_height);
}

$("#textInput").keypress(function(e) {
    if(e.which == 13) {
        getBotResponse();

    }
});

$("#buttonInput").click(function() {
    getBotResponse();
})
