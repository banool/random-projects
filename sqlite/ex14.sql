drop table person;
drop table pet;
drop table person_pet;

/* ===== Exercise 2 ===== */
CREATE TABLE person (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    age INTEGER
);

CREATE TABLE pet (
    id INTEGER PRIMARY KEY,
    name TEXT,
    breed TEXT,
    age INTEGER,
    dead INTEGER
);

CREATE TABLE person_pet (
    person_id INTEGER,
    pet_id INTEGER
);

/* ===== Exercise 3 ===== */
INSERT INTO person (id, first_name, last_name, age)
    VALUES (0, "Daniel", "Porteous", 19);
INSERT INTO person (id, first_name, last_name, age)
    VALUES (1, "Meghan", "Porteous", 18);
INSERT INTO person (id, first_name, last_name, age)
    VALUES (2, "Andrew", "Porteous", 63);
INSERT INTO person (id, first_name, last_name, age)
    VALUES (3, "Deborah", "Porteous", 48);

INSERT INTO pet (id, name, breed, age, dead)
    VALUES (0, "Nudge", "Dog", 8, 1);

INSERT INTO pet VALUES (1, "Toothless", "Cat", 6, 0);

INSERT INTO pet (id, name, breed, age, dead)
    VALUES (2, "Copen", "Cat", 3, 0);
INSERT INTO pet (id, name, breed, age, dead)
    VALUES (3, "Hagen", "Cat", 3, 0);

/* ===== Exercise 4 ===== */
INSERT INTO person_pet (person_id, pet_id) VALUES (0, 1);
INSERT INTO person_pet (person_id, pet_id) VALUES (1, 2);
INSERT INTO person_pet (person_id, pet_id) VALUES (1, 3);

/* ===== Exercise 6 ===== */
SELECT pet.id, pet.name, pet.age, pet.dead
    FROM pet, person_pet, person
    WHERE
    pet.id = person_pet.pet_id AND
    person_pet.person_id = person.id AND
    person.first_name = "Daniel";

/* ===== Exercise 7 ===== */
select name,age from pet where dead=1; /* Not necessary to delete, just seeing that there is something to delete */
DELETE FROM pet WHERE dead = 1;
iNSERT INTO pet VALUES (0, "Nudge", "Dog", 1, 1); /* Readding the dead brown */
SELECT * FROM pet; /* see? */

/* ===== Exercise 8 ===== */
/* Deleting my pets */
delete from pet where id in (
    select pet.id
    from pet, person, person_pet
    where
    person.id = person_pet.person_id AND
    pet.id = person_pet.pet_id AND
    person.first_name = "Daniel"
);

/* Showing remaining pets */
SELECT * FROM pet;
/* Showing that the link to my now non-existant pet is still there */
SELECT * FROM person_pet;

/* Deleting links from person_pet for which there is no ID anymore in the pet table */
DELETE FROM person_pet
    WHERE pet_id NOT IN (
        SELECT id FROM pet
    );

/* Showing the remaining links, now just for Meg 1, none for me 0. */
SELECT * FROM person_pet;

/* Adding a relation between Dad and Nudge and showing it */
insert into person_pet (person_id, pet_id) values (2, 0);
SELECT * FROM person_pet;

/* Now we're deleting people who have dead pets */
delete from person where id in (
    select person.id
    from pet, person, person_pet
    where
    person.id = person_pet.person_id AND
    pet.id = person_pet.pet_id AND
    pet.dead = 1
);

/* Showing that Dad is now gone */
SELECT * FROM person;
/* Showing that the link between dad and nudge is still there */
SELECT * FROM person_pet;

/* Removing Dad from the relation table */
DELETE FROM person_pet
    WHERE person_id NOT IN (
        SELECT id FROM person
    );

/* Showing the remaining links, now just for Meg (1), none for me (0) or dad (2). */
SELECT * FROM person_pet;

/* Rebuilding the tables */
drop table person;
drop table pet;
drop table person_pet;

CREATE TABLE person (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    age INTEGER
);

CREATE TABLE pet (
    id INTEGER PRIMARY KEY,
    name TEXT,
    breed TEXT,
    age INTEGER,
    dead INTEGER
);

CREATE TABLE person_pet (
    person_id INTEGER,
    pet_id INTEGER
);

INSERT INTO person (id, first_name, last_name, age)
    VALUES (0, "Daniel", "Porteous", 19);
INSERT INTO person (id, first_name, last_name, age)
    VALUES (1, "Meghan", "Porteous", 18);
INSERT INTO person (id, first_name, last_name, age)
    VALUES (2, "Andrew", "Porteous", 63);
INSERT INTO person (id, first_name, last_name, age)
    VALUES (3, "Deborah", "Porteous", 48);

INSERT INTO pet (id, name, breed, age, dead)
    VALUES (0, "Nudge", "Dog", 8, 1);

