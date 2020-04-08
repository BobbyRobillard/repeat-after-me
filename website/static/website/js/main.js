var admin_email = "admin@techandmech.com";
//------------------------------------------------------------------------------
// For items that direct a user somewhere. I.e: trashcan (delete), pencil (edit)
//------------------------------------------------------------------------------
$('body').on('click', '.action-link', function(e) {
    e.stopPropagation();
    window.location.href = $(this).attr('href');
});
//------------------------------------------------------------------------------
// For items that direct a user to the "save a recording" page
//------------------------------------------------------------------------------
$('.save').click(function() {
  window.location.href = "{% url 'macros:save_recording' %}";
});
//------------------------------------------------------------------------------
// Real Time Updates Bar
//------------------------------------------------------------------------------
const playModeSocket = new WebSocket(
    'ws://'
    + 'localhost:8000'
    + '/ws/macros/'
    + 'updates/'
);

playModeSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    $("#play-mode").prop('checked', data.playMode);
    $("#recording").prop('checked', data.isRecording);

};

playModeSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

setInterval(function() {
  playModeSocket.send(JSON.stringify({}));
}, 250);
//------------------------------------------------------------------------------
