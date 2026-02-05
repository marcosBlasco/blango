from django.contrib.auth import get_user_model
from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from blog.models import Post
user_model = get_user_model()
register = template.Library()

@register.filter
def author_details(author, current_user=None):
    if not isinstance(author, user_model):
        # return empty string as safe default
        return ""
    
    if author == current_user:
        return mark_safe("<strong>me</strong>")

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    if author.email:
        scaped_email = format_html('<a href="mailto:{}">{}</a>', author.email, name)
    else:
        prefix = ""
        suffix = ""

    return scaped_email


@register.simple_tag
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)

@register.simple_tag
def endrow():
    return mark_safe("</div>")


@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)


@register.simple_tag
def endcol():
    return mark_safe("</div>")


@register.inclusion_tag("blog/post-list.html")
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)[:5]
    return {"title": "Recent Posts", "posts": posts}