$('#btn-copy').click(function () {
    let temp = $("<input>");
    $("body").append(temp);
    const short_url = $('#short_url');
    temp.val(short_url.text()).select();
    //short_url.setSelectionRange(0, 99999); // for mobile devices

    document.execCommand("copy");
    $('#msg-copy').removeClass("d-none");
    temp.remove();
})