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
    gain_unit?: string | null;

    frame_rate?: number | null;
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


async function getErrorMessage(
    response: Response,
    fallback: string
): Promise<string> {

    try {

        const data =
            await response.json();

        return (
            typeof data?.detail === "string"
                ? data.detail
                : fallback
        );

    } catch {

        return fallback;

    }
}


export async function getCameraStatus():
Promise<CameraStatusData> {

    const response = await fetch(
        "/api/camera/status"
    );

    if (!response.ok) {

        throw new Error(
            await getErrorMessage(
                response,
                "Failed to get camera status"
            )
        );

    }


    const result:
        CameraStatusResponse =
            await response.json();


    return result.data;
}


export async function connectCamera():
Promise<void> {

    const response = await fetch(
        "/api/camera/connect",
        {
            method: "POST",
        }
    );


    if (!response.ok) {

        throw new Error(
            await getErrorMessage(
                response,
                "Failed to connect camera"
            )
        );

    }
}


export async function disconnectCamera():
Promise<void> {

    const response = await fetch(
        "/api/camera/disconnect",
        {
            method: "POST",
        }
    );


    if (!response.ok) {

        throw new Error(
            await getErrorMessage(
                response,
                "Failed to disconnect camera"
            )
        );

    }
}


export function getCameraLiveUrl():
string {

    return "/api/camera/live";
}


export function getCameraFrameUrl():
string {

    return (
        `/api/camera/frame?v=${Date.now()}`
    );
}


export async function startCameraStream():
Promise<void> {

    const response = await fetch(
        "/api/camera/stream/start",
        {
            method: "POST",
        }
    );


    if (!response.ok) {

        throw new Error(
            await getErrorMessage(
                response,
                "Failed to start camera stream"
            )
        );

    }
}


export async function stopCameraStream():
Promise<void> {

    const response = await fetch(
        "/api/camera/stream/stop",
        {
            method: "POST",
        }
    );


    if (!response.ok) {

        throw new Error(
            await getErrorMessage(
                response,
                "Failed to stop camera stream"
            )
        );

    }
}


export async function getCameraStreamStatus():
Promise<StreamStatusResponse> {

    const response = await fetch(
        "/api/camera/stream/status"
    );


    if (!response.ok) {

        throw new Error(
            await getErrorMessage(
                response,
                "Failed to get camera stream status"
            )
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
                "Content-Type":
                    "application/json",
            },

            body: JSON.stringify({
                exposure_us:
                    exposureUs,
            }),
        }
    );


    if (!response.ok) {

        throw new Error(
            await getErrorMessage(
                response,
                "Failed to set camera exposure"
            )
        );

    }
}


export async function setCameraGain(
    gain: number
): Promise<void> {

    const response = await fetch(
        "/api/camera/gain",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json",
            },

            body: JSON.stringify({
                gain,
            }),
        }
    );


    if (!response.ok) {

        throw new Error(
            await getErrorMessage(
                response,
                "Failed to set camera gain"
            )
        );

    }
}


export async function setCameraFrameRate(
    fps: number
): Promise<void> {

    const response = await fetch(
        "/api/camera/frame-rate",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json",
            },

            body: JSON.stringify({
                fps,
            }),
        }
    );


    if (!response.ok) {

        throw new Error(
            await getErrorMessage(
                response,
                "Failed to set camera frame rate"
            )
        );

    }
}

export async function captureCameraFrame():
Promise<Blob> {

    const response = await fetch(
        getCameraFrameUrl()
    );

    if (!response.ok) {

        throw new Error(
            await getErrorMessage(
                response,
                "Unable to capture frame"
            )
        );

    }

    return response.blob();
}