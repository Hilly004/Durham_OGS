export interface CameraInfo {
    id: string;
    name: string;
    model: string;
    serial: string;
}


export interface CameraStatusData {
    connected: boolean;
    streaming: boolean;

    camera: CameraInfo | null;

    exposure: number | null;
    gain: number | null;

    frame_count: number;
}


interface CameraStatusResponse {
    success: boolean;
    data: CameraStatusData;
}


interface StreamStatusResponse {
    success: boolean;
    connected: boolean;
    streaming: boolean;
}


export async function getCameraStatus(): Promise<CameraStatusData> {

    const response = await fetch(
        "/api/camera/status"
    );

    if (!response.ok) {
        throw new Error(
            "Failed to get camera status"
        );
    }

    const result: CameraStatusResponse =
        await response.json();

    return result.data;
}


export async function connectCamera(): Promise<void> {

    const response = await fetch(
        "/api/camera/connect",
        {
            method: "POST",
        }
    );

    if (!response.ok) {

        let message =
            "Failed to connect camera";

        try {

            const error =
                await response.json();

            message =
                error.detail ?? message;

        } catch {
            // Keep default message
        }

        throw new Error(message);
    }
}


export async function disconnectCamera(): Promise<void> {

    const response = await fetch(
        "/api/camera/disconnect",
        {
            method: "POST",
        }
    );

    if (!response.ok) {
        throw new Error(
            "Failed to disconnect camera"
        );
    }
}


export async function startCameraStream(): Promise<void> {

    const response = await fetch(
        "/api/camera/stream/start",
        {
            method: "POST",
        }
    );

    if (!response.ok) {

        let message =
            "Failed to start camera stream";

        try {

            const error =
                await response.json();

            message =
                error.detail ?? message;

        } catch {
            // Keep default
        }

        throw new Error(message);
    }
}


export async function stopCameraStream(): Promise<void> {

    const response = await fetch(
        "/api/camera/stream/stop",
        {
            method: "POST",
        }
    );

    if (!response.ok) {

        let message =
            "Failed to stop camera stream";

        try {

            const error =
                await response.json();

            message =
                error.detail ?? message;

        } catch {
            // Keep default
        }

        throw new Error(message);
    }
}


export async function getCameraStreamStatus(): Promise<StreamStatusResponse> {

    const response = await fetch(
        "/api/camera/stream/status"
    );

    if (!response.ok) {
        throw new Error(
            "Failed to get camera stream status"
        );
    }

    return response.json();
}


export async function setCameraExposure(
    exposureUs: number
): Promise<void> {

    const response = await fetch(
        "/api/camera/exposure",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                exposure_us: exposureUs,
            }),
        }
    );

    if (!response.ok) {

        let message =
            "Failed to set camera exposure";

        try {

            const error =
                await response.json();

            message =
                error.detail ?? message;

        } catch {
            // Keep default
        }

        throw new Error(message);
    }
}


export async function setCameraGain(
    gainDb: number
): Promise<void> {

    const response = await fetch(
        "/api/camera/gain",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                gain_db: gainDb,
            }),
        }
    );

    if (!response.ok) {

        let message =
            "Failed to set camera gain";

        try {

            const error =
                await response.json();

            message =
                error.detail ?? message;

        } catch {
            // Keep default
        }

        throw new Error(message);
    }
}