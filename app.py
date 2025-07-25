from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'saurabh'  # Keep your secret key

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Mysql0@@',
    'database': 'alumni_network'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

@app.route('/')
def index():
    if 'email' in session:
        email = session['email']
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT first_name, last_name FROM alumni WHERE email = %s", (email,))
            user = cursor.fetchone()
            conn.close()
            if user:
                return render_template('index.html', user=user)
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = 'remember' in request.form
        
        if not email or not password:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('login'))
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute("SELECT * FROM alumni WHERE email = %s AND password = %s", (email, password))
                user = cursor.fetchone()
                
                if user:
                    session['email'] = user['email']
                    
                    if remember:
                        session.permanent = True
                        app.permanent_session_lifetime = timedelta(days=30)
                    
                    flash('Login successful!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Invalid email or password', 'error')
            except mysql.connector.Error as err:
                flash('Database error occurred', 'error')
                print(f"Database error: {err}")
            finally:
                conn.close()
        
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        user_details = {
            'first_name': request.form.get('first-name'),
            'last_name': request.form.get('last-name'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),
            'confirm_password': request.form.get('confirm-password'),
            'graduation_year': request.form.get('graduation-year'),
            'degree': request.form.get('degree'),
            'phone': request.form.get('phone', ''),  # Optional field
            'current_job': request.form.get('current-job', ''),  # Optional field
            'current_company': request.form.get('current-company', ''),  # Optional field
            'bio': request.form.get('bio', ''),  # Optional field
            'user_type': request.form.get('user-type', 'alumni'),  # Radio button
            'terms': request.form.get('terms')  # Checkbox
        }
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email', 'password', 
                          'confirm_password', 'graduation_year', 'degree', 'terms']
        if not all(user_details[field] for field in required_fields):
            flash('Please fill in all required fields', 'error')
            return render_template('register.html')
        
        # Validate passwords match
        if user_details['password'] != user_details['confirm_password']:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        # Check if email already exists
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM alumni WHERE email = %s", (user_details['email'],))
                existing_user = cursor.fetchone()
                
                if existing_user:
                    flash('Email already registered!', 'error')
                    return render_template('register.html')
                
                # Insert new alumni
                insert_query = """
                INSERT INTO alumni 
                (first_name, last_name, email, password, graduation_year, degree, 
                 phone, current_job, current_company, bio)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (
                    user_details['first_name'],
                    user_details['last_name'],
                    user_details['email'],
                    user_details['password'],  # Note: Storing plaintext - not recommended
                    user_details['graduation_year'],
                    user_details['degree'],
                    user_details['phone'] or None,
                    user_details['current_job'] or None,
                    user_details['current_company'] or None,
                    user_details['bio'] or None
                ))
                conn.commit()
                
                # Set session and redirect
                session['email'] = user_details['email']
                flash('Registration successful!', 'success')
                return redirect(url_for('index'))
                
            except mysql.connector.IntegrityError as e:
                conn.rollback()
                if "Duplicate entry" in str(e):
                    if "email" in str(e):
                        flash('Email already exists', 'error')
                    else:
                        flash('User ID already exists', 'error')
                else:
                    flash('Error creating account', 'error')
                return render_template('register.html')
            except mysql.connector.Error as err:
                conn.rollback()
                flash('Database error occurred', 'error')
                print(f"Database error: {err}")
                return render_template('register.html')
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
        else:
            flash('Database connection failed', 'error')
            return render_template('register.html')
    
    # For GET request, render the form with graduation year options
    graduation_years = [str(year) for year in range(2024, 2000, -1)]
    return render_template('register.html', graduation_years=graduation_years)

# @app.route('/directory')
# def directory():
#     conn = get_db_connection()
#     cur = conn.cursor(dictionray = True)
#     cur.execute("SELECT first_name,last_name,email, graduation_year, degree, phone, current_job, current_company FROM alumni")
#     rows = cur.fetchall()

#     search_query = request.args.get('search', '').strip()
#     alumni = []
    
#     if conn:
#         try:
#             if search_query:
#                 query = """
#                 SELECT * FROM alumni 
#                 WHERE name LIKE %s 
#                 ORDER BY name
#                 """
#                 search_param = f"%{search_query}%"
#                 cur.execute(query, (search_param))
                
#             alumni = cur.fetchall()
            
        
            
