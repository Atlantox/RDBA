"""
A module that contains a list of tuples that represent the initial equipment of each
    profession/class in your roleplay game, the structure is:

    'Profession': (
            ('Item 1 name', item 1 quantity),
            ('Item 2 name', item 2 quantity),
            ('Item 3 name', item 3 quantity),
    )


"""

PROFESSIONS_INVENTORIES = {
    'Guerrero': (
        ('Espada',1),
        ('Armadura',1),
        ('Escudo',1),
        ('Poción',1)
    ),
    'Táctico': (
        ('Estoque',1),
        ('Armadura',1),
        ('Catalejo',1),
        ('Mapa',1)
    ),
    'Sigiloso': (
        ('Daga de pícaro',1),
        ('Herramientas de ladrón',1),
        ('Cuchillas venenosas',3)
    ),
    'Apoyo': (
        ('Ballesta',1),
        ('Flechas',8),
        ('Armadura',1),
        ('Botiquín',3),
        ('Granada pegajosa',3)
    ),
    'Mago': (
        ('Báculo',1),
        ('Libro de hechizos',1),
        ('Lápiz',1),
        ('Daga normal',1)
    )
}