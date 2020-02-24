$(document).ready(function () {
  setTimeout(function () {
    $(".check").attr("class", "check check-complete");
    $(".fill").attr("class", "fill fill-complete");
  }, 5000);

  setTimeout(function () {
    $(".check").attr("class", "check check-complete success");
    $(".fill").attr("class", "fill fill-complete success");
    $(".path").attr("class", "path path-complete");
  }, 6000);
});

$(function () 
{
  $('#submitButton').click(function () 
  {
    $.ajax({
      url: '/post',
      data: $('form').serialize(),
      type: 'POST',
      success: function (response) {
        console.log(response);
      },
      error: function (error) {
        console.log(error);
      }
    });
  });
});