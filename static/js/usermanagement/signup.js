$('#signupForm').submit(function (e) {
    if ($('#password').val() != $('#repeatPassword').val()) {
        e.preventDefault();

        $('#errorMsgCont').removeClass('d-none');
        $('#errormsg').html("Passwords do not match");
    }
});

$('#changeAddress').click(function () {
    $('#locationField').slideDown();
    $('#autocompleteAddressCont').slideUp();
});