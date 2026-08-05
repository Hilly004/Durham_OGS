import {
    parkMount,
    slewMount
} from "../../api/mount";

export default function MountControls() {

    async function handlePark() {
        try {
            await parkMount();
            console.log('Mount parked');
        } 
        catch (error) {
            console.error(error);
        }
    }

    async function handleSlew() {

        await slewMount(
            12.5,
            -30.2
        );

    }

    return (
        <div className='
        bg-slate-800
        rounded-xl
        p-6
        shadow-lg
        border
        border-slate-700
        '>
            <h2>Mount Controls</h2>

            <button onClick={handlePark}>Park Mount</button>
            <button onClick={handleSlew}>Slew Mount</button>
        </div>
    );
}