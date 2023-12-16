//WakeUpNode.js
import React, { useEffect, useState } from "react";

const WakeUpNode = ({label, top, left, wakeup}) => {

    const nodeStyle = {

        position: "absolute",
        left: left,
        top: top,
        borderRadius: "50%",
        width: "20px",
        height: "20px",
        backgroundColor: wakeup ? "#FF0000" : "#FFFFFF",
        animation: wakeup ? "pulse 1s cubic-bezier(0.4,0,0.6,1) infinite" : "none",
      }

    return (
      <>
        <div style={nodeStyle} className="z-40">
            <span>{label}</span>
        </div>
      </>
    );
  };
  
export default WakeUpNode;
  