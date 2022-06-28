"""
An important module that contains all functions referrer to the manipulation of
    characters, professions, inventory and statistics.

All information is saved in a SQlite local database named 'Roleplay'
"""
import sqlite3
from Professions import *

connection = None
cursor = None
dataBaseName = 'Roleplay'

def DataBaseInitier(function):
    """
    A decorator that open the database connection, execute the decorated function and close database
    """

    def InitDataBase(*args):
        global cursor, connection
        connection = sqlite3.connect(dataBaseName)
        cursor = connection.cursor()
        result = function(*args)
        try:
            cursor.close()
        except:
            pass
        connection = None
        cursor = None
        return result

    InitDataBase.__doc__ = function.__doc__
    return InitDataBase

#--------------------------------------- INVENTORY MANAGEMENT ---------------------------------------

@DataBaseInitier
def InitCharacterInventory(name:str , profession:str):
    """
    Creates a character with the initial profession inventory,
    this will delete characters inventories with the same name and create one new.

    param str name: The name of the character, IMPORTANT: use '_' instead of ' '.
    param str profession: The key name of profession of the character in professionsInitialInventory.

    Returns a str: A fedback message and a list of the current equipment of the created character.
    """

    result = ""
    try:
        cursor.execute(f"DROP TABLE {name}_inv")
        connection.commit()
    except:
        result += "Personaje no encontrado, se procede a crear\n"
    finally:
        cursor.execute(f'''CREATE TABLE {name}_inv (
            'item' VARCHAR(30),
            'cantidad' INTEGER
            )''')
        connection.commit()
        cursor.execute(f"DELETE FROM characters WHERE nombre='{name}'")
        cursor.execute("INSERT INTO characters VALUES (?,?,?,?)", (name,profession, 0, 0))

    cursor.executemany(f"INSERT INTO {name}_inv VALUES (?,?)", professionsInitialInventory[profession])
    connection.commit()
    result += f"{name} creado con el siguiente inventario:"

    result += GetInventory(name)
    return result


@DataBaseInitier
def GetInventory(name:str):
    """
    Get the current full inventory of a character.

    param str name: The name of the character.

    Returns a str: A list of the character inventory.
    """

    result = ""
    cursor.execute(f"SELECT * FROM {name}_inv")
    inventory = cursor.fetchall()
    for item in inventory:
        result += f"\n{item[0]}: {item[1]}"
    return result


@DataBaseInitier
def ModifyIventory(name:str, item:str, value:int):
    """
    Add or remove items from the inventory of a character.

    param str name: The name of the character.
    param str item: The item that will be added or removed. Can be anything
    param int value: The quantity of items, must be negative if you want to remove items,
        if you remove and the current item quantity is <= 0, the item will be removed anyway

    Returns a str: A feedback message and a list of the current inventory after the items was added/removed
    """

    result = ""
    try:
        cursor.execute(f"SELECT cantidad FROM {name}_inv WHERE item='{item}'")
        quantity = cursor.fetchall()
        if(quantity == []):
            if(value > 0):
                cursor.execute(f"INSERT INTO {name}_inv VALUES ('{item}', {value})")
            else:
                result += "No puedo quitarle items que no tiene\n"
                raise TypeError
        else:
            quantity = quantity[0][0]
            newQuantity = quantity + value
            if(newQuantity <= 0):
                cursor.execute(f"DELETE FROM {name}_inv WHERE item='{item}'")
            else:
                cursor.execute(f"UPDATE {name}_inv SET cantidad={newQuantity} WHERE item = '{item}'")

        connection.commit()
        result += f"Inventario de {name} modificado, quedó así:"
        result += GetInventory(name)

    except:
        result += "Hubo un error"

    return result


#--------------------------------------- STATISTICS AND CHARACTER MANAGEMENT ---------------------------------------

@DataBaseInitier
def AddStad(name:str, stad:str, value:int):
    """
    Add a statistics to a character.

    param str name: The name of the character.
    param str stad: The name of the stad. Can be kills, deads, money stoled, anything you want.
    param inf value: The quantity of the stad, can be negative to remove instead of add it, thoug not
        remove the stad if the value is <= 0

    Returns a str: A message that shows the current stads values of the character
    """

    try:
        cursor.execute(f"ALTER TABLE characters ADD COLUMN {stad} INT DEFAULT 0")
        connection.commit()
    except:
        pass

    cursor.execute(f"SELECT {stad} FROM characters WHERE nombre = '{name}'")
    currentStat = cursor.fetchall()
    newStat = int(currentStat[0][0]) + value
    cursor.execute(f"UPDATE characters SET {stad}={newStat} WHERE nombre = '{name}'")
    connection.commit()
    name = name.replace('_',' ')
    return f"{name} ahora tiene {newStat} {stad}"


@DataBaseInitier
def DeleteStad(stadName:str):
    """
    Delete the stad column from the characters table in database

    param str stadName: The name of the column to delete

    Return a str: A feedback message
    """

    try:
        cursor.execute(f"ALTER TABLE characters DROP COLUMN {stadName}")
        connection.commit()
        return f'Estadística {stadName} borrada'
    except:
        return f'Estadística {stadName} no encontrada'
        

@DataBaseInitier
def GetCharacters():
    """
    Display a list of all characters with their stads.

    Return a str: A list of all characters and their stads
    """
    cursor.execute("SELECT * FROM characters")
    characters = cursor.fetchall()
    stads = list(map(lambda x: x[0], cursor.description))

    result = ""
    for i in range(len(characters)):
        name = characters[i][0].replace('_',' ')
        result += f"\n {name}->"
        for j in range(1, len(stads)):
            if(j > 1):
                result += f", {stads[j]}: {characters[i][j]}"
            else:
                result += f" {stads[j]}: {characters[i][j]}"
    return result


@DataBaseInitier
def DeleteCharacter(name:str):
    """
    Delete the character inventory and stads of them.

    param str name: The name of the character to delete.

    Returns a str: A feedback message that notice if was deleted or character not exists.
    """

    try:
        cursor.execute(f"DROP TABLE {name}_inv")
        connection.commit()
        cursor.execute(f"DELETE FROM characters WHERE nombre = '{name}'")
        connection.commit()
    except:
        return f"{name} no existe"

    return f"{name} borrado"