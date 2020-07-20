# -*- coding: utf8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

import json

class RecherchePagesJaunes: 
	def __init__(self, quiQuoi, ville, proximite, verboseLevel = 0):
		
		#verbose level 1
		if verboseLevel > 0 :
			print ("RecherchePagesJaunes >  __init__ (quiQuoi : " + quiQuoi + " | ville :  " + ville + " |  proximite : " + str(proximite) + " | verboseLevel : " + str(verboseLevel) + ")" )
		
		#Les propriétés de la classe RecherchePagesJaunes.
		self.quiQuoi = quiQuoi
		self.ville = ville
		self.proximite = proximite
		self.totalPagesResultats = 0
		self.listeUrlPagesResultats = []
		self.societes = []
		self.verboseLevel = verboseLevel
		
		#Driver du constructeur.
		options = Options()
		options.headless = True
		self.driver = webdriver.Firefox(options=options)
		self.driver.get("https://www.pagesjaunes.fr")

		#On attend que la première page soit chargé.
		element = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "SEL-idstatspage")))
		
		#Les éléments que l'on va utiliser.
		inputBoxQuiQuoi = self.driver.find_element_by_id("quoiqui")
		inputBoxOu = self.driver.find_element_by_id("ou")
		checkBoxProximite = self.driver.find_element_by_id("proximite")
		boutonTrouver = self.driver.find_element_by_xpath('//*[@title="Trouver"]')
		
		#Actions sur les éléments.
		inputBoxQuiQuoi.send_keys(self.quiQuoi)
		inputBoxOu.send_keys(ville)
		if (checkBoxProximite.is_selected() and self.proximite == False):
			checkBoxProximite.click()
		elif (not checkBoxProximite.is_selected() and self.proximite == True):
			checkBoxProximite.click()
		boutonTrouver.click()

		#On attend que la nouvelle page soit chargé.
		element = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "SEL-compteur")))
		
		#Les éléments que l'on va utiliser.
		paginationCompteur = self.driver.find_element_by_id("SEL-compteur").text
		urlPremierePageRecherche = self.driver.current_url		
		
		#On renseigne les propriété de l'objet.
		self.totalPagesResultats = int(''.join(paginationCompteur[paginationCompteur.find("/")+1:].split()))
		for numPage in range(1,self.totalPagesResultats + 1):
			self.listeUrlPagesResultats.append(urlPremierePageRecherche + "&page=" + str(numPage))

		#verbose level 2
		if verboseLevel == 2:		
			for UrlPageResultat in self.listeUrlPagesResultats:
				print ("	UrlPageResultat : " + UrlPageResultat)

		self.driver.close()

		for UrlPageResultat in self.listeUrlPagesResultats:
			for UrlAnnonce in PageResultatPagesJaunes(UrlPageResultat, self.verboseLevel).UrlsAnnonces:
				self.societes.append(PageAnnonce(UrlAnnonce,self.verboseLevel))		

		

class PageResultatPagesJaunes:
	def __init__(self, UrlPageResultatPagesJaunes, verboseLevel = 0):
		#verbose level 1
		if verboseLevel > 0:
			print ("PageResultatPagesJaunes >  __init__ (UrlPageResultatPagesJaunes : " + UrlPageResultatPagesJaunes + " | verboseLevel : " + str(verboseLevel) + ")" )		
		
		#Les propriétés de la classe RecherchePagesJaunes.
		self.UrlPageResultatPagesJaunes = UrlPageResultatPagesJaunes
		self.UrlsAnnonces = []

		#Driver du constructeur.
		options = Options()
		options.headless = True
		self.driver = webdriver.Firefox(options=options)
		self.driver.get(self.UrlPageResultatPagesJaunes)

		#On attend que la page soit chargée.
		element = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "SEL-compteur")))		

		#les éléments que l'on va utiliser.
		self.elementsContenantUrlsAnnonces = self.driver.find_elements_by_tag_name("article")

		#On renseigne les propriétés de l'objet.
		for elementContenantUrlAnnonce in self.elementsContenantUrlsAnnonces:
			self.identifiantAnnonce = str(json.loads(elementContenantUrlAnnonce.get_attribute("data-pjtoggleclasshisto"))["idbloc"]["id_bloc"])	
			self.UrlsAnnonces.append("https://www.pagesjaunes.fr/pros/detail?bloc_id=" + self.identifiantAnnonce)

		#verbose level 2
		if verboseLevel == 2:
			for UrlAnnonce in self.UrlsAnnonces:	
				print ("	UrlAnnonce : " + UrlAnnonce)

		self.driver.close()

