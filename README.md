# tietokantasovellus2021
Tietokantojen harjoitustyö HY

In this project I´m gonna build up a simple bulletin board.
I´m doing this for a database course at Helsinki University.
Here're some remarks of the contents I´m supposed to include (Sorry, in Finnish so far...):

Tietokantojen harjoitustyö HY 2021/Keskustelusovellus:

Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.

VÄLIPALAUTUS 2:


Githubin readme päivitetty, siitä selviää projektin tämänhetkinen tila. Unohdin mainita, että syötteentarkistukset on tekemättä joten aika ankeita viestejä/käyttäjänimiä jne menee läpi.

Heroku:

https://tsoha2021vuorenmaa.herokuapp.com/

Admintunnukset: testaaja1: 1234 Usertunnukset (voi myös rekisteröityä itse): Miau:1234

23.09.2021, 17:18:19
Antti Vuorenmaa
Ai niin, koska olen melko noviisi näissä ottaisin mieluusti vastaan (kriittistäkin) palautetta myös koodin muodollisesta oikeellisuudesta ja committien tyylistä, että sais alusta asti opeteltua Pythonia/Gittiä ettei tuu spagettia.

Kiitos!



Voit luoda rekisteröitymällä käyttäjätunnuksen ja salasanan, jolle luodaan user-oikeudet.

PROJEKTIN VAIHE:

VALMISTA/VAATIMUKSET:

Käyttäjä voi kirjautua sisään ja ulos sekä luoda uuden tunnuksen.OK
Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.OK
Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.OK
Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.OK
Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.OK
Ylläpitäjä voi lisätä ja poistaa keskustelualueita.OK

PUUTTEITA/VAATIMUKSET:

Käyttäjä voi muokata luomansa ketjun otsikkoa sekä lähettämänsä viestin sisältöä. Käyttäjä voi myös poistaa ketjun tai viestin.VOI POISTAA VIESTIN, MUTTA KETJUN OTSIKON POISTO JA VIESTIEN/OTSIKOIDEN MUOKKAAMINEN PUUTTUU.
Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.PUUTTUU, USERSTAULUSSA ON TÄLLE VALMIUS. YLLÄPIDON SIVULLA ON JO LISTATTUNA KÄYTTÄJÄT, TÄHÄN LIITETÄÄN OIKEUKSIEN MUUTTAMINEN.

Muita tiedossa olevia vajavaisuuksia:

-tietoturva on kunnossa roolien ja SQL-injektion osalta, CSRF ja XSS vielä puutteellinen.
-ulkoasu aika raakile
-SQL-kyselyt eivät kaikilta osin ole tehokkaimpia vaan ehkä toistaiseksi haetaan liian monessa kyselyssä, niitä voisi varmaan yhdistää.

