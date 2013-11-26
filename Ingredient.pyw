class Ingredient:
    """A liquid ingredient of a mixed drink"""
    def __init__(self, name, sweetness=0, proof=0, bitterness=0, sourness=0, flavorStrength=0, isCarbonated=False, isCreamy=False):
        """Returns a new Ingredient instance.

        Keyword arguments:
        name -- string, name of ingredient
        sweetness -- scale of 0 to 1 (default 0)
        proof -- 0 to 200 (default 0)
        bitterness -- scale of 0 to 1 (default 0)
        sourness -- scale of 0 to 1 (default 0)
        flavorStrength -- how flavorful, scale of 0 to 1 (default 0)
        isCarbonated -- boolean (default false)
        isCreamy -- boolean, true for milk, for example (default false)
        """
        
        #set attributes
        self.name = name
        self.sweetness = sweetness
        self.proof = proof
        self.bitterness = bitterness
        self.sourness = sourness
        self.flavorStrength = flavorStrength
        self.isCarbonated = isCarbonated
        self.isCreamy = isCreamy
    
    def add(self, amnt):
        """Print the adding of an ingredient

        Keyword arguments:
        amnt -- amount to add, in mL
        """
        print "Adding", amnt, "mL of", self.name
