from pydantic import ValidationError
from riotwatcher import Deserializer

from models import MatchDto, TimelineDto


class PydanticDeserializer(Deserializer):
    def deserialize(self, endpoint_name: str, method_name: str, data: str) -> MatchDto | TimelineDto:
        try:
            if endpoint_name == 'MatchApiV5' and method_name == 'by_id':
                return MatchDto.model_validate_json(data)
            elif endpoint_name == 'MatchApiV5' and method_name == 'timeline_by_match':
                return TimelineDto.model_validate_json(data)
            else:
                raise ValidationError('Wrong endpoint or method')

        except ValidationError:
            raise
