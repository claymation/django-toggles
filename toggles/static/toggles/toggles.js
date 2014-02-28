(function ($) {
  // FIXME - the buttons have probably already been initialized with $('.btn').button()
  // $("button.django-toggle").button();

  $(document).on("click", "button.django-toggle", function () {
    var $btn = $(this)
      , active = $btn.data("active")
      , url = $btn.data("url");

    $btn.button("loading");

    $.ajax({
      type: active ? "DELETE" : "PUT",
      url: url
    })
      .success(function () {
        active = !active;
        $btn.data("active", active);
        $btn.button(active ? "on" : "off");
        $btn.button("toggle");
      })
      .fail(function () {
        // FIXME - show the user that something went wrong
        $btn.button("reset");
      });
  });
}(jQuery));
