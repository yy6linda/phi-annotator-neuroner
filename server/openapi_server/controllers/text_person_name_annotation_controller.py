import connexion
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.text_person_name_annotation import TextPersonNameAnnotation  # noqa: E501
from openapi_server.models.text_person_name_annotation_request import TextPersonNameAnnotationRequest  # noqa: E501
from openapi_server.models.text_person_name_annotation_response import TextPersonNameAnnotationResponse  # noqa: E501
from openapi_server.neuroner import neuroner

def create_text_person_name_annotations():  # noqa: E501
    """Annotate person names in a clinical note

    Return the person name annotations found in a clinical note # noqa: E501

    :rtype: TextPersonNameAnnotationResponse
    """
    res = None
    status = None
    if connexion.request.is_json:
        try:
            annotation_request = TextPersonNameAnnotationRequest.from_dict(
                 connexion.request.get_json())
            note = annotation_request._note
            matches = neuroner.annotate(note._text)
            annotations = []
            add_person_name_annotations(annotations, matches)
            res = TextPersonNameAnnotationResponse(annotations)
            status = 200
        except Exception as error:
            status = 500
            res = Error("Internal error", status, str(error))
    else:
        status = 400
        res = Error("Bad request", status, "Missing body")
    return res, status


def add_person_name_annotations(annotations, matches):
    """
    Converts matches to TextLPersonNameAnnotation objects and adds them
    to the annotations array specified.
    """
    for match in matches:
        if match['type'] in ["PATIENT", "DOCTOR"]:
            annotations.append(
                TextPersonNameAnnotation(
                    start=match['start'],
                    length=len(match['text']),
                    text=match['text'],
                    confidence=95.5
                ))