# Génère data/lieux.geojson et data/trajets.geojson de l'Atlas Billy the Kid.
import json, sys, datetime
OUT = sys.argv[1]
UT = "Utley, Robert M. (2015), Wanted: The Outlaw Lives of Billy the Kid and Ned Kelly, New Haven, Yale University Press"
WA = "Wallis, Michael (2007), Billy the Kid: The Endless Ride, New York, W. W. Norton"
GD = "Gardner, Mark Lee (2010), To Hell on a Fast Horse: The True Story of Billy the Kid and Pat Garrett, New York, William Morrow (PDF du Drive de l'auteur, lu en entier)"
GA = "Garrett, Pat F. (1882), The Authentic Life of Billy, the Kid, Santa Fe, New Mexican Printing and Publishing"
CERT = {'c': 'certaine', 'a': 'approximative', 'h': 'hypothetique'}

def dec(d, fin=False):
    d = d.replace('~', '').replace('?', '')
    p = [int(x) for x in d.split('-')]
    if len(p) == 1:
        return p[0] + (0.999 if fin else 0.0)
    if len(p) == 2:
        a, m = p
        return round(a + (m - (0 if fin else 1)) / 12 - (0.001 if fin else 0), 4)
    a, m, j = p
    jour = datetime.date(a, m, j).timetuple().tm_yday
    return round(a + (jour - 1) / 365, 4)

def prec(edtf):
    d = edtf.split('/')[0]
    if '~' in d: return 'circa'
    n = d.count('-')
    return ['annee', 'mois', 'jour'][n]

lieux = []
def L(n, nom, cat, edtf, lon, lat, cert, desc, src, note=''):
    a, b = (edtf.split('/') + [edtf])[:2]
    lieux.append({'type': 'Feature', 'geometry': {'type': 'Point', 'coordinates': [lon, lat]},
                  'properties': {'id': f'L{n:02d}', 'nom': nom, 'debut': dec(a), 'fin': dec(b, True) if '/' in edtf else dec(a),
                                 'date_edtf': edtf, 'precision': prec(edtf), 'certitude': CERT[cert], 'categorie': cat,
                                 'description': desc, 'sources': src, 'note': note, 'type': 'lieu'}})

def u(p): return f"{UT}, PDF p. {p}."
def w(p): return f"{WA}, PDF p. {p}."
def gd(p): return f"{GD}, PDF p. {p}." if p else f"{GD}."
def g(p): return f"{GA}, PDF p. {p}."

# ---- Enfance et errances (1859-1877)
L(1, "New York : naissance d'Henry McCarty", 'naissance', '1859-11', -73.990, 40.725, 'h',
  "Henry McCarty, futur Billy the Kid, naît en novembre 1859, sans doute à New York, de Catherine McCarty, immigrante irlandaise. Le père reste inconnu (Catherine dira plus tard qu'il s'appelait Michael). Henry a un frère, Joe.",
  u(16), "Le lieu et la date restent discutés ; aucun acte de naissance n'a été retrouvé. Point symbolique dans Manhattan.")
L(2, "Indianapolis : Catherine McCarty et William Antrim", 'vie', '1865~/1870', -86.158, 39.768, 'a',
  "Veuve, Catherine McCarty gagne Indianapolis avec ses deux fils. Elle y rencontre William Henry Harrison Antrim, ancien soldat de l'Union, nettement plus jeune qu'elle.",
  u(16), "Dates approximatives : la présence de la famille à Indianapolis n'est attestée que de façon indirecte.")
L(3, "Wichita : la blanchisserie de Catherine", 'vie', '1870/1871-07~', -97.337, 37.687, 'c',
  "En 1870, Catherine McCarty et « Uncle Bill » Antrim sont recensés à Wichita (Kansas). Elle y tient une blanchisserie, et tous deux obtiennent des terres en vertu du Homestead Act. La tuberculose de Catherine les pousse à partir à l'été 1871, vers Denver puis Santa Fe.",
  u(17))
