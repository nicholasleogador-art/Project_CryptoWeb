from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from flask_login import login_required, current_user

crude = Blueprint('crude', __name__)

@crude.route('update', methods=['GET', 'POST'])
@login_required
def update(user_id):


@crude.route('delete', methods=['POST'])
@login_required
def delete():