INSERT INTO pet VALUES (1, "Toothless", "Cat", 6, 0); /* Bad practice */

INSERT INTO pet (id, name, breed, age, dead)
    VALUES (2, "Copen", "Cat", 3, 0);
INSERT INTO pet (id, name, breed, age, dead)
    VALUES (3, "Hagen", "Cat", 3, 0);

INSERT INTO person_pet (person_id, pet_id) VALUES (0, 1);
INSERT INTO person_pet (person_id, pet_id) VALUES (1, 2);
INSERT INTO person_pet (person_id, pet_id) VALUES (1, 3);
INSERT INTO person_pet (person_id, pet_id) VALUES (2, 0);

/* Breaking links to dead pets */
DELETE FROM person_pet where pet_id in (
    select person_pet.pet_id
    from pet, person, person_pet
    where
    pet.id = person_pet.pet_id and
    pet.dead = 1
);

/* Showing the remaining links, Dad's (2) now being gone. */
SELECT * FROM person_pet;

/* ===== Exercise 9 ===== */
update pet set name = "Brown" where name = "Nudge";
update pet set name = "Nudge" where id = 0;
SELECT * FROM person;

/* ===== Exercise 10 ===== */
SELECT * FROM pet;

UPDATE pet SET name = "Daniel's Pet" WHERE id IN (
    SELECT pet.id
    FROM pet, person_pet, person
    WHERE
    person.id = person_pet.person_id AND
    pet.id = person_pet.pet_id AND
    person.first_name = "Daniel"
);

SELECT * FROM pet;
update pet set name = "Toothless" where name = "Daniel's Pet";

/* ===== Exercise 11 ===== */
/* This will fail because there is already someone at id 0 */
insert into person (id, first_name, last_name, age) values (0, "Random", "Guy", 69);
/* Replaces this time, this works */
insert or replace into person (id, first_name, last_name, age)
    values (0, "Random", "Guy", 69);
SELECT * FROM person;
/* Shorthand for the previous command */
replace into person (id, first_name, last_name, age)
    values (0, "Daniel", "Porteous", 19);
SELECT * FROM person;

/* ===== Exercise 12 ===== */
/* Only drop table if it exists. */
/*DROP TABLE IF EXISTS person;*/

/* Create again to work with it. */
CREATE TABLE person (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    age INTEGER
);

/* Rename the table to peoples. */
ALTER TABLE person RENAME TO peoples;

/* Add a hatred column to peoples. */
/*ALTER TABLE pet ADD COLUMN dob DATETIME;*/

/* Rename peoples back to person. */
ALTER TABLE peoples RENAME TO person;

/* We don't need that. */
/*DROP TABLE person;*/


/* ===== Exercise 13 ===== */
/* Doing prelim stuff to get ready for the assignemnt */
.schema

/* k leggo */
alter table person add column dead integer;
alter table person add column phone_number text;
alter table person add column salary float;
ALTER TABLE person ADD COLUMN dob DATETIME;
alter table person_pet add column purchased_on DATETIME;
alter table pet add column parent integer;
update person set dead=0, phone_number="0417 104 590", salary=30000, dob=-555724800 where first_name="Andrew";
update person set dead=0, phone_number="0429 140 296", salary=19500, dob=824270400 where first_name="Daniel";
update person set dead=0, phone_number="0408 971 997", salary=800, dob=868464000 where first_name="Meghan";
update person set dead=0, phone_number="0409 174 725", salary=85000, dob=-79257600 where first_name="Deborah";
update pet set parent=-1;
UPDATE person_pet SET purchased_on=1364486400 WHERE person_id IN (
    SELECT person.id
    FROM pet, person_pet, person
    WHERE
    person.id = person_pet.person_id AND
    pet.id = person_pet.pet_id AND
    person.first_name = "Meghan"
);
update person_pet set purchased_on=1431446400 where person_pet.pet_id=1;
insert into person_pet (person_id, pet_id, purchased_on) values (2, 0, 1147449600);
insert into pet (id, name, breed, age, dead, parent) values (4, "nudge's mum?", "dog", 13, 1, -1);
update pet set parent=4 where name="Nudge";
SELECT * FROM person;
SELECT * FROM pet;
SELECT * FROM person_pet;

/* All pets purchased after 2008 */
SELECT pet.name, person.first_name
    FROM pet, person_pet, person
    WHERE
    person.id = person_pet.person_id AND
    pet.id = person_pet.pet_id AND
    person_pet.purchased_on > 1199145600 /* 2008 */
;

/* All children of nudge's mum? */
SELECT name from pet where pet.parent = (select id from pet where name = "nudge's mum?");

/* ===== Exercise 14 ===== */
/* Made fresh */
alter person add column swag? integer; /* Forced error */

/* ===== Exercise 15 ===== */
/* This is all great advice for how to plan out a database */
/* TODO The extra credit here is big but something that is definitely worth doing TODO */
