//Top.js
import React from "react"
import Login from './Login'
import SignUp from './Signup'
const Top = () => {
    return(
        <>
            <div className="text-center">
                
                <img src='/img/tree-icon.png' alt='tree-icon' className='w-[70%] mx-auto mt-10'></img>
                <Login />
                <SignUp />
            </div>
        </>
    )
}

export default Top