#         except mysql.connector.Error as err:
#             print(f"Error fetching alumni: {err}")
#             flash('Error fetching alumni data', 'error')
#         finally:
#              conn.close()

#     alumni_list = []
#     for row in rows:
#         alumni = {
#             'first_name': row[0],
#             'last_name': row[1],
#             'email':row[2],
#             'graduation_year': row[3],
#             'degree': row[4],
#             'phone': row[5],
#             'current_job': row[6],
#             'current_company':row[7]
#         }
#         alumni_list.append(alumni)

#     return render_template("directory.html", alumni_list=alumni_list)

@app.route('/directory')
def directory():
    search_query = request.args.get('search', '').strip()
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    
    alumni_list = []
    
    try:
        if search_query:
            # Search by name (first or last) or company
            query = """
            SELECT first_name, last_name, email, graduation_year, degree, phone, 
                   current_job, current_company 
            FROM alumni 
            WHERE CONCAT(first_name, ' ', last_name) LIKE %s 
               OR current_company LIKE %s
            ORDER BY first_name
            """
            search_param = f"%{search_query}%"
            cur.execute(query, (search_param, search_param))
        else:
            # Get all alumni if no search query
            cur.execute("""
                SELECT first_name, last_name, email, graduation_year, degree, 
                       phone, current_job, current_company 
                FROM alumni
                ORDER BY first_name
            """)
        
        alumni_list = cur.fetchall()
        
    except Exception as err:
        print(f"Error fetching alumni: {err}")
        flash('Error fetching alumni data', 'error')
    finally:
        if conn:
            conn.close()
    
    return render_template("directory.html", 
                         alumni_list=alumni_list,
                         search_query=search_query)

# Add this in app.py
ADMIN_EMAILS = ['admin1@example.com', 'admin2@example.com']

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('login'))

    if session['email'] not in ADMIN_EMAILS:
        flash('You are not authorized to access the admin section.', 'error')
        return render_template('admin_denied.html', user_email=session['email'])

    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))



@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if 'email' not in session:
        flash('Please log in as admin to create events.', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        event_date = request.form['event_date']
        location = request.form['location']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT alumni_id FROM alumni WHERE email = %s", (session['email'],))
                organizer = cursor.fetchone()
                if organizer:
                    organizer_id = organizer[0]
                    insert_query = """
                        INSERT INTO events (title, description, event_date, location, organizer_id)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (title, description, event_date, location, organizer_id))
                    conn.commit()
                    flash('Event created successfully!', 'success')
                    return redirect(url_for('admin'))
                else:
                    flash('Organizer not found.', 'error')
            except Exception as e:
                print("Error:", e)
                flash('Failed to create event.', 'error')
            finally:
                conn.close()
    return render_template('create_event.html')


@app.route('/profile')
def profile():
    if 'email' not in session:
        flash('Please log in to view your profile.', 'error')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM alumni WHERE email = %s", (session['email'],))
            user = cursor.fetchone()
            if user:
                return render_template('profile.html', user=user)
            else:
                flash('User not found', 'error')
                return redirect(url_for('index'))
        except mysql.connector.Error as err:
            flash('Database error', 'error')
            print(f"Database error: {err}")
        finally:
            cursor.close()
            conn.close()

    flash('Database connection failed', 'error')
    return redirect(url_for('index'))

@app.route('/events')
def events():
    filter = request.args.get('filter', 'upcoming')
    conn = get_db_connection()
    events = []

    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            now = datetime.now()
            if filter == 'upcoming':
                cursor.execute("SELECT * FROM events WHERE event_date >= %s ORDER BY event_date ASC", (now,))
            elif filter == 'past':
                cursor.execute("SELECT * FROM events WHERE event_date < %s ORDER BY event_date DESC", (now,))
            elif filter == 'my' and 'email' in session:
                cursor.execute("""
                    SELECT e.* FROM event_register e
                    JOIN event_attendees a ON e.event_id = a.event_id
                    JOIN alumni al ON a.alumni_id = al.alumni_id
                    WHERE al.email = %s
                """, (session['email'],))
            events = cursor.fetchall()
        except Exception as e:
            print("Error fetching events:", e)
        finally:
            cursor.close()
            conn.close()

    return render_template('events.html', events=events, filter=filter)



if __name__ == '__main__':
    app.run(debug=True)