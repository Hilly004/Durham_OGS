import { useEffect, useState } from "react";
import { getMountStatus, MountStatusData } from "../../api/mount";


export default function MountStatusWidget(){

    const [status, setStatus] = useState<MountStatusData | null>(null);


    useEffect(() => {

        const update = () => {
            getMountStatus()
                .then(setStatus)
                .catch(console.error);
        };

        update();

        const timer = setInterval(update,1000)

        return () => clearInterval(timer);
        

    }, []);


    if (!status) {
        return <p>Loading...</p>;
    }


    return (
        <div>
            <h2>Mount Status</h2>

            <p>
                Connected: {status.connected ? "Yes" : "No"}
            </p>

            <p>
                Altitude: {status.alt}
            </p>

            <p>
                Azimuth: {status.az}
            </p>
        </div>
    );
}