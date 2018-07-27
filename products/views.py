from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone

# Create your views here.
def home(request):
	products = Product.objects
	return render(request, 'products/home.html', {'products' : products})

@login_required
def create(request):
	if request.method == 'POST':
		if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['image'] and request.FILES['icon'] is not None:
			product = Product()
			product.title = request.POST['title']
			product.body = request.POST['body']
			if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
				product.url = request.POST['url']
			else:
				product.url = 'http://' + request.POST['url']
			product.icon = request.FILES['icon']
			product.image = request.FILES['image']
			product.pub_date = timezone.datetime.now()
			product.votes_total = 1
			product.hunter = request.user
			# Inserts it into database
			product.save()
            # product is got on a product.save()
			return redirect('/products/' + str(product.id))
		else:
			return render(request, 'products/create.html', {'error' : "All fields are required"})	
	else:
		return render(request, 'products/create.html')

def detail(request, product_id):
	# Find an object of app Product keyed with product_id
	products = get_object_or_404(Product, pk=product_id)
	return render(request, 'products/detail.html', {'product' : products})

# If they are not logged in, it will take them to Sign Up instead of 404
@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
	if request.method == 'POST':
		product = get_object_or_404(Product, pk=product_id)
		product.votes_total += 1
		product.save()
		return redirect('/products/' + str(product.id))