L(4, "Santa Fe : mariage de Catherine McCarty et William Antrim", 'vie', '1873-03-01', -105.9400, 35.6905, 'c',
  "Le 1er mars 1873, le pasteur de la First Presbyterian Church de Santa Fe unit Catherine McCarty et William H. H. Antrim ; Henry et Joe signent comme témoins. Henry prend aussi le nom d'Antrim.",
  u(17), "Point à l'église presbytérienne (Grant Avenue).")
L(5, "Silver City : mort de la mère", 'mort', '1874-09-16', -108.2747, 32.7701, 'c',
  "La famille descend le Rio Grande puis gagne la ville minière de Silver City, où Antrim espère faire fortune. La tuberculose de Catherine s'aggrave ; elle meurt le 16 septembre 1874. Livrés à eux-mêmes, les deux garçons échappent à toute discipline.",
  u(17))
L(6, "Silver City : premier larcin et évasion par la cheminée", 'prison', '1875-09-23', -108.2733, 32.7712, 'c',
  "Le 23 septembre 1875, à quinze ans, Henry fait son premier pas vers le crime : avec un ivrogne surnommé « Sombrero Jack », il est mêlé au vol de linge d'une blanchisserie chinoise. Le shérif Harvey Whitehill l'enferme ; Henry s'échappe en grimpant dans la cheminée de la prison et quitte le Nouveau-Mexique pour l'Arizona.",
  u('16-18'))
L(7, "Camp Grant et le ranch Hooker : apprentissage du cheval et du revolver", 'vie', '1875-10~/1877-08', -109.95, 32.55, 'a',
  "Le jeune fugitif gravite autour du poste militaire de Camp Grant, au pied du mont Graham, à 150 milles à l'ouest de Silver City, et autour du ranch d'Henry C. Hooker. Il vole selles, couvertures et parfois des chevaux aux soldats ; deux fois arrêté, il s'évade deux fois. C'est là qu'il apprend le cheval et les armes.",
  u('18-20'), "Point entre Camp Grant et le ranch Sierra Bonita de Hooker.")
L(8, "Bonita : mort de « Windy » Cahill, premier homicide", 'fusillade', '1877-08-17', -109.927, 32.664, 'c',
  "Le soir du 17 août 1877, dans le saloon de George Atkins, près de Camp Grant, le forgeron Francis P. « Windy » Cahill, qui le brutalise depuis longtemps, gifle Henry et l'insulte. Dans la lutte, Henry sort un revolver et tire. Cahill meurt le lendemain ; un jury du coroner déclare « Henry Antrim alias Kid » coupable. Il s'enfuit vers le Nouveau-Mexique.",
  u('18-19'))
L(9, "Seven Rivers : avec « The Boys » de Jesse Evans", 'refuge', '1877-10~', -104.42, 32.60, 'a',
  "Revenu au Nouveau-Mexique, le Kid suit un temps la bande de voleurs de bétail de Jesse Evans, « The Boys », jusqu'au bas Pecos, à Seven Rivers. Il y observe la vie de vrais hors-la-loi et loge chez un habitant du lieu.",
  u(23), "Le village de Seven Rivers a disparu sous le réservoir de Brantley ; point approximatif.")

# ---- Guerre du comté de Lincoln (1877-1878)
L(10, "Ranch des Coe, sur le Ruidoso", 'vie', '1877-10~', -105.385, 33.390, 'a',
  "Remontant le Hondo et le Ruidoso depuis Seven Rivers, le Kid rencontre les cousins Frank et George Coe, fermiers d'origine missourienne, au ranch de Frank, juste en aval du confluent du Ruidoso et du Bonito. Frank Coe se souviendra d'un garçon aimable, sobre et excellent tireur.",
  u('27-28'))
L(11, "Ranch de Tunstall sur le Río Feliz", 'vie', '1877-12~/1878-02', -105.17, 33.17, 'a',
  "Sur le Ruidoso, le Kid rencontre Dick Brewer, qui gère aussi, à vingt milles au sud, sur le Río Feliz, le ranch de l'Anglais John H. Tunstall. Tunstall l'engage ; Billy y travaille avec Fred Waite, avec qui il projette de s'établir sur le Río Peñasco.",
  u('30-31'))
