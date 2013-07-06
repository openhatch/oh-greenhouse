/* depends on:
	jquery core 1.4.2 or later <http://jquery.com>
*/

/* jQuery settings */
jQuery.ajaxSettings.traditional = true; /* for compatibility with Django */

$(document).ready(function() {

    // Hide success message after delay
    $("#messages").delay(3200).fadeOut(300);

    // Highligh table rows
    $('tr').mouseover(function(){
        $(this).addClass('highlight');
    }).mouseout(function(){
        $(this).removeClass('highlight');
    });

});
