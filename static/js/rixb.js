/**
 * Created by Ricter on 14-1-23.
 */

var rixb = {
    get: function(id) {
        $.ajax({
            type: "GET",
            url: "/article/" + id,
            data: {"format": "json"},
            dataType: "json",
            success: function(data) {
                console.log(data);
            },
            error: function(msg) {
                console.log(msg.responseText);
            }
        })
    },
    post: function(title, content, tag) {
        $.ajax({
            type: "POST",
            url: "/article",
            data: {"title": title, "content": content, "tag": tag},
            dataType: "json",
            success: function(data) {
                console.log(data);
            },
            error: function(msg) {
                console.log(msg);
            }
        })
    },
    put: function(id, title, content, tag) {
        $.ajax({
            type: "PUT",
            url: "/article/" + id,
            data: {"title": title, "content": content, "tag": tag},
            dataType: "json",
            success: function(data) {
                console.log(data);
            },
            error: function(msg) {
                console.log(msg.responseText);
            }
        })
    },
    delete: function(id) {
        $.ajax({
            type: "DELETE",
            url: "/article/" + id,
            dataType: "json",
            success: function(data) {
                console.log('Article Delete success');
            },
            error: function(msg) {
                console.log(msg.responseText)
            }
        })
    },
    login: function(u, p, obj) {
        $.ajax({
            type: "POST",
            url: "/signin",
            dataType: "json",
            data: {"username": u, "password": p},
            success: function(data) {
                window.location = '/editor';
            },
            error: function(msg) {
                eval("var resopnse = " + msg.responseText);
                obj.text(resopnse.message);
                obj.show();
            }
        })
    }
}