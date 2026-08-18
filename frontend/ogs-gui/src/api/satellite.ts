export interface SatelliteTrackingStatus {
    success: boolean;
    data: {
        status:
            | "slewing"
            | "waiting"
            | "catching"
            | "tracking"
            | "ended"
            | "idle";
        tracking: boolean;
    };
}

export async function getSatelliteTrackingStatus(): Promise<SatelliteTrackingStatus> {
    const response = await fetch(
        "/api/satellites/tracking/status"
    );

    if (!response.ok) {
        throw new Error(
            "Failed to fetch satellite tracking status"
        );
    }

    return response.json();
}

export interface SatelliteSlewResponse {
    success: boolean;
    data: {
        status: string;
        message: string;
    };
}

export async function slewToSatellite(
    satelliteId: number
): Promise<SatelliteSlewResponse> {
    const response = await fetch(
        `/api/satellites/${satelliteId}/slew`,
        {
            method: "POST"
        }
    );

    if (!response.ok) {
        const error = await response.json();

        throw new Error(
            error.detail ?? "Failed to slew to satellite"
        );
    }

    return response.json();
}

export interface SatellitePassPrediction {
    success: boolean;
    data: {
        found: boolean;
        start_jd: number | null;
        end_jd: number | null;
        flags: string | null;
    };
}

export async function predictSatellitePass(
    satelliteId: number,
    jd: number,
    minutes: number
): Promise<SatellitePassPrediction> {
    const response = await fetch(
        `/api/satellites/${satelliteId}/predict`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                jd,
                minutes
            })
        }
    );

    if (!response.ok) {
        const error = await response.json();

        throw new Error(
            error.detail ?? "Failed to predict satellite pass"
        );
    }

    return response.json();
}

export function getCurrentJulianDate(): number {
    return Date.now() / 86400000 + 2440587.5;
}

export interface CreateSatelliteRequest {
    name: string;
    line1: string;
    line2: string;
}


export interface SatelliteRecord {
    id: number;
    name: string;
    line1: string;
    line2: string;
}


interface CreateSatelliteResponse {
    success: boolean;
    data: SatelliteRecord;
}


export async function createSatellite(
    satellite: CreateSatelliteRequest
): Promise<SatelliteRecord> {

    const response = await fetch(
        "/api/satellites",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify(satellite),
        }
    );


    if (!response.ok) {

        let message =
            "Unable to save satellite";

        try {

            const error =
                await response.json();

            message =
                error.detail ?? message;

        } catch {
            // Keep default error message
        }

        throw new Error(message);
    }


    const result: CreateSatelliteResponse =
        await response.json();

    return result.data;
}