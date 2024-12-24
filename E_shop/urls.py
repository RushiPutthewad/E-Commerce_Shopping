from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("base/", views.BASE, name='base'),
    path("", views.HOME, name='index'),
    
    path("SignUp_client/", views.Sign_up_client,name='Sign_up_client'),
    path("Sign_up_business/", views.Sign_up_business,name='Sign_up_business'),
    path("Register/", views.HandleRegister,name='Register'),
    path("login/", views.HandleLogin,name='HandleLogin'),
    path('logout/', views.logoutuser, name="logout"),
    path("Worker-Login/", views.worklogin,name='worklogin'),
    
    
    path("choose/", views.choose,name='choose'),
    path("Worker-Choose/", views.Work_choose,name='Work_choose'),
    
    #admin
    path('adminhome/', views.adminBase, name="adminbase"),  #admin Base
    path("Business-Register/", views.BusinessRegister,name='b_Register'),
    path("Business-login/", views.BusinessLogin,name='b_login'),
    path("Dashboard/", views.a_dashboard,name='a_dashboard'),
    path("Category/", views.add_category,name='category'),
    path('Workers-Form/', views.workers_pro, name='workers_pro'),
    path('worker_view/', views.worker_view, name='worker_view'),
    path('View-category/', views.view_category, name="view_category"),
    path('edit-category/<int:pid>/', views.edit_category, name="edit_category"),
    path('delete-category/<int:pid>/', views.delete_category, name="delete_category"),
    path('add-product/', views.add_product, name='add_product'),
    path('view-product/', views.view_product, name='view_product'),
    path('edit-product/<int:pid>/', views.edit_product, name="edit_product"),
    path('delete-product/<int:pid>/', views.delete_product, name="delete_product"),
    
    path('manage-order/', views.manage_order, name="manage_order"),
    path('delete-order/<int:pid>/', views.delete_order, name="delete_order"), 
    
    
    path("about/", views.about,name='about'),
    path("contact/", views.contact,name='contact'),
    
    #Product
    path("T-Shirt/", views.tshirts,name='tshirts'),
    path("Lower/", views.Lower,name='Lower'),
    path("Kabaddi/", views.kabaddi,name='kabaddi'),
    path('single-product/<uuid:product_id>/', views.single_product, name='single_product'),
    
    
    # User Part
    path("Account/", views.u_account,name='u_account'),
    # path("Cart/", views.u_cart,name='u_cart'),
    path("Checkout/", views.u_checkout,name='u_checkout'),
    path("Wishlist/", views.u_wishlist,name='u_wishlist'),
    
    # User Pause
    path('User-Order/', views.Your_Order, name="your_order"),
    
    #Workers
    # path('Designer/', views.designer, name="designer"),
    # path('Designer-View/', views.designer_view, name="designer_view"),
    
    
    # path('Designer-View/<int:designer_id>/', views.designer_view, name="designer_detail"),
    # path('designer/<int:designer_id>/', views.designer_view, name='designer_detail'),
    
    #######    Previ ous  ###########
    # path('add-design/', views.add_design, name='add_design'),
    # # path('view-design/<int:design_id>/', views.view_design, name='view_design'),
    # path('list-designs/', views.list_designs, name='list_designs'),
    #######    Previ ous  ###########
    
    
    path('add/', views.add_design, name='add_design'),
    path('view/', views.view_designs, name='view_designs'),
    path('update/<int:design_id>/', views.update_status, name='update_status'),
    
    path('approved-designs/', views.approved_designs, name='approved_designs'),#->> adress not define in side bar admin
    
    #Stages
    #Add
    path('fusing/', views.fusing, name='fusing'),
    path('making/', views.making, name='making'),
    path('printing/', views.printing, name='printing'),
    path('dispatch/', views.dispatch, name='dispatch'),
    #View
    path('fusing-view/', views.fusing_view, name='fusing_view'),
    path('making-view/', views.making_view, name='making_view'),
    path('printing-view/', views.printing_view, name='printing_view'),
    path('dispatch-view/', views.dispatch_view, name='dispatch_view'),
    path('Worker-admin/', views.workerBase, name='workerBase'),
    path('Worker-admin/manage-order/', views.admin_manage, name='admin_manage'),
    path('change-order-status/<int:order_id>/', views.change_order_status, name='change_order_status'),
    
    
    #New Think Cart
    # path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    # path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    # path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    # path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    # path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    # path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    
    #gpt cart 
    # path('cart/', views.cart_view, name='view_cart'),
    # path('checkout/', views.checkout, name='checkout'),
    # path('order-confirmation/<uuid:order_id>/', views.order_confirmation, name='order_confirmation'),
    
    #19 Django Multi Vendor Ecommerce Project - Django Shopping Cart Project | Cart | Hindi
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),
    
    path('CheckOut/', views.CheckOut, name='CheckOut'),
    
    path('user-order-track/<int:pid>/', views.user_order_track, name="user_order_track"),
    path('admin-order-track/<int:pid>/', views.admin_order_track, name="admin_order_track"),
    path('manage-user/', views.manage_user, name="manage_user"),
    path('delete-user/<int:pid>/', views.delete_user, name="delete_user"),
 
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
