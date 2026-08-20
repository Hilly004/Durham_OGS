async function api<T>(
    url: string,
    options?: RequestInit
): Promise<T> {

    const response =
        await fetch(
            url,
            options
        );


    if (!response.ok) {

        let message =
            "Mount setup request failed";


        try {

            const error =
                await response.json();


            if (
                typeof error?.detail
                === "string"
            ) {

                message =
                    error.detail;
            }


        } catch {

            // Keep default error message
        }


        throw new Error(
            message
        );
    }


    return response.json();
}


/*
 * ============================================================
 * Types
 * ============================================================
 */

export interface MountSite {

    latitude: number | string;

    longitude: number | string;

    elevation_m: number | string;
}


export interface MountInformation {

    product?: string;

    firmware?: string;

    firmware_date?: string;

    control_box?: string;

    connection_type?: string;

    mount_ip?: string;
}


export interface MountTimeData {

    mount_utc: string;

    computer_utc: string;
}


export interface AlignmentStar {

    index: number;

    hour_angle: string;

    declination: string;

    error_arcsec: number;

    polar_angle?:
        number | null;
}


export interface AlignmentModel {

    azimuth?:
        number | null;

    altitude?:
        number | null;

    polar_error?:
        number | null;

    position_angle?:
        number | null;

    orthogonality_error?:
        number | null;

    azimuth_adjustment_turns?:
        number | null;

    altitude_adjustment_turns?:
        number | null;

    terms?:
        number | null;

    expected_rms_arcsec?:
        number | null;
}


export interface AlignmentData {

    star_count: number;

    model:
        AlignmentModel | null;

    stars:
        AlignmentStar[];
}


/*
 * ============================================================
 * Mount Information
 * ============================================================
 */

export async function getMountInfo() {

    return api<{
        success: boolean;
        data: MountInformation;
    }>(
        "/api/mount/info"
    );
}


/*
 * ============================================================
 * Site Setup
 * ============================================================
 */

export async function getMountSite() {

    return api<{
        success: boolean;
        data: MountSite;
    }>(
        "/api/mount/setup/site"
    );
}


export async function setMountSite(
    latitude: number,
    longitude: number,
    elevation_m: number
) {

    return api<{
        success: boolean;
        data: MountSite;
    }>(
        "/api/mount/setup/site",
        {
            method: "PUT",

            headers: {
                "Content-Type":
                    "application/json",
            },

            body:
                JSON.stringify({
                    latitude,
                    longitude,
                    elevation_m,
                }),
        }
    );
}


/*
 * ============================================================
 * Mount Time
 * ============================================================
 */

export async function getMountTime() {

    return api<{
        success: boolean;

        data: MountTimeData;
    }>(
        "/api/mount/setup/time"
    );
}


export async function syncMountTime() {

    return api<{
        success: boolean;
        message: string;
    }>(
        "/api/mount/setup/time/sync",
        {
            method: "POST",
        }
    );
}


/*
 * ============================================================
 * Home
 * ============================================================
 */

export async function seekHome() {

    return api<{
        success: boolean;
        data: unknown;
    }>(
        "/api/mount/setup/home",
        {
            method: "POST",
        }
    );
}


export async function seekHomeAlign() {

    return api<{
        success: boolean;
        data: unknown;
    }>(
        "/api/mount/setup/home-align",
        {
            method: "POST",
        }
    );
}


export async function getHomeStatus() {

    return api<{
        success: boolean;
        data: unknown;
    }>(
        "/api/mount/setup/home/status"
    );
}


/*
 * ============================================================
 * Alignment
 * ============================================================
 */

export async function getAlignment() {

    return api<{
        success: boolean;
        data: AlignmentData;
    }>(
        "/api/mount/alignment"
    );
}


/*
 * Slew to a known alignment target.
 */
export async function slewToAlignmentTarget(
    name: string,
    ra_hours: number,
    dec_degrees: number
) {

    return api<{
        success: boolean;

        data: {
            name: string;
            ra_hours: number;
            dec_degrees: number;
        };
    }>(
        "/api/mount/alignment/slew",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json",
            },

            body:
                JSON.stringify({
                    name,
                    ra_hours,
                    dec_degrees,
                }),
        }
    );
}


/*
 * Nudge the mount while centring
 * an alignment target.
 */
export async function nudgeAlignmentMount(
    direction:
        | "north"
        | "south"
        | "east"
        | "west",

    step_arcsec: number
) {

    return api<{
        success: boolean;

        data: {
            direction: string;
            step_arcsec: number;
            result: unknown;
        };
    }>(
        "/api/mount/alignment/nudge",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json",
            },

            body:
                JSON.stringify({
                    direction,
                    step_arcsec,
                }),
        }
    );
}


/*
 * Add the currently centred
 * known target as an alignment point.
 */
export async function addAlignmentPoint(
    name: string,
    ra_hours: number,
    dec_degrees: number
) {

    return api<{
        success: boolean;

        data: {
            name: string;
            ra: string;
            dec: string;
            response: unknown;
        };
    }>(
        "/api/mount/alignment/add-point",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json",
            },

            body:
                JSON.stringify({
                    name,
                    ra_hours,
                    dec_degrees,
                }),
        }
    );
}


/*
 * Delete one alignment point.
 */
export async function deleteAlignmentPoint(
    index: number
) {

    return api<{
        success: boolean;
    }>(
        `/api/mount/alignment/points/${index}`,
        {
            method: "DELETE",
        }
    );
}


/*
 * Delete the entire active
 * alignment model.
 */
export async function deleteAlignmentModel() {

    return api<{
        success: boolean;
    }>(
        "/api/mount/alignment",
        {
            method: "DELETE",
        }
    );
}


/*
 * ============================================================
 * Saved Alignment Models
 * ============================================================
 */

export async function getSavedModels() {

    return api<{
        success: boolean;
        data: string[];
    }>(
        "/api/mount/models"
    );
}


/*
 * Save the current active model
 * inside the TenMicron mount.
 */
export async function saveModel(
    name: string
) {

    return api<{
        success: boolean;
    }>(
        "/api/mount/models/save",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json",
            },

            body:
                JSON.stringify({
                    name,
                }),
        }
    );
}


/*
 * Load a saved TenMicron model.
 */
export async function loadModel(
    name: string
) {

    return api<{
        success: boolean;
    }>(
        "/api/mount/models/load",
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json",
            },

            body:
                JSON.stringify({
                    name,
                }),
        }
    );
}


/*
 * Delete a saved TenMicron model.
 */
export async function deleteSavedModel(
    name: string
) {

    return api<{
        success: boolean;
    }>(
        (
            "/api/mount/models/"
            +
            encodeURIComponent(
                name
            )
        ),
        {
            method: "DELETE",
        }
    );
}