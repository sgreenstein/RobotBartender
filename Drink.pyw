class Drink:
    """A mixed drink with a list of ingredients and amounts"""
    def __init__(self, name, ings):
        """Return a new instance of Drink.

        Keyword arguments:
        name -- string, the name of the drink
        ings -- dictionary of Ingredients (keys) and no. of parts (value)
        """
        #set attributes
        self.name = name
        self.ingredients = ings
        #find total number of parts in drink
        total = 0
        for ingredient in self.ingredients:
            total += self.ingredients[ingredient]
        #convert parts to fraction of drink
        for ingredient in self.ingredients:
            self.ingredients[ingredient] /= float(total)

    def make(self, size = 100):
        """Print the actions of making a drink

        Keyowrd arguments:
        size -- int, size of drink in mL (default 100)
        """
        #add each ingredient
        for ingredient in self.ingredients:
            ingredient.add(size * self.ingredients[ingredient])
        print "Your", self.name, "is ready."
