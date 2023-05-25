from utils.api import serializers

class ProfileResultSerializer(serializers.Serializer):
    line = serializers.CharField()
    per_time = serializers.CharField()
