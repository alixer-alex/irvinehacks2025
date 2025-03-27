import { useEffect, useState, FC, CSSProperties } from "react";
import {Graph} from "graphology";
import circular from 'graphology-layout/circular';
import { SigmaContainer, useLoadGraph, ControlsContainer, useRegisterEvents } from "@react-sigma/core";
import "@react-sigma/core/lib/style.css";
import "@react-sigma/layout-noverlap";

import { useWorkerLayoutForceAtlas2 } from '@react-sigma/layout-forceatlas2';
//const sigmaStyle = { height: "500px", width: "500px" };


const sigmaSettings = { allowInvalidContainer: true };


const Fa2 = () => {
  const { start, kill } = useWorkerLayoutForceAtlas2({ settings: { slowDown: 10 } });

  useEffect(() => {
    // start FA2
    start();

    // Kill FA2 on unmount
    return () => {
      kill();
    };
  }, [start, kill]);

  return null;
};

export const LoadGraph = (username) => {
  const loadGraph = useLoadGraph();
  const [friends, setFriends] = useState(null);
  const registerEvents = useRegisterEvents();
  async function getData(){
    
    // can use this line instead:
    //TEMP CHANGE: the port was originally 5000
    //using this below line of code will let you use your local files, instead of the deployed app's files
    //const url = "http://localhost:5000/api/" + username.username;
    //TODO: this was the original line of code, one of the final changes before "finishing" the competition
    //TODO: ask Alex to update the railway app or whatever so that the api now uses the updated version of our files
    const url = "https://irvinehacks2025-production.up.railway.app/api/" + username.username;
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
  
      const json = await response.json();
      console.log(json);
      return json;
      
    } catch (error) {
      console.error(error.message);
    }

  }
    useEffect(() => {
        const graph = new Graph();
        // console.log(username.username)
        // fetch('/api/'+ username.username)
        // .then(response => response.json())
        // .then(data => setData(data))
        // .catch(error => console.log(error))
        
        console.log(username.username)
        getData().then(
          data => {
            
            for (let key in data){
              console.log(key);
              graph.addNode(key, { x: 0, y: 0, size: 10, label: key, color: "##FF0000"});
            }
            for (let key in data){
              for(let i=0;i<data[key].length;i++){
                let value = data[key][i];
                console.log(graph.edges())
                if(!graph.nodes().includes(value)){
                  graph.addNode(value, { x: 0, y: 0, size: 4, label: value, color: "##00FF00"});
                }
                try{
                  graph.addEdge(key,value);
                }
                catch{

                }
                console.log(graph.edges())
              }
            }
            loadGraph(graph);
            circular.assign(graph);
            // Register the events
            // registerEvents({
            //   // node events
            //   enterNode: (event) => console.log('enterNode', event.node),
            //   leaveNode: (event) => console.log('leaveNode', event.node),

            // });
          }
          
          
        )
       
        
    }, [friends,loadGraph,registerEvents]);
    return null;
}

export const DisplayGraph = (props) => {
  return (
  <div className="sigma_graph" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
    <SigmaContainer>
      <ControlsContainer position={'bottom-right'}>
        <LoadGraph username={props.username}/>
        
        <Fa2 />
      </ControlsContainer>
    </SigmaContainer>
  </div>
);
};
export default DisplayGraph;