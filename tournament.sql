-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

CREATE TABLE players (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL
  --wins INT DEFAULT 0,
  --matches INT DEFAULT 0
  );

CREATE TABLE matches (
  id SERIAL PRIMARY KEY,
  winner INT REFERENCES players(id),
  loser INT REFERENCES players(id)
);

-- created a view, but its not completely necessary
CREATE VIEW standings AS
  select p.id,count(m1.*) as wins, (count(m1.*) + count(m2.*)) as matches from players p
  left join matches m1 on m1.winner = p.id
  left join matches m2 on m2.loser = p.id
  group by p.id
  order by 2 DESC;
