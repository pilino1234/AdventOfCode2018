

def improve_recipes(amount):
    recipes = [3, 7]

    elf1 = 0
    elf2 = 1

    while len(recipes) < amount + 10:
        # Create new recipes
        new = recipes[elf1] + recipes[elf2]
        for c in str(new):
            recipes.append(int(c))

        # Advance elf current recipes
        elf1 += (recipes[elf1] + 1)
        elf1 %= len(recipes)
        elf2 += (recipes[elf2] + 1)
        elf2 %= len(recipes)

    print("".join(str(recipes[x]) for x in range(amount, amount+10)))


def improve_recipes2(scores):
    recipes = [3, 7]

    elf1 = 0
    elf2 = 1

    while True:
        # Create new recipes
        new = recipes[elf1] + recipes[elf2]
        recipes.extend(list(map(int, str(new))))

        # Advance elf current recipes
        elf1 += (recipes[elf1] + 1)
        elf1 %= len(recipes)
        elf2 += (recipes[elf2] + 1)
        elf2 %= len(recipes)

        idx = "".join(list(map(str, recipes[-10:]))).find(str(scores))
        if idx > 0:
            print("".join(list(map(str, recipes))).find(str(scores)))
            break


if __name__ == '__main__':
    INPUT = 190221

    improve_recipes(INPUT)
    improve_recipes2(INPUT)
