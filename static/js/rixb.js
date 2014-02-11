/**
 * Created by Ricter on 14-1-23.
 */

var rixb = {
    get: function(id, is_raw, title_obj, tag_obj, content_obj) {
        var is_show = (arguments.length==5)
        $.ajax({
            type: "GET",
            url: "/articles/" + id,
            data: {"format": "json", "raw": is_raw},
            dataType: "json",
            success: function(data) {
                if (is_show) {
                    var data = data.message;
                    var tags = ''
                    title_obj[0].value = data.title;
                    for (var i=0;i<data.tag.length;i++) {
                        tags += data.tag[i].tag_name + ',';
                    }
                    tag_obj[0].value = tags.substring(0, tags.length-1);
                    content_obj.val(data.content);
                }
            },
            error: function(msg) {
                console.log(msg.responseText);
            }
        })
    },
    post: function(title, content, tag, callback) {
        $.ajax({
            type: "POST",
            url: "/articles",
            data: {"title": title, "content": content, "tag": tag},
            dataType: "json",
            success: function(data) {
                callback();
            },
            error: function(msg) {
                callback();
            }
        })
    },
    put: function(id, title, content, tag, callback) {
        $.ajax({
            type: "PUT",
            url: "/articles/" + id,
            data: {"title": title, "content": content, "tag": tag},
            dataType: "json",
            success: function(data) {
                callback();
            },
            error: function(msg) {
                callback();
            }
        })
    },
    delete: function(id, callback) {
        $.ajax({
            type: "DELETE",
            url: "/articles/" + id,
            dataType: "json",
            success: function(data) {
                callback();
            },
            error: function(msg) {
                console.log(msg);
                //callback();
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
    },
    add_friend: function(name, link) {
        $.ajax({
            type: "POST",
            url: "/editor/friends",
            dataType: "json",
            data: {"name": name, "link": link},
            success: function(data) {
                alert("Add success!");
            },
            error: function(msg) {
                alert("Add fail.");
            }
        })
    },
}

function set_button_data(data) {
    $(".delete")[0].attributes['data-article'].nodeValue = data;
    $(".publish")[0].attributes['data-article'].nodeValue = data;
}