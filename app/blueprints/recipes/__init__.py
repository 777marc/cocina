from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from ...extensions import db
from ...models import Recipe, User

recipes_bp = Blueprint('recipes', __name__, url_prefix='/recipes', template_folder='templates')


def _can_edit(recipe) -> bool:
    return current_user.is_authenticated and (current_user.is_admin or recipe.author_id == int(current_user.get_id()))


@recipes_bp.route('/')
@login_required
def list_recipes():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('recipes/index.html', recipes=recipes)


@recipes_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_recipe():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        ingredients = request.form.get('ingredients', '').strip()
        instructions = request.form.get('instructions', '').strip()
        if not title:
            flash('Title is required', 'error')
            return redirect(url_for('recipes.new_recipe'))
        recipe = Recipe(
            title=title,
            description=description or None,
            ingredients=ingredients,
            instructions=instructions,
            author_id=int(current_user.get_id())
        )
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe created', 'success')
        return redirect(url_for('recipes.list_recipes'))
    return render_template('recipes/new.html')


@recipes_bp.route('/<int:recipe_id>')
@login_required
def show_recipe(recipe_id: int):
    recipe = db.session.get(Recipe, recipe_id)
    if not recipe:
        abort(404)
    return render_template('recipes/show.html', recipe=recipe, can_edit=_can_edit(recipe))


@recipes_bp.route('/<int:recipe_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id: int):
    recipe = db.session.get(Recipe, recipe_id)
    if not recipe:
        abort(404)
    if not _can_edit(recipe):
        abort(403)
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        ingredients = request.form.get('ingredients', '').strip()
        instructions = request.form.get('instructions', '').strip()
        recipe.title = title or recipe.title
        recipe.description = description or None
        recipe.ingredients = ingredients or recipe.ingredients
        recipe.instructions = instructions or recipe.instructions
        db.session.commit()
        flash('Recipe updated', 'success')
        return redirect(url_for('recipes.show_recipe', recipe_id=recipe_id))
    return render_template('recipes/edit.html', recipe=recipe)


@recipes_bp.route('/<int:recipe_id>/delete', methods=['POST'])
@login_required
def delete_recipe(recipe_id: int):
    recipe = db.session.get(Recipe, recipe_id)
    if not recipe:
        abort(404)
    if not _can_edit(recipe):
        abort(403)
    db.session.delete(recipe)
    db.session.commit()
    flash('Recipe deleted', 'info')
    return redirect(url_for('recipes.list_recipes'))
