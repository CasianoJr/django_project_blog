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
      $("#reusable_modal_content").html(data);
      $("#reusable_modal").modal("show");
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
      $("#reusable_modal_content").html(data);
      $("#reusable_modal").modal("show");
    },
  });
});
$(document).on("click", ".comment_a_post", function (e) {
  e.preventDefault();
  var url = $(this).attr("data-url");
  $.ajax({
    url: url,
    dataType: "html",
    success: function (data) {
      $("#reusable_modal_content").html(data);
      $("#reusable_modal").modal("show").delay();
      $("#reusable_modal").on("shown.bs.modal", function () {
        $("#comment_input").focus();
      });
    },
  });
});

// Infinite scroll

$(document).ready(function () {
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
});

// Image upload
function previewFiles() {
  var preview = document.querySelector("#preview");
  var files = document.querySelector("input[type=file]").files;
  function readAndPreview(file) {
    if (/\.(jpe?g|png|gif)$/i.test(file.name)) {
      var reader = new FileReader();
      reader.addEventListener(
        "load",
        function () {
          var image = new Image();
          image.className = "m-2";
          image.height = 100;
          image.title = file.name;
          image.src = this.result;
          preview.appendChild(image);
        },
        false
      );
      reader.readAsDataURL(file);
    }
  }
  if (files) {
    if (files.length > 5) {
      alert("We suggest you only upload 5 photos below");
    }
    [].forEach.call(files, readAndPreview);
  }
}

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

// var name = $("#id_name").val();
// var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
