-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP VIEW IF EXISTS standings;
DROP TABLE IF EXISTS matches;
DROP TABLE IF EXISTS players;

CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  wins INT DEFAULT 0,
  matches INT DEFAULT 0
  );

CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  winner INT REFERENCES players(id),
  loser INT REFERENCES players(id)
);

CREATE VIEW standings AS
  select id,wins from players
  order by wins DESC
