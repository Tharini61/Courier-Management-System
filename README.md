<h2>Overview</h2>
<p>The Courier Management System is a Django-based web application that streamlines courier delivery services. 
  It allows admins to manage employees, monitor couriers, and review feedback, while employees can register couriers and update delivery statuses. 
  Customers can send couriers, track them in real time using a unique courier ID, and provide feedback.
  The system ensures efficient courier operations with a secure MySQL database and a simple, user-friendly interface.</p>

<h2>
  Features
</h2>
<p>
<h4>Admin</h4>
Add/manage employees,
Manage couriers (view/update),
Monitor delivery status,
View customer feedback

<h4>Employee</h4>
Login with assigned credentials,
Register couriers (sender/receiver details, weight, amount),
Update courier delivery status (current location, status, expected delivery)

<h4>User (Customer)</h4>
Send couriers by providing details,
Track couriers in real time using courier ID,
Provide feedback
</p>

<h2>Technologies</h2>
<p>
  Programming Language: Python (Version-3.7.0)<br>
Framework: Django 2.1.7 <br>
Database: MySQL with PyMySQL connector<br>
Frontend: Django Templates, HTML5, CSS3, Bootstrap <br>
Data Analysis & Visualization: NumPy, Pandas, Matplotlib, Seaborn <br>
Operating System: Cross-platform (Windows/Linux/Mac) <br>
Automation: Batch script (run.bat) for quick server start <br>
</p>

<h2>Requirements</h2>
<p>
  Python 3.7 <br>
Django 2.1.7 <br>
MySQL database <br>
Required libraries from requirements.txt 
</p>

<h2>Setup and Installation</h2>
<p></p>
Clone the repository <br>
Create & activate virtual environment <br>
Install dependencies using pip install -r requirements.txt <br>
Import database schema from database.txt into MySQL <br>
Run Django migrations (python manage.py migrate) <br>
Start the server (python manage.py runserver or use run.bat)
</p>

<h2>Conclusion</h2>
<p>
  This provides an efficient and reliable way to manage courier operations through role-based access for admins, employees, and customers.
It ensures smooth courier tracking, secure data management, and a user-friendly interface.</p>
