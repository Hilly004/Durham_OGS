export interface ObservatorySafetyData {
    safe: boolean;
    reason: string | null;
}

interface ObservatorySafetyResponse {
    success: boolean;
    data: ObservatorySafetyData;
}

export async function getObservatorySafety(): Promise<ObservatorySafetyData> {
    const response = await fetch("/api/observatory/safety");

    if (!response.ok) {
        throw new Error("Failed to get observatory safety status");
    }

    const result: ObservatorySafetyResponse =
        await response.json();

    return result.data;
}