L(12, "Assassinat de John Tunstall", 'fusillade', '1878-02-18', -105.43, 33.30, 'a',
  "Le 18 février 1878, Tunstall quitte son ranch du Río Feliz avec neuf chevaux par la route du nord, vers la jonction du Ruidoso et du Bonito. Rattrapé par des hommes du détachement du shérif Brady, il est abattu ; Billy, Waite et Middleton, qui chassaient le dindon à l'écart, assistent impuissants à la scène. L'assassinat déclenche la guerre du comté de Lincoln.",
  u('37-39'), "Le lieu exact du meurtre, sur le chemin du Ruidoso, est approximatif.")
L(13, "Lincoln : la ville de la guerre", 'vie', '1878-02-19', -105.3845, 33.4920, 'c',
  "Lincoln, longue rue d'adobes au bord du Bonito : le magasin de Murphy et Dolan (« The House »), celui de Tunstall et McSween, l'hôtel Wortley, le vieux torreón de pierre et l'adobe de « Squire » John B. Wilson, juge de paix. Le 19 février 1878, Billy, Brewer et Middleton y signent leurs dépositions sur le meurtre de Tunstall ; Wilson délivre des mandats et les « Regulators » sont constitués.",
  u('26, 39-40'))
L(14, "Morton et Baker abattus", 'fusillade', '1878-03-09', -104.95, 33.35, 'h',
  "Le 6 mars 1878, les Regulators de Brewer capturent sur le bas Pecos William Morton et Frank Baker, deux membres du détachement accusés du meurtre de Tunstall. En les ramenant vers Lincoln par une route détournée, ils les tuent avec William McCloskey ; la version des Regulators, selon laquelle Morton aurait abattu McCloskey avant de fuir, reste peu crédible.",
  u('43-44'), "Lieu hypothétique, entre le Pecos et Lincoln (la tradition parle d'Agua Negra ou de Blackwater Draw).")
L(15, "Ranch de South Spring (John Chisum)", 'refuge', '1878-03~/1878-07', -104.535, 33.355, 'c',
  "Le grand éleveur John Chisum, sympathisant des Regulators sans prendre part aux combats, ouvre son ranch de South Spring aux hommes de McSween, qui s'y réunissent pour arrêter leur stratégie fin mars 1878.",
  u(45))
L(16, "Lincoln : le shérif Brady abattu", 'fusillade', '1878-04-01', -105.3832, 33.4924, 'c',
  "Au matin du 1er avril 1878, jour prévu pour l'ouverture de la cour, six Regulators, dont Billy, Waite et Middleton, embusqués derrière le mur d'adobe du corral du magasin Tunstall, abattent le shérif William Brady et un adjoint qui descendent la rue.",
  u(45))
L(17, "Blazer's Mill : l'agence mescalero et la mort de Buckshot Roberts", 'fusillade', '1878-04-04', -105.785, 33.162, 'a',
  "Le dentiste Joseph Blazer loue sa maison d'adobe à étage, près de sa scierie, au gouvernement pour loger l'agent des Apaches mescaleros, Frederick C. Godfroy ; Mme Godfroy sert des repas aux voyageurs. Le 4 avril 1878, les Regulators y dînent quand arrive Buckshot Roberts. L'affrontement tourne au drame : mortellement blessé, Roberts tue Dick Brewer d'une balle de Springfield.",
  w(186) + " " + u('26, 48-51'), "En 1878, le grand jury de Lincoln releva de fortes présomptions de fraude contre l'agent Godfroy.")
L(18, "Fort Stanton : le colonel Dudley", 'prison', '1878-07-19', -105.522, 33.495, 'c',
  "Le poste militaire de Fort Stanton, en amont de Lincoln sur le Bonito, est commandé par le lieutenant-colonel Nathan A. M. Dudley. Le 19 juillet 1878, il descend sur Lincoln avec des cavaliers noirs et de l'artillerie, ce qui fait basculer la bataille en faveur de la faction Dolan ; une cour d'enquête l'exonérera ensuite. Des membres des deux camps seront plus tard détenus au fort.",
  u('62, 78, 90'))
