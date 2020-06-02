--Insertar en track, playlist, artista, album

CREATE OR REPLACE FUNCTION add_track_bitacora()
RETURNS TRIGGER AS
$$
BEGIN
	INSERT INTO bitacora(username,fecha,tipo,accion, nombre)
	VALUES( NEW.useradd, now(),'track','agregada', NEW.name);
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER nw_track_bitacora
BEFORE INSERT
ON Track
FOR EACH ROW
EXECUTE PROCEDURE add_track_bitacora();


--INSERTAR PLAYLIST
CREATE OR REPLACE FUNCTION add_playlist_bitacora()
RETURNS TRIGGER AS
$$
BEGIN
	INSERT INTO bitacora(username,fecha,tipo,accion, nombre)
	VALUES( NEW.useradd, now(),'playlist','agregada', NEW.name);
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER nw_playlist_bitacora
BEFORE INSERT
ON playlist
FOR EACH ROW
EXECUTE PROCEDURE add_playlist_bitacora();


--INSERTAR ARTISTA
CREATE OR REPLACE FUNCTION add_artist_bitacora()
RETURNS TRIGGER AS
$$
BEGIN
	INSERT INTO bitacora(username,fecha,tipo,accion, nombre)
	VALUES( NEW.user_edit, now(),'Artista','agregada', NEW.name);
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER nw_artist_bitacora
BEFORE INSERT
ON Artist
FOR EACH ROW
EXECUTE PROCEDURE add_artist_bitacora();

--INSERTAR ALBUM
CREATE OR REPLACE FUNCTION add_album_bitacora()
RETURNS TRIGGER AS
$$
BEGIN
	INSERT INTO bitacora(username,fecha,tipo,accion, nombre)
	VALUES( NEW.user_edit, now(),'album','agregada', NEW.title);
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER nw_album_bitacora
BEFORE INSERT
ON Album
FOR EACH ROW
EXECUTE PROCEDURE add_album_bitacora();

/*********************************************************************/
/*EDITAR TRACK*/
CREATE OR REPLACE FUNCTION edit_track_bitacora()
RETURNS TRIGGER AS
$$
BEGIN
	INSERT INTO bitacora(username,
						 fecha,
						 tipo,
						 accion,
						 nombre,
						 old_nombre, 
						 genre_old, 
						 genre, 
						 time_old,
						 time_nw,
						 price_old ,
    					price_nw ,
    					album_nw,
    					album_old)
	VALUES(NEW.user_edit, now(),'Track','Modificado', NEW.name,OLD.name
		   ,OLD.genreid,NEW.genreid,OLD.milliseconds,NEW.milliseconds,
		  OLD.unitprice,NEW.unitprice,NEW.albumid,OLD.albumid);
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER ed_track_bitacora
BEFORE UPDATE
ON Track
FOR EACH ROW
EXECUTE PROCEDURE edit_track_bitacora();

/*EDITAR ARTISTA*/
CREATE OR REPLACE FUNCTION edit_artist_bitacora()
RETURNS TRIGGER AS
$$
BEGIN
	INSERT INTO bitacora(username,fecha,tipo,accion, nombre,old_nombre)
	VALUES(NEW.user_edit, now(),'artista','modificado', NEW.name,old.name);
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER ed_artist_bitacora
BEFORE UPDATE
ON Artist
FOR EACH ROW
EXECUTE PROCEDURE edit_artist_bitacora();

/*EDITAR ALBUM*/
CREATE OR REPLACE FUNCTION edit_album_bitacora()
RETURNS TRIGGER AS
$$
BEGIN
	INSERT INTO bitacora(username,fecha,tipo,accion, nombre,old_nombre)
	VALUES(NEW.user_edit, now(),'Album','modificado', NEW.title,old.title);
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER ed_album_bitacora
BEFORE UPDATE
ON Album
FOR EACH ROW
EXECUTE PROCEDURE edit_album_bitacora();

/*EDITAR PLAYLIST*/

CREATE OR REPLACE FUNCTION edit_playlist_bitacora()
RETURNS TRIGGER AS
$$
BEGIN
	INSERT INTO bitacora(username,fecha,tipo,accion, nombre, old_nombre)
	VALUES(NEW.user_edit, now(),'Album','modificado', NEW.name,old.name);
RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER ed_playlist_bitacora
BEFORE UPDATE
ON Playlist
FOR EACH ROW
EXECUTE PROCEDURE edit_playlist_bitacora();


/********************************************************************/
/*ELIMINAR TRACK*/
CREATE OR REPLACE FUNCTION delete_track_bitacora()
RETURNS TRIGGER AS
$$
DECLARE 
usuario  VARCHAR(30);
BEGIN
	DELETE FROM bitacora WHERE fecha IN (SELECT fecha FROM bitacora WHERE fecha<now() ORDER BY FECHA DESC LIMIT 1);
	usuario := (SELECT user_edit FROM track WHERE track.name = old.name);
	INSERT INTO bitacora(username, fecha,tipo,accion,nombre)
	VALUES(usuario, now(),'Track','Eliminado',old.name);
RETURN OLD;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER del_track_bitacora
BEFORE DELETE
ON Track
FOR EACH ROW
EXECUTE PROCEDURE delete_track_bitacora();

/*ELIMINAR ARTISTA*/
CREATE OR REPLACE FUNCTION delete_artist_bitacora()
RETURNS TRIGGER AS
$$
DECLARE 
usuario  VARCHAR(30);
BEGIN
	DELETE FROM bitacora WHERE fecha IN (SELECT fecha FROM bitacora WHERE fecha<now() ORDER BY FECHA DESC LIMIT 1);
	usuario := (SELECT user_edit FROM artist WHERE artist.name = old.name);
	INSERT INTO bitacora(username, fecha,tipo,accion,nombre)
	VALUES(usuario, now(),'Artista','Eliminado',old.name);
RETURN OLD;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER del_artist_bitacora
BEFORE DELETE
ON Artist
FOR EACH ROW
EXECUTE PROCEDURE delete_artist_bitacora();

/*ELIMINAR ALBUM*/
CREATE OR REPLACE FUNCTION delete_album_bitacora()
RETURNS TRIGGER AS
$$
DECLARE 
usuario  VARCHAR(30);
BEGIN
	DELETE FROM bitacora WHERE fecha IN (SELECT fecha FROM bitacora WHERE fecha<now() ORDER BY FECHA DESC LIMIT 1);
	usuario := (SELECT user_edit FROM album WHERE album.title = old.title);
	INSERT INTO bitacora(username, fecha,tipo,accion,nombre)
	VALUES(usuario, now(),'Album','Eliminado',old.title);
RETURN OLD;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER del_album_bitacora
BEFORE DELETE
ON Album
FOR EACH ROW
EXECUTE PROCEDURE delete_album_bitacora();

/*ELIMINAR PLAYLIST*/
CREATE OR REPLACE FUNCTION delete_playlist_bitacora()
RETURNS TRIGGER AS
$$
DECLARE 
usuario  VARCHAR(30);
BEGIN
	DELETE FROM bitacora WHERE fecha IN (SELECT fecha FROM bitacora WHERE fecha<now() ORDER BY FECHA DESC LIMIT 1);
	usuario := (SELECT user_edit FROM playlist WHERE playlist.name = old.name);
	INSERT INTO bitacora(username, fecha,tipo,accion,nombre)
	VALUES(usuario, now(),'Album','Eliminado',old.name);
RETURN OLD;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER del_playlist_bitacora
BEFORE DELETE
ON Playlist
FOR EACH ROW
EXECUTE PROCEDURE delete_playlist_bitacora();
