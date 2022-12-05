"""
A module that contains all functions that reference the use of dices 
"""

from random import randrange
import os

class Dice():
    """
    Class that contains all dices methods
    """


    def launch_dice(min:int, max:int, times:int, rep:bool = True):
        """
        Launch a especify number of dices.

        param int min: The smallest number of the dice.
        param int max: The greatest number of the dice.
        param int times: The quantity of dices to launch.
        param bool rep: False if you want the results don't repeat. Per default True.

        """

        """
        Necessaries variables to use the commented code more forward

        timeSpace = len(str(tim)) + 4
        timeValue = ""
        numSpace = len(str(max)) 
        numValue = ""

        """
        
        numbersShowed = []
        finalText = ''
        if min == 1:
            finalText = f'Lanzando **{times} d{max}**:\n'
        else:
            finalText = f'Generando **{times}** número(s) entre **{min}** y **{max}**:\n'
        for i in range(times):
            if not rep and times <= max:
                while True:
                    result = randrange(min,max + 1)
                    if not(result in set(numbersShowed)):
                        numbersShowed.append(result)
                        break
            elif not rep and times > max:
                return "Me pides más repeticiones de las posibles"
            else:
                result = randrange(min,max + 1)

            """
            timeValue = f" Nº{i + 1} "
            while(len(timeValue) < timeSpace):
                timeValue += " "
            numValue = f"{result}"
            while(len(numValue) < numSpace):
                numValue += " "
            finalText += f"|{timeValue}| {numValue} |\n"

            This is for display the numbers like that:

            | Nº1 | 100 |
            | Nº2 | 26  |
            | Nº3 | 4   |
            | Nº4 | 12  |
            | Nº5 | 2   |
            | Nº6 | 56  |
            
            In console the looks good, but in Discord that separation is not respected and looks ugly
            """

            finalText += f"-> **{result}**\n"
        return finalText


    def get_dice_path(diceNumber:int):
        """
        Get the path of a dice image

        param int diceNumber: the dice image to show

        return a string with the fullpath of the image
        
        """
        
        path = os.getcwd()
        path = path.replace('\\', '/')
        path = f"{path}/bot_images/dices/{diceNumber}.png"
        print(path)
        return path