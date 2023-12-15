// WakeUpTree.js
import React, { useEffect, useState } from 'react';
import WakeUpNode from './WakeUpNode';

const WakeUpTree = () => {
  const [nodesData, setNodesData] = useState([
    { node_id: 1, wakeup: true, edge: 0 },
    { node_id: 2, wakeup: false, edge: 1 },
    { node_id: 3, wakeup: false, edge: 2 },
    { node_id: 4, wakeup: false, edge: 3 },
    { node_id: 5, wakeup: false, edge: 3 },
    { node_id: 6, wakeup: false, edge: 3 },
    { node_id: 7, wakeup: false, edge: 3 },
    { node_id: 8, wakeup: false, edge: 4 },
    { node_id: 9, wakeup: false, edge: 4 },
    { node_id: 10, wakeup: false, edge: 5 },
    { node_id: 11, wakeup: false, edge: 5 },
    { node_id: 12, wakeup: false, edge: 6 },
    { node_id: 13, wakeup: false, edge: 6 },
    { node_id: 14, wakeup: false, edge: 7 },
    { node_id: 15, wakeup: false, edge: 7 },

    // Add more nodes as needed
  ]);

  const calcNodePosition=(nodeId) => {
    switch (nodeId) {
      case 1:
        return { left: '50%', top: '80%' };
      case 2:
        return { left: '50%', top: '70%' };
      case 3:
        return { left: '25%', top: '60%' };
      case 4:
        return { left: '25%', top: '60%' };
      case 5:
        return { left: '75%', top: '60%' };
      case 6:
        return { left: '15%', top: '60%' };
      case 7:
        return { left: '20%', top: '10%' };
      case 8:
        return { left: '20%', top: '10%' };
      case 9:
        return { left: '20%', top: '10%' };
      case 10:
        return { left: '20%', top: '10%' };
      // Add more cases as needed
      default:
        return { left: '50%', top: '50%' };
    }
  }

  useEffect(() => {
    // Simulating data updates from socket
    const simulatedDataUpdate = {
      node_id: 7,
      wakeup: true,
    };

    const isNodeUpdated = nodesData.some(node => node.node_id === simulatedDataUpdate.node_id && node.wakeup !== simulatedDataUpdate.wakeup);

    if(isNodeUpdated){
      const updatedNodesData = nodesData.map(node => {
        if (node.node_id === simulatedDataUpdate.node_id) {
          return { ...node, wakeup: simulatedDataUpdate.wakeup };
        } else {
          return node;
        }
      });

      setNodesData(updatedNodesData);
    }
  }, [nodesData]);

  const filterdNoeds = nodesData.filter(node => {
    return !node.edge || (nodesData.find(parentNode => parentNode.node_id === node.edge)?.wakeup===true)
  })

  return (
    <div className='w-[80%] h-[500px] mx-auto relative'>
      {filterdNoeds.map((node, index) => {
        const {left, top} = calcNodePosition(node.node_id)
        return (
          <WakeUpNode 
          key={index} 
          label={node.node_id} 
          wakeup={node.wakeup} 
          edge={node.edge} 
          left={left}
          top={top}
          />
        )
      })}
    </div>
  );
};

export default WakeUpTree;
