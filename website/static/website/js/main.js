var admin_email = "admin@techandmech.com";
//------------------------------------------------------------------------------
// For items that direct a user somewhere. I.e: trashcan (delete), pencil (edit)
//------------------------------------------------------------------------------
$('body').on('click', '.action-link', function(e) {
    e.stopPropagation();
    window.location.href = $(this).attr('href');
});
//------------------------------------------------------------------------------
// Real Time Updates Bar
//------------------------------------------------------------------------------
const playModeSocket = new WebSocket(
    'ws://'
    + '192.168.50.201:8000'
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
//------------------------------------------------------------------------------
// Convert Hex Color to opacity
//------------------------------------------------------------------------------
function convertHex(hex, opacity){
  return 'rgba(' + parseInt(hex.slice(-6, -4), 16)
        + ',' + parseInt(hex.slice(-4, -2), 16)
        + ',' + parseInt(hex.slice(-2), 16)
        +',' + opacity + ')';
}
//------------------------------------------------------------------------------
