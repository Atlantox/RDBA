"""
An important module that contains all functions referrer to the manipulation of
    characters, professions, inventory and statistics.

All information is saved in a SQlite local database named 'Roleplay'
"""
import sqlite3
from professions import *


class CharacterManagement():
    """
    Contains methods to manipulate and manage characters inventory and stads
    """

    def __init__(self) -> None:
        self.connection = None
        self.cursor = None
        self.database = 'Roleplay'  # Database name

    #--------------------------------------- DATABASE FUNCTIONS ---------------------------------------

    def open_connection(self) -> None:
        self.connection = sqlite3.connect(self.database)
        self.cursor = self.connection.cursor()
    
    def close_connection(self) -> None:
        self.cursor = None
        try:
            self.connection.close()
        except:
            print('Base de datos ya está cerrada')

    def initialize_database(self) -> None:
        """
        Initialize all the databases necessary tables
        """
        self.open_connection()

        try:
            self.cursor.execute('SELECT * FROM characters')
            self.connection.commit()
            characters = self.cursor.fetchall()
            if not characters:
                print('Tabla characters vacía')
            else:
                stads = list(map(lambda x: x[0], self.cursor.description))
                
                if 'muertes' in stads and 'kills' in stads:
                    print('Base de datos correcta')
                else:
                    print('Tabla characters incorrecta, se procede a añadir las columnas faltantes')

                    if 'muertes' not in stads:
                        self.cursor.execute('ALTER TABLE characters ADD COLUMN muertes INTEGER DEFAULT 0')
                        self.connection.commit()

                    if 'kills' not in stads:
                        self.cursor.execute('ALTER TABLE characters ADD COLUMN kills INTEGER DEFAULT 0')
                        self.connection.commit()
                    print('Tabla characters corregida')
        except:
            self.cursor.execute('''CREATE TABLE characters (
                    'nombre' VARCHAR(30),
                    'clase' VARCHAR(20),
                    'muertes' INTEGER,
                    'kills' INTEGER
                    )''')
            print('Base de datos lista para usar')
            self.connection.commit()

        self.close_connection()


    #--------------------------------------- INVENTORY MANAGEMENT ---------------------------------------

    def initialize_character_inventory(self, name:str , profession:str) -> str:
        """
        Creates a character with the initial profession inventory,
        this will delete characters inventories with the same name and create one new.

        param str name: The name of the character, IMPORTANT: use '_' instead of ' '.
        param str profession: The key name of profession of the character in professionsInitialInventory.

        Returns a str: A fedback message and a list of the current equipment of the created character.
        """

        result = ''
        state = 'creado'
        self.open_connection()

        try:
            self.cursor.execute(f"DROP TABLE {name}_inv")
            self.connection.commit()
            state = 'reseteado'
        except:
            result += "Personaje no encontrado, se procede a crear\n"

        self.cursor.execute(f'''CREATE TABLE {name}_inv (
            'item' VARCHAR(30),
            'cantidad' INTEGER
            )''')
        self.connection.commit()

        try:
            self.cursor.execute(f"DELETE FROM characters WHERE nombre='{name}'")
            self.connection.commit()
        except:
            print('Se intentó borrar un personaje no existente')

        self.cursor.execute("""
            INSERT INTO characters
            (nombre, clase, muertes, kills)
            VALUES (?,?,?,?)""",
        (name,profession, 0, 0))

        self.cursor.executemany(f"INSERT INTO {name}_inv VALUES (?,?)", PROFESSIONS_INVENTORIES[profession])
        self.connection.commit()
        result += f"{name} {profession} {state} con el siguiente inventario:"

        self.close_connection()
        result += self.get_inventory(name)
        return result

    def get_inventory(self, name:str) -> str:
        """
        Get the current full inventory of a character.

        param str name: The name of the character.

        Returns a str: A list of the character inventory.
        """
        result = ''
        self.open_connection()

        try:
            self.cursor.execute(f"SELECT * FROM {name}_inv")
            inventory = self.cursor.fetchall()
            for item in inventory:
                result += f"\n{item[0]}: {item[1]}"
        except:
            result = f'{name} no encontrado'

        self.close_connection()

        return result

    def modify_inventory(self, name:str, item:str, value:int) -> str:
        """
        Add or remove items from the inventory of a character.

        param str name: The name of the character.
        param str item: The item that will be added or removed. Can be anything
        param int value: The quantity of items, must be negative if you want to remove items,
            if you remove and the current item quantity is <= 0, the item will be removed anyway

        Returns a str: A feedback message and a list of the current inventory after the items was added/removed
        """

        result = ''
        self.open_connection()

        try:
            self.cursor.execute(f"SELECT cantidad FROM {name}_inv WHERE item='{item}'")
            quantity = self.cursor.fetchall()
            if(quantity == []):
                if(value > 0):
                    self.cursor.execute(f"INSERT INTO {name}_inv VALUES ('{item}', {value})")
                else:
                    result += "No puedo quitarle items que no tiene\n"
                    raise TypeError
            else:
                quantity = quantity[0][0]
                newQuantity = quantity + value
                if(newQuantity <= 0):
                    self.cursor.execute(f"DELETE FROM {name}_inv WHERE item='{item}'")
                else:
                    self.cursor.execute(f"UPDATE {name}_inv SET cantidad={newQuantity} WHERE item = '{item}'")

            self.connection.commit()
            result += f"Inventario de {name} modificado, quedó así:"
            result += self.get_inventory(name)

        except:
            result += "Hubo un error"

        self.close_connection()

        return result


    #--------------------------------------- STATISTICS AND CHARACTER MANAGEMENT ---------------------------------------

    def add_stad(self, name:str, stad:str, value:int) -> str:
        """
        Add a statistics to a character.

        param str name: The name of the character.
        param str stad: The name of the stad. Can be kills, deads, money stoled, anything you want.
        param inf value: The quantity of the stad, can be negative to remove instead of add it, thoug not
            remove the stad if the value is <= 0

        Returns a str: A message that shows the current stads values of the character
        """
        result = ''
        self.open_connection()

        try:
            self.cursor.execute(f"ALTER TABLE characters ADD COLUMN {stad} INT DEFAULT 0")
            self.connection.commit()
        except:
            pass

        self.cursor.execute(f"SELECT {stad} FROM characters WHERE nombre = '{name}'")
        self.connection.commit()

        currentStat = self.cursor.fetchall()
        if len(currentStat) >= 1:
            newStat = int(currentStat[0][0]) + value
            self.cursor.execute(f"UPDATE characters SET {stad}={newStat} WHERE nombre = '{name}'")
            self.connection.commit()
            name = name.replace('_',' ')
            result = f"{name} ahora tiene {newStat} {stad}"
        else:
            result = f'{name} no encontrado'

        self.close_connection()

        return result

    def delete_stad(self, stadName:str) -> str:
        """
        Delete the stad column from the characters table in database

        param str stadName: The name of the column to delete

        Return a str: A feedback message
        """

        result = ''
        self.open_connection()
        try:
            self.cursor.execute(f"ALTER TABLE characters DROP COLUMN {stadName}")
            self.connection.commit()
            result = f'Estadística {stadName} borrada'
        except:
            result = f'Estadística {stadName} no encontrada'
        
        self.close_connection()

        return result
            
    def get_stads(self, name:str) -> str:
        '''
        Get the stads of a character

        param str name: Character name

        Return a str: The list of stads
        '''

        result = ''
        self.open_connection()

        self.cursor.execute(f"SELECT * FROM characters WHERE nombre = '{name}'")
        stads = self.cursor.fetchall()
        if stads:
            stads = stads[0]
            result = f'{stads[0]}:'
            columns = list(map(lambda x: x[0], self.cursor.description))
            for i in range(1,len(columns)):
                result += f'\n{columns[i]}-> {stads[i]}'
        else:
            result = f'{name} no encontrado'
    
        self.close_connection()

        return result

    def get_characters(self) -> str:
        """
        Display a list of all characters with their stads.

        Return a str: A list of all characters and their stads
        """

        result = ''
        self.open_connection()

        self.cursor.execute("SELECT * FROM characters")
        characters = self.cursor.fetchall()
        stads = list(map(lambda x: x[0], self.cursor.description))

        for i in range(len(characters)):
            name = characters[i][0].replace('_',' ')
            result += f"\n{name}->"
            for j in range(1, len(stads)):
                if(j > 1):
                    result += f", {stads[j]}: {characters[i][j]}"
                else:
                    result += f"{stads[j]}: {characters[i][j]}"

        if result == "":
            result = 'No hay personajes creados'

        self.close_connection()

        return result

    def delete_character(self, name:str) -> str:
        """
        Delete the character inventory and stads of them.

        param str name: The name of the character to delete.

        Returns a str: A feedback message that notice if was deleted or character not exists.
        """
        
        result = ''
        self.open_connection()

        try:
            self.cursor.execute(f"DROP TABLE {name}_inv")
            self.connection.commit()
            self.cursor.execute(f"DELETE FROM characters WHERE nombre = '{name}'")
            self.connection.commit()
            result = f"{name} borrado"
        except:
            result = f"{name} no existe"

        self.close_connection()
        return result