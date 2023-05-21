$(document).ready(function() {
    if ($('#result') != null) {
        Read();
    }
    $('#create').on('click', function() {
        $task = $('#task').val();
        // $lastname = $('#lastname').val();

        if ($task != "") {
            $.ajax({
                url: 'create',
                type: 'POST',
                data: {
                    task: $task,
                    // lastname: $lastname,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function() {
                    Read();
                    $('#task').val('');
                    // $('#lastname').val('');
                }
            });

        } else {
            alert("You can't create empty task.");
        }
    });

    $(document).on('click', '.edit', function() {
        $id = $(this).attr('name');
        window.location = "edit/" + $id;
    });

    $('#update').on('click', function() {
        $task = $('#task').val();
        // $lastname = $('#lastname').val();

        if ($task == "") {
            alert("You can't create empty task.");
        } else {
            $id = $('#todo_id').val();
            $.ajax({
                url: 'update/' + $id,
                type: 'POST',
                data: {
                    task: $task,
                    // lastname: $lastname,
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                },
                success: function() {
                    window.location = '/';
                    alert('The task has been UPDATED successfully!!!');
                }
            });
        }
    });

    $(document).on('click', '.delete', function() {
        $id = $(this).attr('name');
        $.ajax({
            url: 'delete/' + $id,
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function() {
                Read();
                alert("The task has been DELETED!")
            }
        });
    });
});

function Read() {
    $.ajax({
        url: 'read',
        type: 'POST',
        async: false,
        data: {
            res: 1,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(response) {
            $('#result').html(response);
        }
    });
}