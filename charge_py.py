import requests
from bs4 import BeautifulSoup
import json
from database import Recipe, Ingredient, Step, db_session
from flask import Flask, url_for, request, session, send_from_directory, render_template, jsonify, redirect, flash
from flask_cors import CORS
import flask_restless

app = Flask(__name__, static_url_path='/user_interface/static', template_folder='user_interface/templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'XXXXXXXXXXX'
manager = flask_restless.APIManager(app, session=db_session)


blueprints = [
    manager.create_api_blueprint(Ingredient, methods=['GET', 'PATCH', 'POST'], results_per_page=0),
    manager.create_api_blueprint(Recipe, methods=['GET', 'PATCH', 'POST'], results_per_page=0),
    manager.create_api_blueprint(Step, methods=['GET', 'PATCH', 'POST'], results_per_page=0)
]

for blueprint in blueprints:
    app.register_blueprint(blueprint)

CORS(app)

'''
class Recipe(object):
    def __init__(self, recipe_json):
        self.ingredients = []
        self.instructions = []

        for item in recipe_json:
            if "recipeIngredient" in item:
                for ingredient in item["recipeIngredient"]:
                    self.ingredients.append(ingredient)

            if "recipeInstructions" in item:
                for instruction in item["recipeInstructions"]:
                    self.instructions.append(instruction["text"])

    def print_recipe(self):
        for item in self.ingredients:
            print(item)

        for item in self.instructions:
            print(item)
'''


@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('user_interface/static/', path)


@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello World!'


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/get_recipes', methods=['GET'])
def get_rec():
    return db_session.query(Recipe).all()


def get_recipe(recipe_number):
    web_page = requests.get("https://www.allrecipes.com/recipe/%s" % recipe_number)
    soup = BeautifulSoup(web_page.content, 'html.parser')

    json_contents = json.loads(soup.script.string)
    new_recipe = Recipe()

    for item in json_contents:
        if "recipeIngredient" in item:
            for ingredient in item["recipeIngredient"]:
                new_recipe.ingredients.append(Ingredient(name=ingredient))

        if "recipeInstructions" in item:
            for instruction in item["recipeInstructions"]:
                new_recipe.steps.append(Step(text=instruction))

    db_session.add(new_recipe)
    db_session.commit()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=54321, debug=True)

    '''
    #for i in range(240600, 240602):
    #    get_recipe(i)

    test = db_session.query(Recipe).filter_by(id=1).first()
    ingredeints = db_session.query(Ingredient).filter_by(name="onion", quantity=0.5).all()
    for item in ingredeints:
        print(item.recipe.name)

    print(test.recipe.name)
    print(test.name)
    '''