L(19, "Lincoln : la « Big Killing » et l'incendie de la maison McSween", 'fusillade', '1878-07-15/1878-07-19', -105.3862, 33.4927, 'c',
  "Le 14 juillet 1878, les Regulators de McSween reprennent position dans Lincoln : maison McSween, magasin Ellis, maison Montaño. Après plusieurs jours de tirs, l'arrivée de Dudley le 19 permet aux hommes de Dolan et de Peppin d'incendier la maison McSween. Le soir, McSween est tué en sortant ; Billy s'échappe à travers les tirs.",
  u('75-80'), "L'emplacement de la maison McSween est aujourd'hui occupé par d'autres bâtiments.")
L(20, "Tascosa : vente des chevaux volés", 'vie', '1878-10~', -102.17, 35.53, 'c',
  "À l'automne 1878, le Kid et quelques compagnons conduisent des chevaux volés au Texas. Dans la ville-champignon de Tascosa, au Panhandle, il les vend sans peine aux éleveurs et se lie avec un jeune médecin.",
  u('86'))

# ---- Le gouverneur et le Kid (1879)
L(21, "Lincoln : meurtre de l'avocat Chapman", 'fusillade', '1879-02-18', -105.3850, 33.4921, 'c',
  "Le soir du 18 février 1879, jour d'une trêve entre les factions, l'avocat manchot Huston Chapman, venu avec Susan McSween, est abattu dans la rue de Lincoln par Billy Campbell, en présence d'un Dolan ivre et de Jesse Evans ; Billy assiste au meurtre.",
  u('87-89'))
L(22, "Lincoln : rencontre nocturne avec le gouverneur Wallace", 'vie', '1879-03-17', -105.3840, 33.4919, 'c',
  "Pour témoigner contre les meurtriers de Chapman, Billy rencontre de nuit le gouverneur Lew Wallace dans la maison de Squire Wilson. Wallace lui laisse entendre qu'il sera gracié ; la seule source de cette conversation est une interview donnée par Wallace en 1901.",
  u('90-93'), "Date d'après la tradition (17 mars 1879) ; Utley ne la précise pas.")
L(23, "San Patricio : refuge et arrestation consentie", 'refuge', '1879-03-21', -105.33, 33.41, 'c',
  "Avec Tom O'Folliard, Billy se cache chez un ami à San Patricio, au confluent du Bonito et du Ruidoso. Comme convenu avec Wallace, le shérif Kimball les y arrête le 21 mars 1879. Détenu à Lincoln, Billy est fêté par les habitants ; il s'évade quelques semaines plus tard, faute de voir la grâce promise.",
  u('26, 90-92'))

# ---- Le hors-la-loi (1880)
L(24, "Fort Sumner : la maison Maxwell et le refuge des bergers", 'refuge', '1878-08~/1881-07', -104.1930, 34.4045, 'c',
  "Quand l'armée abandonne Fort Sumner, Lucien Maxwell achète les bâtiments de l'ancien poste et s'y retire ; à sa mort en 1875, son fils Pete reprend le ranch, et la famille habite l'ancien quartier des officiers. Charlie Bowdre et Doc Scurlock s'y établissent en 1878 et travaillent pour Pete Maxwell. Peuplé surtout de bergers hispaniques qui l'aiment et le protègent, Fort Sumner devient le refuge favori de Billy : bailes, queridas et saloons.",
  w(200) + " " + u('95, 113, 115'), "Utley attribue l'achat du fort à Pete Maxwell, Wallis à Lucien.")
L(25, "Fort Sumner : Joe Grant tué au saloon de Hargrove", 'fusillade', '1880-01-10', -104.1915, 34.4050, 'c',
  "Le 10 janvier 1880, au saloon de Bob Hargrove, un Texan ivre et bravache, Joe Grant, parie qu'il tuera quelqu'un avant Billy. Billy admire le revolver de Grant, en fait tourner le barillet et le lui rend une chambre vide sous le chien ; quand Grant le met en joue dans son dos, le chien tombe à vide, et Billy se retourne et l'abat. C'est le seul homicide qu'il ait commis seul.",
  u('96-97'))
