import os
import shutil
import subprocess
import ipaddress


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from assignment.models import Assignment
from contest.models import ContestStatus, ContestRuleType
from judge.tasks import judge_task
from options.options import SysOptions
# from judge.dispatcher import JudgeDispatcher
from problem.models import Problem, ProblemRuleType
from account.models import User, AdminType
from utils.api import APIView, validate_serializer
from utils.constants import AssignmentStatus
from utils.cache import cache
from utils.captcha import Captcha
from utils.decorators import login_required, check_contest_permission, admin_role_required, check_assignment_permission
from utils.shortcuts import file_func
from utils.throttling import TokenBucket
from utils.shortcuts import ffff, fffm
from .models import Submission
from profileResult.models import Codeprofile
from .serializers import (CreateSubmissionSerializer, SubmissionModelSerializer,
                          ShareSubmissionSerializer, SubmissionSafeModelSerializer, SubmissionListSerializer,
                          SubmissionListProfessorSerializer, EditSubmissionScoreSerializer)


class SubmissionAPI(APIView):
    def throttling(self, request):
        user_bucket = TokenBucket(key=str(request.user.id),
                                  redis_conn=cache, **SysOptions.throttling["user"])
        can_consume, wait = user_bucket.consume()
        if not can_consume:
            return "Please wait %d seconds" % (int(wait))

    @check_contest_permission(check_type="problems")
    def check_contest_permission(self, request):
        contest = self.contest
        if contest.status == ContestStatus.CONTEST_ENDED:
            return self.error("The contest have ended")
        if not request.user.is_contest_admin(contest):
            user_ip = ipaddress.ip_address(request.session.get("ip"))
            if contest.allowed_ip_ranges:
                if not any(user_ip in ipaddress.ip_network(cidr, strict=False) for cidr in contest.allowed_ip_ranges):
                    return self.error("Your IP is not allowed in this contest")

    @check_assignment_permission()
    def check_assignment_permission(self, request):
        assignment = self.assignment
        if assignment.status == AssignmentStatus.ASSIGNMENT_ENDED:
            return self.error("The Assignment deadline has expired")

    @swagger_auto_schema(request_body=CreateSubmissionSerializer)
    @validate_serializer(CreateSubmissionSerializer)
    @login_required
    def post(self, request):
        data = request.data
        hide_id = False
        if data.get("contest_id"):
            error = self.check_contest_permission(request)
            if error:
                return error
            contest = self.contest
            if not contest.problem_details_permission(request.user):
                hide_id = True

        if data.get("assignment_id"):
            error = self.check_assignment_permission(request)
            if error:
                return error
            # assignment = self.assignment
            # if not assignment.problem_details_permission(request.user):
            #     hide_id = True

        if data.get("captcha"):
            if not Captcha(request).check(data["captcha"]):
                return self.error("Invalid captcha")
        error = self.throttling(request)
        if error:
            return self.error(error)

        try:
            problem = Problem.objects.get(id=data["problem_id"], contest_id=data.get("contest_id"), assignment_id=data.get("assignment_id"), visible=True)
        except Problem.DoesNotExist:
            return self.error("Problem not exist")
        if data["language"] not in problem.languages:
            return self.error(f"{data['language']} is now allowed in the problem")
        submission = Submission.objects.create(user_id=request.user.id,
                                               username=request.user.username,
                                               language=data["language"],
                                               code=data["code"],
                                               problem_id=problem.id,
                                               ip=request.session["ip"],
                                               contest_id=data.get("contest_id"),
                                               assignment_id=data.get("assignment_id"))
        #code analysis test
        #__problem_id = submission.problem_id
        __sample = Problem.objects.get(id=submission.problem_id).samples[0]
        file_name = submission.id+'.py'
        t1 = open(file_name, 'w')
        t1.write('@profile'+'\n' + 'def main():\n')
        file_func(t1, submission.code)
        t1.write('main()')
        t1.close()
        command = "kernprof -l " + file_name
        _commandM = "python -m memory_profiler " + file_name + " > " + submission.id + "m.txt"
        subprocess.run(args=command.split(), input=__sample['input'], text=True)
        subprocess.run(_commandM, shell =True, input=__sample['input'], text=True)
        os.system("python -m line_profiler "+file_name+".lprof > "+submission.id+".txt")
        os.remove(file_name+".lprof")
        os.remove(file_name)
        shutil.move(submission.id+".txt", "./profileResult/results")
        shutil.move(submission.id+"m.txt", "./profileResult/results")
        line, per_time = ffff(submission.id)
        line_m, increment = fffm(submission.id)
        Codeprofile.objects.create(submission_id=submission.id, line=line, per_time=per_time)

        # use this for debug
        # JudgeDispatcher(submission.id, problem.id).judge()

        judge_task(submission.id, problem.id)
        if hide_id:
            return self.success()
        else:
            return self.success({"submission_id": submission.id})

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="id", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER
            )
        ]
    )
    @login_required
    def get(self, request):
        submission_id = request.GET.get("id")
        if not submission_id:
            return self.error("Parameter id doesn't exist")
        try:
            submission = Submission.objects.select_related("problem").get(id=submission_id)
        except Submission.DoesNotExist:
            return self.error("Submission doesn't exist")
        if not submission.check_user_permission(request.user):
            return self.error("No permission for this submission")

        if submission.problem.rule_type == ProblemRuleType.OI or request.user.is_admin_role():
            submission_data = SubmissionModelSerializer(submission).data
        else:
            submission_data = SubmissionSafeModelSerializer(submission).data
        # if there is permission to cancel sharing
        submission_data["can_unshare"] = submission.check_user_permission(request.user, check_share=False)
        return self.success(submission_data)

    @swagger_auto_schema(request_body=ShareSubmissionSerializer)
    @validate_serializer(ShareSubmissionSerializer)
    @login_required
    def put(self, request):
        """
        share submission
        """
        try:
            submission = Submission.objects.select_related("problem").get(id=request.data["id"])
        except Submission.DoesNotExist:
            return self.error("Submission doesn't exist")
        if not submission.check_user_permission(request.user, check_share=False):
            return self.error("No permission to share the submission")
        if submission.contest and submission.contest.status == ContestStatus.CONTEST_UNDERWAY:
            return self.error("Can not share submission now")
        submission.shared = request.data["shared"]
        submission.save(update_fields=["shared"])
        return self.success()


class SubmissionListAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="limit",
                in_=openapi.IN_QUERY,
                required=True,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="offset",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="problem_id",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="myself",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_STRING,
                description="Set to '1' to get my submissions"
            ),
            openapi.Parameter(
                name="result",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="username",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name="page",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request):
        if not request.GET.get("limit"):
            return self.error("Limit is needed")
        if request.GET.get("contest_id"):
            return self.error("Parameter error")

        submissions = Submission.objects.filter(contest_id__isnull=True, assignment_id__isnull=True).select_related("problem__created_by")
        problem_id = request.GET.get("problem_id")
        myself = request.GET.get("myself")
        result = request.GET.get("result")
        username = request.GET.get("username")
        if problem_id:
            try:
                problem = Problem.objects.get(_id=problem_id, contest_id__isnull=True, assignment_id__isnull=True, visible=True)
            except Problem.DoesNotExist:
                return self.error("Problem doesn't exist")
            submissions = submissions.filter(problem=problem)
        if (myself and myself == "1") or not SysOptions.submission_list_show_all:
            submissions = submissions.filter(user_id=request.user.id)
        elif username:
            submissions = submissions.filter(username__icontains=username)
        elif (myself and myself == "0") and not request.user.is_admin_role():
            user_ids = submissions.values_list("user_id", flat=True)
            users = User.objects.filter(id__in=user_ids, admin_type=AdminType.REGULAR_USER)
            user_ids = users.values_list("id")
            submissions = submissions.filter(user_id__in=user_ids)
        if result:
            submissions = submissions.filter(result=result)
        data = self.paginate_data(request, submissions)
        data["results"] = SubmissionListSerializer(data["results"], many=True, user=request.user).data
        return self.success(data)


class ContestSubmissionListAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="limit",
                in_=openapi.IN_QUERY,
                required=True,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="offset",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="contest_id",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="problem_id",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="myself",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_STRING,
                description="Set to '1' to get my submissions"
            ),
            openapi.Parameter(
                name="result", in_=openapi.IN_QUERY, required=False, type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="username", in_=openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name="page", in_=openapi.IN_QUERY, required=False, type=openapi.TYPE_INTEGER
            )
        ]
    )
    @check_contest_permission(check_type="submissions")
    def get(self, request):
        if not request.GET.get("limit"):
            return self.error("Limit is needed")

        contest = self.contest
        submissions = Submission.objects.filter(contest_id=contest.id).select_related("problem__created_by")
        problem_id = request.GET.get("problem_id")
        myself = request.GET.get("myself")
        result = request.GET.get("result")
        username = request.GET.get("username")
        if problem_id:
            try:
                problem = Problem.objects.get(_id=problem_id, contest_id=contest.id, visible=True)
            except Problem.DoesNotExist:
                return self.error("Problem doesn't exist")
            submissions = submissions.filter(problem=problem)

        if myself and myself == "1":
            submissions = submissions.filter(user_id=request.user.id)
        elif username:
            submissions = submissions.filter(username__icontains=username)
        elif (myself and myself == "0") and not request.user.is_admin_role():
            user_ids = submissions.values_list("user_id", flat=True)
            users = User.objects.filter(id__in=user_ids, admin_type=AdminType.REGULAR_USER)
            user_ids = users.values_list("id")
            submissions = submissions.filter(user_id__in=user_ids)
        if result:
            submissions = submissions.filter(result=result)

        # filter the test submissions submitted before contest start
        if contest.status != ContestStatus.CONTEST_NOT_START:
            submissions = submissions.filter(create_time__gte=contest.start_time)

        # You can only see your submissions when you close the list
        if contest.rule_type == ContestRuleType.ACM:
            if not contest.real_time_rank and not request.user.is_contest_admin(contest):
                submissions = submissions.filter(user_id=request.user.id)

        data = self.paginate_data(request, submissions)
        data["results"] = SubmissionListSerializer(data["results"], many=True, user=request.user).data
        return self.success(data)


class AssignmentSubmissionListAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="limit",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="offset",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="assignment_id",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="problem_id",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="result", in_=openapi.IN_QUERY, required=False, type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="username", in_=openapi.IN_QUERY, required=False, type=openapi.TYPE_STRING
            ),
        ],
        operation_description="Submission list for assignment problem page",
        responses={200: SubmissionListSerializer}
    )
    @check_assignment_permission()
    def get(self, request):
        assignment = self.assignment
        submissions = Submission.objects.filter(assignment_id=assignment.id).select_related("problem__created_by")
        problem_id = request.GET.get("problem_id")
        result = request.GET.get("result")
        username = request.GET.get("username")
        if problem_id:
            try:
                problem = Problem.objects.get(_id=problem_id, assignment_id=assignment.id, visible=True)
            except Problem.DoesNotExist:
                return self.error("Problem doesn't exist")
            submissions = submissions.filter(problem=problem)

        if username:
            submissions = submissions.filter(username__icontains=username)
        if result:
            submissions = submissions.filter(result=result)

        # students can only see their own submissions
        if not request.user.is_assignment_admin(assignment):
            submissions = submissions.filter(user_id=request.user.id)

        # filter the test submissions submitted before contest start
        if assignment.status != AssignmentStatus.ASSIGNMENT_NOT_START:
            submissions = submissions.filter(create_time__gte=assignment.start_time)

        data = self.paginate_data(request, submissions)
        data["results"] = SubmissionListSerializer(data["results"], many=True, user=request.user).data
        return self.success(data)


class AssignmentSubmissionListProfessorAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="limit",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="offset",
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="assignment_id",
                in_=openapi.IN_QUERY,
                required=True,
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="problem_id",
                in_=openapi.IN_QUERY,
                required=True,
                type=openapi.TYPE_INTEGER
            ),
        ],
        operation_description="Submission list for professor page",
        responses={200: SubmissionListProfessorSerializer}
    )
    @admin_role_required
    def get(self, request):
        assignment_id = request.GET.get("assignment_id")
        problem_id = request.GET.get("problem_id")
        if not assignment_id:
            return self.error("Invalid parameter, assignment_id is required")
        if not problem_id:
            return self.error("Invalid parameter, problem_id is required")

        try:
            Assignment.objects.get(id=assignment_id)
            Problem.objects.get(id=problem_id)
        except Assignment.DoesNotExist:
            return self.error("Assignment does not exist")
        except Problem.DoesNotExist:
            return self.error("Problem does not exist")

        submissions = Submission.objects.filter(assignment_id=assignment_id).order_by("username", "-create_time").distinct("username")
        return self.success(self.paginate_data(request, submissions, SubmissionListProfessorSerializer))


class EditSubmissionScoreAPI(APIView):
    @swagger_auto_schema(
        request_body=EditSubmissionScoreSerializer,
        operation_description="Edit submission score",
        responses={200: SubmissionListSerializer},
    )
    @validate_serializer(EditSubmissionScoreSerializer)
    @admin_role_required
    def put(self, request):
        data = request.data
        submission_id = data["id"]
        score = data["score"]

        try:
            submission = Submission.objects.get(id=submission_id)
        except Submission.DoesNotExist:
            return self.error("Submission does not exist")

        submission.statistic_info["score"] = score
        submission.save()
        return self.success(SubmissionListSerializer(submission).data)


class SubmissionExistsAPI(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="problem_id", in_=openapi.IN_QUERY, required=True, type=openapi.TYPE_INTEGER
            )
        ]
    )
    def get(self, request):
        if not request.GET.get("problem_id"):
            return self.error("Parameter error, problem_id is required")
        return self.success(request.user.is_authenticated and
                            Submission.objects.filter(problem_id=request.GET["problem_id"],
                                                      user_id=request.user.id).exists())
