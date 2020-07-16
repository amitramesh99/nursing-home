function updateQuery(){
  location.href = $(location).attr('origin') + $(location).attr('pathname') + "?" + $('#patient-search').serialize();
}

$(document).ready(function() {
  $("#patient-search").on('submit', updateQuery);
});

document.getElementById('medication').onclick = function() {
    // access properties using this keyword
    if ( this.checked ) {
        // if checked ...
        alert( this.value );
        
    } else {
        // if not checked ...
    }
};
