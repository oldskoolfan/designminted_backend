function clearContactForm() {
    // clear fields
    document.getElementById('id_firstname').value = '';
    document.getElementById('id_lastname').value = '';
    document.getElementById('id_email').value = '';
    document.getElementById('id_message').value = '';

    // get rid of any error messages
    var errors = document.getElementsByClassName('errorlist');
    var errArray = [];
    if (errors.length > 0) {
        for (var i = 0; i < errors.length; i++) {
            errArray.push(errors[i]);
        }
        errArray.forEach(function(err) { err.remove() });
    }
}

function toggleNav() {
    var html = document.getElementsByTagName('html')[0];
    html.classList.toggle('nav-visible');
}