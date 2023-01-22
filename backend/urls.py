from django.urls import path

from .views import (
    UserSignupView,
    UserLoginView,
    JobView,
    UserJobListView,
    UserJobApplicationView
)

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="signup"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("job/post/", JobView.as_view(), name="create"),
    path("job/<int:pk>/update/", JobView.as_view(), name="update"),
    path("job/view/", UserJobListView.as_view(), name="list"),
    path("job/apply/", UserJobApplicationView.as_view(), name="create")
]
