var admin_email = "admin@techandmech.com";
//------------------------------------------------------------------------------
// For items that direct a user somewhere. I.e: trashcan (delete), pencil (edit)
//------------------------------------------------------------------------------
$('body').on('click', '.action-link', function(e) {
    e.stopPropagation();
    window.location.href = $(this).attr('href');
});
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
