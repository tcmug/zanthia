$(function() {

    // $("form input[type='submit']").bind('click', function (event) {
    //     $.post('/users', $('form').serialize());
    //     alert("Submitted");
    //     event.preventDefault();
    // });

    var Zanthia = {
        open: function (page) {
            console.log(page);
        },

        loadRepositories: function () {
            $.getJSON("ajax/repositories", function( data ) {
                var items = [];
                $.each( data, function( key, val ) {
                    items.push("<option id='" + val + "'>" + val + "</option>");
                });
                $("#repositories").html(items).removeAttr('disabled');
            });
        }
    };

    $(window).on('hashchange', function(event){
        var name = window.location.hash.substring(1);
        $.getScript('/js/' + name + ".js", function () {
            var fn = window[name];
            if (typeof fn === 'function') {
                fn();
            } else {
                console.log("Missing controller " + name);
            }
        });
        event.preventDefault();
        return false;
    });


    $("#users").bind('change', function (event) {
        var user = $(this).val();

        $("#user").attr('disabled');
        $.getJSON("ajax/user/" + user, function( data ) {
            $("#user").html(data).removeAttr('disabled');
        });

    });

    $("#repositories").bind('change', function (event) {
        var repository = $(this).val();
        $("#users").html('').attr('disabled');
        $("#user").html('').attr('disabled');
        $.getJSON("ajax/repository/" + repository, function( data ) {
            var items = [];
            $.each( data, function( key, val ) {
                items.push("<option id='" + val + "'>" + val + "</option>");
            });
            $("#users").html(items).removeAttr('disabled');
        });
    });


    Zanthia.loadRepositories();
});
