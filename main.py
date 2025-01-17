from flask import Flask, render_template, request, Response,send_file,send_from_directory,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from itertools import groupby

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///resources.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

app.app_context().push()

class Resources(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), nullable=False)
    student_id = db.Column(db.String(20), nullable=False)
    Course_Code = db.Column(db.String(10), nullable=False)
    f_type = db.Column(db.String(10), nullable=False)
    Description = db.Column(db.Text, nullable=False)
    up_file=db.Column(db.String(100), nullable=False)

    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    # def __repr__(self) -> str:
    #     return f"{self.Course_Code} - {self.Description}"
  
@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/cse1')
# def cse1():
#     all_resource=Resources.query.filter(Resources.Course_Code.like('cse1%')).all()
#     print(all_resource)
#     return render_template('cse1.html',all_resource=all_resource)

@app.route('/Add_resources', methods=['GET', 'POST'])
def Add_resources():
    filename2 = None
    if request.method == "POST":
        Course_Code = request.form['Course_Code']
        email = request.form['email']
        student_id = request.form['student_id']
        f_type = request.form['f_type']
        Description = request.form['Description']
    #     up_file = request.files['up_file']
    #     if up_file:
            
        
    #         filename2 = up_file.filename 
           
    #         resource = Resources(
    #             email=email, up_file=filename2, student_id=student_id, Course_Code=Course_Code,
    #             f_type=f_type, Description=Description
    #         )

    #         db.session.add(resource)
    #         db.session.commit()
    #         up_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(up_file.filename)))
    # all_resource = Resources.query.all()
    # return render_template('Add_resources.html', all_resource=all_resource, filename2=filename2)
    # return render_template('Add_resources.html')


        up_file = request.files['up_file']

        if up_file:
            
            # file_data = up_file.read()
            filename2 = up_file.filename  # Get the filename
           
            resource = Resources(
                email=email, up_file=filename2, student_id=student_id, Course_Code=Course_Code,
                f_type=f_type, Description=Description
            )

            db.session.add(resource)
            db.session.commit()
            up_file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(up_file.filename)))
    all_resource = Resources.query.all()
    return render_template('Add_resources.html', all_resource=all_resource, filename2=filename2)




    return render_template('Add_resources.html')
# @app.route('/get_file/<int:sno>')
# def get_file(sno):
#     resource = Resources.query.get_or_404(sno)
#     return Response(resource.up_file, content_type="image/png")  
@app.route('/view')
def View():
    all_resource=Resources.query.all()
    return render_template('view.html',all_resource=all_resource)


@app.route('/get_file/<int:sno>')
def get_file(sno):
    resource = Resources.query.get_or_404(sno)
    return Response(resource.up_file, content_type="application/octet-stream")  # Update the content type based on the file type

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    # Access the file name
    filename = file.filename

    # You can now use the 'filename' variable as needed
    return f'Uploaded file name: {filename}'
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/serve_file/<filename>')
def serve_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)






@app.route('/cse1')
def cse1():
    all_resource=Resources.query.filter(Resources.Course_Code.like('cse1%')).all()
    grouped_resources = {}
    
    # Group resources by course code
    all_resource.sort(key=lambda x: x.Course_Code)
    for course_code, resources in groupby(all_resource, key=lambda x: x.Course_Code):
        grouped_resources[course_code] = list(resources)
    
    return render_template('cse1.html', grouped_resources=grouped_resources)

comments = []
ratings = []
Serials=[]
course_codes=[]


@app.route('/comment')
def comment():
    return render_template('comment.html', course_data=zip(course_codes, Serials, comments, ratings))

@app.route('/submit', methods=['POST'])
def submit():
    comment = request.form.get('comment')
    rating = request.form.get('rating')
    course_code=request.form.get('course_code')
    Serial=request.form.get('num')
    print(course_code)

    if comment and rating and course_code and Serial:
        comments.append(comment)
        ratings.append(int(rating))
        course_codes.append(course_code)
        Serials.append(Serial)

    print(Serials,course_codes)

    return redirect(url_for('comment'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0",debug=True, port=8000)