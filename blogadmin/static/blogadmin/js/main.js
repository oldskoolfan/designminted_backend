/* main.js */

var tinymceOptions = {
    image_title: true,

    // NOTE: see https://www.tinymce.com/docs/demo/file-picker/
    file_picker_callback: function(cb, value, meta) {
        var input = document.createElement('input');
        input.setAttribute('type', 'file');
        input.setAttribute('accept', 'image/*');

        // Note: In modern browsers input[type="file"] is functional without
        // even adding it to the DOM, but that might not be the case in some older
        // or quirky browsers like IE, so you might want to add it to the DOM
        // just in case, and visually hide it. And do not forget do remove it
        // once you do not need it anymore.

        input.onchange = function() {
          var file = this.files[0];

          // Note: Now we need to register the blob in TinyMCEs image blob
          // registry. In the next release this part hopefully won't be
          // necessary, as we are looking to handle it internally.
          var id = 'blobid' + (new Date()).getTime();
          var blobCache = tinymce.activeEditor.editorUpload.blobCache;
          var blobInfo = blobCache.create(id, file);
          blobCache.add(blobInfo);

          // call the callback and populate the Title field with the file name
          cb(blobInfo.blobUri(), { title: file.name });
        };

        input.click();
    },
    // NOTE: see https://www.tinymce.com/docs/configure/file-image-upload/
    images_upload_handler: function (blobInfo, success, failure) {
        var xhr,
            formData,
            tokenVal = $('input[name=csrfmiddlewaretoken]').val();

        xhr = new XMLHttpRequest();
        xhr.withCredentials = true;
        xhr.open('POST', '/admin/upload/');

        xhr.onload = function() {
          var json;

          if (xhr.status != 200) {
            failure('HTTP Error: ' + xhr.status);
            return;
          }

          json = JSON.parse(xhr.responseText);

          if (!json || typeof json.location != 'string') {
            failure('Invalid JSON: ' + xhr.responseText);
            return;
          }

          success(json.location);
        };

        formData = new FormData();
        formData.append('image_upload', blobInfo.blob(), blobInfo.filename());

        xhr.setRequestHeader('X-CSRFToken', tokenVal);
        xhr.send(formData);
    },
    file_picker_types: 'file image media',
    automatic_uploads: true,
    image_dimensions: false,
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
    var sure = confirm('Are you sure you want to delete this content?');

    if (sure) {
        el = el.target != null && typeof el == "object" ? el.target : el;
        var $content = $(el).closest('.blog-content'),
            $formRow = $(el).closest('.form-row'),
            type = $formRow.data('type'),
            callback = function(data) {
                console.debug(data);
            };

        if (type == window.contentTypes.TEXT) {
            tinymce.remove();
            tinymce.init(tinymceOptions);
        }

        $content.find($formRow).remove();

        if (contentId != null) {
            var url = '/admin/delete-content/' + contentId,
                verb = 'delete';
            makeAjaxCall(url, verb, null, callback);
        }

        adjustPositions();
        window.contentCount--;
    }
}

function adjustPositions() {
    var positionCounter = 1;
    $('.form-row').each(function() {
        $el = $(this);
        $el.data('position', positionCounter);
        $el.find('input[name=position]').val(positionCounter++);
    });
}

$(function() {

    // add image to page if uploaded
    $('.new-blog-form').on('change', 'input[type=file]', function() {
        var file = this.files[0],
            $this = $(this),
            $row = $this.closest('.form-row');
        var reader = new FileReader();
        reader.onloadend = function() {
            $row.find('img')
                .remove()
                .end()
                .find('input[type=file]')
                .after($('<p><img src="' + reader.result + '" alt="image"/></p>'));
        };
        reader.readAsDataURL(file);

        // set hidden image flag
        $row.find('input[name=hasImage]').val('1');

    }).on('dragover', '[draggable=true]', function(e) { // prevent default drag handler
        e.preventDefault();

    }).on('dragstart', '[draggable=true]', function(e) {
        // get text editor content
        var $textarea = $(e.target).find('textarea'),
            editor,
            text,
            position = $(e.target).data('position');
        if ($textarea.length > 0) {
            editor = tinymce.get($textarea.attr('id'));
        }
        if (editor) {
            text = editor.getContent();
        }
        e.originalEvent.dataTransfer.setData('editor', $textarea.attr('id'));
        e.originalEvent.dataTransfer.setData('text', text);
        e.originalEvent.dataTransfer.setData('position', position);

        // get html
        e.originalEvent.dataTransfer.setData('html', e.target.id);
    }).on('drop', '[draggable=true]', function(e) {
        var $target = $(e.target),
            dragPosition,
            dragData,
            targetPosition,
            $row,
            text,
            editor;

        // get form-row
        if ($target.hasClass('form-row')) {
            $row = $target;
        } else {
            $row = $target.closest('.form-row');
        }

        // get data
        targetPosition = $row.data('position');
        dragPosition = e.originalEvent.dataTransfer.getData('position');
        dragData = document.getElementById(e.originalEvent.dataTransfer.getData('html'));

        // move elements
        if (targetPosition < dragPosition) {
            $row.before(dragData);
        } else {
            $row.after(dragData);
        }

        // adjust positions
        adjustPositions();

        text = e.originalEvent.dataTransfer.getData('text');
        editor = tinymce.get(e.originalEvent.dataTransfer.getData('editor'));
        if (editor) {
            editor.setContent(text);
            tinymce.remove();
            tinymce.init(tinymceOptions);
        }
    });

    // add new content section
    $('#add-content').on('click', function() {
        var type = $('#content-type').val(),
            $blogContent = $('.blog-content'),
            $rowDiv = $('<div>').addClass('form-row'),
            $newEl,
            html;
        window.contentCount++;
        $rowDiv.data('type', type)
            .attr('id', 'content-' + window.contentCount.toString())
            .attr('draggable', true)
            .data('position', window.contentCount)
            .append('<input type="hidden" name="contentid" value="-1"/>')
            .append('<input type="hidden" name="position" value="' + window.contentCount.toString() + '"/>')
            .append('<input type="hidden" name="type" value="' + type + '"/>')
            .append('<label>')
            .append('<i></i>')
            .find('i')
            .addClass('fa fa-close fa-lg')
            .on('click', this, removeContent);
        switch (+type) {
            case window.contentTypes.TEXT:
                $rowDiv.find('label').text('Body:').attr('for', 'body');
                $newEl = $('<textarea name="body">');
                break;
            case window.contentTypes.IMAGE:
                $rowDiv.find('label').text('Image:').attr('for', 'image');
                $newEl = '<input name="hasImage" type="hidden" value="0"/><input name="image" type="file"/>';
                $newEl += '<br><br><label for="caption">Caption:</label>';
                $newEl += '<input type="text" id="caption" name="caption"/>';
                break;
        }
        $rowDiv.append($newEl);
        $blogContent.append($rowDiv);
        if (type == 1)
            tinymce.remove();
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
            comment = $(this).closest('tr'),
            callback = function() {
                $(comment).remove();
            };
        makeAjaxCall(url, verb, null, callback);
    });

    // init tinymce on doc.ready
    if (typeof tinymce != "undefined")
        tinymce.init(tinymceOptions);

    window.blogContents = [];
    // get intial content positions
    $('.form-row').each(function() {
        window.blogContents.push(this.id);
    });
});