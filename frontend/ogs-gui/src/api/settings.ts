export type CameraType =
    | 'allied'
    | 'zwo';

export interface ObservatorySettings {
    id: number;
    site_name: string;
    latitude: number;
    longitude: number;
    elevation_m: number;
    mount_host: string;
    mount_port: number;
    dome_host: string;
    dome_port: number;
    weather_port: string;
    weather_baudrate: number;
    camera_type: CameraType;
    camera_id: string;
    max_wind_speed: number;
    max_humidity: number;
    weather_timeout_seconds: number;
    automatic_shutdown_enabled: boolean;
    default_nudge_arcsec: number;
    default_prediction_minutes: number;
    activity_log_max_entries: number;
}

export type SettingsUpdate = Omit<ObservatorySettings, "id">;

async function errorMessage(response: Response, fallback: string) {
    try {
        const data = await response.json();
        return typeof data?.detail === "string" ? data.detail : fallback;
    } catch {
        return fallback;
    }
}

export async function getSettings(): Promise<ObservatorySettings> {
    const response = await fetch("/api/settings");
    if (!response.ok) throw new Error(await errorMessage(response, "Unable to load settings"));
    return response.json();
}

export async function saveSettings(settings: SettingsUpdate): Promise<ObservatorySettings> {
    const response = await fetch("/api/settings", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(settings),
    });
    if (!response.ok) throw new Error(await errorMessage(response, "Unable to save settings"));
    return response.json();
}

async function postTest(url: string, body: object): Promise<string> {
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });
    if (!response.ok) throw new Error(await errorMessage(response, "Connection test failed"));
    const data = await response.json();
    return data.message;
}

export const testMountConnection = (host: string, port: number) =>
    postTest("/api/settings/test/mount", { host, port });

export const testDomeConnection = (host: string, port: number) =>
    postTest("/api/settings/test/dome", { host, port });

export const testWeatherConnection = (port: string, baudrate: number) =>
    postTest("/api/settings/test/weather", { port, baudrate });