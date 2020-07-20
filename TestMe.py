# -*- coding: utf8 -*-

from Lib import libPagesJaunes as PJ
import sqlite3

QUIQUOI = "SSII"
VILLE = "Paris"
PROXIMITE = False
VERBOSE = 2

recherche = PJ.RecherchePagesJaunes(QUIQUOI,VILLE,PROXIMITE, VERBOSE)
societes = recherche.societes

SQL_CREATE_TABLE =  \
	"CREATE TABLE IF NOT EXISTS `Societes` ( \
	`nomSociete` varchar, \
	`adresse` varchar, \
	`codePostal` varchar, \
	`ville` varchar, \
	`numTelephoneFix` varchar, \
	`numTelephoneMobile` varchar, \
	`siteWeb` varchar, \
	`prestations` varchar, \
	`produits` varchar, \
	`siret`  varchar, \
	`codeNAF` varchar,  \
	`effectifEtablissement` varchar,  \
	`siren` varchar,  \
	`formeJuridique` varchar,  \
	`dateCreationEntreprise` varchar \
	) ;"

conn = sqlite3.connect('societes.db')
c = conn.cursor()
c.execute(SQL_CREATE_TABLE)
for societe in societes: 
	c.execute( \
"INSERT INTO Societes \
( \
`nomsociete`, \
`adresse`, \
`codePostal`, \
`ville`, \
`numTelephoneFix`, \
`numTelephoneMobile`, \
`siteWeb`, \
`prestations`, \
`produits`, \
`siret` , \
`codeNAF`,  \
`effectifEtablissement`,  \
`siren`,  \
`formeJuridique`,  \
`dateCreationEntreprise`\
) \
VALUES " \
"( + \
?, \
?, \
?, \
?, \
?, \
?, \
?, \
?, \
?, \
?, \
?, \
?, \
?, \
?, \
? \
);" \
,( \
str(societe.nomSociete), \
str(societe.adresse), \
str(societe.codePostal), \
str(societe.ville), \
str(societe.numTelephoneFix), \
str(societe.numTelephoneMobile), \
str(societe.siteWeb), \
str(societe.prestations), \
str(societe.produits), \
str(societe.siret), \
str(societe.codeNAF), \
str(societe.effectifEtablissement), \
str(societe.siren), \
str(societe.formeJuridique), \
str(societe.dateCreationEntreprise), \
))

conn.commit()
conn.close()

