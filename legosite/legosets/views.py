from django.shortcuts import get_object_or_404, render
from .models import LegoSet, Vendor, Discount

def index(request):
    last_add = LegoSet.objects.order_by('-add_datetime')[:5]
    context = {'last_add': last_add}
    return render(request, 'legosets/index.html', context)

def detail(request, set_id):
    legoset = get_object_or_404(LegoSet, pk=set_id)
    return render(request, 'legosets/detail.html', {'legoset': legoset})
    
def discount(request):
    discount = Discount.objects.order_by('discount')[:20]
    return render(request, 'legosets/discount.html', {'discount': discount})


