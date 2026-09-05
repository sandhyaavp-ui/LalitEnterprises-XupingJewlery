from django.shortcuts import render, get_object_or_404
from .models import Collection, Product


def product_list(request):
    collections = Collection.objects.all()
    all_products = Product.objects.select_related('collection').all()
    return render(request, 'catalog/product_list.html', {
        'collections': collections,
        'products': all_products,
        'product_count': all_products.count(),
        'collection_count': collections.count(),
    })


def collection_detail(request, slug):
    collection = get_object_or_404(Collection, slug=slug)
    products = collection.products.all()
    return render(request, 'catalog/collection_detail.html', {
        'collection': collection,
        'products': products,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    recommended = (
        Product.objects.filter(collection=product.collection)
        .exclude(pk=product.pk)[:3]
    )

    other_collections = Collection.objects.exclude(pk=product.collection_id)
    complete_the_pair = []
    for c in other_collections:
        pick = Product.objects.filter(collection=c).order_by('?').first()
        if pick:
            complete_the_pair.append(pick)

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'recommended': recommended,
        'complete_the_pair': complete_the_pair,
    })


def search(request):
    query = request.GET.get('q', '').strip()
    results = Collection.objects.filter(name__icontains=query) if query else Collection.objects.none()
    return render(request, 'catalog/search_results.html', {
        'query': query,
        'results': results,
    })
