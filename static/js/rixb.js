/**
 * Created by Ricter on 14-1-23.
 */

var rixb = {
    get: function(id) {
        $.ajax({
            type: "GET",
            url: "/article/" + id,
            data: {format: "json"},
            dataType: "json",
            success: function(data) {
                console.log(data);
            },
            error: function(msg) {
                console.log(msg.responseText);
            }
        })
    },
    post: function(title, content) {
        $.ajax({
            type: "POST",
            url: "/article",
            data: {title: title, content: content},
            dataType: "json",
            success: function(data) {
                console.log(data);
            },
            error: function(msg) {
                console.log(msg);
            }
        })
    },
    put: function(id) {

    },
    delete: function(id) {
        $.ajax({
            type: "DELETE",
            url: "/article/" + id,
            dataType: "json",
            success: function(data) {
                console.log(data);
            },
            error: function(msg) {
                console.log(msg)
            }
        })
    }
}