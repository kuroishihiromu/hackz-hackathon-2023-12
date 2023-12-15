import React from "react";
import SetTime from "./SetTime"
import WakeUpTree from "./WakeUpTree";
const Home = () => {
    
    return (
        <>
            <div className="text-center">
                <h1>Home</h1>
                <div>
                    render the tree...
                    <WakeUpTree />
                </div>
            </div>
            <SetTime />
        </>

    )
}

export default Home
