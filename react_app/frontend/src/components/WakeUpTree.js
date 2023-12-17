import React, { useEffect, useState } from 'react';
import WakeUpNode from './WakeUpNode';
import AnimatedCurve from './AnimatedCurve';
import axios from 'axios'
const WakeUpTree = () => {
  
  const [nodesData, setNodesData] = useState([
    { node_id: 1, wakeup: false, edge: 0 },
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
  ]);

  const calcNodePosition = (nodeId) => {
    switch (nodeId) {
      case 1:
        return { left: '50%', top: '90%' };
      case 2:
        return { left: '50%', top: '80%' };
      case 3:
        return { left: '50%', top: '70%' };
      case 4:
        return { left: '25%', top: '55%' };
      case 5:
        return { left: '40%', top: '47%' };
      case 6:
        return { left: '60%', top: '47%' };
      case 7:
        return { left: '75%', top: '55%' };
      case 8:
        return { left: '0%', top: '50%' };
      case 9:
        return { left: '10%', top: '40%' };
      case 10:
        return { left: '20%', top: '30%' };
      case 11:
        return { left: '35%', top: '25%' };
      case 12:
        return { left: '60%', top: '25%' };
      case 13:
        return { left: '75%', top: '30%' };
      case 14:
        return { left: '85%', top: '40%' };
      case 15:
        return { left: '95%', top: '50%' };
      default:
        return { left: '50%', top: '50%' };
    }
  };

  const [simulatedNodeId, setSimulatedNodeId] = useState(null)

  useEffect(() => {
    // ソケットからのデータ更新をシミュレート

    const fetchData = async () => {
      try{
      
        const user_id = sessionStorage.getItem('userid')

        if(user_id){
          const response = await axios.post('http://localhost:5000/tree_state', {user_id})
          const responseData = response.data
          const simulatedDataUpdate = [...responseData]
          // console.log(responseData)
          // simulatedDataUpdate = [{node_id:responseData["node_id"], wakeup:responseData["wakeup"]}]
          const nodeId = simulatedDataUpdate[0]?.node_id
          setSimulatedNodeId(nodeId)
          const updatedNodesData = nodesData.map((node) => {
            const update = simulatedDataUpdate.find((update) => update.node_id === node.node_id);
            if (update && node.wakeup !== update.wakeup) {
              return { ...node, wakeup: update.wakeup };
            } else {
              return node;
            }
          });
      
          if (JSON.stringify(nodesData) !== JSON.stringify(updatedNodesData)) {
            setNodesData(updatedNodesData);
          }
        } else {
          console.error('User ID not found in session storage');
        }
      }catch(error){
        console.error('Error during post request', error)
      }
    }

    fetchData()

    const intervalId = setInterval(() => {
      fetchData()
    }, 10000)
    
  }, [nodesData]);

  return (
    <>
      <div className='w-[80%] h-[500px] mx-auto relative z-10 mb-20'>
        {nodesData.map((node, index) => {
          const { left, top } = calcNodePosition(node.node_id);
          return (
            <React.Fragment key={index}>
              <WakeUpNode label={node.node_id} wakeup={node.wakeup} edge={node.edge} left={left} top={top} />
              <AnimatedCurve render_index={simulatedNodeId} />
            </React.Fragment>
          );
        })}
      </div>
    </>
  );
};

export default WakeUpTree;
