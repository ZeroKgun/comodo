from utils.api import serializers
from profileResult.models import Codeprofile

class ProfileResultModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Codeprofile
        fields = ['line', 'per_time','line_m','increment']
