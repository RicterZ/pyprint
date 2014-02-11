$(".article-item").click(function() {
    var article_id = this.attributes['data-article'].nodeValue;
    if (!$(this).hasClass("article-active")) {
        $(".delete").show();
        $(".article-item").removeClass("article-active");
        $(this).addClass("article-active");
        set_button_data(article_id);
        $(".publish").text("Update");
        rixb.get(article_id, true, $("#edit-title"), $("#edit-tag"), $("#edit-content"));
    } else {
        $(this).removeClass("article-active");
        $(".delete").hide();
        $(".article-area > *").val("");
        $(".publish").text("Publish");
        set_button_data("");
    };
})

$(".delete").click(function() {
    var _this = this;
    rixb.delete(this.attributes['data-article'].nodeValue, 
        function(){
            $($(".article-active").parent()).hide();
            $(".article-active").removeClass("article-active");
            set_button_data("");
            $(".article-area > *").val("");
            $(_this).hide();
        }
    );
})

$(".publish").click(function() {
    var article_id = this.attributes['data-article'].nodeValue;
    if (article_id != "") {
        rixb.put(article_id, $("#edit-title").val(), $("#edit-content").val(), 
                 $("#edit-tag").val(), function() {
                $(".article-area > *").val("");
                alert('Update successful!');
                window.location.reload();
            })
    } else {
        rixb.post($("#edit-title").val(), $("#edit-content").val(), 
                  $("#edit-tag").val(), function() {
                $(".article-area > *").val("");
                alert('Publish successful!');
                window.location.reload();
            });
    }
})

$(".add-link").click(function(){
    rixb.add_friend($("#friend").val(), $("#link").val());
})