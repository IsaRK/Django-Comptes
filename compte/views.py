from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404, render
from compte.models import Categorie, Compte, User
from compte.forms import CompteForm, CategorieForm
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseRedirect
from datetime import datetime

def index(request):
    calcul_all = calcul()
    latest_compte_list = Compte.objects.all().exclude(date_sup__isnull = False).order_by('date')[:5]
    t = loader.get_template('compte/index.html')
    c = Context({
        'latest_compte_list': latest_compte_list,
	'calcul_user': calcul_all[0],
	'calcul_sum': calcul_all[1],
    })
    return HttpResponse(t.render(c))
    
def ajout(request) :
    if request.method == 'POST': 	#S'il s'agit d'une requête POST
        submit = request.POST.get('cancel',None)
        if submit :
            return HttpResponseRedirect(reverse('compte.views.index'))
	else :
            form = CompteForm(request.POST) #On reprend les donnees
            if form.is_valid(): #On verifie que les donnees envoyees sont valides
                #Ici on peut traiter les donnees du formulaire
                new_compte = form.save(commit=False)
                new_compte.date = datetime.now()
                new_compte.save()
                if request.POST.get('submitAnotherOne',None) :
                    return HttpResponseRedirect(reverse('compte.views.ajout'))
                else :
                    return HttpResponseRedirect(reverse('compte.views.detail'))
    else: #Si c'est pas du POST, c'est probablement une requete GET
        form = CompteForm() # On cree un formulaire vide

    return render(request, 'compte/ajout.html', {
        'form': form,
    }) #On balance le template avec le formulaire qu'on a construit plus haut

def ajoutCategorie(request) :
    if request.method == 'POST' :
        form = CategorieForm(request.POST)
        if form.is_valid() :
            new_cat = form.save()
            return HttpResponseRedirect(reverse('compte.views.ajout'))
    else :
        form = CategorieForm()
    return render( request, 'compte/ajoutCategorie.html', {
        'form' : form,
    })
    
def detail(request):
    all_compte_list = Compte.objects.all().exclude(date_sup__isnull = False).order_by('date')
    t = loader.get_template('compte/detail.html')
    c = Context({
        'all_compte_list': all_compte_list,
    })
    return HttpResponse(t.render(c))
	
def calcul() :
	users = User.objects.values_list('nom', flat = True)
	user1, user2 = users[0], users[1]
	all_compte_user1 = Compte.objects.filter(user__nom = user1).exclude(date_sup__isnull = False).values_list('mnt', flat = True)
	sum_user1 = sum([int(a) for a in all_compte_user1])
	all_compte_user2 = Compte.objects.filter(user__nom = user2).exclude(date_sup__isnull = False).values_list('mnt', flat = True)
	sum_user2 = sum([int(a) for a in all_compte_user2])
	if sum_user1 > sum_user2 :
		user = user2
		sumTot = sum_user1 - sum_user2
	else :
		user = user1
		sumTot = sum_user2 - sum_user1
	return [user, sumTot]
	
def detailModifier(request, detailId) :
    toedit = Compte.objects.get(id = detailId)
    if request.method == 'POST': #S'il s'agit d'une requête POST
        submit = request.POST.get('cancel',None)
        if submit :
            return HttpResponseRedirect(reverse('compte.views.detail'))
        else :
            form = CompteForm(data = request.POST or None, instance = toedit) #On reprend les donnees
            if form.is_valid(): #On verifie que les donnees envoyees sont valides
                #Ici on peut traiter les donnees du formulaire
                form.save()
                return HttpResponseRedirect(reverse('compte.views.detail'))
    else: #Si c'est pas du POST, c'est probablement une requete GET
        form = CompteForm(instance = toedit)
        return render(request, 'compte/detailModifier.html', {
        'form': form,
        'toedit' : toedit,
        })

def detailSupprimer(request, detailId) :
    todel = Compte.objects.get(id = detailId)
    todel.date_sup = datetime.now()
    todel.save()
    return HttpResponseRedirect(reverse('compte.views.detail'))
