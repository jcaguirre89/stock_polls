//CRUD generic processing
$(document).ready(function() {
    loadForm = function(event) {
        var btn = $(event.target);
        $.ajax({
            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function () {
                $('#modal .modal-content').html("");
                $('#modal').modal('show');
            },
            success: function (data) {
                $("#modal .modal-content").html(data.html_form);
            }
        });

    };


    //function to save a form when submitted
    saveForm = function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();
        var form = $(event.target);
        var data = new FormData(form.get(0));
        $.ajax({
            url:  form.attr('action'),
            data: data,
            type: form.attr("method"),
            dataType: 'json',
            cache: false,
            processData: false,
            contentType: false,
            beforeSend: function() {
                $("#modal .modal-content").html('');
                $("#modal .modal-content").addClass('loader');
            },
            success: function(data) {
                $("#modal .modal-content").removeClass('loader');
                if (data.form_is_valid) {
                    $("#object-table tbody").html(data.html_data);
                    $("#modal").modal("hide");
                }
                else {
                    $("#modal .modal-content").html(data.html_form);
                }
            }
        });
        return false;


    };


});


//Create
$("#js-create").click(function (event) {
    loadForm(event);
});
$("#modal").on("submit", ".js-create-form", function (event) {
    saveForm(event);
});

//Update
$("#object-table").on("click", "#js-update", function (event) {
    loadForm(event);
});
$("#modal").on("submit", ".js-update-form", function (event) {
    saveForm(event);
});

//Delete
$("#object-table").on("click", "#js-delete", function (event) {
    loadForm(event);
});
$("#modal").on("submit", ".js-delete-form", function (event) {
    saveForm(event);
});