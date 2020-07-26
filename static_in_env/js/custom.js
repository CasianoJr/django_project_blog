$("#search_post").on("shown.bs.modal", function () {
  $("#searchOn").focus();
});


// To Like A Post
$(document).on("click", ".like_a_post", function (e) {
  e.preventDefault();
  url = $(this).attr("data-url");
  pk = $(this).attr("pk");
  $.ajax({
    url: url,
    dataType: "html",
    success: function (data) {
      $("#footer_post_button_" + pk).html(data);
    },
  });
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
// var category = $("#id_category").val();
// var stock = $("#id_stock").val();
// var remark = $("#id_remark").val();
// var csrf_token = $("input[name=csrfmiddlewaretoken]").val();
