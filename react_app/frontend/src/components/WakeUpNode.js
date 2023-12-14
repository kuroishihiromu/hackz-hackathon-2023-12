//WakeUpNode.js
import React, { useEffect, useState } from "react";
import socketIOClient from 'socket.io-client'

const WakeUpNode = ({label, top, left}) => {
  const [status, setStatus] = useState(false)
  const [nodesData, setNodesData] = useState([])

    useEffect(() => {
      const socket = socketIOClient("http://localhost:5000")

      socket.on("status_changed", (data) =>{
          setStatus(data.status)
          const updatedNodesData = JSON.parse(data.nodesData)

          if(data.status){
            setNodesData(updatedNodesData)
          } else {
            setNodesData([])
          }
      })

      return () => {
        socket.disconnect()
      }
    }, [])

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
      <>
        <div style={nodeStyle}>
            <span>{label}</span>
        </div>
      </>
    );
  };
  
export default WakeUpNode;
  