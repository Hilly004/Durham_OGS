export interface SatelliteRecord {
    id: number;
    name: string;
    tle_line1: string;
    tle_line2: string;
}


export interface CreateSatelliteRequest {
    name: string;
    tle_line1: string;
    tle_line2: string;
}


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

        satellite_id?: number | null;
        satellite_name?: string | null;
    };
}


export interface SatelliteSlewResponse {
    success: boolean;

    data: {
        status: string;
        message: string;
    };
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


export interface StopTrackingResponse {
    success: boolean;

    data: {
        status: string;
        message: string;
    };
}


/*
 * Get all stored satellites
 */
export async function listSatellites():
    Promise<SatelliteRecord[]> {

    const response = await fetch(
        "/api/satellites/"
    );


    if (!response.ok) {

        throw new Error(
            "Failed to load satellites"
        );
    }


    return response.json();
}


/*
 * Create / upload TLE
 */
export async function createSatellite(
    satellite: CreateSatelliteRequest
): Promise<SatelliteRecord> {

    const response = await fetch(
        "/api/satellites/",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json",
            },

            body: JSON.stringify(
                satellite
            ),
        }
    );


    if (!response.ok) {

        let message =
            "Unable to save satellite";


        try {

            const error =
                await response.json();


            if (
                typeof error.detail ===
                "string"
            ) {

                message =
                    error.detail;

            } else if (
                error.detail
            ) {

                message =
                    JSON.stringify(
                        error.detail
                    );
            }

        } catch {
            // Keep default message
        }


        throw new Error(
            message
        );
    }


    /*
     * Backend returns SatelliteResponse
     * directly, not { success, data }.
     */
    return response.json();
}


/*
 * Get satellite tracking status
 */
export async function
getSatelliteTrackingStatus():
Promise<SatelliteTrackingStatus> {

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


/*
 * Slew / begin tracking satellite
 */
export async function slewToSatellite(
    satelliteId: number
): Promise<SatelliteSlewResponse> {

    const response = await fetch(
        `/api/satellites/${satelliteId}/slew`,
        {
            method: "POST",
        }
    );


    if (!response.ok) {

        let message =
            "Failed to slew to satellite";


        try {

            const error =
                await response.json();

            message =
                error.detail ??
                message;

        } catch {
            // Keep default
        }


        throw new Error(
            message
        );
    }


    return response.json();
}


/*
 * Predict satellite pass
 */
export async function
predictSatellitePass(
    satelliteId: number,
    jd: number,
    minutes: number
): Promise<SatellitePassPrediction> {

    const response = await fetch(
        `/api/satellites/${satelliteId}/predict`,
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json",
            },

            body: JSON.stringify({
                jd,
                minutes,
            }),
        }
    );


    if (!response.ok) {

        let message =
            "Failed to predict satellite pass";


        try {

            const error =
                await response.json();

            message =
                error.detail ??
                message;

        } catch {
            // Keep default
        }


        throw new Error(
            message
        );
    }


    return response.json();
}


/*
 * Stop satellite tracking
 *
 * This endpoint needs to exist in
 * backend/api/satellite.py.
 */
export async function
stopSatelliteTracking():
Promise<StopTrackingResponse> {

    const response = await fetch(
        "/api/satellites/tracking/stop",
        {
            method: "POST",
        }
    );


    if (!response.ok) {

        let message =
            "Failed to stop satellite tracking";


        try {

            const error =
                await response.json();

            message =
                error.detail ??
                message;

        } catch {
            // Keep default
        }


        throw new Error(
            message
        );
    }


    return response.json();
}


/*
 * Current Julian Date
 */
export function
getCurrentJulianDate():
number {

    return (
        Date.now()
        / 86400000
        + 2440587.5
    );
}