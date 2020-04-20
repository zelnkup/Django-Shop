from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# List view

def ProductList(request, category_slug=None):
    category = None
    categories = Category.objects.all()

    # Variable for searching
    search_query = request.GET.get('search', '')
    if search_query:
        products = Product.objects.filter(Q(available=True) & Q(name__icontains=search_query))
    else:
        products = Product.objects.filter(available=True)

    # QuerySet for new products
    newproducts = Product.objects.filter(available=True).order_by('-created')[:8]

    # QuerySet for products in category
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

        # Quantity of shown products in categories
        paginator = Paginator(products, 8)
        page = request.GET.get('page')
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            if request.is_ajax():
                return HttpResponse('')
            products = paginator.page(paginator.num_pages)

        # Variable return query set if request is ajax
        if request.is_ajax():
            return render(request, 'shop/product/list_ajax.html', {'products': products,
                                                                   'category': category, })
        return render(request, 'shop/product/list.html', {'products': products,
                                                          'category': category,
                                                          'categories': categories,
                                                          'newproducts': newproducts,
                                                          })

    # Quantity of shown products in main list
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        products = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'shop/product/list_ajax.html', {'products': products})
    return render(request, 'shop/product/list.html', {'products': products,
                                                      'category': category,
                                                      'categories': categories,
                                                      'newproducts': newproducts,
                                                      'search_query': search_query,
                                                      })


# Detail view
def ProductDetail(request, id,
                  slug):
    product = get_object_or_404(Product, id=id,
                                slug=slug, available=True)

    # Function which add item to cart
    cart_product_form = CartAddProductForm()
    categories = Category.objects.all()
    return render(request, 'shop/product/product.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'categories': categories,
                   })
