import { useEffect, useState } from "react";
import { getMountStatus } from "../../api/mount";
import type { MountStatusData } from "../../api/mount";
import {
    connectMount,
    disconnectMount
} from "../../api/mount";

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
        return(
            <div>
                <button onClick={handleConnect}>
                    Connect
                </button>

                <p>Mount not connected</p>
            </div>    
        );
    }

   

    async function handleConnect() {
        try {
            await connectMount();
            console.log('Mount connected');
        } 
        catch (error) {
            console.error(error);
        }
    }

    async function handleDisconnect() {
        try {
            await disconnectMount();
            console.log('Mount disconnected');
        } 
        catch (error) {
            console.error(error);
        }
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

            <button onClick={status.connected ? handleDisconnect : handleConnect}>
                {status.connected ? "Disconnect" : "Connect"}
            </button>   
        </div>
    );
}

