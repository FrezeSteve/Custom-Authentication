from django.urls import path
from .views import PostListView, PostDetailView, CreateCommentView, list_comments, CreatePostView

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="home")
    , path("<slug:slug>/", PostDetailView.as_view(), name="detail")
    # uuid of the post being commented on
    , path("comment/create/<uuid:id>/", CreateCommentView.as_view(), name="create_comment")
    # get the list of comments
    , path("blog/list_comments/<uuid:comment_id>/<str:page_number>/", list_comments, name="get_comments")
    , path("blog/create_post", CreatePostView.as_view(), name="create_post")
]
