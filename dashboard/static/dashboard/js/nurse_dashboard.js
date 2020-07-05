function updateQuery(){
  location.href = $(location).attr('origin') + $(location).attr('pathname') + "?" + $('#patient-search').serialize();
}

$(document).ready(function() {
  $("#patient-search").on('submit', updateQuery);
});
