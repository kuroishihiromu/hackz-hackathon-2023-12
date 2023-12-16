import React from "react";
import SetTime from "./components/SetTime"
import WakeUpTree from "./components/WakeUpTree";
const Home = () => {
    
    return (
        <>
            <div className="bg-[#b8a1c5] flex  items-center w-[120px] h-[120px] rounded-[50%] shadow-lg mt-[30px] ml-[10px]">
                <img src="../img/alerm-icon3.png" className="mx-5 mx-auto w-[80%]"></img>
            </div>
            <div className="text-center">
                <h1></h1>
                <div>
                    <WakeUpTree />
                </div>
            </div>
            <SetTime />
        </>

    )
}

export default Home
