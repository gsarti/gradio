"""gr.HighlightedTextbox() component."""

from __future__ import annotations

import warnings
from typing import Callable, Literal

import numpy as np
from gradio_client.documentation import document, set_documentation_group
from gradio_client.serializing import JSONSerializable

from gradio.components.base import (
    FormComponent,
    IOComponent,
    _Keywords,
)
from gradio.deprecation import warn_style_method_deprecation
from gradio.events import (
    Changeable,
    EventListenerMethod,
    Focusable,
    Inputable,
    Selectable,
    Submittable,
)
from gradio.interpretation import TokenInterpretable

set_documentation_group("component")


@document()
class HighlightedTextbox(
    FormComponent,
    Changeable,
    Inputable,
    Selectable,
    Submittable,
    Focusable,
    IOComponent,
    JSONSerializable,
    TokenInterpretable,
):
    """
    Creates a textarea for user to enter string input or display string output where some
    elements are highlighted.
    Preprocessing: passes a list of tuples as a {List[Tuple[str, float | str | None]]]} into the function. If no labels are provided, the text will be displayed as a single span.
    Postprocessing: expects a {List[Tuple[str, float | str]]]} consisting of spans of text and their associated labels, or a {Dict} with two keys: 
        (1) "text" whose value is the complete text, and 
        (2) "highlights", which is a list of dictionaries, each of which have the keys: 
            "highlight_type" (consisting of the highlight label), 
            "start" (the character index where the label starts), and 
            "end" (the character index where the label ends). 
        Highlights should not overlap.

    Demos: TBD
    """

    def __init__(
        self,
        value: list[tuple[str, str | None]] | dict | Callable | None = None,
        *,
        color_map: dict[str, str] | None = None,
        show_legend: bool = False,
        show_legend_label: bool = False,
        legend_label: str = "",
        combine_adjacent: bool = False,
        adjacent_separator: str = "",
        label: str | None = None,
        info: str | None = None,
        every: float | None = None,
        show_label: bool | None = None,
        container: bool = True,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool = True,
        elem_id: str | None = None,
        autofocus: bool = False,
        autoscroll: bool = True,
        elem_classes: list[str] | str | None = None,
        show_copy_button: bool = False,
        **kwargs,
    ):
        """
        Parameters:
            value: Default value to show. If callable, the function will be called whenever the app loads to set the initial value of the component.
            color_map: A dictionary mapping labels to colors. The colors may be specified as hex codes or by their names. For example: {"person": "red", "location": "#FFEE22"}
            show_legend: whether to show span categories in a separate legend or inline.
            combine_adjacent: If True, will merge the labels of adjacent tokens belonging to the same category.
            adjacent_separator: Specifies the separator to be used between tokens if combine_adjacent is True.
            label: component name in interface.
            info: additional component description.
            every: If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. Queue must be enabled. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.
            show_label: if True, will display label.
            container: If True, will place the component in a container - providing some extra padding around the border.
            scale: relative width compared to adjacent Components in a Row. For example, if Component A has scale=2, and Component B has scale=1, A will be twice as wide as B. Should be an integer.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            interactive: if True, will be rendered as an editable textbox; if False, editing will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.
            visible: If False, component will be hidden.
            autofocus: If True, will focus on the textbox when the page loads. Use this carefully, as it can cause usability issues for sighted and non-sighted users.
            autoscroll: If True, will automatically scroll to the bottom of the textbox when the value changes, unless the user scrolls up. If False, will not scroll to the bottom of the textbox when the value changes.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            show_copy_button: If True, includes a copy button to copy the text in the textbox. Only applies if show_label is True.
        """
        self.color_map = color_map
        self.show_legend = show_legend
        self.combine_adjacent = combine_adjacent
        self.adjacent_separator = adjacent_separator
        self.show_copy_button = show_copy_button
        self.show_legend_label = show_legend_label
        self.legend_label = legend_label
        self.autofocus = autofocus
        self.select: EventListenerMethod
        self.autoscroll = autoscroll
        """
        Event listener for when the user selects text in the Textbox.
        Uses event data gradio.SelectData to carry `value` referring to selected substring, and `index` tuple referring to selected range endpoints.
        See EventData documentation on how to use this event data.
        """
        IOComponent.__init__(
            self,
            label=label,
            info=info,
            every=every,
            show_label=show_label,
            container=container,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value,
            **kwargs,
        )
        TokenInterpretable.__init__(self)

    @staticmethod
    def update(
        value: list[tuple[str, str | None]]
        | dict
        | Literal[_Keywords.NO_VALUE]
        | None = _Keywords.NO_VALUE,
        color_map: dict[str, str] | None = None,
        show_legend: bool | None = None,
        show_legend_label: bool | None = None,
        legend_label: str | None = None,
        label: str | None = None,
        info: str | None = None,
        show_label: bool | None = None,
        container: bool | None = None,
        scale: int | None = None,
        min_width: int | None = None,
        visible: bool | None = None,
        interactive: bool | None = None,
        show_copy_button: bool | None = None,
        autofocus: bool | None = None,
        autoscroll: bool | None = None,
    ):
        warnings.warn(
            "Using the update method is deprecated. Simply return a new object instead, e.g. `return gr.HighlightedTextbox(...)` instead of `return gr.HighlightedTextbox.update(...)`."
        )
        return {
            "color_map": color_map,
            "show_legend": show_legend,
            "show_legend_label": show_legend_label,
            "legend_label": legend_label,
            "label": label,
            "info": info,
            "show_label": show_label,
            "container": container,
            "scale": scale,
            "min_width": min_width,
            "visible": visible,
            "value": value,
            "interactive": interactive,
            "show_copy_button": show_copy_button,
            "autofocus": autofocus,
            "autoscroll": autoscroll,
            "__type__": "update",
        }

    def preprocess(self, x: str | None) -> str | None:
        """
        Preprocesses input (converts it to a string) before passing it to the function.
        Parameters:
            x: text
        Returns:
            text
        """
        return None if x is None else str(x)

    def postprocess(
        self, y: list[tuple[str, str | float | None]] | dict | None
    ) -> list[tuple[str, str | float | None]] | None:
        """
        Parameters:
            y: List of (word, category) tuples, or a dictionary of two keys: "text", and "highlights", which itself is 
            a list of dictionaries, each of which have the keys: "highlight_type", "start", and "end"
        Returns:
            List of (word, category) tuples
        """
        if y is None:
            return None
        if isinstance(y, dict):
            try:
                text = y["text"]
                highlights = y["highlights"]
            except KeyError as ke:
                raise ValueError(
                    "Expected a dictionary with keys 'text' and 'highlights' "
                    "for the value of the HighlightedText component."
                ) from ke
            if len(highlights) == 0:
                y = [(text, None)]
            else:
                list_format = []
                index = 0
                entities = sorted(highlights, key=lambda x: x["start"])
                for entity in entities:
                    list_format.append((text[index : entity["start"]], None))
                    highlight_type = entity.get("highlight_type")
                    list_format.append(
                        (text[entity["start"] : entity["end"]], highlight_type)
                    )
                    index = entity["end"]
                list_format.append((text[index:], None))
                y = list_format
        if self.combine_adjacent:
            output = []
            running_text, running_category = None, None
            for text, category in y:
                if running_text is None:
                    running_text = text
                    running_category = category
                elif category == running_category:
                    running_text += self.adjacent_separator + text
                elif not text:
                    # Skip fully empty item, these get added in processing
                    # of dictionaries.
                    pass
                else:
                    output.append((running_text, running_category))
                    running_text = text
                    running_category = category
            if running_text is not None:
                output.append((running_text, running_category))
            return output
        else:
            return y

    def set_interpret_parameters(
        self, separator: str = " ", replacement: str | None = None
    ):
        """
        Calculates interpretation score of characters in input by splitting input into tokens, then using a "leave one out" method to calculate the score of each token by removing each token and measuring the delta of the output value.
        Parameters:
            separator: Separator to use to split input into tokens.
            replacement: In the "leave one out" step, the text that the token should be replaced with. If None, the token is removed altogether.
        """
        self.interpretation_separator = separator
        self.interpretation_replacement = replacement
        return self

    def tokenize(self, x: str) -> tuple[list[str], list[str], None]:
        """
        Tokenizes an input string by dividing into "words" delimited by self.interpretation_separator
        """
        tokens = x.split(self.interpretation_separator)
        leave_one_out_strings = []
        for index in range(len(tokens)):
            leave_one_out_set = list(tokens)
            if self.interpretation_replacement is None:
                leave_one_out_set.pop(index)
            else:
                leave_one_out_set[index] = self.interpretation_replacement
            leave_one_out_strings.append(
                self.interpretation_separator.join(leave_one_out_set)
            )
        return tokens, leave_one_out_strings, None

    def get_masked_inputs(
        self, tokens: list[str], binary_mask_matrix: list[list[int]]
    ) -> list[str]:
        """
        Constructs partially-masked sentences for SHAP interpretation
        """
        masked_inputs = []
        for binary_mask_vector in binary_mask_matrix:
            masked_input = np.array(tokens)[np.array(binary_mask_vector, dtype=bool)]
            masked_inputs.append(self.interpretation_separator.join(masked_input))
        return masked_inputs

    def get_interpretation_scores(
        self, x, neighbors, scores: list[float], tokens: list[str], masks=None, **kwargs
    ) -> list[tuple[str, float]]:
        """
        Returns:
            Each tuple set represents a set of characters and their corresponding interpretation score.
        """
        result = []
        for token, score in zip(tokens, scores):
            result.append((token, score))
            result.append((self.interpretation_separator, 0))
        return result

    def style(
        self,
        *,
        show_copy_button: bool | None = None,
        color_map: dict[str, str] | None = None,
        container: bool | None = None,
        **kwargs,
    ):
        """
        This method is deprecated. Please set these arguments in the constructor instead.
        """
        warn_style_method_deprecation()
        if show_copy_button is not None:
            self.show_copy_button = show_copy_button
        if container is not None:
            self.container = container
        if color_map is not None:
            self.color_map = color_map
        return self
