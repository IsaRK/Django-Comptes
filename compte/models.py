from django.db import models
from django.utils import timezone
import datetime
from django.core.exceptions import ValidationError

class Categorie(models.Model):
    Cat = models.CharField(max_length=200, unique = True, verbose_name = 'Categorie')
    def __unicode__(self):
        return self.Cat

class User(models.Model):
	nom = models.CharField(max_length=30)
	def __unicode__(self):
		return self.nom

class Compte(models.Model):
	def __unicode__(self):
		return self.motif

	date = models.DateTimeField(auto_now = False, auto_now_add = False)
	date_sup = models.DateTimeField(null = True, blank = True)
	mntTotal = models.IntegerField()
	mnt = models.IntegerField()
	remb = models.BooleanField(verbose_name = 'Remboursement ?')
	motif = models.CharField(max_length=400)
	categorie = models.ForeignKey(Categorie)
	user = models.ForeignKey(User, verbose_name = 'Qui a payé ou reçoit le remboursement ?')

	
   