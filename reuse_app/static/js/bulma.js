$(document).ready(function() {
  // Check for click events on the navbar burger icon
  $(".navbar-burger").click(function() {
      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      $(".navbar-burger").toggleClass("is-active");
      $(".navbar-menu").toggleClass("is-active");
  });
});

$('.file-input').change(function() {
    let filename = '';
    if (this.files.length > 0) {
        filename = this.files[0].name;
    }
    let labels = $(this).parent().children('.file-name');
    if (labels.length > 0) {
        $(labels[0]).text(filename);
    }
});

document.addEventListener('DOMContentLoaded', () => {
  (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
    $notification = $delete.parentNode;
    $delete.addEventListener('click', () => {
      $notification.parentNode.removeChild($notification);
    });
  });
});


