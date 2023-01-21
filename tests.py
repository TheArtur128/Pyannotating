from typing import Any, Union, Optional, Callable, Iterable, Sized

from pytest import mark

from pyannotating import FormalAnnotation, InputAnnotationAnnotation, AnnotationTemplate, input_annotation, Special


@mark.parametrize(
    "input_resource, result",
    [(42, 42), (Any, Any), (int | float, int | float)]
)
def test_formal_annotation(input_resource: Any, result: Any):
    assert FormalAnnotation()[input_resource] == result


@mark.parametrize(
    'doc',
    ["Documentation", "\n\t.!#@$2*-_\n", b"\tHello\n\tWorld\n\t!", str()]
)
def test_formal_annotation_documenting(doc: str):
    assert FormalAnnotation(doc).__doc__ == doc


@mark.parametrize('number_of_creation', [8])
def test_input_annotation_annotation_loneliness(number_of_creation: int):
    annotations = tuple(InputAnnotationAnnotation() for _ in range(number_of_creation))

    for first_annotation_index in range(number_of_creation):
        for second_annotation in annotations[first_annotation_index + 1:]:
            assert annotations[first_annotation_index] is second_annotation


@mark.parametrize(
    "type_to_group",
    [int, float, int | float, Union[set, frozenset], Optional[tuple], InputAnnotationAnnotation]
)
def test_input_annotation_annotation_grouping(type_to_group: type):
    annotation = InputAnnotationAnnotation()

    assert annotation | type_to_group == Union[annotation, type_to_group]
    assert type_to_group | annotation == Union[type_to_group | annotation]


@mark.parametrize(
    "annotation_template, input_resource, result",
    [
        (AnnotationTemplate(Optional, [input_annotation]), int, Optional[int]),
        (
            AnnotationTemplate(Callable, [[input_annotation | int, input_annotation], Any]),
            float,
            Callable[[float | int, float], Any]
        ),
        (
            AnnotationTemplate(
                Callable,
                [[input_annotation], AnnotationTemplate(Optional, [input_annotation])]
            ),
            str,
            Callable[[str], Optional[str]]
        ),
    ]
)
def test_annotation_template(annotation_template: AnnotationTemplate, input_resource: Any, result: Any):
    assert annotation_template[input_resource] == result
