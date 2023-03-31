import React, { useContext, useState, useRef } from "react";

const SheContext = React.createContext();

export function SheProvider({ children }) {
    const [openauthmodal, setopenauthmodal] = useState(false);
    const [isuserreg, setisuserreg] = useState(true);
    const [isuser, setisuser] = useState(false);

    const value = {
        openauthmodal,
        setopenauthmodal,
        isuserreg,
        setisuserreg,
        isuser,
        setisuser
    };
    return <SheContext.Provider value={value}>{children}</SheContext.Provider>;
}

export function useAuthModal() {
    return useContext(SheContext);
}
