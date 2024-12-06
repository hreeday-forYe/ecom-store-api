from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F
from django.db.models.aggregates import Count, Avg, Min, Max, Sum
from store.models import Product, OrderItem, Order

# Create your views here.

def hello_world(request):
  # query_set = Product.objects.all()
  # for product in query_set:
  #   print(product)
  # try:
  #   product = Product.objects.get(pk=1)
  # except ObjectDoesNotExist:
  #   # Show error to the user
  #   pass

  # product = Product.objects.filter(pk=0).first()
  # product = Product.objects.filter(pk=0)
  # product = Product.objects.filter(pk=0).exists()

  # QUery SEt in filtering 
  # query_set = Product.objects.filter(unit_price=20)
  # query_set = Product.objects.filter(unit_price_gt=20)
  
  # query_set = Product.objects.filter(collection__id__range = (1,2))
  # query_set= Product.objects.filter(unit_price__range=(20,30))

  # query_set = Product.objects.filter(title__contains = 'coffeee') # case sensitive
  query_set = Product.objects.filter(title__icontains = 'coffee') # case Insensitive

  # Filter Products with inventory < 10 and and Price < 20
  query_set = Product.objects.filter(inventory__lt=10, unit_price__lt=20)
  query_set = Product.objects.filter(inventory__lt=10).filter(unit_price__lt = 20)

  # Combine the conditions using or operator 
  # inventory < 10 or unit_price < 20
  query_set = Product.objects.filter(Q(inventory__lt = 10) | Q(unit_price__lt =20))

  # Referincing fields using F objects  FOR SAY PRODUCTS where inventory = price
  # Comparing two fields  we use f object 
  query_set = Product.objects.filter(inventory = F('unit_price'))

  # Reference a field in a related table 
  query_set = Product.objects.filter(inventory=F('collection__id'))


  # Sorting data
  query_set = Product.objects.order_by('unit_price','-title').reverse()

  query_set = Product.objects.filter(collection_id=3).order_by('unit_price').reverse()

  # sort the result and pick only the first object 
  # product = Product.objects.order_by('unit_price')[0]
  # Another way 
  product = Product.objects.filter(collection_id=4).earliest('unit_price') # SOrts in ascending and returns the top product as object 

  product = Product.objects.filter(collection_id=4).latest('unit_price') # Sorts in descending order and returns the top product as object 
  
  
  # Limiting Result 
  # Sometimes we want to only show fewer of the many result to the user for that we use limit list like syntax
  query_set = Product.objects.all()[:5] # Products on Index 0,1,2,3,4
  query_set = Product.objects.all()[5:10] # Products on INDEX 5, 6, 7, 8, 9
  
  # Selecting fields to query the products we can use values 
  query_set = Product.objects.values('id', 'title') # returns title and id in the form of dictionary
  query_set = Product.objects.values_list('id', 'title') # Returns title and id in the form of dictionary 
  # Getting the fields of the foreign key from Proeduct table 
  query_set = Product.objects.values('id', 'title', 'collection__title')


  # SELECT PRODUCTS THAT HVE BEEN ORDERED AND SORT BY title
  query_set = Product.objects.filter(id__in =OrderItem.objects.values('product__id').distinct()).order_by('title')

  query_set = Product.objects.only('id', 'title') # Returns only id and title
  query_set = Product.objects.defer('description') # Returns except description
  
  # This will create the inner join between product and collection preloading the collection table for easier access to the collection title of the product and not making 1000 queries to db
  query_set = Product.objects.select_related('collection').all()
  
  # When the other end of the objects has many items then we use the prefetch_select for say Product has only one collection so we use __ select_related() but when we have to utilize many to many relationship  and get the related objects we will use prefetch_realted
  query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()

  # Exercise get the last five orders with therir customer and items including product 
  query_set = Order.objects.select_related('customer').order_by('-placed_at')[:5].prefetch_related('orderitem_set__product')

# Count the number of products we have 
  result = Product.objects.aggregate(count=Count('id'))
  

  # Count the number of products we have in collection 1 
  result = Product.objects.filter(collection_id=6).aggregate(count=Count('id'),mini = Min('unit_price'), maxi=Max('inventory'), )
  

  # How many orders do we have 
  result = Order.objects.aggregate(Count('id'))

  # How many units of the product 1 we have sold 
  result = OrderItem.objects.filter(product_id=1).aggregate(units_sold = Sum('quantity'))

  # HOw many orders has the customer 1 placed
  result = Order.objects.filter(customer__id=1).aggregate(Count('id'))

  # what are the min max avg price of the products in collection 1 
  result = Product.objects.filter(collection__id=3).aggregate(Min('unit_price'), Max('unit_price'), Avg('unit_price'))
  print(result)
  

  return render(request, 'index.html', {'name':'Hello world','age':21, 'orders': list(query_set)})