from django.shortcuts import redirect, render, get_object_or_404, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
##
from store_app.models import *
from django.contrib import messages
## Cart
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import json
from django.urls import reverse
import uuid
from django.http import JsonResponse
from store_app.constants import ORDERSTATUS

def BASE(request):
    return render(request, 'Main/base.html')

def HOME(request):
    product = Product.objects.filter(status = 'Publish')
    context ={
        'product' : product,
    }
    return render(request, 'Main/index.html', context)


def choose(request):
    return render(request,'choose.html')

def Sign_up_client(request):
    return render(request,'Sign_up_client.html')

def Sign_up_business(request):
    return render(request,'Sign_up_business.html')


def HandleRegister(request):
    if request.method == "POST":
        first = request.POST.get('first')
        last = request.POST.get('last')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        
        
        customer = User.objects.create_user(username,email,password)
        customer.save()
        UserProfile.objects.create(user=customer, name=first,last=last,username=username,email=email,mobile=phone)
        messages.success(request, "Registeration Successful")
        
        return redirect('login')
    return render(request,'Sign_up_client.html')


def HandleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('u_account')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('HandleLogin')
    return render(request,'Sign_up_client.html')

#Admin 
def BusinessRegister(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        
        customer = User.objects.create_user(username,email,password)
        customer.save()
        return redirect('b_login')
        
    return render(request,'Sign_up_business.html')

def BusinessLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username,password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Business Login successful!")
            return redirect('adminbase')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('b_login')
    return render(request,'Sign_up_business.html')

def logoutuser(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('index')

def worklogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')  # This comes from the dropdown

        # Authenticate user credentials
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is registered in the Designer table and role matches
            try:
                worker = Designer.objects.get(user=user)
                if str(worker.role_p) == str(role):  # Match role ID as string for consistency
                    login(request, user)
                    messages.success(request, "Worker Login successful!")
                    return redirect('workerBase')
                else:
                    messages.error(request, "Role mismatch. Please check your role.")
                    return redirect('worker_login')

            except Designer.DoesNotExist:
                messages.error(request, "You are not registered as a worker.")
                return redirect('worker_login')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect('worker_login')

    # For GET request, render login page with role options
    return render(request, 'worker_login.html', {'ORDERSTATUS': ORDERSTATUS})

def Work_choose(request):
    return render(request,'worker_choose.html')


# Start fillup content

def about(request):
    return render(request,'Main/about.html')

def contact(request):
    return render(request,'Main/contact.html')

#Product
def tshirts(request):
    return render(request,'Product/tshirts.html')

def Lower(request):
    return render(request,'Product/Lower.html')

def kabaddi(request):
    products = Product.objects.filter(category__name="Kabaddi", status="Publish")
    return render(request, 'Product/Kabaddi.html', {'products': products})
def single_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    context = {'product': product}
    return render(request, 'Product/single_product.html', context)



# User Part
def u_account(request):
    return render(request,'User/my-account.html')

# def u_cart(request):
#     return render(request,'User/cart.html')

def u_checkout(request):
    return render(request,'User/checkout.html')

def u_wishlist(request):
    return render(request,'User/wishlist.html')

#Admin
def adminBase(request): #----->admin base
    return render(request, 'admin/admin_base.html')

def a_dashboard(request): #----->admin base
    return render(request, 'admin/a_dashboard.html')

def add_category(request):
    if request.method == "POST":
        name = request.POST['name']
        Category.objects.create(name=name)
        messages.success(request, "Category added")
        return redirect('view_category')
    return render(request, 'admin/Category.html', locals())

def view_category(request):
    category = Category.objects.all()
    return render(request, 'admin/view_category.html', locals())

def edit_category(request, pid):
    category = Category.objects.get(id=pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        messages.success(request, "Category Updated")
        return redirect('view_category')
    return render(request, 'admin/edit_category.html', locals())

def delete_category(request, pid):
    category = Category.objects.get(id=pid)
    category.delete()
    messages.success(request, "Category Deleted")
    return redirect('view_category')

def add_product(request):
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        image = request.FILES['image']
        catobj = Category.objects.get(id=cat)
        Product.objects.create(name=name, price=price, discount=discount, category=catobj, description=desc, image=image)
        messages.success(request, "Product added")
    return render(request, 'admin/add_product.html', locals())

def view_product(request):
    product = Product.objects.all()
    return render(request, 'admin/view_product.html', locals())

def edit_product(request, pid):
    product = Product.objects.get(id=pid)
    category = Category.objects.all()
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        cat = request.POST['category']
        discount = request.POST['discount']
        desc = request.POST['desc']
        try:
            image = request.FILES['image']
            product.image = image
            product.save()
        except:
            pass
        catobj = Category.objects.get(id=cat)
        Product.objects.filter(id=pid).update(name=name, price=price, discount=discount, category=catobj, description=desc)
        messages.success(request, "Product Updated")
        return redirect('view_product')
    return render(request, 'admin/edit_product.html', locals())

def delete_product(request, pid):
    product = Product.objects.get(id=pid)
    product.delete()
    messages.success(request, "Product Deleted")
    return redirect('view_product')

#Worker
#Regitraion
def workers_pro(request):
    if request.method == "POST":
        designer_name = request.POST.get('work_name')
        role = request.POST.get('role')  # This will get the selected role's id (as a string)
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        pic = request.FILES.get('profil_pic')
        
        
        customer = User.objects.create_user(username=designer_name,email=email,password=contact,first_name=designer_name)
        customer.save()
        # Saving the new Designer instance
        Designer.objects.create(
            user=customer,
            designer_name=designer_name,
            role_p=role,  # This will save the role as an integer
            contact=contact,
            email=email,
            profile_pic=pic
        )
        messages.success(request, "Worker Registration Successful")
    return render(request, 'admin/workers_assign.html', {'ORDERSTATUS': ORDERSTATUS})

# customer = User.objects.create_user(username,email,password)#Remain
#         customer.save()
#         UserProfile.objects.create(user=customer, name=first,last=last,username=username,email=email,mobile=phone)

def worker_view(request):
    yt=Designer.objects.all()
    return render(request, 'admin/worker_view.html',{'yt':yt})

def workerBase(request): #----->admin base
    if request.user.is_authenticated:
            worker = Designer.objects.get(user=request.user)
            role = worker.role_p
    return render(request, 'admin/worker_admin_base.html',{'role':role})

def admin_manage(request):
    # Check if the user is logged in
    if request.user.is_authenticated:
        try:
            # Get the worker's role from the Designer table
            worker = Designer.objects.get(user=request.user)
            role = worker.role_p  # Assuming 'role_p' represents the worker's role
            
            # Map role to a human-readable format if needed
            ROLE_NAMES = {
                "1": "Designer",
                "2": "Fusing",
                "3": "Making",
                "4": "Printing",
                "5": "Dispatch",
                "6": "Delivery"
            }
            role_name = ROLE_NAMES.get(str(role), "Unknown Role")
            
            # Filter data based on the worker's role
            table_data = Order.objects.filter(status=role)  # Replace 'TableData' with your actual model
        except Designer.DoesNotExist:
            messages.error(request, "You are not registered as a worker.")
            return redirect('worklogin')
    else:
        messages.error(request, "You need to log in first.")
        return redirect('worklogin')

    # Render the worker_admin_base.html with filtered table data
    return render(request, 'admin/worker_manage_ordered.html', {'table_data': table_data,'role':role_name})


# def admin_manage(request): #----->   manage_order
#     action = request.GET.get('action', 0)
#     order = Order.objects.filter(status=int(action))
#     order_status = ORDERSTATUS[int(action)-1][1]
#     return render(request, 'admin/worker_manage_ordered.html', locals())


def change_order_status(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id)
        current_status = order.status
        next_status = current_status + 1

        # Ensure the next status is within the valid range
        if next_status > len(ORDERSTATUS):
            return JsonResponse({'error': 'Status cannot be changed further.'}, status=400)

        # Update the status and save
        order.status = next_status
        order.save()

        return JsonResponse({'message': 'Status updated successfully.', 'status': next_status})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

#Worker Login



#19 Django Multi Vendor Ecommerce Project - Django Shopping Cart Project | Cart | Hindi
@login_required(login_url="/users/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="/users/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/users/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/users/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/users/login/")
def cart_detail(request):
    return render(request, 'User/cart_detail.html')
# @login_required(login_url="/users/login/")
# def cart_detail(request):
#     cart = request.session.get('cart', {})
#     context = {
#         'cart_items': cart.items(),  # Ensure you pass items correctly
#     }
#     return render(request, 'User/cart_detail.html', context)

def CheckOut(request): # -> Cart Collect User Items
    if request.method == "POST":
        phone = request.POST.get('phone')
        prod_des = request.POST.get('prod_des')
        address = request.POST.get('addres')
        cart = request.session.get('cart')
        # uid = request.session.get('_auth_user_id')
        user = User.objects.get(username=request.user.username)
        user_profile = UserProfile.objects.get(user=user)
        for i in cart:
            print('Cart:{{{',i,'}}} End')
            # Modify the image address
            original_image_url = cart[i]['image']
            modified_image_url = original_image_url.replace('/media/', '')
            print('<<<<<<<<<---',modified_image_url,'->>>>>>>>>')
            order= Order(
                user= user,
                user_p=user_profile,  # Add this line
                product= cart[i]['name'],
                quantity = cart[i]['quantity'],
                # image = cart[i]['image'],
                image=modified_image_url,
                phone=phone,
                product_description=prod_des,
                address=address,
            )
            order.save()
        request.session['cart']={}
            
        return redirect('index')
    return HttpResponse('This is checkout page')


#User order
def Your_Order(request):
#     uid = request.session.get('_auth_user_id') -> he cha av ji he downard

    user = User.objects.get(username=request.user.username)
    order = Order.objects.filter(user=user)
    print(user,order)
    context ={
        'order': order,
    }
    return render(request,"User/ordered_user.html",context)

#admin manage Order User(client)
def manage_order(request):
    action = request.GET.get('action', 0)
    order = Order.objects.filter(status=int(action))
    order_status = ORDERSTATUS[int(action)-1][1]
    if int(action) == 0:
        order = Order.objects.filter()
        order_status = 'All'
    return render(request, 'admin/manage_ordered.html', locals()) 

def delete_order(request, pid):
    order = Order.objects.get(id=pid)
    order.delete()
    messages.success(request, 'Order Deleted')
    return redirect('/manage-order/?action='+request.GET.get('action'))

def user_order_track(request, pid):
    order = Order.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    return render(request, "User/user-order-track.html", locals())

def admin_order_track(request, pid):
    order = Order.objects.get(id=pid)
    orderstatus = ORDERSTATUS
    status = int(request.GET.get('status',0))
    if status:
        order.status = status
        order.save()
        return redirect('admin_order_track', pid)
    print('order: ',order,'orderstatus: ',orderstatus, 'status: ',status, '::::',order.status)
    return render(request, 'admin/admin-order-track.html', locals()) 

def manage_user(request):
    userprofile = UserProfile.objects.all()
    return render(request, 'admin/manage_user.html', locals())

def delete_user(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    messages.success(request, "User deleted successfully")
    return redirect('manage_user')

#Workers -<<<
# def designer(request):
#     cate = Category.objects.all()
#     return render(request,'workers/designer_add.html',locals())

# def designer(request):
#     if request.method == 'POST':
#         designer_name = request.POST['designer_name']
#         category_id = request.POST['category']
#         design_name = request.POST['design_name']
#         desc = request.POST['desc']
#         front_image = request.FILES['front_image']
#         back_image = request.FILES.get('back_image')
#         sleeve_image = request.FILES.get('sleeve_image')
#         sample_images = request.FILES.getlist('sample_images')

#         try:
#             category = Category.objects.get(id=category_id)
#             tshirt_design = TShirtDesign.objects.create(
#                 designer_name=designer_name,
#                 category=category,
#                 design_name=design_name,
#                 desc=desc,
#                 front_image=front_image,
#                 back_image=back_image,
#                 sleeve_image=sleeve_image,
#             )

#             for image in sample_images:
#                 TShirtDesign.objects.create(
#                     designer_name=designer_name,
#                     category=category,
#                     design_name=f'{design_name} Sample',
#                     desc=desc,
#                     front_image=image
#                 )

#             messages.success(request, 'T-shirt design added successfully!')
#             return redirect('designer') #add ->>
#         except Category.DoesNotExist:
#             messages.error(request, 'Invalid category selected.')

#     cate = Category.objects.all()
#     return render(request, 'workers/designer_add.html', {'cate': cate})


# def designer_view(request):
#     designer=TShirtDesign.objects.all()
#     return render(request,'workers/designer_view.html', {'designer': designer})

#GPT T-Shirt
# def add_design(request):
#     categories = Category.objects.all()
#     if request.method == "POST":
#         designer_name = request.POST['designer_name']
#         category = get_object_or_404(Category, id=request.POST['category'])
#         design_name = request.POST['design_name']
#         desc = request.POST['desc']
#         front_image = request.FILES['front_image']
#         back_image = request.FILES.get('back_image')
#         sleeve_image = request.FILES.get('sleeve_image')
#         sample_images = request.FILES.getlist('sample_images')

#         design = TShirtDesign.objects.create(
#             designer_name=designer_name,
#             category=category,
#             design_name=design_name,
#             desc=desc,
#             front_image=front_image,
#             back_image=back_image,
#             sleeve_image=sleeve_image
#         )
#         for image in sample_images:
#             design.sample_images.save(image.name, image)

#         messages.success(request, 'Design submitted successfully!')
#         return redirect('add_design')

#     return render(request, 'workers/designer_add.html', {'cate': categories})

#GPT T-Shirt
# def add_design(request):
#     categories = Category.objects.all()
#     if request.method == "POST":
#         designer_name = request.POST['designer_name']
#         category = get_object_or_404(Category, id=request.POST['category'])
#         design_name = request.POST['design_name']
#         desc = request.POST['desc']
#         front_image = request.FILES['front_image']
#         back_image = request.FILES.get('back_image')
#         sleeve_image = request.FILES.get('sleeve_image')
#         sample_images = request.FILES.getlist('sample_images')

#         design = TShirtDesign.objects.create(
#             designer_name=designer_name,
#             category=category,
#             design_name=design_name,
#             desc=desc,
#             front_image=front_image,
#             back_image=back_image,
#             sleeve_image=sleeve_image
#         )

#         for img in sample_images:
#             sample = SampleImage.objects.create(design=design, image=img)
#             design.sample_images.add(sample)

#         design.save()
#         messages.success(request, 'Design submitted successfully!')
#         return redirect('add_design')

#     return render(request, 'workers/designer_add.html', {'cate': categories})

# from django.shortcuts import render, redirect, get_object_or_404
# from .models import TShirtDesign, Category, SampleImage
# from django.contrib import messages

#######    Previ ous  ###########
# def add_design(request):
#     categories = Category.objects.all()

#     if request.method == "POST":
#         # Get form data
#         designer_name = request.POST['designer_name']
#         contact = request.POST.get('contact')
#         email = request.POST.get('email')
#         category = get_object_or_404(Category, id=request.POST['category'])
#         design_name = request.POST['design_name']
#         desc = request.POST['desc']

#         # Handle uploaded files
#         front_image = request.FILES['front_image']
#         back_image = request.FILES.get('back_image')
#         sleeve_image = request.FILES.get('sleeve_image')
#         sample = request.FILES.getlist('sample_images')

#         # Create TShirtDesign entry
#         design = TShirtDesign.objects.create(
#             designer_name=designer_name,
#             contact=contact,
#             email=email,
#             category=category,
#             design_name=design_name,
#             desc=desc,
#             front_image=front_image,
#             back_image=back_image,
#             sleeve_image=sleeve_image
#         )

#         # Save multiple sample images
#         for img in sample:
#             TShirtDesign.objects.create(sample_images=img)

#         messages.success(request, 'Design submitted successfully!')
#         return redirect('add_design')

#     return render(request, 'workers/designer_add.html', {'cate': categories})
#######    Previ ous  ###########


# def view_design(request, design_id):
#     designer = get_object_or_404(TShirtDesign, id=design_id)
#     if request.method == "POST":
#         status = request.POST['status']
#         designer.status = status
#         designer.save()
#         messages.success(request, 'Designer status updated successfully!')
#         return redirect('view_design', design_id=designer.id)

#     return render(request, 'workers/designer_view.html', {'designer': designer})

#######    Previ ous  ###########
# def list_designs(request):
#     designs = TShirtDesign.objects.all()
#     return render(request, 'workers/designer_view.html', locals())
#######    Previ ous  ###########



#Workers Add
def add_design(request):
    if request.method == "POST":
        designer_name = request.POST.get('designer_name')
        design_name = request.POST.get('design_name')
        category_id = request.POST.get('category')
        desc = request.POST.get('desc')
        role = request.POST.get('role')
        front_image = request.FILES.get('front_image')
        back_image = request.FILES.get('back_image')
        sample_files = request.FILES.getlist('sample_images')

        category = get_object_or_404(Category, id=category_id)
        designer, _ = Designer.objects.get_or_create(designer_name=designer_name)
        design = Design.objects.create(
            designer=designer,
            category=category,
            design_name=design_name,
            role=role,
            desc=desc,
            front_image=front_image,
            back_image=back_image,
        )

        for file in sample_files:
            sample_image = SampleImage.objects.create(image=file)
            design.sample_images.add(sample_image)

        design.save()
        messages.success(request, 'Design added successfully!')
        return redirect('view_designs')

    categories = Category.objects.all()
    return render(request, 'workers/designer_add.html', {'cate': categories})

def view_designs(request):
    designs = Design.objects.prefetch_related('sample_images').select_related('designer').all()
    return render(request, 'workers/designer_view.html', {'designs': designs})

def fusing(request):
    if request.method == "POST":
        designer_name = request.POST.get('designer_name')
        design_name = request.POST.get('design_name')
        category_id = request.POST.get('category')
        desc = request.POST.get('desc')
        role = request.POST.get('role')
        front_image = request.FILES.get('front_image')
        back_image = request.FILES.get('back_image')
        sample_files = request.FILES.getlist('sample_images')

        category = get_object_or_404(Category, id=category_id)
        designer, _ = Designer.objects.get_or_create(designer_name=designer_name)
        design = Design.objects.create(
            designer=designer,
            category=category,
            design_name=design_name,
            role=role,
            desc=desc,
            front_image=front_image,
            back_image=back_image,
        )

        for file in sample_files:
            sample_image = SampleImage.objects.create(image=file)
            design.sample_images.add(sample_image)

        design.save()
        messages.success(request, 'Design added successfully!')
        return redirect('view_designs')

    categories = Category.objects.all()
    return render(request, 'workers/fusing_add.html', {'cate': categories})

def fusing_view(request):
    designs = Design.objects.prefetch_related('sample_images').select_related('designer').filter(role='Fusing').all()
    return render(request, 'workers/fusing_view.html', {'designs': designs})

def update_status(request, design_id):
    if request.method == "POST":
        status = request.POST.get('status')
        design = get_object_or_404(Design, id=design_id)
        design.status = status
        design.save()
        messages.success(request, 'Design status updated successfully!')
        return redirect('view_designs')

def approved_designs(request):
    designs = Design.objects.filter(status="Approved").select_related('designer').prefetch_related('sample_images')
    return render(request, 'workers/work_doned_designer.html', {'designs': designs})


def fusing(request):
    return render(request, 'workers/fusing_add.html')
def making(request):
    return render(request, 'workers/making_add.html')
def printing(request):
    return render(request, 'workers/printing_add.html')
def dispatch(request):
    return render(request, 'workers/dispatch.html')





def fusing_view(request):
    return render(request, 'workers/fusing_view.html')
def making_view(request):
    return render(request, 'workers/making_view.html')
def printing_view(request):
    return render(request, 'workers/printing_view.html')
def dispatch_view(request):
    return render(request, 'workers/dispatch_view.html')
