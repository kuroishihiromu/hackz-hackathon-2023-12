// WakeUpLine.js
import React from 'react';

const WakeUpLine = ({ from, to }) => {
  const lineStyle = {
    position: 'absolute',
    border: '1px solid #000000',
    width: '0',
    height: '0',
    borderLeft: '10px solid transparent',
    borderRight: '10px solid transparent',
    left: from.left,
    top: from.top,
  };

  const angle = Math.atan2(to.top - from.top, to.left - from.left);
  const length = Math.sqrt((to.top - from.top) ** 2 + (to.left - from.left) ** 2);
  const transform = `rotate(${angle}rad)`;
  lineStyle.width = `${length}px`;
  lineStyle.transform = transform;

  return <div style={lineStyle} />;
};

export default WakeUpLine;
