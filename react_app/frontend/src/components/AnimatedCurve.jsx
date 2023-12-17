//AnimatedCurve.jsx
import { render } from '@testing-library/react';
import React, { useEffect, useState } from 'react';

const AnimatedCurve = (props) => {
  const {render_index} = props
  const [pathLengths, setPathLengths] = useState([]);
  const [pathsData, setPathsData] = useState([
    {startX:180, startY:450, controlX:180,controlY:425,endX:180,endY:410,render:false},
    {startX:180, startY:420, controlX:180,controlY:410,endX:180,endY:350,render:false},
    {startX:180, startY:350, controlX:150,controlY:265,endX:100,endY:290,render:false},
    {startX:180, startY:350, controlX:180,controlY:280,endX:140,endY:240,render:false},
    {startX:180, startY:350, controlX:205,controlY:270,endX:210,endY:240,render:false},
    {startX:180, startY:350, controlX:200,controlY:285,endX:257.25,endY:285,render:false},
    {startX:90, startY:285, controlX:30,controlY:250,endX:10,endY:260,render:false},
    {startX:90, startY:285, controlX:0,controlY:300,endX:50,endY:210,render:false},
    {startX:140, startY:235, controlX:160,controlY:180,endX:80,endY:160,render:false},
    {startX:140, startY:235, controlX:100,controlY:200,endX:130,endY:140,render:false},
    {startX:210, startY:240, controlX:160,controlY:200,endX:220,endY:130,render:false},
    {startX:210, startY:240, controlX:220,controlY:150,endX:270,endY:160,render:false},
    {startX:270, startY:287, controlX:300,controlY:300,endX:300,endY:210,render:false},
    {startX:270, startY:287, controlX:250,controlY:230,endX:340,endY:255,render:false},
    {startX:0, startY:0, controlX:0,controlY:0,endX:0,endY:0,render:false},  
  ])
  useEffect(() => {
    const lengths = [];
    for (let i = 0; i <= pathsData.length-1; i++) {
      const path = document.getElementById(`animatedPath${i}`);
      const length = path.getTotalLength();
      lengths.push(length);
    }
    setPathLengths(lengths);

    const selectedPathIndices = (() => {
      switch (render_index) {
        case 1:
          return [0];
        case 2:
          return [1];
        case 3:
          return [2, 3, 4, 5];
        case 4:
          return [6, 7];
        case 5:
          return [8, 9];
        case 6:
          return [10, 11];
        case 7:
          return [12, 13];

        default:
          return [14];
      }
    })()

    setPathsData((prevPathsData) => {
      return prevPathsData.map((path, index) => {
        console.log(path,index)
        return {
          ...path,
          render: selectedPathIndices.includes(index)
        }
      })
    })
  }, [ render_index]);

  return (
    <div style={{ position: 'absolute', height: '500px', width: '343px', zIndex: '30' }}>
      <svg width="343" height="500">
        {pathsData.map((data,i) => {

          const {startX,startY,controlX,controlY,endX,endY,render}=data

          return (
            <g key={i} display={render ? "block" : "none"}>
              <path
                id={`animatedPath${i}`}
                d={`M${startX} ${startY} Q${controlX} ${controlY} ${endX} ${endY}`}
                fill="transparent"
                stroke="#864A2B"
                strokeWidth="6"
                strokeDasharray={pathLengths[i]}
                strokeDashoffset={pathLengths[i]}
                style={{
                  animation: 'draw 2s linear forwards',
                }}
              />
            </g>
          )
        })}
      </svg>
    </div>
  );
};

export default AnimatedCurve;