class PageAnnonce:
	def __init__(self, urlAnnonce, verboseLevel = 0):
		#verbose level 1
		if verboseLevel > 0:
			print ("PageAnnonce >  __init__ (urlAnnonce : " + urlAnnonce + " | verboseLevel : " + str(verboseLevel)  + ")" )

		#Les propriétés de la classe PageAnnonce.
		self.urlAnnonce = urlAnnonce
		self.nomSociete = ""
		self.numTelephoneFix = ""
		self.numTelephoneMobile = ""
		self.siteWeb = []
		self.adresse = ""
		self.codePostal = ""
		self.ville = ""
		self.prestations = []
		self.produits = []
		self.activites = ""
		self.siret = ""
		self.nombreEmployee = ""
		self.siren = ""
		self.codeNAF = ""
		self.effectifEtablissement = ""

		#Driver du constructeur.
		options = Options()
		options.headless = True
		self.driver = webdriver.Firefox(options=options)
		self.driver.get(self.urlAnnonce)

		#On attend que la page soit chargée.
		element = WebDriverWait(self.driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "footer")))

		#On renseigne les propriétés de la classe PageAnnonce
		elementsAtraiter = self.driver.find_elements_by_xpath("//*[@class='no-margin pro-title noTrad']")
		if len(elementsAtraiter) > 0:
			self.nomSociete = elementsAtraiter[0].text
		else:
			self.nomSociete = ""

		
		elementsAtraiter = self.driver.find_elements_by_xpath("//*[@class='coord-numero noTrad']")
		if len(elementsAtraiter) > 0:
			self.numTelephoneFix = elementsAtraiter[0].text
		else:
			self.numTelephoneFix = ""

		elementsAtraiter = self.driver.find_elements_by_xpath("//*[@class='coord-numero-mobile noTrad']")
		if len(elementsAtraiter) > 0:
			self.numTelephoneMobile = elementsAtraiter[0].text
		else:
			self.numTelephoneMobile = ""
		
		elementsAtraiter = self.driver.find_elements_by_xpath("//*[@class='teaser-item black-icon address streetAddress clearfix map-click-zone pj-lb pj-link']")
		if len(elementsAtraiter) > 0:
			self.adresse = elementsAtraiter[0].find_elements_by_tag_name("span")[0].text
			self.codePostal = elementsAtraiter[0].find_elements_by_tag_name("span")[2].text[2:]
			self.ville = elementsAtraiter[0].find_elements_by_tag_name("span")[3].text
		else:
			self.adresse = ""
			self.codePostal = ""
			self.ville = ""
		
		elementsAtraiter = self.driver.find_elements_by_xpath("//*[@class='bloc-info-sites-reseaux']//span[@class='value']")
		if len(elementsAtraiter) > 0:
			for siteWeb in elementsAtraiter :
				self.siteWeb.append(siteWeb.text)
		else:
			self.siteWeb = []

		elementsAtraiter = self.driver.find_elements_by_xpath("//*[@class='cri-prestations']//span | //*[@class='ligne prestations marg-btm-m generique']//span")
		if len(elementsAtraiter) > 0:
			for prestation in elementsAtraiter :
				self.prestations.append(prestation.text)
		else:
			self.prestations = []
		
		elementsAtraiter = self.driver.find_elements_by_xpath("//*[@class='cri-produits']//span | //*[@class='ligne produits']//span")
		if len(elementsAtraiter) > 0:
			for produit in elementsAtraiter:
				self.produits.append(produit.text)
		else:
			self.produits = []

		elementsAtraiter = self.driver.find_elements_by_xpath("//*[@class='row siret']/span")
		if len(elementsAtraiter) > 0:
			self.siret = elementsAtraiter[0].text
		else:
			self.siret = ""
		
		elementsAtraiter = self.driver.find_elements_by_xpath("//*[@class='row naf']/span")
		if len(elementsAtraiter) > 0:
			self.codeNAF = elementsAtraiter[0].text
		else:
			self.codeNAF = ""
		
		elementsAtraiter = self.driver.find_elements_by_xpath("//*[@class='row effectif']/span")
		if len(elementsAtraiter) > 0:
			self.effectifEtablissement = elementsAtraiter[0].text
		else:
			self.effectifEtablissement = ""

		elementsAtraiter = self.driver.find_elements_by_xpath("//*[@class='row siren']/span")
		if len(elementsAtraiter) > 0:
			self.siren = elementsAtraiter[0].text
		else:
			self.siren = ""

		elementsAtraiter = self.driver.find_elements_by_xpath("//*[@class='row forme_juridique']/span")
		if len(elementsAtraiter) > 0:
			self.formeJuridique = elementsAtraiter[0].text
		else:
			self.formeJuridique = ""

		elementsAtraiter = self.driver.find_elements_by_xpath("//*[@class='row date_creation_entreprise']/span")
		if len(elementsAtraiter) > 0:
			self.dateCreationEntreprise = elementsAtraiter[0].text
		else:
			self.dateCreationEntreprise = ""

		#self.activites = self.driver.find_elements_by_xpath("//*[@class='activite']")

		self.driver.close()

		#verbose level 2
		if verboseLevel == 2:
			print("     nomsociete : " + self.nomSociete)
			print("     adresse : " + self.adresse)
			print("     codePostal : " + self.codePostal)
			print("     ville : " + self.ville)
			print("     numTelephoneFix : " + self.numTelephoneFix)
			print("     numTelephoneMobile : " + self.numTelephoneMobile)
			print("     siteWeb : " + ' | '.join(self.siteWeb))
			print("     prestations : " + ' | '.join(self.prestations))
			print("     produits : " + ' | '.join(self.produits))	
			print("     siret : " + self.siret)
			print("     codeNAF : " + self.codeNAF)
			print("     effectifEtablissement : " + self.effectifEtablissement)
			print("     siren : " + self.siren)
			print("     formeJuridique : " + self.formeJuridique)
			print("     dateCreationEntreprise : " + self.dateCreationEntreprise)	
