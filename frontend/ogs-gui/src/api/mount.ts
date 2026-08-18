export interface MountStatusData {
    connected: boolean;
    alt: number;
    az: number;
}

interface ApiResponse {
    success: boolean;
    data: MountStatusData;
}

export async function getMountStatus(): Promise<MountStatusData> {

    const response = await fetch('/api/mount/status');

    if (!response.ok) {
        throw new Error('Failed to get mount status');
    }

    const result: ApiResponse = await response.json();
    return result.data;
}

export interface MountPosition {
    alt: number;
    az: number;
}

export interface MountPosition_rd {
    ra: number;
    dec: number;
}

interface PositionApiResponse {
    success: boolean;
    data: MountPosition;
}

interface PositionRdApiResponse {
    success: boolean;
    data: MountPosition_rd;
}

export async function getMountPosition(): Promise<MountPosition> {

    const response = await fetch("/api/mount/position_aa");

    if (!response.ok) {
        throw new Error("Failed to get mount position");
    }

    const result: PositionApiResponse =
        await response.json();

    return result.data;
}

export async function getMountPosition_rd(): Promise<MountPosition_rd> {

    const response = await fetch("/api/mount/position_rd");

    if (!response.ok) {
        throw new Error("Failed to get mount position");
    }

    const result: PositionRdApiResponse =
        await response.json();

    return result.data;
}

export async function parkMount(): Promise<void> {

    const response = await fetch("/api/mount/park", {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to park mount");
    }
}


export async function slewMount(
    ra: number,
    dec: number
): Promise<void> {

    const response = await fetch("/api/mount/slew", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            ra,
            dec
        })
    });

    if (!response.ok) {
        throw new Error("Failed to slew mount");
    }
}

export async function connectMount(): Promise<void> {

    const response = await fetch("/api/mount/connect", {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to connect mount");
    }
}   

export async function disconnectMount(): Promise<void> {

    const response = await fetch("/api/mount/disconnect", {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to disconnect mount");
    }
}   

export type ManualMoveDirection =
    | "north"
    | "south"
    | "east"
    | "west";


export async function startManualMove(
    direction: ManualMoveDirection
): Promise<void> {

    const response = await fetch(
        `/api/mount/move/${direction}`,
        {
            method: "POST",
        }
    );


    if (!response.ok) {

        const message =
            await response.text();

        throw new Error(
            `Unable to move mount ${direction}: ${message}`
        );
    }
}


export async function stopManualMove(
    direction: ManualMoveDirection
): Promise<void> {

    const response = await fetch(
        `/api/mount/stop/${direction}`,
        {
            method: "POST",
        }
    );


    if (!response.ok) {

        const message =
            await response.text();

        throw new Error(
            `Unable to stop mount ${direction}: ${message}`
        );
    }
}