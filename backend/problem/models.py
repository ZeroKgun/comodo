from django.db import models
from django.db.models import JSONField

from account.models import User
from contest.models import Contest
from utils.models import RichTextField
from utils.constants import Choices

from assignment.models import Assignment


class ProblemTag(models.Model):
    name = models.TextField()

    class Meta:
        db_table = "problem_tag"


class ProblemRuleType(Choices):
    ACM = "ACM"
    OI = "OI"
    ASSIGNMENT = "ASSIGNMENT"


class ProblemDifficulty(object):
    Level1 = "Level1"
    Level2 = "Level2"
    Level3 = "Level3"
    Level4 = "Level4"
    Level5 = "Level5"
    Level6 = "Level6"
    Level7 = "Level7"


class ProblemIOMode(Choices):
    standard = "Standard IO"
    file = "File IO"


def _default_io_mode():
    return {"io_mode": ProblemIOMode.standard, "input": "input.txt", "output": "output.txt"}


class Problem(models.Model):
    # display ID
    _id = models.TextField(db_index=True)
    # assignment ID
    assignment = models.ForeignKey(Assignment, null=True, on_delete=models.CASCADE, related_name="problems")
    contest = models.ForeignKey(Contest, null=True, on_delete=models.CASCADE)
    # for contest problem
    is_public = models.BooleanField(default=False)
    title = models.TextField()
    # HTML
    description = RichTextField()
    input_description = RichTextField()
    output_description = RichTextField()
    # [{input: "test", output: "123"}, {input: "test123", output: "456"}]
    samples = JSONField()
    test_case_id = models.TextField()
    # [{"input_name": "1.in", "output_name": "1.out", "score": 0}]
    test_case_score = JSONField()
    hint = RichTextField(null=True)
    languages = JSONField()
    template = JSONField()
    create_time = models.DateTimeField(auto_now_add=True)
    # we can not use auto_now here
    last_update_time = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    # ms
    time_limit = models.IntegerField()
    # MB
    memory_limit = models.IntegerField()
    # io mode
    io_mode = JSONField(default=_default_io_mode)
    # special judge related
    spj = models.BooleanField(default=False)
    spj_language = models.TextField(null=True)
    spj_code = models.TextField(null=True)
    spj_version = models.TextField(null=True)
    spj_compile_ok = models.BooleanField(default=False)
    rule_type = models.TextField()
    visible = models.BooleanField(default=True)
    difficulty = models.TextField()
    tags = models.ManyToManyField(ProblemTag)
    source = models.TextField(null=True)
    # for OI mode
    total_score = models.IntegerField(default=0)
    submission_number = models.BigIntegerField(default=0)
    accepted_number = models.BigIntegerField(default=0)
    # {JudgeStatus.ACCEPTED: 3, JudgeStaus.WRONG_ANSWER: 11}, the number means count
    statistic_info = JSONField(default=dict)
    share_submission = models.BooleanField(default=False)
    # Submission type
    type = models.TextField(default="Problem", null=True)
    bank = models.BooleanField(default=False)

    class Meta:
        db_table = "problem"
        unique_together = (("_id", "contest"),)
        ordering = ("create_time",)

    def add_submission_number(self):
        self.submission_number = models.F("submission_number") + 1
        self.save(update_fields=["submission_number"])

    def add_ac_number(self):
        self.accepted_number = models.F("accepted_number") + 1
        self.save(update_fields=["accepted_number"])


class ProblemSetGroup(models.Model):
    title = models.TextField()
    button_type = models.TextField()
    is_disabled = models.BooleanField()


class ProblemSet(models.Model):
    title = models.TextField()
    problem_set_group = models.ForeignKey(ProblemSetGroup, null=True, on_delete=models.CASCADE, related_name="problem_set")
    color = models.TextField()
    is_disabled = models.BooleanField()
    is_public = models.BooleanField()
    problems = models.ManyToManyField(Problem, blank=True, related_name="problem_set")

