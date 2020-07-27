// Search Focus on Click
$("#search_post").on("shown.bs.modal", function () {
  $("#searchOn").focus();
});

// To Like A Post, Live
$(document).on("click", ".like_a_post", function (e) {
  e.preventDefault();
  var url = $(this).attr("data-url");
  var pk = $(this).attr("pk");
  $.ajax({
    url: url,
    dataType: "html",
    success: function (data) {
      $("#footer_post_button_" + pk).html(data);
    },
  });
});

// Update a post 
$(document).on("click", ".update_a_post", function (e) {
  e.preventDefault();
  var url = $(this).attr("data-url");
  $.ajax({
    url: url,
    dataType: "html",
    success: function (data) {
      $("#update_or_create").html(data);
      $("#create_post").modal('show');
    },
  });
});

// Detail of post
$(document).on("click", ".post_detail_view", function (e) {
  e.preventDefault();
  var url = $(this).attr("data-url");
  $.ajax({
    url: url,
    dataType: "html",
    success: function (data) {
      $("#update_or_create").html(data);
      $("#create_post").modal('show');
    },
  });
});



// Infinite scroll
var infinite = new Waypoint.Infinite({
  element: $(".infinite-container")[0],
  handler: function (direction) {},
  offset: "bottom-in-view",

  onBeforePageLoad: function () {
    $(".spinner-border").show();
  },
  onAfterPageLoad: function () {
    $(".spinner-border").hide();
  },
});

//   $(document).ready(function() {
//     $("#content").hide();
//     $("#buttonSubmit").click(function(e) {
//       e.preventDefault();
//       var form = $(this).closest("form");
//       $.ajax({
//         type: "POST",
//         url: "{% url 'ajax-create' %}",
//         data: form.serialize(),
//         dataType: "json",
//         success: function(data) {
//           if (data.created) {
//             alert(data.created);
//           }
//           if (data.notCreated) {
//             alert(data.notCreated);
//           }
//         }
//       });
//     });
//   });

// var name = $("#id_name").val();
// var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
