// WakeUpTree.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import WakeUpNode from './WakeUpNode';


const WakeUpTree = () => {

    const [nodesData, setNodesData] = useState([])

    useEffect(() => {
        axios.get("http://localhost:5000/get_tree")
        .then(response => {
            setNodesData(response.data)
        })
        .catch(error => {
            console.error('Error fetching data:', error)
        })
    }, [])

  return (
    <>
        <WakeUpNode label="15"/>
        <WakeUpNode label="14"/>
        <WakeUpNode label="13"/>
        <WakeUpNode label="12"/>
        <WakeUpNode label="11"/>
        <WakeUpNode label="10"/>
        <WakeUpNode label="9"/>
        <WakeUpNode label="8"/>
        <WakeUpNode label="7"/>
        <WakeUpNode label="6"/>
        <WakeUpNode label="5"/>
        <WakeUpNode label="4"/>
        <WakeUpNode label="3"/>
        <WakeUpNode label="2"/>
        <WakeUpNode label="1"/>
    </>
  );
};

export default WakeUpTree;
