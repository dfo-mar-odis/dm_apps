from django.urls import path
from . import views, utils

app_name = 'whalesdb'

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),

    # CRUISES #
    ###########
    path('list/cru/', views.CruList.as_view(), name="list_cru"),
    path('create/cru/', views.CruCreate.as_view(), name="create_cru"),
    path('details/cru/<int:pk>/', views.CruDetails.as_view(), name="details_cru"),
    path('update/cru/<int:pk>/', views.CruUpdate.as_view(), name="update_cru"),
    path('delete/cru/<int:pk>/', views.CruDelete.as_view(), name="delete_cru"),

    path('create/dep/', views.DepCreate.as_view(), name="create_dep"),
    path('create/dep/<str:pop>/', views.DepCreate.as_view(), name="create_dep"),
    path('update/dep/<int:pk>/', views.DepUpdate.as_view(), name="update_dep"),
    path('update/dep/<int:pk>/<str:pop>/', views.DepUpdate.as_view(), name="update_dep"),
    path('details/dep/<int:pk>/', views.DepDetails.as_view(), name="details_dep"),
    path('list/dep/', views.DepList.as_view(), name="list_dep"),

    path('list/eca/', views.EcaList.as_view(), name="list_eca"),
    path('create/eca/', views.EcaCreate.as_view(), name="create_eca"),
    path('update/eca/<int:pk>/', views.EcaUpdate.as_view(), name="update_eca"),
    path('details/eca/<int:pk>/', views.EcaDetails.as_view(), name="details_eca"),

    path('create/ecp/<int:eqr>/<str:pop>/', views.EcpCreate.as_view(), name="create_ecp"),

    path('create/ecc/<int:eca>/<str:pop>/', views.EccCreate.as_view(), name="create_ecc"),
    path('delete/ecc/<int:pk>/', views.ecc_delete, name="delete_ecc"),

    path('create/eda/<int:dep>/', views.EdaCreate.as_view(), name="create_eda"),
    path('create/eda/<int:dep>/<str:pop>/', views.EdaCreate.as_view(), name="create_eda"),
    path('delete/eda/<int:pk>/', views.eda_delete, name="delete_eda"),

    path('create/emm/', views.EmmCreate.as_view(), name="create_emm"),
    path('create/emm/<str:pop>/', views.EmmCreate.as_view(), name="create_emm"),
    path('update/emm/<int:pk>/', views.EmmUpdate.as_view(), name="update_emm"),
    path('details/emm/<int:pk>/', views.EmmDetails.as_view(), name="details_emm"),
    path('list/emm/', views.EmmList.as_view(), name="list_emm"),

    path('create/ehe/<int:rec>/<int:ecp_channel_no>/<str:pop>/', views.EheCreate.as_view(), name="create_ehe"),
    path('remove/ehe/<int:pk>/<str:pop>/', views.EheUpdateRemove.as_view(), name="remove_ehe"),

    path('create/eqh/<int:pk>/<str:pop>/', views.EqhCreate.as_view(), name="create_eqh"),
    path('update/eqh/<int:pk>/<str:pop>/', views.EqhUpdate.as_view(), name="update_eqh"),

    path('create/eqo/<str:pop>/', views.EqoCreate.as_view(), name="create_eqo"),

    path('create/eqp/', views.EqpCreate.as_view(), name="create_eqp"),
    path('update/eqp/<int:pk>/', views.EqpUpdate.as_view(), name="update_eqp"),
    path('update/eqp/<int:pk>/<str:pop>/', views.EqpUpdate.as_view(), name="update_eqp"),
    path('details/eqp/<int:pk>/', views.EqpDetails.as_view(), name="details_eqp"),
    path('list/eqp/', views.EqpList.as_view(), name="list_eqp"),

    path('create/eqr/<int:pk>/<str:pop>/', views.EqrCreate.as_view(), name="create_eqr"),
    path('update/eqr/<int:pk>/<str:pop>/', views.EqrUpdate.as_view(), name="update_eqr"),

    path('list/etr/', views.EtrList.as_view(), name="list_etr"),
    path('create/etr/', views.EtrCreate.as_view(), name="create_etr"),
    path('details/etr/<int:pk>/', views.EtrDetails.as_view(), name="details_etr"),
    path('update/etr/<int:pk>/', views.EtrUpdate.as_view(), name="update_etr"),
    path('update/etr/<int:pk>/<str:pop>/', views.EtrUpdate.as_view(), name="update_etr"),

    path('create/mor/', views.MorCreate.as_view(), name="create_mor"),
    path('create/mor/<str:pop>/', views.MorCreate.as_view(), name="create_mor"),
    path('update/mor/<int:pk>/', views.MorUpdate.as_view(), name="update_mor"),
    path('update/mor/<int:pk>/<str:pop>/', views.MorUpdate.as_view(), name="update_mor"),
    path('details/mor/<int:pk>/', views.MorDetails.as_view(), name="details_mor"),
    path('list/mor/', views.MorList.as_view(), name="list_mor"),

    path('create/prj/', views.PrjCreate.as_view(), name="create_prj"),
    path('create/prj/<str:pop>/', views.PrjCreate.as_view(), name="create_prj"),
    path('update/prj/<int:pk>/', views.PrjUpdate.as_view(), name="update_prj"),
    path('update/prj/<int:pk>/<str:pop>/', views.PrjUpdate.as_view(), name="update_prj"),
    path('details/prj/<int:pk>/', views.PrjDetails.as_view(), name="details_prj"),
    path('list/prj/', views.PrjList.as_view(), name="list_prj"),

    path('create/rsc/', views.RscCreate.as_view(), name="create_rsc"),
    path('update/rsc/<int:pk>/', views.RscUpdate.as_view(), name="update_rsc"),
    path('details/rsc/<int:pk>/', views.RscDetails.as_view(), name="details_rsc"),
    path('list/rsc/', views.RscList.as_view(), name="list_rsc"),

    path('create/rst/<int:rsc>/<str:pop>/', views.RstCreate.as_view(), name="create_rst"),
    path('delete/rst/<int:pk>/', views.rst_delete, name="delete_rst"),

    path('create/ste/<int:dep_id>/<int:set_id>/<str:pop>/', views.SteCreate.as_view(), name="create_ste"),
    path('delete/ste/<int:pk>/<str:pop>/', views.SteDelete.as_view(), name="delete_ste"),
    path('update/ste/<int:pk>/<str:pop>/', views.SteUpdate.as_view(), name="update_ste"),

    path('create/stn/', views.StnCreate.as_view(), name="create_stn"),
    path('create/stn/<str:pop>/', views.StnCreate.as_view(), name="create_stn"),
    path('update/stn/<int:pk>/', views.StnUpdate.as_view(), name="update_stn"),
    path('update/stn/<int:pk>/<str:pop>/', views.StnUpdate.as_view(), name="update_stn"),
    path('details/stn/<int:pk>/', views.StnDetails.as_view(), name="details_stn"),
    path('list/stn/', views.StnList.as_view(), name="list_stn"),

    path('create/tea/', views.TeaCreate.as_view(), name="create_tea"),
    path('update/tea/<int:pk>/', views.TeaUpdate.as_view(), name="update_tea"),
    path('list/tea/', views.TeaList.as_view(), name="list_tea"),

    path('create/rec/', views.RecCreate.as_view(), name="create_rec"),
    path('create/rec/<int:eda>/', views.RecCreate.as_view(), name="create_rec"),
    path('list/rec/', views.RecList.as_view(), name="list_rec"),
    path('details/rec/<int:pk>/', views.RecDetails.as_view(), name="details_rec"),
    path('update/rec/<int:pk>/', views.RecUpdate.as_view(), name="update_rec"),
    path('update/rec/<int:pk>/<str:pop>/', views.RecUpdate.as_view(), name="update_rec"),
    path('delete/rec/<int:pk>/<str:pop>/', views.RecDelete.as_view(), name="delete_rec"),

    path('create/ret/', views.RetCreate.as_view(), name="create_ret"),
    path('list/ret/', views.RetList.as_view(), name="list_ret"),
    path('update/ret/<int:pk>/', views.RetUpdate.as_view(), name="update_ret"),

    path('create/rci/<int:rec_id>/<str:pop>/', views.RciCreate.as_view(), name="create_rci"),
    path('delete/rci/<int:pk>/', views.rci_delete, name="delete_rci"),

    path('create/ree/<int:rec_id>/<str:pop>/', views.ReeCreate.as_view(), name="create_ree"),

    path('settings/help-texts/', views.HelpTextFormsetView.as_view(), name="manage_help_texts"),
    path('settings/help-text/<int:pk>/delete/', views.HelpTextHardDeleteView.as_view(), name="delete_help_text"),

    path('ajax/get_fields/', utils.ajax_get_fields, name='ajax_get_fields'),

    # managed lists
    path('settings/delete-managed/<str:key>/<int:pk>/', views.delete_managed, name="delete_managed"),
    path('settings/managed-eqt/', views.EqtMangedView.as_view(), name="managed_eqt"),
    path('settings/managed-ert/', views.ErtMangedView.as_view(), name="managed_ert"),
    path('settings/managed-prm/', views.PrmMangedView.as_view(), name="managed_prm"),
    path('settings/managed-rtt/', views.RttMangedView.as_view(), name="managed_rtt"),
    path('settings/managed-set/', views.SetMangedView.as_view(), name="managed_set"),

]

