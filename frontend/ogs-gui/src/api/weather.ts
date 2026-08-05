export interface WeatherStatusData {
    connected: boolean
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