L(26, "White Oaks : la ville minière", 'vie', '1880-11~', -105.738, 33.745, 'c',
  "La ville minière de White Oaks sert de débouché au bétail et aux chevaux volés par Billy et ses compagnons. En novembre 1880, un détachement de citoyens s'y forme pour les arrêter.",
  u(98))
L(27, "Relais de Greathouse : mort de Jimmy Carlyle", 'fusillade', '1880-11-27', -105.60, 34.20, 'h',
  "À mi-chemin entre White Oaks et Fort Sumner, le relais de « Whiskey Jim » Greathouse abrite les voleurs. À l'aube du 27 novembre 1880, le détachement de White Oaks encercle la maison ; le forgeron Jimmy Carlyle entre négocier, Greathouse servant d'otage. Retenu prisonnier, Carlyle est tué en sautant par une fenêtre ; les assiégés s'échappent.",
  u('98, 109'), "Localisation hypothétique (le relais était au nord de White Oaks, vers l'actuelle Corona).")
L(28, "Près de Puerto de Luna : le ranch de Pablo Beaubien", 'prison', '1880-12-17/1880-12-18', -104.560, 34.770, 'h',
  "Parti du magasin d'Alexander Grzelachowski à Puerto de Luna le 17 décembre 1880 avant une tempête, le shérif Pat Garrett fait halte au ranch de Pablo Beaubien. Son éclaireur, déguisé en berger cherchant des bêtes égarées, y confirme que le Kid et cinq compagnons sont à Fort Sumner.",
  g(68), "Position hypothétique sur le Pecos, en aval de Puerto de Luna.")
L(29, "Fort Sumner : l'embuscade et la mort de Tom O'Folliard", 'fusillade', '1880-12-19', -104.1940, 34.4038, 'c',
  "Garrett arrive à Fort Sumner sous la neige le 17 décembre 1880 et y tend un piège. Le soir du 19, le Kid, O'Folliard, Pickett, Rudabaugh et Wilson entrent au village par l'ancien hôpital, où le guette le détachement. O'Folliard est mortellement touché à la poitrine ; il meurt pendant que les hommes de Garrett reprennent leur partie de poker. Les autres s'enfuient.",
  u('100-101'))
L(30, "Stinking Springs : la capture", 'prison', '1880-12-23', -103.98, 34.47, 'a',
  "Le détachement de Garrett suit les traces dans la neige jusqu'à une cabane de pierre à Stinking Springs. À l'aube du 23 décembre 1880, Charlie Bowdre sort et est abattu. Garrett tue un cheval dans l'embrasure de la porte et coupe à la carabine les longes des autres bêtes ; affamés, Billy, Rudabaugh, Wilson et Pickett se rendent.",
  u('67, 102-104'), "Site approximatif, à l'est de Fort Sumner, près de l'actuelle Taiban.")
L(31, "Fort Sumner, veille de Noël 1880 : adieux à Paulita Maxwell", 'vie', '1880-12-24', -104.1925, 34.4040, 'c',
  "Ramené enchaîné à Fort Sumner, Billy obtient, grâce à Deluvina Maxwell, servante navajo très attachée à lui, de dire adieu à Paulita Maxwell. Toujours enchaîné à Rudabaugh, il entre dans l'ancien quartier des officiers ; la mère de Paulita, Luz Beaubien Maxwell, demande en vain qu'on lui ôte ses fers pour un moment d'intimité.",
  w(217) + " " + u(102))
L(32, "Las Vegas : le prisonnier célèbre", 'prison', '1880-12-26', -105.218, 35.594, 'c',
  "À Las Vegas, une foule accueille les prisonniers. Billy, enjoué, salue les badauds depuis la diligence et plaisante avec un journaliste qui l'interroge en prison le lendemain. Le lendemain, le train emmène les prisonniers à Santa Fe ; Tom Pickett reste détenu à Las Vegas.",
  u('103'))
