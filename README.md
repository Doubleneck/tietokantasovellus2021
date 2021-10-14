# tietokantasovellus2021
In this project I´m gonna build up a simple bulletin board.
I´m doing this for a database course at Helsinki University.

Tietokantojen harjoitustyö HY 2021/Keskustelusovellus:

Sovelluksessa näkyy keskustelualueita, joista jokaisella on tietty aihe. Alueilla on keskusteluketjuja, jotka muodostuvat viesteistä. Jokainen käyttäjä on peruskäyttäjä tai ylläpitäjä.


Heroku:

https://tsoha2021vuorenmaa.herokuapp.com/

Testaamista varten: 

-Tavalliseksi käyttäjäksi kirjaudu ja luo tunnukset
-Admintunnukset: Admin2, password:tsoha21 (voit muuttaa luomasi tunnusten oikeuksia admin-käyttäjänä).
-Valmiit priviledged user -tunnukset: Oxygen, password:rantapallo.


- [x] Käyttäjä voi kirjautua sisään ja ulos sekä rekisteröityä ja luoda uuden tunnuksen.
- [x] Käyttäjä näkee sovelluksen etusivulla listan alueista sekä jokaisen alueen ketjujen ja viestien määrän ja viimeksi lähetetyn viestin ajankohdan.
- [x] Käyttäjä voi luoda alueelle uuden ketjun antamalla ketjun otsikon ja aloitusviestin sisällön.
- [x] Käyttäjä voi kirjoittaa uuden viestin olemassa olevaan ketjuun.
- [x] Käyttäjä voi etsiä kaikki viestit, joiden osana on annettu sana.
- [x] Ylläpitäjä voi lisätä ja poistaa keskustelualueita.
- [x] Käyttäjä voi poistaa viestin.
- [x] tietoturva: roolit, ja SQL-injektio, XSS.
- [x] Käyttäjä voi muokata lähettämänsä viestin sisältöä.
- [x] Ylläpitäjä voi luoda salaisen alueen ja määrittää, keillä käyttäjillä on pääsy alueelle.
- [x] Käyttäjä ja ylläpitäjä voi poistaa ketjun
- [x] Käyttäjä voi muokata luomansa ketjun otsikkoa. 
- [x] Admin voi muokata ketjun otsikkoa. 
- [x] syötteentarkistukset: username, password, message, topic (=message chain title)
- [x] ulkoasu
- [x] tietoturva: CSRF 
- [x] Kolmannen välipalautuksen fixit tehty
