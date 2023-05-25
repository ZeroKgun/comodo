from utils.api import APIView, validate_serializerfrom
from utils.decorators import login_required
from options.options import SysOptions
from profileResult.models import Codeprofile
from .serializers import ProfileResultSerializer

class CodeProfileAPI(APIView):
    @login_required
    def get(self, request):
        submission_id = request.GET.get("id")
        profile_result = Codeprofile.objects.get(id=submission_id)
        profile_result_data = ProfileResultSerializer(profile_result).data
        return self.success(profile_result_data)