L(33, "Santa Fe : la prison du comté", 'prison', '1880-12-27/1881-03-28', -105.9420, 35.6880, 'c',
  "Billy passe trois mois dans la prison de Santa Fe avec Rudabaugh et Wilson, écrivant en vain au gouverneur Wallace pour lui rappeler sa promesse. Une tentative d'évasion en creusant le mur de la prison échoue ; le shérif fait dès lors enchaîner les détenus.",
  u('105-107'))
L(34, "La Mesilla : procès et condamnation à mort", 'proces', '1881-03-30/1881-04-13', -106.7950, 32.2735, 'c',
  "Le 28 mars 1881, deux marshals adjoints conduisent Billy en train à La Mesilla, où le juge Warren Bristol ouvre la session le 30. L'accusation fédérale (meurtre de Roberts) tombe ; Albert J. Fountain et John Bail le défendent. Le 9 avril, Billy est reconnu coupable du meurtre du shérif Brady ; le juge Bristol fixe l'exécution au 13 mai 1881, à Lincoln.",
  u('106-108') + " " + w('123-125'))

# ---- Évasion et mort (1881)
L(35, "Lincoln : l'évasion du palais de justice", 'fusillade', '1881-04-28', -105.3835, 33.4923, 'c',
  "Détenu au premier étage de l'ancien magasin Dolan, devenu palais de justice, sous la garde de James W. Bell et de Bob Olinger, Billy s'évade le 28 avril 1881. Il tue Bell dans l'escalier, puis abat Olinger, qui accourt de l'hôtel Wortley, avec le fusil que celui-ci avait chargé. Le vieux cuisinier Godfrey Gauss lui amène un cheval ; il quitte Lincoln à l'ouest, ses chaînes battant ses jambes.",
  u('64, 109-111'))
L(36, "Fort Sumner : la mort dans la chambre de Pete Maxwell", 'mort', '1881-07-14', -104.1928, 34.4042, 'c',
  "Au lieu de fuir au Mexique, Billy revient à Fort Sumner. Dans la nuit du 14 juillet 1881, Garrett l'attend dans la chambre obscure de Pete Maxwell et l'abat d'une balle près du cœur. Au matin, Deluvina Maxwell frappe Garrett de ses poings, et les femmes de Fort Sumner veillent le corps à la chandelle.",
  u('113, 115-117') + " " + w(216))
L(37, "Fort Sumner : la tombe au vieux cimetière militaire", 'mort', '1881-07-15', -104.1886, 34.4031, 'c',
  "Proprement vêtu, Billy est mis en bière et porté au vieux cimetière militaire, où les habitants enterrent désormais leurs morts ; Lucien Maxwell y repose déjà. Sa tombe voisine celles de Tom O'Folliard et de Charlie Bowdre.",
  u(117) + " " + w(226))

# ---- Trajets
# ---- Pat Garrett, d'après Gardner (2010)
L(38, "Llano Estacado, près de Rath City : Pat Garrett tue le chasseur de bisons Joe Briscoe (automne 1876)", 'fusillade', '1876~', -100.38, 33.07, 'h',
  "Né en Alabama le 5 juin 1850 et élevé sur une plantation de la paroisse de Claiborne, en Louisiane, Pat Garrett chasse le bison au Texas. À l'automne 1876, après s'être équipée à Fort Griffin, l'équipe de Glenn et Garrett gagne le Llano Estacado. Un matin, une querelle éclate avec le jeune Irlandais Joe Briscoe : Garrett le frappe, Briscoe court chercher la hache du cuisinier, et Garrett l'abat d'une balle de pistolet. C'est le premier homme qu'il tue.",
  gd(29) + " ; " + gd(32), "Glenn était parti chercher une pièce de fusil à Rath City : point schématique dans ce secteur.")
L(39, "Anton Chico : Garrett épouse Apolinaria Gutiérrez (janvier 1880)", 'vie', '1880-01-14', -105.15, 35.20, 'c',
  "Veuf de Juanita Gutiérrez, épousée sans prêtre à l'automne 1879 à Fort Sumner et morte peu après, Pat Garrett se remarie quatre jours après que le Kid a tué Joe Grant au saloon de Fort Sumner : il épouse devant le curé d'Anton Chico, à 90 milles au nord-ouest, Apolinaria (« Polinaria », dite « La Negra ») Gutiérrez, fille de José Dolores et de Feliciana Gutiérrez. Les bailes du vieux dépôt de l'intendance de Fort Sumner attiraient les jeunes filles de Puerto de Luna, de Santa Rosa et même d'Anton Chico.",
  gd('77, 85-86'), "Point au village d'Anton Chico (comté de Guadalupe).")
