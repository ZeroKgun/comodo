from django.urls import include, path


urlpatterns = [
    path("api/", include("account.urls.oj")),
    path("api/admin/", include("account.urls.admin")),
    path("api/", include("announcement.urls.oj")),
    path("api/admin/", include("announcement.urls.admin")),
    path("api/", include("conf.urls.oj")),
    path("api/admin/", include("conf.urls.admin")),
    path("api/professor/", include("conf.urls.professor")),
    path("api/", include("problem.urls.oj")),
    path("api/", include("profileResult.urls")),
    path("api/admin/", include("problem.urls.admin")),
    path("api/lecture/", include("problem.urls.student")),
    path("api/lecture/professor/", include("problem.urls.professor")),
    path("api/", include("contest.urls.oj")),
    path("api/admin/", include("contest.urls.admin")),
    path("api/", include("submission.urls")),
    path("api/admin/", include("utils.urls")),
    path("api/", include("banner.urls.oj")),
    path("api/admin/", include("banner.urls.admin")),
    path("api/", include("group.urls.oj")),
    path("api/admin/", include("group.urls.admin")),
    path("api/lecture/", include("course.urls.student")),
    path("api/lecture/professor/", include("course.urls.professor")),
    path("api/lecture/", include("assignment.urls.student")),
    path("api/lecture/professor/", include("assignment.urls.professor")),
    path("api/lecture/", include("qna.urls.student")),
    path("api/lecture/professor/", include("qna.urls.professor")),
]

