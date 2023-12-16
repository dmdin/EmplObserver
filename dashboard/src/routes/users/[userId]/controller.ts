import { writable, derived, type Readable} from 'svelte/store';
import { TimeInterval } from '$lib/enums';
import { page } from '$app/stores';
import { rpc } from '$lib/client';

export const period = writable(TimeInterval.Month);

export const userId = derived(page, ($page) => Number($page.params.userId ))

export type Events = Awaited<ReturnType<typeof rpc.EventTimeInterval.getForUser>>;
export const events: Readable<Events> = derived([userId, period], ([$userId, $period], set) => {
	(async () => {
		const res = await rpc.EventTimeInterval.getForUser($userId, $period);
		set(res);
	})();
});

export type AppsInfo = Awaited<ReturnType<typeof rpc.EventApplication.getForUser>>;
export const appsInfo: Readable<AppsInfo> = derived([userId, period], ([$userId, $period], set) => {
	(async () => {
		const res = await rpc.EventApplication.getForUser($userId, $period)
		set(res)
	})()
})