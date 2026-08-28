export interface DomeStatusData {
    connected: boolean;
    open: boolean;
    closed: boolean;
    opening: boolean;
    closing: boolean;
    moving: boolean;
    fault: boolean;
}


interface DomeStatusResponse {
    success: boolean;
    data: DomeStatusData;
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


async function domePost(
    endpoint: string,
    fallback: string
): Promise<void> {

    const response =
        await fetch(
            `/api/dome/${endpoint}`,
            {
                method: "POST",
            }
        );


    if (!response.ok) {

        const message =
            await getErrorMessage(
                response,
                fallback
            );

        throw new Error(message);

    }

}


export async function getDomeStatus():
Promise<DomeStatusData> {

    const response =
        await fetch(
            "/api/dome/status"
        );


    if (!response.ok) {

        const message =
            await getErrorMessage(
                response,
                "Failed to get dome status"
            );

        throw new Error(message);

    }


    const result:
        DomeStatusResponse =
            await response.json();


    return result.data;

}


export function connectDome():
Promise<void> {

    return domePost(
        "connect",
        "Failed to connect dome"
    );

}


export function disconnectDome():
Promise<void> {

    return domePost(
        "disconnect",
        "Failed to disconnect dome"
    );

}


export function openDome():
Promise<void> {

    return domePost(
        "open",
        "Failed to open dome"
    );

}


export function closeDome():
Promise<void> {

    return domePost(
        "close",
        "Failed to close dome"
    );

}


export function openDomeOne():
Promise<void> {

    return domePost(
        "open_one",
        "Failed to open left shutter"
    );

}


export function closeDomeOne():
Promise<void> {

    return domePost(
        "close_one",
        "Failed to close left shutter"
    );

}


export function openDomeTwo():
Promise<void> {

    return domePost(
        "open_two",
        "Failed to open right shutter"
    );

}


export function closeDomeTwo():
Promise<void> {

    return domePost(
        "close_two",
        "Failed to close right shutter"
    );

}

