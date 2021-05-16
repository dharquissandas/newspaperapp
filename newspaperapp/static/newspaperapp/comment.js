$.ajaxSetup({
    headers: { "X-CSRFToken": $("input[name='csrfmiddlewaretoken']").val()}
});

$("#submitComment").click(function(){
    var data = $(".postComment").serialize()
    data = data + "&article=" + $(this).data('id')
    $.ajax({
        url: '/newspaperapp/addcomment/',
        type: 'POST',
        data: data,
        success: function (response) {
            console.log(response)
            $(".commentlist").append('<div class="comments card mb-1" id="comment'+response.comment.id+'" data-id="'+response.comment.id+'">'+
            '<div class="card-body">'+
            '<h6 class="card-subtitle mb-2 text-muted">'+response.comment.commenter+'</h6>'+
            '<p class="card-text body">'+response.comment.body+'</p>'+
            '<button data-id="'+response.comment.id+'" class="btn btn-info commentbutton">Reply</button>'+
            '<button data-id="'+response.comment.id+'" class="btn btn-warning editbutton ml-1">Edit</button>'+
            '<button data-id="'+response.comment.id+'" class="btn btn-danger deletebutton ml-1">Delete</button>'+
            '<div style="display: none;" class="mx-4" id="subcommentform'+response.comment.id+'">'+
            '<hr>'+
            '<form class="postSubComment" id="postSubComment'+response.comment.id+'" method="POST">'+
            '<div class="form-group">'+
            '<label for="subcomment">Reply:</label>'+
            '<textarea class="form-control" id="subcomment" name="subcomment" rows="3"></textarea>'+
            '</div>'+
            '<button type="button" class="btn btn-info" id="submitSubComment" data-id="'+response.comment.id+'">Reply</button>'+
            '</form>'+
            '</div>'+
            '<div style="display: none;" class="mx-4" id="editcommentform'+response.comment.id+'">'+
            '<hr>'+
            '<form class="postEditComment" id="postEditComment'+response.comment.id+'" method="POST">'+
            '<div class="form-group">'+
            '<label for="editcomment">Edit:</label>'+
            '<textarea class="form-control" id="editcomment" name="editcomment" rows="3">'+response.comment.body+'</textarea>'+
            '</div>'+
            '<button type="button" class="btn btn-warning" id="submitEdit" data-id="'+response.comment.id+'">Edit</button>'+
            '</form>'+
            '</div>'+
            '<div id="subcomments'+response.comment.id+'">'+
            '</div></div></div>')
            $("#id_body").val('');
        }
    })
})

$(".commentlist").on('click', '.deletebutton', function () {
    var id = $(this).data('id')
    $.ajax({
        type: 'DELETE',
        url: '/newspaperapp/deletecomment/'+ id +'/',
        success: function(){
            $("#comment" + id).remove()
        }
    })
})

$(".commentlist").on('click', '.editbutton', function () {
    console.log("hi")
    var id = $(this).data('id')
    $("#editcommentform"+id).show()
    $("#subcommentform"+id).hide()
})


$('.commentlist').on('click', '.commentbutton', function(event){
    var id = $(this).data('id')
    console.log("ehy?")
    $("#subcommentform"+id).show()
    $("#editcommentform"+id).hide()
})

$(".commentlist").on('click', '#submitSubComment', function () {
    var id = $(this).data('id')
    var data = $("#postSubComment"+id).serialize()
    data = data + "&comment=" + id
    console.log(data)
    $.ajax({
        url: '/newspaperapp/addsubcomment/',
        type: 'POST',
        data: data,
        success: function (response) {
            $("#subcomments"+id).append(
                '<hr>'+
                '<div class="card subcomment ml-5 mb-1" id="subcomment'+ response.comment.id +'" data-id="'+ response.comment.id +'">'+
                '<div class="card-body">'+
                '<h6 class="card-subtitle mb-2 text-muted">'+response.comment.subcommenter+'</h6>'+
                '<p class="card-text body">'+ response.comment.body +'</p>'+
                '<button type="button" class="btn btn-danger deletesubbutton" data-id="'+response.comment.id+'">Delete</button>'+
                '</div></div>')
            $("#postSubComment"+id)[0].reset();
            $("#subcommentform"+id).hide()
        }
    })	
})

$(".commentlist").on('click', '.deletesubbutton', function () {
    var id = $(this).data('id')
    $.ajax({
        type: 'DELETE',
        url: '/newspaperapp/deletesubcomment/'+ id +'/',
        success: function(response){
            console.log(response)
            $(".comments #subcomment" + id).remove()
        }
    })
})

$(".commentlist").on('click', '#submitEdit', function () {
    var id = $(this).data('id')
    var data = $("#postEditComment"+id).serialize()
    console.log(data)
    $.ajax({
        url: '/newspaperapp/editcomment/'+ id +'/',
        type: 'POST',
        data: data,
        success: function (response) {
            $("#comment"+id+' .body').text(response.comment.body)
            $("#comment"+id+'  textarea #editcomment').text(response.comment.body)
            $("#editcommentform"+id).hide()
        }
    })
})

$(".followbuttons").on('click', '.follow', function () {
    var id = $(this).data('id')
    console.log(id)
    $.ajax({
        url: '/newspaperapp/addfavorite/'+ id +'/',
        type: 'POST',
        data: {},
        success: function (response) {
            $(".followbuttons #follow"+id).removeClass("btn btn-outline-info follow");
            $(".followbuttons #follow"+id).addClass("btn btn-info unfollow"); 
            $(".followbuttons #follow"+id).html('Unfollow');
            $("#follow"+id).attr("id","unfollow"+id+"");
        }
    }) 
})

$(".followbuttons").on('click', '.unfollow', function () {
    var id = $(this).data('id')
    console.log(id)
    $.ajax({
        url: '/newspaperapp/removefavorite/'+ id +'/',
        type: 'POST',
        data: {},
        success: function (response) {
            $(".followbuttons #unfollow"+id).removeClass("btn btn-info unfollow");
            $(".followbuttons #unfollow"+id).addClass("btn btn-outline-info follow"); 
            $(".followbuttons #unfollow"+id).html('Follow');
            $("#unfollow"+id).attr("id","follow"+id+"");
        }
    }) 
})

$(".likebuttons").on('click', '.like', function () {
    var id = $(this).data('id')
    console.log(id)
    $.ajax({
        url: '/newspaperapp/addlike/'+ id +'/',
        type: 'POST',
        data: {},
        success: function (response) {
            $(".likebuttons #like"+id).removeClass("btn btn-outline-success like");
            $(".likebuttons #like"+id).addClass("btn btn-success dislike"); 
            $(".likebuttons #like"+id).html('Dislike');
            $("#like"+id).attr("id","dislike"+id+"");
        }
    }) 
})

$(".likebuttons").on('click', '.dislike', function () {
    var id = $(this).data('id')
    console.log(id)
    $.ajax({
        url: '/newspaperapp/removelike/'+ id +'/',
        type: 'POST',
        data: {},
        success: function (response) {
            $(".likebuttons #dislike"+id).removeClass("btn btn-success dislike");
            $(".likebuttons #dislike"+id).addClass("btn btn-outline-success like"); 
            $(".likebuttons #dislike"+id).html('Like');
            $("#dislike"+id).attr("id","like"+id+"");
        }
    }) 
})