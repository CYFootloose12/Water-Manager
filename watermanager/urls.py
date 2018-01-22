from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'watermanager.views.homeLogin', name='home'),
    url(r'^register$', 'watermanager.views.register', name='register'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'watermanager/index.html'}),
    url(r'^home_login$', 'django.contrib.auth.views.login', {'template_name':'watermanager/index.html'}),

    url(r'^myplants$', 'watermanager.views.myplants', name="myplants"),
    url(r'^add_plant$', 'watermanager.views.add_plant', name="add_plant"),
    url(r'^delete_plant/(\d+)$', 'watermanager.views.delete_plant', name="delete_plant"),

    url(r'^schedule/(\d+)$', 'watermanager.views.schedule', name="schedule"),
 
    url(r'^add_watering_time$', 'watermanager.views.addWateringTime', name="add_watering_time"),
    url(r'^add_events$', 'watermanager.views.add_events', name="add_events"),
    url(r'^add_AI$', 'watermanager.views.add_AI', name="add_AI"),
    url(r'^add_forecast$', 'watermanager.views.add_forecast', name="add_forecast"),
    url(r'^delete_watering_time$', 'watermanager.views.deleteWateringTime', name="delete_watering_time"),

    url(r'^my_weather$', 'watermanager.views.my_weather', name="my_weather"),
    url(r'^notifications$', 'watermanager.views.notifications', name="notifications"),
    url(r'^send_email_notifications$', 'watermanager.views.send_email_notifications', name="send_email_notifications"),

    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'watermanager.views.confirm_registration', name='confirm'),
)

