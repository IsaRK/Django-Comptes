#-*- coding:utf-8 -*-

from django.forms import ModelForm, CharField
from django.db import models
from compte.models import Compte, Categorie, User
from django.forms.util import ErrorList

class CompteForm(ModelForm):
	class Meta :
		model = Compte
		exclude = ('date','date_sup',)
	
	def clean(self):
	
		if self.cleaned_data['remb'] == True and \
			self.cleaned_data['mnt'] != self.cleaned_data['mntTotal'] :
			msg = "Il s'agit d'un remboursement : mnt et mntTotal doivent etre égaux."
			self._errors['remb'] = ErrorList([msg])	
			del self.cleaned_data['remb']
		
		if self.cleaned_data['mnt'] > self.cleaned_data['mntTotal'] :
			msg = "Le montant remboursé doit etre inférieur au montant Total."
			self._errors['mnt'] = ErrorList([msg])
			del self.cleaned_data['mnt']
		
		return self.cleaned_data
		
class CategorieForm(ModelForm):
	class Meta :
		model = Categorie
