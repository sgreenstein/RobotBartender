def main():
    #Create preset ingredients
    #Alcoholic ingredients
    Rum = Ingredient("Rum", sweetness=.2, proof=80, flavorStrength=.3)
    Gin = Ingredient("Gin", proof=100, flavorStrength=1)
    Whiskey = Ingredient("Whiskey", proof=86, flavorStrength=0.5)
    Bourbon = Ingredient("Bourbon", proof=86, flavorStrength=0.5)
    Scotch = Ingredient("Scotch", proof=86, flavorStrength=0.5)
    Vodka = Ingredient("Vodka", proof=80)
    Tequila = Ingredient("Tequila", proof=80, flavorStrength=0.7)
    Bitters = Ingredient("Bitters", proof=70, bitterness=.5, flavorStrength=0.9)
    Pisco = Ingredient("Pisco", proof=70, sweetness=.2, flavorStrength=0.5)

    #Liqueurs
    Kahlua = Ingredient("Kahlua", proof=40, sweetness=.5, flavorStrength=.5, isCreamy=True)
    IrishCream = Ingredient("Irish cream", proof=34, sweetness=.3, flavorStrength=.5, isCreamy=True)
    OrangeLiqueur = Ingredient("Orange liqueur", proof=62, sweetness=.7, flavorStrength=.6)
    PeppermintSchnapps = Ingredient("Peppermint schnapps", proof=50, sweetness=.7, flavorStrength=.7)
    BlueCuracao = Ingredient("Blue curacao", proof=48, sweetness=.8, flavorStrength=.6)

    #Nonalcoholic ingredients
    Milk = Ingredient("Milk", flavorStrength=.3, isCreamy=True)
    Coke = Ingredient("Coke", sweetness=.6, flavorStrength=0.5, isCarbonated=True)
    ClubSoda = Ingredient("Club soda", isCarbonated=True)
    LemonJuice = Ingredient("Lemon juice", sweetness=.3, sourness=1, flavorStrength=.7)
    LimeJuice = Ingredient("Lime juice", sweetness=.3, sourness=1, flavorStrength=.7)
    Grenadine = Ingredient("Grenadine", sweetness=1, flavorStrength=.5)
    SimpleSyrup = Ingredient("Simple syrup", sweetness=1)
    GingerAle = Ingredient("Ginger ale", sweetness=.5, flavorStrength=.3, isCarbonated=True)
    OrangeJuice = Ingredient("Orange juice", sweetness=.2, sourness = 0.2, flavorStrength=.5)
    Water = Ingredient("Water")

    #Create preset drinks
    RumAndCoke = Drink("Rum and coke", {Rum:1,Coke:2})
    GinAndTonic = Drink("Gin and tonic", {Gin:2,ClubSoda:5})
    WhiteRussian = Drink("White russian", {Vodka:2,Milk:4,Kahlua:1})
    Piscola = Drink("Piscola", {Pisco:1,Coke:2})
    ShirleyTemple = Drink("Shirley Temple", {GingerAle:16,Grenadine:1})
    Margarita = Drink("Margarita", {OrangeLiqueur:1,Tequila:4,LemonJuice:1,LimeJuice:1,SimpleSyrup:2})
    Mojito = Drink("Mojito", {Rum:3,LimeJuice:1,SimpleSyrup:1,ClubSoda:5}) #mint
    MintJulep = Drink("Mint julep", {Bourbon:4,SimpleSyrup:1}) #mint
    Screwdriver = Drink("Screwdriver", {Vodka:1,OrangeJuice:2})
    WhiskeySour = Drink("Whiskey sour", {Whiskey:4,SimpleSyrup:3,LemonJuice:3})
    ElectricLemonade = Drink("Electrice lemonade", {Rum:3,BlueCuracao:1,SimpleSyrup:3,LemonJuice:3})
    OldFashioned = Drink("Old-fashioned", {Whiskey:4,SimpleSyrup:2,Bitters:1})
    TequilaSunrise = Drink("Tequila sunrise", {Tequila:8,OrangeJuice:12,Grenadine:1})
    MindEraser = Drink("Mind eraser", {Vodka:1,Kahlua:1,ClubSoda:3})
    LongIslandIcedTea = Drink("Long Island iced tea", {Vodka:1,Gin:1,Rum:1,OrangeLiqueur:1,Tequila:1,SimpleSyrup:2,LemonJuice:2,Coke:1})
    RoyRogers = Drink("Roy Rogers", {Coke:9,Grenadine:1})

    MindEraser.make()
if __name__ == "__main__":
    main()