L(40, "Los Portales : la cache du Kid pour le bétail volé (décembre 1880)", 'refuge', '1880-12', -103.25, 34.12, 'a',
  "Rocher saillant de quinze pieds au-dessus de la plaine, à 65 milles au sud-est de Fort Sumner, sur une piste à bétail vers le Panhandle texan, Los Portales doit son nom à son surplomb calcaire en forme de porches ; deux sources et une grotte y offrent un abri. Billy y cache le bétail volé. En décembre 1880, Garrett et sa troupe y espèrent reprendre une soixantaine de bêtes : ils ne trouvent que deux vaches, leurs veaux et un yearling, et dans la grotte de la farine moisie, un peu de sel et des couvertures ; le Kid avait déplacé le troupeau à quinze milles de là. Au retour, la troupe s'arrête au ranch de Wilcox et Brazil, à douze milles à l'est de Fort Sumner.",
  gd(None), "Point aux sources de Los Portales, au sud-est de la ville de Portales, approximatif.")
L(41, "Roswell : Garrett, Ash Upson et The Authentic Life of Billy, the Kid (1881-1882)", 'vie', '1881-08/1882', -104.523, 33.394, 'c',
  "Après la mort du Kid, Garrett s'installe à Roswell. Le journaliste, maître de poste et juge de paix Ash Upson, qui avait connu Billy enfant à Silver City, emménage chez lui en août 1881 et rédige en grande partie The Authentic Life of Billy, the Kid (1882), la réponse de Garrett aux insinuations sur la mort du Kid. Garrett restera à Roswell jusqu'en 1891 (irrigation de la vallée du Pecos), avant de partir pour Uvalde, au Texas, puis de devenir shérif du comté de Doña Ana (affaire Fountain, 1896) et collecteur des douanes à El Paso (1901) ; il est tué près de Las Cruces en février 1908.",
  gd('41, 157') + " ; " + GA + ".", "Point au centre historique de Roswell.")

traj = []
def T(n, nom, mode, edtf, coords, cert, desc, src, note=''):
    a, b = (edtf.split('/') + [edtf])[:2]
    traj.append({'type': 'Feature', 'geometry': {'type': 'LineString', 'coordinates': coords},
                 'properties': {'id': f'T{n:02d}', 'nom': nom, 'debut': dec(a), 'fin': dec(b, True) if '/' in edtf else dec(a),
                                'date_edtf': edtf, 'certitude': CERT[cert], 'mode': mode, 'description': desc,
                                'sources': src, 'note': note, 'type': 'trajet'}})
P = {f['properties']['id']: f['geometry']['coordinates'] for f in lieux}
T(1, "De New York à Indianapolis", 'train', '1865~', [P['L01'], [-80.0, 40.44], P['L02']], 'h',
  "Veuve, Catherine McCarty quitte New York avec ses fils pour Indianapolis.", u(16), "Itinéraire inconnu ; tracé schématique.")
T(2, "D'Indianapolis à Wichita", 'train', '1870~', [P['L02'], [-90.2, 38.63], [-94.58, 39.1], P['L03']], 'h',
  "La famille gagne le Kansas, où elle est recensée à Wichita en 1870.", u(17), "Itinéraire inconnu ; tracé schématique.")
T(3, "De Wichita à Santa Fe par Denver", 'cheval', '1871-07~/1873-03', [P['L03'], [-101.5, 38.5], [-104.99, 39.74], [-104.82, 38.83], [-105.0, 37.17], [-105.6, 36.4], P['L04']], 'h',
  "La tuberculose de Catherine pousse la famille vers l'air sec de l'Ouest : Denver, puis le sud jusqu'à Santa Fe.", u(17), "Tracé schématique.")
