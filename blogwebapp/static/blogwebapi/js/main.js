/* main.js */

function goBack() {
    location = "/admin/blogs/";
}

function removeContent(el, contentId) {
    el = el.target != null && typeof el == "object" ? el.target : el;
    var $content = $(el).parents('.blog-content'),
        $formRow = $(el).parents('.form-row');

    $content.find($formRow).remove();

    if (contentId != null) {
        var tokenVal = $('input[name=csrfmiddlewaretoken]').val();
        $.ajax({
            url: 'http://localhost:8888/contents/' + contentId,
            headers: { 'X-CSRFToken': tokenVal },
            method: 'DELETE'
        });
    }
}

$(function() {
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
            tinymce.init({selector: "textarea"});
    });

    tinymce.init({selector: "textarea"});
});