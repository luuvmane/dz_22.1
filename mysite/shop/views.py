from django.shortcuts import render, get_object_or_404
from .models import Product, Version
from .forms import ProductForm, VersionForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse
from .models import BlogPost
from django.db.models import F
from django.utils.text import slugify
import uuid


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


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        active_version = product.versions.filter(is_active=True).first()
        context['active_version'] = active_version
        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/product_form.html'
    success_url = reverse_lazy('product_list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')


class ProductListView(ListView):
    model = Product
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.prefetch_related('versions')
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


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    template_name = 'shop/version_form.html'
    success_url = reverse_lazy('product_list')


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
