from django.urls import path
from .views import (
    PostListView, PostDetailView, CreateCommentView, list_comments, CreatePostView, EditPostView,
    ProcessEditForm, archive_post, DraftPostListView, ArchivedPostListView, publish_post
)

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="home")
    , path("draft_list/", DraftPostListView.as_view(), name="draft_list")
    , path("archived_list/", ArchivedPostListView.as_view(), name="archived_list")
    , path("<slug:slug>/", PostDetailView.as_view(), name="detail")
    # uuid of the post being commented on
    , path("comment/create/<uuid:id>/", CreateCommentView.as_view(), name="create_comment")
    # get the list of comments
    , path("blog/list_comments/<uuid:comment_id>/<str:page_number>/", list_comments, name="get_comments")
    , path("blog/create_post", CreatePostView.as_view(), name="create_post")
    , path("blog/edit_post/<uuid:pk>/", EditPostView.as_view(), name="edit_post")
    , path("blog/process_edit_form/<uuid:pk>/", ProcessEditForm.as_view(), name="process_edit_form")
    , path("blog/archive_post/<uuid:pk>/", archive_post, name="archive_post")
    , path("blog/publish_post/<uuid:pk>/", publish_post, name="publish_post")
]
