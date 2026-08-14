export interface DomeStatusData {
    connected: boolean;
    isOpen: boolean;
    moving: boolean;
    fault: boolean;
}

interface ApiResponse {
    success: boolean;
    data: DomeStatusData;
}

export async function getDomeStatus(): Promise<DomeStatusData> {

    const response = await fetch('/api/dome/status');

    if (!response.ok) {
        throw new Error('Failed to get dome status');
    }

    const result: ApiResponse = await response.json();
    return result.data;
}

export async function openDome(): Promise<void> {

    const response = await fetch("/api/dome/open", {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to open dome");
    }
}

export async function closeDome(): Promise<void> {

    const response = await fetch("/api/dome/close", {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to close dome");
    }
}

export async function connectDome(): Promise<void> {

    const response = await fetch("/api/dome/connect", {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to connect dome");
    }
}

export async function disconnectDome(): Promise<void> {

    const response = await fetch("/api/dome/disconnect", {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to disconnect dome");
    }
}

export async function closeDomeOne(): Promise<void> {
    
    const response = await fetch("/api/dome/close_one", {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to close dome one");
    }
}

export async function closeDomeTwo(): Promise<void> {
    
    const response = await fetch("/api/dome/close_two", {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to close dome two");
    }
}

export async function openDomeOne(): Promise<void> {
    
    const response = await fetch("/api/dome/open_one", {
        method: "POST"
    }); 

    if (!response.ok) {
        throw new Error("Failed to open dome one");
    }
}

export async function openDomeTwo(): Promise<void> {
    
    const response = await fetch("/api/dome/open_two", {
        method: "POST"
    });

    if (!response.ok) {
        throw new Error("Failed to open dome two");
    }
}   