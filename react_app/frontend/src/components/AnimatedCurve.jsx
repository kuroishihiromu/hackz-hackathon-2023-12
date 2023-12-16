//AnimatedCurve.jsx
import React, { useEffect, useState } from 'react';

const pathsData = [
  {startX:180, startY:450, controlX:180,controlY:425,endX:180,endY:410},
  {startX:180, startY:420, controlX:180,controlY:410,endX:180,endY:350},
  {startX:180, startY:350, controlX:150,controlY:265,endX:100,endY:290},
  {startX:180, startY:350, controlX:180,controlY:280,endX:140,endY:240},
  {startX:180, startY:350, controlX:205,controlY:270,endX:210,endY:240},
  {startX:180, startY:350, controlX:200,controlY:285,endX:257.25,endY:285},
  {startX:90, startY:285, controlX:30,controlY:250,endX:10,endY:260},
  {startX:90, startY:285, controlX:0,controlY:300,endX:50,endY:210},
  {startX:140, startY:235, controlX:160,controlY:180,endX:80,endY:160},
  {startX:140, startY:235, controlX:100,controlY:200,endX:130,endY:140},
  {startX:210, startY:240, controlX:160,controlY:200,endX:210,endY:130},
  {startX:210, startY:240, controlX:220,controlY:150,endX:270,endY:160},
  {startX:270, startY:287, controlX:300,controlY:300,endX:300,endY:210},
  {startX:270, startY:287, controlX:250,controlY:230,endX:340,endY:255},
]

const AnimatedCurve = () => {
  const [pathLengths, setPathLengths] = useState([]);

  useEffect(() => {
    const lengths = [];
    for (let i = 1; i <= pathsData.length-1; i++) {
      const path = document.getElementById(`animatedPath${i}`);
      const length = path.getTotalLength();
      lengths.push(length);
    }
    setPathLengths(lengths);
  }, []);

  // const paths = Array.from({ length: 15 }, (_, i) => i + 1);
  // const startXs =[171.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  // const startYs = [500,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  // const controlXs = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  // const controlYs = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  // const endXs = [171.5,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
  // const endYs = [10,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

  return (
    <div style={{ position: 'absolute', height: '500px', width: '343px', zIndex: '30' }}>
      <svg width="343" height="500">
        {pathsData.map((data,i) => {

          const {startX,startY,controlX,controlY,endX,endY}=data

          return (
            <g key={i}>
              <path
                id={`animatedPath${i}`}
                d={`M${startX} ${startY} Q${controlX} ${controlY} ${endX} ${endY}`}
                fill="transparent"
                stroke="#000"
                strokeWidth="2"
                strokeDasharray={pathLengths[i - 1]}
                strokeDashoffset={pathLengths[i - 1]}
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
            </g>
          );
        })}
      </svg>
    </div>
  );
};

export default AnimatedCurve;
