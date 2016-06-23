/**
 * Created by User on 6/23/2016.
 */

$(function () {
    $("#like").on("click", function () {
       $.post("likes/", {}, function (resp) {
          $("#likes_count").append($("<pre>")).prepend("<pre>").text(resp['likes_count'])
       });
    });
});
