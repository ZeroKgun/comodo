from utils.api import APIView
from utils.decorators import login_required
from options.options import SysOptions
from profileResult.models import Codeprofile
from .serializers import ProfileResultModelSerializer

class CodeProfileAPI(APIView):
    @login_required
    def get(self, request):
        submissionID = request.GET.get("id")
        profile_result = Codeprofile.objects.get(submission_id=submissionID)
        profile_result_data = ProfileResultModelSerializer(profile_result).data
        return self.success(profile_result_data)
