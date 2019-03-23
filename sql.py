import sqlite3
connection = sqlite3.connect('CLEVER.db')
cursor = connection.cursor()

def create_inactives():
    '''
    Creates inactives table
    '''
    cursor.execute("""CREATE TABLE inactives (
        RSN text,
        JOIN_DATE text,
        LAST_XP text,
        RANK text,
        CLAN_XP text,
        MONTHS_INACTIVE integer 
                )""")

    connection.commit()


def delete_inactives():
    cursor.execute("""DROP TABLE inactives""")
    connection.commit()


def add_inactive(rsn, join_date, last_xp, rank, clan_xp, months_inactive):
    with connection:
        cursor.execute("INSERT INTO inactives VALUES (:RSN, :JOIN_DATE, :LAST_XP, :RANK, :CLAN_XP, :MONTHS_INACTIVE)",
                  {'RSN': rsn, 'JOIN_DATE': join_date, 'LAST_XP': last_xp, 'RANK': rank, 'CLAN_XP': clan_xp,
                   'MONTHS_INACTIVE': months_inactive})

def get_inactives(num_inactive = 3):
    '''
    Returns all inactive members based on months supplied
    '''
    cursor.execute("SELECT * FROM inactives WHERE MONTHS_INACTIVE >= :MONTHS_INACTIVE", {'MONTHS_INACTIVE': num_inactive}) #WHERE last_xp LIKE ? ", (('%-'+str(num_inactive)+'-%',)))
    return cursor.fetchall()


def create_stats():
    cursor.execute("""
    CREATE TABLE stats (
    RSN text,
    OVERALL text,
    ATTACK text,
    DEFENCE text,
    STRENGTH text,
    CONSTITUTION text,
    RANGED text,
    PRAYER text,
    MAGIC text,
    COOKING text,
    WOODCUTTING text,
    FLETCHING text,
    FISHING text,
    FIREMAKING text,
    CRAFTING text,
    SMITHING text,
    MINING text,
    HERBLORE text,
    AGILITY text,
    THIEVING text,
    SLAYER text,
    FARMING text,
    RUNECRAFTING text,
    HUNTER text,
    CONSTRUCTION text,
    SUMMONING  text,
    DUNGEONEERING text,
    DIVINATION text,
    INVENTION text
    )""")
    connection.commit()

def add_stats(user):
    pass