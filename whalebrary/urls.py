from . import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'whalebrary'

urlpatterns = [
    path('close/', views.CloserTemplateView.as_view(), name="close_me"),
    path('', views.index, name="index"),

    # SETTINGS #

    path('admin_tools', views.admin_tools, name="admin_tools"),
    path('settings/locations/', views.LocationFormsetView.as_view(), name="manage_locations"),
    path('settings/location/<int:pk>/delete/', views.LocationHardDeleteView.as_view(), name="delete_location"),
    path('settings/tags/', views.TagFormsetView.as_view(), name="manage_tags"),
    path('settings/tag/<int:pk>/delete/', views.TagHardDeleteView.as_view(), name="delete_tag"),
    path('settings/owners/', views.OwnerFormsetView.as_view(), name="manage_owners"),
    path('settings/owner/<int:pk>/delete/', views.OwnerHardDeleteView.as_view(), name="delete_owner"),
    path('settings/sizes/', views.SizeFormsetView.as_view(), name="manage_sizes"),
    path('settings/size/<int:pk>/delete/', views.SizeHardDeleteView.as_view(), name="delete_size"),
    path('settings/organisations/', views.OrganisationFormsetView.as_view(), name="manage_organisations"),
    path('settings/organisation/<int:pk>/delete/', views.OrganisationHardDeleteView.as_view(), name="delete_organisation"),
    path('settings/trainings/', views.TrainingFormsetView.as_view(), name="manage_trainings"),
    path('settings/training/<int:pk>/delete/', views.TrainingHardDeleteView.as_view(), name="delete_training"),
    path('settings/species/', views.SpeciesFormsetView.as_view(), name="manage_species"),
    path('settings/species/<int:pk>/delete/', views.SpeciesHardDeleteView.as_view(), name="delete_species"),

    # ADMIN USERS #
    path('settings/users/', views.UserListView.as_view(), name='user_list'),
    path('settings/users/whalebrary/<int:whalebrary>/', views.UserListView.as_view(), name='user_list'),
    path('settings/user/<int:pk>/toggle/<str:type>/', views.toggle_user, name='toggle_user'),


    # ITEMS #

    path('item_list/', views.ItemListView.as_view(), name="item_list"),
    path('item/<int:pk>/transaction-list/', views.ItemTransactionListView.as_view(),
         name="item_transaction_detail"),
    path('item_detail/<int:pk>/view/', views.ItemDetailView.as_view(), name="item_detail"),
    path('item/new/', views.ItemCreateView.as_view(), name="item_new"),
    path('item/<int:pk>/edit/', views.ItemUpdateView.as_view(), name="item_edit"),
    path('item/<int:pk>/delete/', views.ItemDeleteView.as_view(), name="item_delete"),
    path('supplier/<int:supplier>/to/item/<int:item>/', views.add_supplier_to_item, name="add_supplier_to_item"),
    path('item/<int:item>/add-suppliers', views.AddSuppliersToItemView.as_view(), name="item_suppliers_list"),
    path('supplier/<int:supplier>/from/item/<int:item>/', views.remove_supplier_from_item, name="remove_supplier_from_item"),
    path('item_list/download-csv', views.inventory_download, name="inventory_download"),

    # TRANSACTIONS #

    path('transaction_list/', views.TransactionListView.as_view(), name="transaction_list"),
    path('transaction_detail/<int:pk>/view/', views.TransactionDetailView.as_view(), name="transaction_detail"),
    path('item/<int:pk>/transaction/new/', views.TransactionCreateView.as_view(), name="transaction_new"),
    path('transaction/new/', views.TransactionCreateView.as_view(), name="transaction_new"),
    path('transaction/<int:pk>/edit/', views.TransactionUpdateView.as_view(), name="transaction_edit"),
    # path('transaction/<int:pk>/edit/pop/<int:pop>/', views.TransactionUpdatePopoutView.as_view(), name="transaction_edit"),
    path('transaction/<int:pk>/receive/order/<int:pop>/', views.OrderReceivedTransactionUpdateView.as_view(), name="transaction_edit"),
    path('transaction/<int:pk>/delete/pop/<int:pop>/', views.TransactionDeletePopoutView.as_view(), name="transaction_delete"),
    path('transaction/<int:pk>/delete/', views.TransactionDeleteView.as_view(), name="transaction_delete"),
    path('transaction/return/item/<int:transaction>/', views.lending_return_item, name="lending_return_item"),
    path('transaction/lend/item/<int:pk>/', views.TransactionLendCreateView.as_view(), name="transaction_lend"),

    # BULK TRANSACTIONS #

    path('bulk_transaction_list/', views.BulkTransactionListView.as_view(), name="bulk_transaction_list"),
    # path('bulk_transaction_detail/<int:pk>/view/', views.BulkTransactionDetailView.as_view(), name="bulk_transaction_detail"),
    path('bulk_transaction/<int:pk>/delete/', views.BulkTransactionDeleteView.as_view(), name="bulk_transaction_delete"),

    # ORDER #

    path('order_list/', views.OrderListView.as_view(), name="order_list"),
    path('order_detail/<int:pk>/view/', views.OrderDetailView.as_view(), name="order_detail"),
    path('order/new/', views.OrderCreateView.as_view(), name="order_new"),
    path('item/<int:pk>/order/new/', views.OrderCreateView.as_view(), name="order_new"),
    path('order/<int:pk>/edit/', views.OrderUpdateView.as_view(), name="order_edit"),
    path('order/<int:pk>/edit/pop/<int:pop>/', views.OrderUpdatePopoutView.as_view(), name="order_edit"),
    path('order/<int:pk>/delete/pop/<int:pop>/', views.OrderDeletePopoutView.as_view(), name="order_delete"),
    path('order/<int:pk>/delete/', views.OrderDeleteView.as_view(), name="order_delete"),
    path('order/<int:order>/received/', views.mark_order_received,
         name="mark_order_received"),


    # LOCATION #

    path('location_list/', views.LocationListView.as_view(), name="location_list"),
    path('location_detail/<int:pk>/view/', views.LocationDetailView.as_view(), name="location_detail"),
    path('location/new/', views.LocationCreateView.as_view(), name="location_new"),
    path('location/<int:pk>/edit/', views.LocationUpdateView.as_view(), name="location_edit"),
    path('location/<int:pk>/delete/', views.LocationDeleteView.as_view(), name="location_delete"),

    # PERSONNEL #

    path('personnel_list/', views.PersonnelListView.as_view(), name="personnel_list"),
    path('personnel_detail/<int:pk>/view/', views.PersonnelDetailView.as_view(), name="personnel_detail"),
    path('personnel/new/', views.PersonnelCreateView.as_view(), name="personnel_new"),
    path('personnel/<int:pk>/edit/', views.PersonnelUpdateView.as_view(), name="personnel_edit"),
    path('personnel/<int:pk>/delete/', views.PersonnelDeleteView.as_view(), name="personnel_delete"),

    # SUPPLIER #

    path('supplier_list/', views.SupplierListView.as_view(), name="supplier_list"),
    path('supplier_detail/<int:pk>/view/', views.SupplierDetailView.as_view(), name="supplier_detail"),
    path('supplier/new/', views.SupplierCreateView.as_view(), name="supplier_new"),
    path('item/<int:pk>/supplier/new/', views.SupplierCreateView.as_view(), name="supplier_new"),
    path('supplier/<int:pk>/edit/', views.SupplierUpdateView.as_view(), name="supplier_edit"),
    path('supplier/<int:pk>/edit/pop/<int:pop>/', views.SupplierUpdatePopoutView.as_view(), name="supplier_edit"),
    path('supplier/<int:pk>/delete/pop/<int:pop>/', views.SupplierDeletePopoutView.as_view(), name="supplier_delete"),
    path('supplier/<int:pk>/delete/', views.SupplierDeleteView.as_view(), name="supplier_delete"),

    # ITEM FILES #

    path('file_list/', views.FileListView.as_view(), name="file_list"),
    path('item/<int:item>/file/new/', views.FileCreateView.as_view(), name="file_new"),
    path('file/<int:pk>/edit/', views.FileUpdateView.as_view(), name="file_edit"),
    path('file/<int:pk>/delete/', views.FileDeleteView.as_view(), name="file_delete"),


    # INCIDENT #

    path('incident_list/', views.IncidentListView.as_view(), name="incident_list"),
    path('incident_detail/<int:pk>/view/', views.IncidentDetailView.as_view(), name="incident_detail"),
    path('incident/new/', views.IncidentCreateView.as_view(), name="incident_new"),
    path('incident/<int:pk>/edit/', views.IncidentUpdateView.as_view(), name="incident_edit"),
    path('incident/<int:pk>/delete/', views.IncidentDeleteView.as_view(), name="incident_delete"),
    path('incident/<int:pk>/email/', views.send_incident_email, name="incident_email"),

    # INCIDENT IMAGES #

    path('image_list/', views.ImageListView.as_view(), name="image_list"),
    path('incident/<int:incident>/image/new/', views.ImageCreateView.as_view(), name="image_new"),
    path('image/<int:pk>/edit/', views.ImageUpdateView.as_view(), name="image_edit"),
    path('image/<int:pk>/delete/', views.ImageDeleteView.as_view(), name="image_delete"),

    # REPORTS #

    path('reports/generator/', views.ReportGeneratorFormView.as_view(), name="report_generator"),
    path('reports/generator/<int:report_number>/', views.ReportGeneratorFormView.as_view(), name="report_generator"),
    path('reports/container_summary/location/<int:location>/', views.ContainerSummaryListView.as_view(), name="report_container"),
    path('reports/sized_item_summary/item_name/<slug:item_name>/', views.SizedItemSummaryListView.as_view(), name="report_sized_item"),




]

