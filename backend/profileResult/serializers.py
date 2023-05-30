from utils.api import serializers
from profileResult.models import Codeprofile

class ProfileResultModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Codeprofile
        fields = "__all__"
