<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio, SelectData } from "@gradio/utils";
	import { createEventDispatcher } from "svelte";

	import HighlightedTextbox from "../shared";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { merge_elements } from "../utils";

	const dispatch = createEventDispatcher<{
		change: string;
		submit: never;
		blur: never;
		select: SelectData;
		input: never;
		focus: never;
	}>();

	export let gradio:
		| Gradio<{
				change: string;
				submit: never;
				blur: never;
				select: SelectData;
				input: never;
				focus: never;
		  }>
		| { dispatch: typeof dispatch } = {
		dispatch
	};
	export let label = "Highlighted Textbox";
	export let legend_label = "Highlights:"
	export let info: string | undefined = undefined;
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value: [string, string | null][];
	export let show_label: boolean;
	export let show_legend: boolean;
	export let show_legend_label: boolean;
	export let color_map: Record<string, string> = {};
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let show_copy_button = false;
	export let loading_status: LoadingStatus | undefined = undefined;
	export let value_is_output = false;
	export let autofocus = false;
	export let combine_adjacent = false;

	$: if (!color_map && Object.keys(color_map).length) {
		color_map = color_map;
	}

	$: if (value && combine_adjacent) {
		value = merge_elements(value, "equal");
	}
</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={container}
>
	{#if loading_status}
		<StatusTracker {...loading_status} />
	{/if}

	<HighlightedTextbox
		bind:value
		bind:value_is_output
		{label}
		{info}
		{show_label}
		{show_legend}
		{show_legend_label}
		{legend_label}
		{color_map}
		{show_copy_button}
		{autofocus}
		{container}
		on:change={() => gradio.dispatch("change")}
		on:input={() => gradio.dispatch("input")}
		on:submit={() => gradio.dispatch("submit")}
		on:blur={() => gradio.dispatch("blur")}
		on:select={(e) => gradio.dispatch("select", e.detail)}
		on:focus={() => gradio.dispatch("focus")}
	/>
</Block>
