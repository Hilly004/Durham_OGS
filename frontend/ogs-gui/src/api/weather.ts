export interface WeatherStatusData {
    connected: boolean;
    safe: boolean;
    actualSafe: boolean;
    override: boolean | null;
    state: "safe" | "unsafe" | "unknown";
    reason: string | null;
}
interface ApiResponse {
    success: boolean;
    data: WeatherStatusData;
}


export async function getWeatherStatus(): Promise<WeatherStatusData> {

    const response = await fetch('/api/weather/status');

    if (!response.ok) {
        throw new Error('Failed to get weather status');
    }

    const result: ApiResponse = await response.json();
    return result.data;
}

export async function connectWeather(): Promise<void> {

    const response = await fetch("/api/weather/connect", {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to connect weather station");
    }
}   

export async function disconnectWeather(): Promise<void> {

    const response = await fetch("/api/weather/disconnect", {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to disconnect weather station");
    }
}   

export type WeatherOverrideMode =
    | "auto"
    | "safe"
    | "unsafe";

export async function setWeatherOverride(
    mode: WeatherOverrideMode
): Promise<void> {

    const response = await fetch(
        "/api/weather/override",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                mode,
            }),
        }
    );

    if (!response.ok) {

        let message =
            "Failed to change weather override";

        try {

            const error =
                await response.json();

            message =
                error.detail ?? message;

        } catch {
            // Use default message
        }

        throw new Error(message);
    }
}