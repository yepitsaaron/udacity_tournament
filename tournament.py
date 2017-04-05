#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete FROM matches;")
    c.execute("update players set matches = 0, wins = 0;")
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("delete FROM players;")
    conn.commit()
    conn.close()

def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    c = conn.cursor()
    c.execute("select count(*) FROM players;")
    result = c.fetchone()
    conn.close()
    return result[0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    c = conn.cursor()
    # when substituting, make sure to (basic) sanitize the input
    c.execute("insert INTO players(name) values(%s)", (name,))
    conn.commit()
    conn.close()

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    c = conn.cursor()
    c.execute("select * FROM players order by wins desc;")
    results = c.fetchall()
    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()
    c.execute("insert INTO matches(winner,loser) values(%i,%i)" % (winner,loser))
    # update winner
    c.execute("update players set wins = (wins+1),matches = (matches+1) where id = %i" % winner)
    # update loser
    c.execute("update players set matches = (matches+1) where id = %i" % loser)
    conn.commit()
    conn.close()
 
def swissPairings():
    conn = connect()
    c = conn.cursor()
    # determine the max # of wins for initial pairing
    c.execute("select max(wins) FROM players;")
    results = c.fetchone()
    max_wins = results[0]
    # find winning pairings
    c.execute("select s.id,p.name FROM standings s join players p on s.id=p.id where s.wins = %s order by s.wins desc;" % max_wins)
    winning_players = c.fetchall()
    # add winning players to array
    winning_pairs = []
    for i in range(1, len(winning_players), 2):
        # to eliminate the extra set of parenthesis, we have to return the actual values of the dict
        winning_pairs += [(winning_players[i - 1][0],winning_players[i - 1][1], winning_players[i][0],winning_players[i][1])]

    # find losing pairs
    c.execute("select s.id,p.name FROM standings s join players p on s.id=p.id where s.wins < %s order by s.wins desc;" % max_wins)
    losing_players = c.fetchall()
    losing_pairs = []
    for i in range(1, len(losing_players), 2):
        # to eliminate the extra set of parenthesis, we have to return the actual values of the dict
        losing_pairs += [(losing_players[i - 1][0],losing_players[i - 1][1], losing_players[i][0],losing_players[i][1])]
    # add winning and losing lists together
    pairs = winning_pairs + losing_pairs
    conn.close()
    return pairs