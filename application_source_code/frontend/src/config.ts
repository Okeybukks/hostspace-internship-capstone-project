declare global {
    interface Window {
        REACT_APP_BACKEND_IP:any;
    }
}

const REACT_APP_BACKEND_IP: string = window.REACT_APP_BACKEND_IP || '';

export default REACT_APP_BACKEND_IP