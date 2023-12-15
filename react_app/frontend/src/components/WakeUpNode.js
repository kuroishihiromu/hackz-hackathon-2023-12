//WakeUpNode.js
import React, { useEffect, useState } from "react";

const WakeUpNode = ({label, top, left, wakeup}) => {

    const nodeStyle = {

        position: "absolute",
        left: left || "50%",
        top: top || "50%",
        borderRadius: "50%",
        width: "20px",
        height: "20px",
        backgroundColor: wakeup ? "#FF0000" : "#FFFFFF",
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
  