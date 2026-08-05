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