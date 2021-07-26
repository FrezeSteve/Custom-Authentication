from accounts.models import DeviceTracker
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import reverse, get_object_or_404, render
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import CommentForm, CreatePostForm
from .models import Post, Comment, Category
from .utils import custom_set_cookie, get_create_device_tracker, unique_slug_generator, store_device_to_user

User = get_user_model()


# Create your views here.
class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    queryset = Post.objects.filter(published=True, archived=False)

    def get(self, request, *args, **kwargs):
        response = super(PostListView, self).get(request, *args, **kwargs)
        custom_set_cookie(self.request, response)
        return response


class DraftPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    queryset = Post.objects.filter(published=False, archived=False)

    def get(self, request, *args, **kwargs):
        response = super(DraftPostListView, self).get(request, *args, **kwargs)
        custom_set_cookie(self.request, response)
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse('blog:home'))
        return response


class ArchivedPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'
    queryset = Post.objects.filter(published=True, archived=True)

    def get(self, request, *args, **kwargs):
        response = super(ArchivedPostListView, self).get(request, *args, **kwargs)
        custom_set_cookie(self.request, response)
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse('blog:home'))
        return response


class PostDetailView(LoginRequiredMixin, DetailView):
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
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse('blog:home'))
        return response


class CreateCommentView(CreateView):
    form_class = CommentForm
    model = Comment

    def form_valid(self, form):
        device = get_create_device_tracker(self.request)
        # if authenticated
        if self.request.user.is_authenticated:
            form.instance.registered_user = True
            form.instance.user = self.request.user
            store_device_to_user(self.request, device)
        form.instance.device = device
        form.instance.post = get_object_or_404(Post, id=self.kwargs.get('id'))
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, id=self.kwargs.get('id'))
        return HttpResponseRedirect(reverse('blog:detail', kwargs={'slug': instance.slug}))


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm
    model = Post

    def form_valid(self, form):
        # device
        device = get_create_device_tracker(self.request)
        store_device_to_user(self.request, device)
        # form fields
        form.instance.slug = unique_slug_generator(form.instance)
        # author
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse('blog:home'))
        form = self.get_form_class()()
        if Category.objects.count() == 0:
            Category.objects.create(
                name="Default"
            )
        return render(request, "blog/create_post.html", {'form': form})


class EditPostView(LoginRequiredMixin, UpdateView):
    form_class = CreatePostForm
    model = Post
    template_name = 'blog/create_post.html'

    def form_valid(self, form):
        # device
        device = get_create_device_tracker(self.request)
        store_device_to_user(self.request, device)
        # form fields
        # form.instance.slug = unique_slug_generator(form.instance)
        # author
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def get_object(self, queryset=None):
    #     instance = Post.objects.filter(id=self.kwargs.get('pk')).first()
    #     if instance:
    #         instance.pk = None
    #         instance.save()
    #     return instance

    # def post(self, request, *args, **kwargs):
    #     return HttpResponseRedirect(reverse('blog:home'))

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseRedirect(reverse('blog:home'))
        if Category.objects.count() == 0:
            Category.objects.create(
                name="Default"
            )
        return super().get(request, *args, **kwargs)


class ProcessEditForm(LoginRequiredMixin, CreateView):
    form_class = CreatePostForm
    model = Post

    def form_valid(self, form):
        device = get_create_device_tracker(self.request)
        # if authenticated
        if self.request.user.is_authenticated:
            form.instance.registered_user = True
            form.instance.user = self.request.user
            store_device_to_user(self.request, device)
        form.instance.device = device
        form.instance.post = get_object_or_404(Post, id=self.kwargs.get('pk'))
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        instance = get_object_or_404(Post, id=self.kwargs.get('pk'))
        return HttpResponseRedirect(reverse('blog:detail', kwargs={'slug': instance.slug}))


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


def archive_post(request, pk):
    instance = get_object_or_404(Post, id=pk)
    instance.archived = True
    instance.save()
    return HttpResponseRedirect(reverse('blog:detail', kwargs={'slug': instance.slug}))
