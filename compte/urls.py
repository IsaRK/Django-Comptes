from django.conf.urls import patterns, include, url

urlpatterns = patterns('compte.views',
    url(r'^$', 'index'),
    url(r'^ajout/$', 'ajout'),
    url(r'^detail/$', 'detail'),
	url(r'^ajoutCategorie/$', 'ajoutCategorie'),
	url(r'^detail/modifier/(?P<detailId>\d+)/?', 'detailModifier', name = 'detailModifier'),
	url(r'^detail/supprimer/(?P<detailId>\d+)/?$', 'detailSupprimer'),
)
