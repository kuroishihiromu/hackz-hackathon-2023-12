import React, { useEffect, useState } from 'react';

const AnimatedCurve = () => {
  const [pathLength, setPathLength] = useState(0);

  useEffect(() => {
    const path = document.getElementById('animatedPath');
    const length = path.getTotalLength();
    setPathLength(length);
  }, []);

  const startX = 220;
  const startY = 10;
  const controlX = 220;
  const controlY = 20;
  const endX = 220;
  const endY = 200;

  return (
    <div style={{ position: 'absolute', height: '500px', width: '400px', zIndex:'30'}}>
      <svg width="400" height="400">
          <path
            id="animatedPath"
            d={`M${startX} ${startY} Q${controlX} ${controlY} ${endX} ${endY}`}
            fill="transparent"
            stroke="#000"
            strokeWidth="2"
            strokeDasharray={pathLength}
            strokeDashoffset={pathLength}
            style={{
              animation: 'draw 2s linear forwards',
              
            }}
          />
        <text x={startX} y={startY - 10} textAnchor="middle" fontSize="12" fill="#000">
          始点
        </text>
        <text x={endX} y={endY + 20} textAnchor="middle" fontSize="12" fill="#000">
          終点
        </text>
      </svg>
    </div>
  );
};

export default AnimatedCurve;
