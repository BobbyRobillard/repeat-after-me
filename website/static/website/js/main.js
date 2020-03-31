var admin_email = "admin@techandmech.com";
//------------------------------------------------------------------------------
$('body').on('click', '.action-link', function(e) {
    e.stopPropagation();
    window.location.href = $(this).attr('href');
});
//------------------------------------------------------------------------------
