from copy import deepcopy

from django.shortcuts import render


DATA = {
    'omlet': {
        'Название': 'Классический омлет',
        'Ингредиенты': {
            'яйца, шт': 2,
            'молоко, л': 0.1,
            'соль, ч.л.': 0.5,
        }
    },
    'pasta': {
        'Название': 'Простая паста с сыром',
        'Ингредиенты': {
            'макароны, г': 0.3,
            'сыр, г': 0.05,
        }
    },
    'buter': {
        'Название': 'Бутерброд "обыкновенный"',
        'Ингредиенты': {
            'хлеб, ломтик': 1,
            'колбаса, ломтик': 1,
            'сыр, ломтик': 1,
            'помидор, ломтик': 1,
        }
    },
}


def show_recipes_list(request):
    recipes = {itm: DATA.get(itm).get('Название') for itm in DATA}
    context = {
        'recipes': recipes
    }
    return render(request, 'calculator/index.html', context)


def show_recipe(request, recipe_key):
    mult = int(request.GET.get('servings', 1))
    recipe_name = DATA.get(recipe_key).get('Название')
    ingredients = DATA.get(recipe_key).get('Ингредиенты')

    ingredients_with_qty = deepcopy(ingredients)
    ingredients_with_qty.update((ingred, qty * mult) for ingred, qty in ingredients_with_qty.items())

    context = {
        'recipe_key': recipe_key,
        'recipe_name': recipe_name,
        'ingredients': ingredients_with_qty
    }
    return render(request, 'calculator/recipe.html', context)