T(4, "De Santa Fe à Silver City par le Rio Grande", 'cheval', '1873-03', [P['L04'], [-106.65, 35.08], [-106.88, 34.06], [-107.25, 33.13], [-107.75, 32.85], P['L05']], 'a',
  "Peu après le mariage, la famille descend le Rio Grande puis oblique à l'ouest vers la ville minière de Silver City.", u(17))
T(5, "Fuite vers l'Arizona", 'cheval', '1875-09', [P['L06'], [-108.95, 32.65], [-109.45, 32.6], P['L07']], 'a',
  "Évadé de la prison de Silver City, Henry gagne l'Arizona et les environs de Camp Grant.", u(18))
T(6, "Retour au Nouveau-Mexique et descente du Pecos", 'cheval', '1877-08/1877-10', [P['L08'], [-108.27, 32.77], [-106.78, 32.31], [-105.66, 32.95], [-104.95, 32.85], P['L09']], 'h',
  "Après la mort de Cahill, le Kid repasse au Nouveau-Mexique, rejoint « The Boys » de Jesse Evans près de La Mesilla et les suit jusqu'au bas Pecos.", u('19-23'), "Tracé schématique.")
T(7, "Du Pecos au Ruidoso", 'cheval', '1877-10', [P['L09'], [-104.52, 33.39], [-104.95, 33.38], P['L10']], 'a',
  "De Seven Rivers, le Kid remonte le Hondo et le Ruidoso jusqu'au ranch des Coe.", u(27))
T(8, "La dernière route de Tunstall", 'cheval', '1878-02-18', [P['L11'], [-105.30, 33.24], P['L12']], 'a',
  "Le 18 février 1878 au matin, Tunstall quitte le Río Feliz vers le nord avec ses hommes et neuf chevaux.", u(37))
T(9, "Les prisonniers de Stinking Springs : Fort Sumner, Las Vegas, Santa Fe", 'cheval', '1880-12-24/1880-12-27', [P['L30'], P['L31'], [-104.68, 34.95], [-105.0, 35.3], P['L32'], [-105.6, 35.55], P['L33']], 'a',
  "Les prisonniers sont ramenés à Fort Sumner, puis conduits en chariot à Las Vegas, et de là en train jusqu'à Santa Fe.", u('102-105'))
T(10, "En train de Santa Fe à La Mesilla", 'train', '1881-03-28', [P['L33'], [-106.65, 35.08], [-106.88, 34.06], [-107.25, 33.13], P['L34']], 'a',
  "Le 28 mars 1881, deux marshals adjoints emmènent Billy et Billy Wilson en train, en descendant la vallée du Rio Grande.", u(106), "Le chemin de fer n'atteignait pas encore La Mesilla ; fin du trajet en voiture.")
T(11, "De La Mesilla à Lincoln, sous escorte", 'cheval', '1881-04-16/1881-04-21', [P['L34'], [-106.0, 32.9], [-105.66, 33.1], P['L35']], 'a',
  "Condamné, Billy est conduit à Lincoln dans un chariot, menotté et enchaîné au siège, sous la garde de sept hommes, dont Billy Mathews et Bob Olinger, ses ennemis jurés.", u('108-109'))
T(12, "L'évadé retourne à Fort Sumner", 'cheval', '1881-04-28/1881-05', [P['L35'], [-105.42, 33.55], [-105.33, 33.40], [-105.05, 32.98], [-104.75, 33.55], [-104.45, 34.0], P['L36']], 'h',
  "Évadé, Billy descend le versant nord des monts Capitan, traverse le Ruidoso en amont de San Patricio et gagne le ranch de son ami John Meadows sur le Peñasco (2 mai 1881). Au lieu de fuir au Mexique, il remonte ensuite vers Fort Sumner et ses amis bergers.", u('112-113'), "Tracé schématique.")

for nom, fs in (('lieux', lieux), ('trajets', traj)):
    json.dump({'type': 'FeatureCollection', 'features': fs}, open(f'{OUT}/data/{nom}.geojson', 'w'), ensure_ascii=False, indent=1)
print(len(lieux), 'lieux,', len(traj), 'trajets')
