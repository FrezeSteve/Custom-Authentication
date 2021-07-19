from accounts.models import DeviceTracker
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import reverse, get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView

from .forms import CommentForm, CreatePostForm
from .models import Post, Comment
from .utils import custom_set_cookie

User = get_user_model()


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    queryset = Post.objects.filter(published=True, archived=False)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['comment_form'] = CommentForm()
        return context

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        custom_set_cookie(self.request, response)
        # for i in range(10000):
        #     Comment.objects.create(
        #         title="stupid",
        #         body="not that bad.",
        #         post=self.get_object(),
        #         device=DeviceTracker.objects.first()
        #     )
        return response


class CreateCommentView(CreateView):
    form_class = CommentForm
    model = Comment

    def form_valid(self, form):
        # raise forms.ValidationError("Error!!")
        session_id = self.request.get_signed_cookie('custom_session_id', default=None)
        # get or create anonymous user
        device = DeviceTracker.objects.filter(
            device_id=session_id
        )
        if not device.exists():
            device = DeviceTracker.objects.create(
                device_id=session_id
            )
        else:
            device = device.first()
        device.last_used = timezone.now()
        device.save()
        # if authenticated
        if self.request.user.is_authenticated:
            form.instance.registered_user = True
            form.instance.user = self.request.user
            logged_in_user = User.objects.filter(id=self.request.user.id).first()
            logged_in_user.device.add(device)
            logged_in_user.save()
        form.instance.device = device
        form.instance.post = get_object_or_404(Post, id=self.kwargs.get('id'))
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, id=self.kwargs.get('id'))
        return HttpResponseRedirect(reverse('blog:detail', kwargs={'slug': instance.slug}))


class CreatePostView(CreateView):
    form_class = CreatePostForm
    model = Post

    def form_valid(self, form):
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return render(request, "blog/create_post.html", {'form': self.get_form_class()})


# handles listing ajax requests
@require_http_methods(["GET"])
def list_comments(request, comment_id, page_number):
    data = []
    instance = Post.objects.filter(id=comment_id).first()
    if instance:
        page_number = 1 if not page_number else page_number
        if page_number == 1:
            data = [
                {
                    "title": i.title
                    , "body": i.body
                    , "published": i.published
                    , "registered_user": i.registered_user
                    , "user": str(i.user) if i.user else None
                }
                for i in instance.comments.all()[:int(page_number) * 10]
            ]
        else:
            data = [
                {
                    "title": i.title
                    , "body": i.body
                    , "published": i.published
                    , "registered_user": i.registered_user
                    , "user": str(i.user) if i.user else None
                }
                for i in instance.comments.all()[(int(page_number) - 1) * 10:int(page_number) * 10]
            ]
    return JsonResponse(data, safe=False)
