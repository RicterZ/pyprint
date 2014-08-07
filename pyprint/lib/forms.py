from web import form

post_form = form.Form(
    form.Textbox('title'),
    form.Textbox('tags'),
    form.Textarea('content'),
)

link_form = form.Form(
    form.Textbox('name'),
    form.Textbox('url'),
)