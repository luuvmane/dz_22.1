from django.shortcuts import render, get_object_or_404
from .models import Product, Version
from .forms import ProductForm, VersionForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse


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
