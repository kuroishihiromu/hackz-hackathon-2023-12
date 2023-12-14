//WakeUpNode.js
import React, { useEffect, useState } from "react";
import socketIOClient from 'socket.io-client'

const WakeUpNode = ({label, top, left}) => {
    const [status, setStatus] = useState(false)

    useEffect(() => {
        const socket = socketIOClient("http://localhost/get_status")

        socket.on("statusChanged", (newStatus) =>
        {
            setStatus(newStatus)
        })
    })

    const nodeStyle = {

        position: "abusolute",
        left: left || "50%",
        top: top || "50%",
        borderRadius: "50%",
        width: "20px",
        height: "20px",
        backgroundColor: "#FF0000",
    }

    return (
        socket.disconnect()
    )

    return (
      <>
        <div style={nodeStyle}>
            <span>{label}</span>
        </div>
      </>
    );
  };
  
export default WakeUpNode;
  