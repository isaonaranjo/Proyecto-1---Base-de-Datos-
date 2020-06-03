-- 1 | Total de ventas por semana dado un rango de fechas a ser ingresado por el usuario

-- 2 | Los N (<-ingresado por el usuario) artistas con las mayores ventas para un rango de fechas a ser ingresado por el usuario
CREATE VIEW ventas_por_artista AS
SELECT artist.name, invoice.invoicedate, invoice.total
FROM artist
JOIN album on artist.artistid = album.artistid
JOIN track on track.albumid = album.albumid
JOIN invoiceline on invoiceline.trackid = track.TrackId
JOIN invoice on invoiceline.invoiceid = invoice.invoiceid

-- SELECT a utilizarse para el 2 en python:
-- select name, sum(total) FROM ventas_por_artista WHERE invoicedate > (ingresado por usu) AND invoicedate < (ingresado por usu)
-- GROUP BY name ORDER BY sum(total) DESC LIMIT (ingresado por usu)

-- 3 | Total de ventas por genero para un rango de fechas a ser ingresado por el usuario
CREATE VIEW ventas_por_genero AS
SELECT genre.name, invoice.total, invoice.invoicedate
FROM genre
JOIN track ON track.genreid = genre.genreid
JOIN invoiceline ON invoiceline.trackid = track.trackId
JOIN invoice ON invoice.invoiceid = invoiceline.invoiceid

-- SELECT a utilizarse para el 3 en python:
-- select name, sum(total) FROM ventas_por_genero WHERE invoicedate > (ingresado por usu) AND invoicedate < (ingresado por usu)
-- GROUP BY name ORDER BY sum(total) DESC

-- 4 | Las n (<-ingresado por el usuario) canciones con mas reporiducciones para un artista a ser ingresado por el usuario
CREATE VIEW reprod_por_artista AS
SELECT artist.name, track.name, reproducciones.cant_rep
FROM reproducciones
JOIN track ON track.trackid = reproducciones.songid
JOIN album ON track.albumid = album.albumid
JOIN artist ON album.artistid = artist.artistid

-- SELECT a utilizarse para el 4 en python:
-- select artist.name, track.name, sum(cant_rep) FROM reprod_por_artista WHERE artist.name = (ingresado por usu) GROUP BY track.name LIMIT (ingresado por usu)
