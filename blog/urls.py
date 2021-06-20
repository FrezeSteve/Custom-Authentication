from django.urls import path
from .views import PostListView, PostDetailView, CreateCommentView


app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="home")
    , path("<slug:slug>/", PostDetailView.as_view(), name="detail")
    # uuid of the post being commented on
    , path("comment/create/<uuid:id>/", CreateCommentView.as_view(), name="create_comment")
]
