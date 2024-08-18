from django.shortcuts import render, get_object_or_404
from .models import Product, Version, BlogPost
from .forms import VersionForm
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.text import slugify
import uuid
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import ProductForm, ModeratorProductForm
from django.core.exceptions import PermissionDenied
from .models import Category
from .services import get_cached_categories


class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return get_cached_categories()


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'shop/product_detail.html', context)


def index(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop/index.html', context)


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        has_change_permission = self.request.user.has_perm('shop.change_product')
        has_delete_permission = self.request.user.has_perm('shop.delete_product')
        context['has_change_permission'] = has_change_permission
        context['has_delete_permission'] = has_delete_permission
        context['active_version'] = product.versions.filter(is_active=True).first()
        return context


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('product_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.get_object().owner:
            return ProductForm
        elif user.has_perm("shop.can_edit_description") and user.has_perm("shop.can_edit_category"):
            return ModeratorProductForm
        else:
            raise PermissionDenied

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        product = self.get_object()
        return self.request.user == product.owner or self.request.user.has_perm("shop.can_edit_description") and self.request.user.has_perm("shop.can_edit_category")


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')


class ProductListView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'product_list'

    def get_queryset(self):
        return Product.objects.prefetch_related('versions').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = self.get_queryset()
        for product in products:
            active_version = product.versions.filter(is_active=True).first()
            product.active_version = active_version
        context['products'] = products
        return context


class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    template_name = 'shop/version_form.html'
    success_url = reverse_lazy('product-list')

    def form_valid(self, form):
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        form.instance.product = product
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('product-detail', kwargs={'pk': self.kwargs['product_id']})


class VersionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'shop/version_form.html'
    success_url = reverse_lazy('product_list')

    def test_func(self):
        version = self.get_object()
        return self.request.user == version.product.owner or self.request.user.has_perm('shop.change_version')


class VersionDetailView(DetailView):
    model = Version
    template_name = 'shop/version_detail.html'


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blog_posts'

    def get_queryset(self):
        return BlogPost.objects.filter(published=True)


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        post = super().get_object(queryset=queryset)
        post.views += 1
        post.save(update_fields=['views'])
        return post


class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview_image', 'published']
    success_url = reverse_lazy('blogpost_list')

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        if BlogPost.objects.filter(slug=form.instance.slug).exists():
            form.instance.slug += f"-{uuid.uuid4().hex[:5]}"
        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview_image', 'published']

    def get_success_url(self):
        return reverse('blogpost_detail', args=[self.object.slug])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blogpost_list')
