import os
import boto3
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from botocore.exceptions import ClientError
import json
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

# DynamoDB configuration
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table_name = os.environ.get('DYNAMODB_TABLE', 'ecommerce-users')

# Initialize DynamoDB table
def init_table():
    try:
        logger.info(f"Attempting to access DynamoDB table: {table_name}")
        table = dynamodb.Table(table_name)
        table.load()
        logger.info(f"Successfully loaded table: {table_name}")
        return table
    except ClientError as e:
        logger.error(f"DynamoDB error: {e}")
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            logger.info(f"Table {table_name} not found, creating it...")
            try:
                # Create table if it doesn't exist
                table = dynamodb.create_table(
                    TableName=table_name,
                    KeySchema=[
                        {
                            'AttributeName': 'email',
                            'KeyType': 'HASH'
                        }
                    ],
                    AttributeDefinitions=[
                        {
                            'AttributeName': 'email',
                            'AttributeType': 'S'
                        }
                    ],
                    BillingMode='PAY_PER_REQUEST'
                )
                table.wait_until_exists()
                logger.info(f"Successfully created table: {table_name}")
                return table
            except Exception as create_error:
                logger.error(f"Failed to create table: {create_error}")
                raise
        else:
            logger.error(f"Unexpected DynamoDB error: {e}")
            raise

# Forms
class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# Sample product data
products = [
    {
        'id': 1,
        'name': 'Wireless Headphones',
        'price': 99.99,
        'description': 'High-quality wireless headphones with noise cancellation',
        'image': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop'
    },
    {
        'id': 2,
        'name': 'Smart Watch',
        'price': 199.99,
        'description': 'Feature-rich smartwatch with health monitoring',
        'image': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop'
    },
    {
        'id': 3,
        'name': 'Laptop',
        'price': 899.99,
        'description': 'Powerful laptop for work and gaming',
        'image': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop'
    },
    {
        'id': 4,
        'name': 'Smartphone',
        'price': 699.99,
        'description': 'Latest smartphone with advanced camera system',
        'image': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop'
    }
]

@app.route('/')
def home():
    return render_template('home.html', products=products)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_email' in session:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            table = init_table()
            logger.info(f"Attempting to register user: {form.email.data}")
            
            # Check if user already exists
            try:
                response = table.get_item(Key={'email': form.email.data})
                if 'Item' in response:
                    flash('Email already registered!', 'error')
                    logger.info(f"Registration failed: Email already exists: {form.email.data}")
                    return render_template('register.html', form=form)
            except ClientError as e:
                logger.error(f"Error checking existing user: {e}")
                flash('Error checking user existence. Please try again.', 'error')
                return render_template('register.html', form=form)
            
            # Hash password
            hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), bcrypt.gensalt())
            
            # Store user in DynamoDB
            try:
                table.put_item(Item={
                    'email': form.email.data,
                    'name': form.name.data,
                    'password': hashed_password.decode('utf-8'),
                    'created_at': datetime.utcnow().isoformat()
                })
                logger.info(f"Successfully registered user: {form.email.data}")
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
            except ClientError as e:
                logger.error(f"Error storing user in DynamoDB: {e}")
                flash('Registration failed. Please try again.', 'error')
                return render_template('register.html', form=form)
                
        except Exception as e:
            logger.error(f"Unexpected error during registration: {e}")
            flash('Registration failed. Please try again.', 'error')
            return render_template('register.html', form=form)
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_email' in session:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            table = init_table()
            logger.info(f"Attempting to login user: {form.email.data}")
            
            try:
                response = table.get_item(Key={'email': form.email.data})
                if 'Item' in response:
                    user = response['Item']
                    if bcrypt.checkpw(form.password.data.encode('utf-8'), user['password'].encode('utf-8')):
                        session['user_email'] = user['email']
                        session['user_name'] = user['name']
                        logger.info(f"Successfully logged in user: {form.email.data}")
                        flash('Login successful!', 'success')
                        return redirect(url_for('home'))
                    else:
                        logger.info(f"Login failed: Invalid password for user: {form.email.data}")
                        flash('Invalid password!', 'error')
                else:
                    logger.info(f"Login failed: Email not found: {form.email.data}")
                    flash('Email not found!', 'error')
            except ClientError as e:
                logger.error(f"Error during login: {e}")
                flash('Login failed. Please try again.', 'error')
        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            flash('Login failed. Please try again.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/profile')
def profile():
    if 'user_email' not in session:
        return redirect(url_for('login'))
    
    try:
        table = init_table()
        response = table.get_item(Key={'email': session['user_email']})
        if 'Item' in response:
            user = response['Item']
            return render_template('profile.html', user=user)
    except Exception as e:
        logger.error(f"Error loading profile: {e}")
        flash('Error loading profile.', 'error')
    
    return redirect(url_for('home'))

@app.route('/api/users')
def api_users():
    if 'user_email' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        table = init_table()
        response = table.scan()
        users = []
        for item in response['Items']:
            users.append({
                'email': item['email'],
                'name': item['name'],
                'created_at': item['created_at']
            })
        return jsonify(users)
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 