const findFirstExistingProperty = (properties, errorMessage) => {
    const notEmptyProperties = properties.filter(property => property !== undefined);
    if (notEmptyProperties.length === 0) {
        throw new Error(errorMessage);
    }
    return notEmptyProperties[0];
}

const resolveBackendIP = () => {
    return findFirstExistingProperty(
        [window.env.REACT_APP_BACKEND_IP, process.env.REACT_APP_BACKEND_IP],
        'Failed to resolve dynamic name...'
    );
}

export const BACKEND_IP = resolveBackendIP();