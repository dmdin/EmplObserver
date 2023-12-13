import { writable } from "svelte/store";
import { TimeInterval } from "$lib/enums";

export const period = writable(TimeInterval.Month)

