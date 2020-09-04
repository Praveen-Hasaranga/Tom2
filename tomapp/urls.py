from django.urls import path, include
from . import views

urlpatterns = [

    # common page urls
    path('index', views.index_view, name='index'),

    # urls for the sales person view
    path('sales_person_view', views.SalesPerson, name='sales_person_view'),
    path('move_to_que/<str:pk>', views.MoveToQueue, name='move_to_que'),
    path('move_to_reg/<str:pk>', views.MoveToReg, name='move_to_reg'),

    # urls for the production manager view
    path('production_manager_view', views.ProductionManager, name='production_manager_view'),
    path('ws_split/<str:pk>', views.SplitWorkShop, name='ws_split'),
    path('move_to_ws/<str:pk>', views.MoveToWorkShop, name='move_to_ws'),
    path('move_to_qw/<str:pk>', views.MoveToQueueW, name='move_to_qw'),
    path('move_to_wip/<str:pk>', views.MoveToWIP, name='move_to_wip'),

    # urls for the production engineer view
    path('production_engineer_view', views.ProductionEngineer, name='production_engineer_view'),
    path('move_to_comp/<str:pk>', views.MoveToComplete, name='move_to_comp'),
    path('move_to_invoice/<str:pk>', views.MoveToInvoice, name='move_to_invoice'),
    path('wip_split/<str:pk>', views.SplitWIP, name='wip_split'),
    path('pause_job/<str:pk>', views.PauseWIP, name='pause_job'),
    path('resume_job/<str:pk>', views.ResumeWIP, name='resume_job'),

    # urls for the accountant view
    path('accountant_view', views.Accountant, name='accountant_view'),
    path('move_to_invoice_comp/<str:pk>', views.MoveToInvoiceComp, name='move_to_invoice_comp'),

]
