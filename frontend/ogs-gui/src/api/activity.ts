export type ActivityLevel =
    | "info"
    | "success"
    | "warning"
    | "error";


export interface ActivityEntry {
    id: number;
    timestamp: string;
    level: ActivityLevel;
    source: string;
    message: string;
}


interface ActivityResponse {
    success: boolean;
    data: ActivityEntry[];
}


export async function getActivity(
    limit: number = 100
): Promise<ActivityEntry[]> {

    const response = await fetch(
        `/api/activity?limit=${limit}`
    );

    if (!response.ok) {

        let detail: string;

        try {
            const errorData = await response.json();

            detail =
                errorData.detail ??
                JSON.stringify(errorData);

        } catch {
            detail = await response.text();
        }

        throw new Error(
            `Activity request failed (${response.status}): ${detail}`
        );
    }

    const result: ActivityResponse =
        await response.json();

    return result.data;
}


export async function clearActivity(): Promise<void> {

    const response = await fetch(
        "/api/activity",
        {
            method: "DELETE"
        }
    );

    if (!response.ok) {
        throw new Error(
            "Failed to clear activity"
        );
    }
}