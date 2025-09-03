from django.urls import path

from . import views

urlpatterns = [
  path('', views.index, name='home'),
  path("index.html", views.index, name="index"),
               path("AdminLogin.html", views.AdminLogin, name="AdminLogin"),	      
               path("AdminLoginAction", views.AdminLoginAction, name="AdminLoginAction"),
               path("AddEmployeeAction", views.AddEmployeeAction, name="AddEmployeeAction"),
               path("AddEmployee.html", views.AddEmployee, name="AddEmployee"),
               path("ViewEmployees", views.ViewEmployees, name="ViewEmployees"),
	       path("ViewCouriers", views.ViewCouriers, name="ViewCouriers"),
	       path("EmployeeLogin.html", views.EmployeeLogin, name="EmployeeLogin"),	      
               path("EmployeeLoginAction", views.EmployeeLoginAction, name="EmployeeLoginAction"),
	       path("CollectCourier.html", views.CollectCourier, name="CollectCourier"),	      
               path("CollectCourierAction", views.CollectCourierAction, name="CollectCourierAction"),
	       path("UpdateCourier.html", views.UpdateCourier, name="UpdateCourier"),	      
               path("UpdateCourierAction", views.UpdateCourierAction, name="UpdateCourierAction"),
	       path("ViewCurrentStatus.html", views.ViewCurrentStatus, name="ViewCurrentStatus"),	      
               path("ViewCurrentStatusAction", views.ViewCurrentStatusAction, name="ViewCurrentStatusAction"),
	       path("EmployeeMap", views.EmployeeMap, name="EmployeeMap"),
	       path("CourierTrack.html", views.CourierTrack, name="CourierTrack"),	      
               path("CourierTrackAction", views.CourierTrackAction, name="CourierTrackAction"),
	       path("UserMap", views.UserMap, name="UserMap"),
	       path("Feedback.html", views.Feedback, name="Feedback"),	      
               path("FeedbackAction", views.FeedbackAction, name="FeedbackAction"),
	        path("ViewFeedback", views.ViewFeedback, name="ViewFeedback"),
]
