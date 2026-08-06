export interface SatelliteStatusData {
    connected:boolean
}

interface ApiResponse {
    success:boolean;
    data:SatelliteStatusData
}

export async function 