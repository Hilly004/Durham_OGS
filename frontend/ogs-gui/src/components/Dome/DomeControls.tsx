import {
    openDome,
    closeDome,
    connectDome,
    disconnectDome,
    openDomeOne,
    closeDomeOne,
    openDomeTwo,
    closeDomeTwo
} from '../../api/dome';   

export default function DomeControls() {
    
    async function handleOpen() {
        try {
            await openDome();
            console.log('Dome opened');
        } 
        catch (error) {
            console.error(error);
        }
    }

    async function handleClose() {
        try {
            await closeDome();
            console.log('Dome closed');
        } 
        catch (error) {
            console.error(error);
        }
    }

    async function handleConnect() {
        try {
            await connectDome();
            console.log('Dome connected');
        } 
        catch (error) {
            console.error(error);
        }
    }

    async function handleDisconnect() {
        try {
            await disconnectDome();
            console.log('Dome disconnected');
        } 
        catch (error) {
            console.error(error);
        }
    }

    async function handleOpenOne() {
        try {
            await openDomeOne();
            console.log('Dome one opened');
        } 
        catch (error) {
            console.error(error);
        }
    }

    async function handleCloseOne() {
        try {
            await closeDomeOne();
            console.log('Dome one closed');
        } 
        catch (error) {
            console.error(error);
        }
    }

    async function handleOpenTwo() {
        try {
            await openDomeTwo();
            console.log('Dome two opened');
        } 
        catch (error) {
            console.error(error);
        }
    }

    async function handleCloseTwo() {
        try {
            await closeDomeTwo();
            console.log('Dome two closed');
        } 
        catch (error) {
            console.error(error);
        }
    }

    return (
        <div className='panel'>
            <h2>Dome Controls</h2> 
            <button onClick={handleOpen}>Open Dome</button>
            <button onClick={handleClose}>Close Dome</button>
            <button onClick={handleConnect}>Connect Dome</button>
            <button onClick={handleDisconnect}>Disconnect Dome</button>
            <button onClick={handleOpenOne}>Open Dome One</button>
            <button onClick={handleCloseOne}>Close Dome One</button>
            <button onClick={handleOpenTwo}>Open Dome Two</button>
            <button onClick={handleCloseTwo}>Close Dome Two</button>
        </div>
    );
}