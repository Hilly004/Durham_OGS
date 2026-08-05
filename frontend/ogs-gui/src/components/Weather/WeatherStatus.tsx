import { useEffect, useState } from "react";
import { getWeatherStatus } from "../../api/weather";
import type { WeatherStatusData } from "../../api/weather";
import {
    connectWeather,
    disconnectWeather
} from "../../api/weather";

export default function WeatherStatusWidget(){

    const [status, setStatus] = useState<WeatherStatusData | null>(null);


    useEffect(() => {

        const update = () => {
            getWeatherStatus()
                .then(setStatus)
                .catch(console.error);
        };

        update();

        const timer = setInterval(update,1000000) //this needs changing to a more reasonable value when the ui has been built

        return () => clearInterval(timer);
        

    }, []);


    if (!status) {
        return(
            <div className="
            bg-slate-800
            rounded-xl
            p-6
            shadow-lg
            border
            border-slate-700
            "
            >
                <h2 className="text-xl font-bold mb-4 text-white"
                >Weather Station Status</h2>

                <p className="text-red-400"
                >
                    Not connected
                </p>

                <button onClick={handleConnect}
                className="mt-4 px-4 py-2 rounded bg-blue-600 hover:bg-blue-700 text-white"
                >
                    Connect
                </button>
            </div>    
        );
    }

   

    async function handleConnect() {
        try {
            await connectWeather();
            console.log('Weather station connected');
        } 
        catch (error) {
            console.error(error);
        }
    }

    async function handleDisconnect() {
        try {
            await disconnectWeather();
            console.log('Weather station disconnected');
        } 
        catch (error) {
            console.error(error);
        }
    }

    return (
        <div className='
        bg-slate-800
        rounded-xl
        p-6
        shadow-lg
        border
        border-slate-700'
        >
            <h2>Mount Status</h2>

            <p>
                Connected: {status.connected ? "Yes" : "No"}
            </p>
            <button onClick={status.connected ? handleDisconnect : handleConnect}>
                {status.connected ? "Disconnect" : "Connect"}
            </button>   
        </div>
    );
}



   

