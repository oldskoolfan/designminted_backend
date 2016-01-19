/* main.js */

var tinymceOptions = {
    selector: 'textarea',
    height: 300,
    plugins: [
        'advlist autolink lists link image charmap print preview anchor',
        'searchreplace visualblocks code fullscreen',
        'insertdatetime media table contextmenu paste code'
    ],
    toolbar: 'insertfile undo redo | styleselect | bold italic | alignleft aligncenter ' +
    'alignright alignjustify | bullist numlist outdent indent | link image'
};

function goBack() {
    //location = "/admin/blogs/";
    window.history.back();
}

function makeAjaxCall(url, verb, data, callback) {
    var tokenVal = $('input[name=csrfmiddlewaretoken]').val(),
        options = {
            type: verb,
            url: url,
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', tokenVal);
            }
        };
    if (data != null) options.data = data;
    $.ajax(options)
        .done(callback)
        .fail(function(xhr, status, err) {
            alert('Problem updating data. See console for error log.');
            console.debug(err);
        });
}

function removeContent(el, contentId) {
    el = el.target != null && typeof el == "object" ? el.target : el;
    var $content = $(el).parents('.blog-content'),
        $formRow = $(el).parents('.form-row');

    $content.find($formRow).remove();

    if (contentId != null) {
        var url = '/contents/' + contentId,
            verb = 'delete';
        makeAjaxCall(url, verb, null, null);
    }
}

$(function() {
    // add image to page if uploaded
    $('.new-blog-form').on('change', 'input[type=file]', function() {
        var file = this.files[0],
            $this = $(this);
        var reader = new FileReader();
        reader.onloadend = function() {
            $this.parents('.form-row').find('img')
                .remove()
                .end()
                .append($('<p><img src="' + reader.result + '" alt="image"/></p>'));
        };
        reader.readAsDataURL(file);
    });

    // add new content section
    $('#add-content').on('click', function() {
        var type = $('#content-type').val(),
            $rowDiv = $('<div>').addClass('form-row'),
            $newEl;
        $rowDiv.append('<label>').append('<i></i>').find('i')
            .addClass('fa fa-close fa-lg').on('click', this, removeContent);
        switch (type) {
            case "1":
                $rowDiv.find('label').text('Body:').attr('for', 'body');
                $newEl = $('<textarea name="body">');
                break;
            case "2":
                $rowDiv.find('label').text('Image:').attr('for', 'image');
                $newEl = $('<input name="image">').attr('type', 'file');
                break;
        }
        $rowDiv.append($newEl);
        $('.blog-content').append($rowDiv);
        if (type == 1) //$newEl.focus();
            tinymce.init(tinymceOptions);
    });

    // approve/unapprove comments
    $('button[class$=approve]').on('click', function() {
        var approve = $(this).hasClass('approve'),
            commentId = $(this).data('commentid'),
            verb = 'post',
            data = { approve: approve },
            button = this,
            url = '/update-comment-approval/' + commentId,
            callback = function() {
                button.className = approve ? 'unapprove' : 'approve';
                button.innerHTML = approve ? 'Unapprove' : 'Approve';
                alert('Comment updated successfully!');
            };
        makeAjaxCall(url, verb, data, callback);
    });

    $('button[class=delete]').on('click', function() {
        var commentId = $(this).data('commentid'),
            verb = 'delete',
            url = '/comments/' + commentId,
            comment = $(this).parents('tr'),
            callback = function() {
                $(comment).remove();
            };
        makeAjaxCall(url, verb, null, callback);
    })

    // init tinymce on doc.ready
    if (typeof tinymce != "undefined")
        tinymce.init(tinymceOptions);
});