$(document).on('submit', '#post-form', function (e) {
        e.preventDefault();
         mes = $('#message').val();
            send_data = {
                "message":mes,
                "csrfmiddlewaretoken":$('input[name=csrfmiddlewaretoken]').val()
            };

            $.ajax({
                url:'/reload/',
                type:"post",
                data:send_data,
                success: function(data){
                    $('#message-list').append("<p  class='' >" + data['message'] + "</p>");
                    $('#message-list').append("<p  class=''>" + data['answer'] + "</p>");
                },
                error: function() {
                  alert('problem');
                }
            });
    })