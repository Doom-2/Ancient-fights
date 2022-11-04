from flask import Flask, render_template, request, redirect, url_for
from base import Arena
from unit import BaseUnit, PlayerUnit, EnemyUnit
from equipment import Equipment
from classes import unit_classes

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()  # Initializing the Arena class


@app.route("/")
def menu_page():
    """
    'New game' button.
    Renders 'index.html' template.
    """
    return render_template('index.html')


@app.route("/fight/")
def start_fight():
    """
    Initializes players and renders 'fight.html' template.
    Changes 'game_is_running' flag of Arena class.
    """
    arena.start_game(player=heroes['player'], enemy=heroes['enemy'])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    """
    'Hit enemy' button.
    Renders 'fight.html' template.
    """
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template('fight.html', heroes=heroes, result=result)
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    """
    'Use skill' button.
    Renders 'fight.html' template.
    """
    if arena.game_is_running:
        result = arena.player_use_skill()
        return render_template('fight.html', heroes=heroes, result=result)
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    """
    'Skip turn' button.
    Renders 'fight.html' template.
    """

    if arena.game_is_running:
        result = arena.next_turn()
        return render_template('fight.html', heroes=heroes, result=result)
    else:
        result = arena.battle_result

    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    """
    'End game' button.
    Renders 'index.html' template.
    """
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    """
    'Confirm' button.
    GET-method renders 'hero_choosing.html' template.
    POST-method sends form to initialize the player instance and redirects to '/choose-enemy' URL.
    """

    if request.method == 'GET':
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes

        result = {
            'header': 'Choose a hero',
            'classes': classes,
            'weapons': weapons,
            'armors': armors
        }
        return render_template('hero_choosing.html', result=result)

    elif request.method == 'POST':
        name = request.form['name']
        unit_class = request.form['unit_class']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        player = PlayerUnit(name=name, unit_class=unit_classes[unit_class])
        equipment = Equipment()
        player.equip_weapon(equipment.get_weapon(weapon_name))
        player.equip_armor(equipment.get_armor(armor_name))
        heroes['player'] = player
        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    """
    'Confirm' button (for enemy).
    GET-method is the same as for the previous one.
    POST-method sends form to initialize the enemy instance and redirects to '/fight' URL.
    """
    if request.method == 'GET':
        equipment = Equipment()
        weapons = equipment.get_weapons_names()
        armors = equipment.get_armors_names()
        classes = unit_classes

        result = {
            'header': 'Choose an enemy',
            'classes': classes,
            'weapons': weapons,
            'armors': armors
        }
        return render_template('hero_choosing.html', result=result)

    elif request.method == 'POST':
        name = request.form['name']
        unit_class = request.form['unit_class']
        weapon_name = request.form['weapon']
        armor_name = request.form['armor']
        enemy = EnemyUnit(name=name, unit_class=unit_classes[unit_class])
        equipment = Equipment()
        enemy.equip_weapon(equipment.get_weapon(weapon_name))
        enemy.equip_armor(equipment.get_armor(armor_name))
        heroes['enemy'] = enemy
        return redirect(url_for('start_fight'))


if __name__ == "__main__":
    app.run()
