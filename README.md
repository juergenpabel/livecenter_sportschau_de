# https://livecenter-sportschau-de.appspot.com/

**This is in german, because the provided content is in german**

## tl;dr ##
* Auf http://livecenter-sportschau-de.appspot.com/livestreams/podcast gibt es die Livestreams als Podcast bereitgestellt.
* Auf http://livecenter-sportschau-de.appspot.com/livestreams/redirect gibt es HTTP redirects (HTTP 302) für einzelne Livestreams.
Wie das konkret genutzt werden kann wird im Abschnitt "How-To" weiter unten beschrieben.

## Einführung ##

Auf https://livecenter.sportschau.de stellt die ARD für viele Sportarten Ergebnisse bereit. Für mindestens Bundesliga-Fussball gibt es ab der Saison 2021/22 auch Livestreams: die per Livestream übertragenen Spiele (oder auch Konferenzen) sind dann mit einem entsprechendem Audio-Symbol markiert. Ein Klick auf das Symbol führt zu einer Seite, auf der der Livestream im Browser abgespielt werden kann.

## Motivation ##

Für die Nutzung per Browser (oder wohl auch per Sportschau App, aber nicht selber ausprobiert) ist die Webseite wohl praktisch - für eine Weiterverwendung der darin enthaltenen Livestream-Daten aber *ein Graus*: 
* Die Webseite ist (bzw. war mit Stand September 2021) nicht XHTML konform, so dass eine Transformation per XSLT nicht möglich war
* Die HTML Struktur der Daten-Elemente, die die eigentlichen Spielinformationen ausmachen und die Links auf die Livestreams enthalten ist...sagen wir mal....ungewöhnlich (im Sinne von HTML oder XML oder auch genenrell programmiertechnischer Konstrukte);
* Die auf der Webseite angebotenen RSS Feeds haben auch nicht auf die direkten Livestreams verwiesen, sondern wieder nur auf die Browser-Seiten
**Kurzum: Eine Verwendung außerhalb von Web-Browser und Sportschau-App war nicht möglich.**

Was sind Beispiele für solche andersartigen Verwendungsszenarien?
* Immer die (aktuelle) Bundesliga-Konferenz auf einem Sound-System abspielen: https://livecenter-sportschau-de.appspot.com/livestreams/redirect?comp=Bundesliga
* Immer das (aktuelle) Spiel mit Eintracht Frankfurt auf einem Sound-System abspielen: https://livecenter-sportschau-de.appspot.com/livestreams/redirect?team=Eintracht+Frankfurt
* Ein (aktuelles) Spiel aus der 2. Bundesliga per Podcast-Client auswählen/anhören: https://livecenter-sportschau-de.appspot.com/livestreams/podcast?comp=2.+Bundesliga

## Lösung ##

Auf Google AppEngine läuft eine kleine Python-Anwendung (deren Quelltext in diesem Repository enthalten ist), die sowohl Podcast-Feeds als auch HTTP redirects auf die direkten MP3-Livestreams bereitstellt. Die Bereitstellung erfolgt durch Verarbeitung der von livecenter.sportschau.de bereitgestellten HTML-Seite in python.

## HOWTO ##

Sowohl die Generierung der Podcast-Feeds als auch die der HTTP redirects kann über folgende HTTP GET Parameter gefiltert werden:
* **date**: Für welches Datum, z.B. "2021-09-25"; wenn weggelassen, dann immer das tagesaktuelle Datum
* **comp**: Welcher Wettbewerb, z.B. "Bundesliga" oder "2. Bundesliga" (ohne Anführungszeichen)
* **team**: Welches Team, z.B. "Eintracht Frankfurt" oder "1. FC Köln" (ohne Anführungszeichen)

**WICHTIG**: Sowohl für die Podcast-Generierung als auch dir HTTP-redirect Generierung wird die gleiche Filter-Logik angewendet, aber: in den Podcasts werden alle gefilterten Livestreams aufgeführt - beim HTTP-redirect führt aber der erstbeste Treffer direkt zum Livestream. Hier ist also eine konkrete Parametrisierung wichtig.

Beispiele Podcast:
* Nur 1. Bundesliga-Spiele im Podcast auflisten: https://livecenter-sportschau-de.appspot.com/livestreams/podcast?comp=Bundesliga
* Nur 2. Bundesliga-Spiele im Podcast auflisten: https://livecenter-sportschau-de.appspot.com/livestreams/podcast?comp=2.+Bundesliga
* Nur Spiele mit Eintracht Frankfurt (auch im DFB-Pokal...äh...ach nee), aber vom Prinzíp her: https://livecenter-sportschau-de.appspot.com/livestreams/podcast?team=Eintracht+Frankfurt

Beispiele HTTP-Redirect:
* Das aktuelle Spiel des 1. FC Köln:  https://livecenter-sportschau-de.appspot.com/livestreams/redirect?team=1.+FC+Köln
* Die Bundesliga-Spiele als Konferenz: https://livecenter-sportschau-de.appspot.com/livestreams/redirect?comp=Bundesliga (Hinweis: Sonderfall - hier wird ein fehlender team-Filter als "nehme die Konferenz" interpretiert) 
